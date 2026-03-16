#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║         SUBDOMAIN FINDER - Recon Tool        ║
║     For educational / bug bounty use only    ║
╚══════════════════════════════════════════════╝
DISCLAIMER: Only use on domains you own or have
explicit permission to test. Unauthorized scanning
may be illegal in your jurisdiction.
"""

import socket
import concurrent.futures
import sys
import os
from datetime import datetime

# ─── COLORS ───────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# ─── COMMON SUBDOMAINS WORDLIST ────────────────────
COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "ns2",
    "webdisk", "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap",
    "test", "ns", "blog", "pop3", "dev", "www2", "admin", "forum", "news",
    "vpn", "ns3", "mail2", "new", "mysql", "old", "lists", "support",
    "mobile", "mx", "static", "docs", "beta", "shop", "api", "secure",
    "origin", "staging", "dashboard", "portal", "intranet", "internal",
    "cdn", "media", "images", "img", "video", "download", "downloads",
    "upload", "uploads", "store", "auth", "login", "register", "signup",
    "git", "github", "gitlab", "jenkins", "jira", "confluence", "wiki",
    "status", "monitor", "monitoring", "grafana", "kibana", "elastic",
    "app", "apps", "web", "server", "server1", "server2", "db", "database",
    "redis", "cache", "search", "help", "uat", "qa", "prod", "production",
    "cloud", "office", "remote", "backup", "files", "assets", "payment",
]

def banner():
    print(f"""
{CYAN}{BOLD}
  ██████  ██    ██ ██████  ██████   ██████  ███    ███  █████  ██ ███    ██ 
  ██       ██  ██  ██   ██ ██   ██ ██    ██ ████  ████ ██   ██ ██ ████   ██ 
  ███████   ████   ██████  ██   ██ ██    ██ ██ ████ ██ ███████ ██ ██ ██  ██ 
       ██    ██    ██   ██ ██   ██ ██    ██ ██  ██  ██ ██   ██ ██ ██  ██ ██ 
  ██████     ██    ██████  ██████   ██████  ██      ██ ██   ██ ██ ██   ████ 
                                                                             
  {YELLOW}FINDER{RESET}  {CYAN}v1.0 | Grey Hat Learning Tool{RESET}
""")

def resolve_subdomain(subdomain, domain):
    """Try to resolve a subdomain and return its IP if successful."""
    full_domain = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(full_domain)
        return (full_domain, ip)
    except socket.gaierror:
        return None

def load_wordlist(filepath):
    """Load a custom wordlist from a file."""
    if not os.path.exists(filepath):
        print(f"{RED}[ERROR] Wordlist file not found: {filepath}{RESET}")
        sys.exit(1)
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]

def save_results(domain, found, output_file):
    """Save discovered subdomains to a file."""
    with open(output_file, "w") as f:
        f.write(f"# Subdomain Scan Results\n")
        f.write(f"# Target  : {domain}\n")
        f.write(f"# Date    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Found   : {len(found)} subdomains\n\n")
        for subdomain, ip in found:
            f.write(f"{subdomain} => {ip}\n")
    print(f"\n{GREEN}[✔] Results saved to: {output_file}{RESET}")

def scan(domain, wordlist, threads=50):
    """Main scanning function using thread pool."""
    found = []
    total  = len(wordlist)
    scanned = 0

    print(f"\n{YELLOW}[*] Target   : {BOLD}{domain}{RESET}")
    print(f"{YELLOW}[*] Wordlist : {total} subdomains{RESET}")
    print(f"{YELLOW}[*] Threads  : {threads}{RESET}")
    print(f"{CYAN}{'─'*55}{RESET}\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(resolve_subdomain, sub, domain): sub
            for sub in wordlist
        }
        for future in concurrent.futures.as_completed(futures):
            scanned += 1
            result = future.result()
            if result:
                subdomain, ip = result
                found.append(result)
                print(f"  {GREEN}[+] FOUND  {BOLD}{subdomain:<40}{RESET} => {CYAN}{ip}{RESET}")

            # Progress indicator every 50 scans
            if scanned % 50 == 0:
                pct = (scanned / total) * 100
                print(f"  {YELLOW}[~] Progress: {scanned}/{total} ({pct:.0f}%){RESET}", end="\r")

    return found

def main():
    banner()

    # ─── GET INPUT ──────────────────────────────────
    print(f"{CYAN}[?] Enter target domain (e.g. example.com): {RESET}", end="")
    domain = input().strip().lower()

    if not domain:
        print(f"{RED}[ERROR] Domain cannot be empty.{RESET}")
        sys.exit(1)

    # Remove http/https if provided
    domain = domain.replace("https://", "").replace("http://", "").rstrip("/")

    print(f"\n{CYAN}[?] Use custom wordlist? (y/n, default=n): {RESET}", end="")
    use_custom = input().strip().lower()

    if use_custom == "y":
        print(f"{CYAN}[?] Enter wordlist path: {RESET}", end="")
        wordlist_path = input().strip()
        wordlist = load_wordlist(wordlist_path)
    else:
        wordlist = COMMON_SUBDOMAINS

    print(f"\n{CYAN}[?] Thread count (default=50): {RESET}", end="")
    thread_input = input().strip()
    threads = int(thread_input) if thread_input.isdigit() else 50

    # ─── SCAN ────────────────────────────────────────
    start_time = datetime.now()
    found = scan(domain, wordlist, threads)
    elapsed = (datetime.now() - start_time).seconds

    # ─── SUMMARY ─────────────────────────────────────
    print(f"\n{CYAN}{'═'*55}{RESET}")
    print(f"  {BOLD}SCAN COMPLETE{RESET}")
    print(f"  Subdomains tested : {len(wordlist)}")
    print(f"  Subdomains found  : {GREEN}{BOLD}{len(found)}{RESET}")
    print(f"  Time elapsed      : {elapsed}s")
    print(f"{CYAN}{'═'*55}{RESET}")

    if found:
        print(f"\n{CYAN}[?] Save results to file? (y/n): {RESET}", end="")
        save = input().strip().lower()
        if save == "y":
            filename = f"subdomains_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            save_results(domain, found, filename)
    else:
        print(f"\n{RED}[!] No subdomains found. Try a larger wordlist.{RESET}")

if __name__ == "__main__":
    main()
