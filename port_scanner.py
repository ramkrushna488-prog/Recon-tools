#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║          PORT SCANNER - Recon Tool           ║
║     For educational / bug bounty use only    ║
╚══════════════════════════════════════════════╝
DISCLAIMER: Only use on systems you own or have
explicit permission to test. Unauthorized port
scanning may be illegal in your jurisdiction.
"""

import socket
import concurrent.futures
import sys
from datetime import datetime

# ─── COLORS ───────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
MAGENTA= "\033[95m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# ─── WELL-KNOWN PORT DATABASE ──────────────────────
PORT_DB = {
    21:   ("FTP",        "File Transfer Protocol - check for anonymous login"),
    22:   ("SSH",        "Secure Shell - check for weak credentials / old versions"),
    23:   ("Telnet",     "UNENCRYPTED remote login - serious vulnerability if open"),
    25:   ("SMTP",       "Mail server - check for open relay"),
    53:   ("DNS",        "Domain Name System - check for zone transfer"),
    80:   ("HTTP",       "Web server - check for web vulnerabilities"),
    110:  ("POP3",       "Mail retrieval - check for plaintext auth"),
    111:  ("RPC",        "Remote Procedure Call - often exploitable"),
    135:  ("MSRPC",      "Microsoft RPC - Windows attack surface"),
    139:  ("NetBIOS",    "Windows file sharing - SMB vulnerabilities"),
    143:  ("IMAP",       "Mail access - check for plaintext auth"),
    443:  ("HTTPS",      "Secure web server - check SSL/TLS config"),
    445:  ("SMB",        "Windows sharing - EternalBlue / ransomware target"),
    993:  ("IMAPS",      "Secure IMAP"),
    995:  ("POP3S",      "Secure POP3"),
    1433: ("MSSQL",      "Microsoft SQL Server - check for default creds"),
    1521: ("Oracle DB",  "Oracle database - check for default creds"),
    2375: ("Docker API", "UNPROTECTED Docker API - critical exposure"),
    3000: ("Dev Server", "Node.js / Grafana / dev apps often here"),
    3306: ("MySQL",      "MySQL database - check for remote root access"),
    3389: ("RDP",        "Remote Desktop - brute force / BlueKeep target"),
    4444: ("Metasploit", "Common reverse shell / Metasploit listener port"),
    5432: ("PostgreSQL", "Postgres DB - check for remote access"),
    5900: ("VNC",        "Virtual Network Computing - check for no-auth"),
    6379: ("Redis",      "Redis DB - often exposed without auth"),
    8080: ("HTTP-Alt",   "Alternative HTTP - admin panels often here"),
    8443: ("HTTPS-Alt",  "Alternative HTTPS"),
    8888: ("Jupyter",    "Jupyter Notebook - often no auth in dev environments"),
    9200: ("Elasticsearch","ES API - often exposed without auth"),
    27017:("MongoDB",    "MongoDB - often exposed without auth"),
}

# ─── PORT PROFILES ────────────────────────────────
PROFILES = {
    "quick":  list(range(1, 1025)),
    "common": list(PORT_DB.keys()),
    "full":   list(range(1, 10001)),
    "web":    [80, 443, 8080, 8443, 8000, 8008, 3000, 5000, 9000],
    "db":     [1433, 1521, 3306, 5432, 6379, 9200, 27017, 5984, 7474],
}

def banner():
    print(f"""
{MAGENTA}{BOLD}
  ██████   ██████  ██████  ████████     ███████  ██████  █████  ███    ██ 
  ██   ██ ██    ██ ██   ██    ██        ██      ██      ██   ██ ████   ██ 
  ██████  ██    ██ ██████     ██        ███████ ██      ███████ ██ ██  ██ 
  ██      ██    ██ ██   ██    ██             ██ ██      ██   ██ ██  ██ ██ 
  ██       ██████  ██   ██    ██        ███████  ██████ ██   ██ ██   ████ 
{RESET}  {MAGENTA}v1.0 | Grey Hat Learning Tool{RESET}
""")

def get_banner_grab(ip, port, timeout=2):
    """Attempt to grab service banner."""
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((ip, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()
        return banner[:80] if banner else None
    except:
        return None

def scan_port(ip, port, timeout=1):
    """Scan a single port."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        s.close()
        return port if result == 0 else None
    except:
        return None

def resolve_host(host):
    """Resolve hostname to IP."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None

def print_open_port(port, ip):
    """Pretty print an open port with info."""
    service, note = PORT_DB.get(port, ("Unknown", "Research this service"))
    risk = ""
    if port in [23, 2375, 445, 3389, 5900, 6379, 9200, 27017]:
        risk = f" {RED}[HIGH RISK]{RESET}"
    elif port in [21, 80, 3306, 5432, 8080]:
        risk = f" {YELLOW}[MEDIUM]{RESET}"
    else:
        risk = f" {GREEN}[INFO]{RESET}"

    print(f"  {GREEN}[+]{RESET} Port {CYAN}{BOLD}{port:<6}{RESET} | {YELLOW}{service:<15}{RESET}{risk}")
    print(f"      {MAGENTA}↳  {note}{RESET}")

def scan(ip, ports, threads=100):
    """Multi-threaded port scan."""
    open_ports = []
    total = len(ports)
    scanned = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, ip, p): p for p in ports}
        for future in concurrent.futures.as_completed(futures):
            scanned += 1
            result = future.result()
            if result:
                open_ports.append(result)
                print_open_port(result, ip)

            if scanned % 200 == 0:
                pct = (scanned / total) * 100
                print(f"  {YELLOW}[~] Scanning... {scanned}/{total} ({pct:.0f}%){RESET}", end="\r")

    return sorted(open_ports)

def save_results(target, ip, open_ports, elapsed, output_file):
    with open(output_file, "w") as f:
        f.write(f"# Port Scan Results\n")
        f.write(f"# Target  : {target} ({ip})\n")
        f.write(f"# Date    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Elapsed : {elapsed}s\n\n")
        for port in open_ports:
            service, note = PORT_DB.get(port, ("Unknown", ""))
            f.write(f"PORT {port:<6} | {service:<15} | {note}\n")
    print(f"\n{GREEN}[✔] Results saved to: {output_file}{RESET}")

def main():
    banner()

    # ─── INPUT ───────────────────────────────────────
    print(f"{CYAN}[?] Enter target IP or hostname: {RESET}", end="")
    target = input().strip()

    if not target:
        print(f"{RED}[ERROR] Target cannot be empty.{RESET}")
        sys.exit(1)

    print(f"\n{CYAN}[?] Select scan profile:{RESET}")
    print(f"  {YELLOW}1{RESET} - Quick    (ports 1-1024)")
    print(f"  {YELLOW}2{RESET} - Common   (well-known service ports)")
    print(f"  {YELLOW}3{RESET} - Full     (ports 1-10000, slow)")
    print(f"  {YELLOW}4{RESET} - Web      (HTTP/HTTPS ports)")
    print(f"  {YELLOW}5{RESET} - Database (DB ports only)")
    print(f"  {YELLOW}6{RESET} - Custom   (enter your own range)")
    print(f"\n{CYAN}[?] Choice (1-6): {RESET}", end="")
    choice = input().strip()

    profile_map = {"1": "quick", "2": "common", "3": "full", "4": "web", "5": "db"}

    if choice in profile_map:
        ports = PROFILES[profile_map[choice]]
    elif choice == "6":
        print(f"{CYAN}[?] Enter port range (e.g. 1-1000 or 80,443,8080): {RESET}", end="")
        port_input = input().strip()
        if "-" in port_input:
            start, end = port_input.split("-")
            ports = list(range(int(start), int(end) + 1))
        else:
            ports = [int(p) for p in port_input.split(",")]
    else:
        ports = PROFILES["common"]

    # ─── RESOLVE ─────────────────────────────────────
    print(f"\n{YELLOW}[*] Resolving {target}...{RESET}")
    ip = resolve_host(target)
    if not ip:
        print(f"{RED}[ERROR] Could not resolve host: {target}{RESET}")
        sys.exit(1)

    print(f"{GREEN}[✔] Resolved to: {BOLD}{ip}{RESET}")
    print(f"{YELLOW}[*] Scanning {len(ports)} ports...{RESET}")
    print(f"{CYAN}{'─'*55}{RESET}\n")

    # ─── SCAN ─────────────────────────────────────────
    start = datetime.now()
    open_ports = scan(ip, ports)
    elapsed = (datetime.now() - start).seconds

    # ─── SUMMARY ──────────────────────────────────────
    print(f"\n{CYAN}{'═'*55}{RESET}")
    print(f"  {BOLD}SCAN COMPLETE{RESET}")
    print(f"  Target      : {target} ({ip})")
    print(f"  Ports tested: {len(ports)}")
    print(f"  Open ports  : {GREEN}{BOLD}{len(open_ports)}{RESET}")
    print(f"  Elapsed     : {elapsed}s")
    print(f"{CYAN}{'═'*55}{RESET}")

    if open_ports:
        print(f"\n{CYAN}[?] Save results to file? (y/n): {RESET}", end="")
        if input().strip().lower() == "y":
            fname = f"portscan_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            save_results(target, ip, open_ports, elapsed, fname)

if __name__ == "__main__":
    main()
