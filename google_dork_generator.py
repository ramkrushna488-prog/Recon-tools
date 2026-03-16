#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║       GOOGLE DORK GENERATOR - Recon Tool     ║
║     For educational / bug bounty use only    ║
╚══════════════════════════════════════════════╝
DISCLAIMER: Google dorking uses public search
results. Only investigate findings on systems
you own or have permission to test. Never access
or download sensitive data you find.
"""

import webbrowser
import urllib.parse
from datetime import datetime

# ─── COLORS ───────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
MAGENTA= "\033[95m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

# ─── DORK CATEGORIES & TEMPLATES ──────────────────
DORK_CATEGORIES = {
    "1": {
        "name": "🔐 Login Pages & Admin Panels",
        "dorks": [
            ('Admin Panel',         'site:{domain} inurl:admin'),
            ('Login Page',          'site:{domain} inurl:login'),
            ('Dashboard',           'site:{domain} inurl:dashboard'),
            ('Control Panel',       'site:{domain} inurl:cpanel OR inurl:control-panel'),
            ('WordPress Admin',     'site:{domain} inurl:wp-admin'),
            ('phpMyAdmin',          'site:{domain} inurl:phpmyadmin'),
            ('Webmail',             'site:{domain} inurl:webmail OR inurl:roundcube'),
            ('Sign In Page',        'site:{domain} intitle:"sign in" OR intitle:"log in"'),
        ]
    },
    "2": {
        "name": "📄 Sensitive Files & Documents",
        "dorks": [
            ('Config Files',        'site:{domain} ext:xml OR ext:conf OR ext:config'),
            ('SQL Dumps',           'site:{domain} ext:sql'),
            ('Log Files',           'site:{domain} ext:log'),
            ('Backup Files',        'site:{domain} ext:bak OR ext:backup OR ext:old'),
            ('Env Files',           'site:{domain} ext:env'),
            ('Excel/CSV Data',      'site:{domain} ext:xlsx OR ext:csv'),
            ('PDF Documents',       'site:{domain} ext:pdf'),
            ('Private Keys',        'site:{domain} ext:pem OR ext:key'),
            ('PHP Source',          'site:{domain} ext:php intitle:index'),
        ]
    },
    "3": {
        "name": "🔑 Exposed Credentials & API Keys",
        "dorks": [
            ('API Keys in URLs',    'site:{domain} inurl:api_key OR inurl:apikey OR inurl:api-key'),
            ('Passwords in URL',    'site:{domain} inurl:password OR inurl:passwd'),
            ('Token Exposure',      'site:{domain} inurl:token OR inurl:access_token'),
            ('AWS Keys',            'site:{domain} "AWS_SECRET_ACCESS_KEY"'),
            ('DB Credentials',      'site:{domain} "DB_PASSWORD" OR "database_password"'),
            ('Secret Keys',         'site:{domain} intext:"secret_key" OR intext:"SECRET_KEY"'),
        ]
    },
    "4": {
        "name": "⚙️ Technology & Infrastructure",
        "dorks": [
            ('Apache Server Info',  'site:{domain} intitle:"Apache Status" OR "server-status"'),
            ('PHP Info Pages',      'site:{domain} intitle:"phpinfo()"'),
            ('Error Pages w/ Info', 'site:{domain} "Warning: mysql_connect()"'),
            ('Stack Traces',        'site:{domain} "Fatal error" "stack trace"'),
            ('Directory Listing',   'site:{domain} intitle:"Index of /"'),
            ('Jenkins',             'site:{domain} intitle:"Dashboard [Jenkins]"'),
            ('Grafana',             'site:{domain} intitle:"Grafana"'),
            ('Kibana',              'site:{domain} inurl:5601 intitle:"Kibana"'),
            ('Swagger API Docs',    'site:{domain} inurl:swagger OR inurl:api-docs'),
            ('Git Exposed',         'site:{domain} inurl:.git'),
        ]
    },
    "5": {
        "name": "📋 Open Redirects & Injection Points",
        "dorks": [
            ('Open Redirect',       'site:{domain} inurl:redirect= OR inurl:url= OR inurl:next='),
            ('Search with Input',   'site:{domain} inurl:search= OR inurl:query= OR inurl:q='),
            ('ID Parameters',       'site:{domain} inurl:id= OR inurl:user_id= OR inurl:uid='),
            ('File Params',         'site:{domain} inurl:file= OR inurl:path= OR inurl:dir='),
            ('PHP GET Params',      'site:{domain} ext:php inurl:"?"'),
        ]
    },
    "6": {
        "name": "🌐 Subdomains & Infrastructure",
        "dorks": [
            ('All Subdomains',      'site:*.{domain}'),
            ('Dev/Staging',         'site:{domain} site:dev.{domain} OR site:staging.{domain}'),
            ('API Endpoints',       'site:api.{domain}'),
            ('Test Environments',   'site:{domain} inurl:test OR inurl:demo OR inurl:sandbox'),
            ('S3 Buckets',          '"{domain}" site:s3.amazonaws.com'),
            ('Old/Legacy',          'site:{domain} inurl:old OR inurl:legacy OR inurl:v1'),
        ]
    },
    "7": {
        "name": "📧 Email & User Data",
        "dorks": [
            ('Email Addresses',     'site:{domain} "@{domain}" email'),
            ('Employee Info',       'site:linkedin.com "{domain}" employee'),
            ('Contact Info',        'site:{domain} "contact" "@{domain}"'),
        ]
    },
}

def banner():
    print(f"""
{YELLOW}{BOLD}
  ██████   ██████  ██████  ██   ██     ██████  ███████ ███    ██ 
  ██   ██ ██    ██ ██   ██ ██  ██     ██       ██      ████   ██ 
  ██   ██ ██    ██ ██████  █████      ██   ███ █████   ██ ██  ██ 
  ██   ██ ██    ██ ██   ██ ██  ██     ██    ██ ██      ██  ██ ██ 
  ██████   ██████  ██   ██ ██   ██     ██████  ███████ ██   ████ 
{RESET}  {YELLOW}GENERATOR v1.0 | Grey Hat Learning Tool{RESET}
""")

def generate_google_url(dork):
    """Generate a clickable Google search URL from a dork."""
    base = "https://www.google.com/search?q="
    return base + urllib.parse.quote(dork)

def generate_bing_url(dork):
    """Generate a Bing search URL (less filtered than Google)."""
    base = "https://www.bing.com/search?q="
    return base + urllib.parse.quote(dork)

def print_dork(name, dork, idx):
    google_url = generate_google_url(dork)
    bing_url   = generate_bing_url(dork)
    print(f"\n  {CYAN}{BOLD}[{idx}] {name}{RESET}")
    print(f"  {YELLOW}Dork  :{RESET} {dork}")
    print(f"  {GREEN}Google:{RESET} {DIM}{google_url[:90]}...{RESET}")
    print(f"  {MAGENTA}Bing  :{RESET} {DIM}{bing_url[:90]}...{RESET}")

def show_menu():
    print(f"\n{CYAN}{'─'*55}{RESET}")
    print(f"  {BOLD}SELECT DORK CATEGORY:{RESET}")
    print(f"{CYAN}{'─'*55}{RESET}")
    for key, val in DORK_CATEGORIES.items():
        print(f"  {YELLOW}{key}{RESET} - {val['name']}")
    print(f"  {YELLOW}A{RESET} - Run ALL categories")
    print(f"  {YELLOW}C{RESET} - Custom dork (manual input)")
    print(f"  {YELLOW}Q{RESET} - Quit")
    print(f"{CYAN}{'─'*55}{RESET}")

def run_category(domain, cat_key, open_browser=False, results=[]):
    category = DORK_CATEGORIES[cat_key]
    print(f"\n  {BOLD}{category['name']}{RESET}")
    print(f"  {CYAN}{'─'*50}{RESET}")
    for idx, (name, template) in enumerate(category["dorks"], 1):
        dork = template.replace("{domain}", domain)
        print_dork(name, dork, idx)
        results.append((name, dork, generate_google_url(dork)))
        if open_browser:
            webbrowser.open(generate_google_url(dork))

def save_dorks(domain, results, output_file):
    with open(output_file, "w") as f:
        f.write(f"# Google Dork Results\n")
        f.write(f"# Target : {domain}\n")
        f.write(f"# Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total  : {len(results)} dorks generated\n\n")
        for name, dork, url in results:
            f.write(f"# {name}\n")
            f.write(f"Dork: {dork}\n")
            f.write(f"URL : {url}\n\n")
    print(f"\n{GREEN}[✔] Dorks saved to: {output_file}{RESET}")

def main():
    banner()

    # ─── TARGET ──────────────────────────────────────
    print(f"{CYAN}[?] Enter target domain (e.g. example.com): {RESET}", end="")
    domain = input().strip().lower().replace("https://", "").replace("http://", "").rstrip("/")

    if not domain:
        print(f"{RED}[ERROR] Domain cannot be empty.{RESET}")
        return

    print(f"{CYAN}[?] Auto-open results in browser? (y/n): {RESET}", end="")
    open_browser = input().strip().lower() == "y"

    if open_browser:
        print(f"{YELLOW}[!] Warning: Opening many tabs. Use responsibly!{RESET}")

    results = []

    while True:
        show_menu()
        print(f"\n{CYAN}[?] Your choice: {RESET}", end="")
        choice = input().strip().upper()

        if choice == "Q":
            break
        elif choice == "A":
            for key in DORK_CATEGORIES:
                run_category(domain, key, open_browser, results)
        elif choice == "C":
            print(f"{CYAN}[?] Enter your custom dork (use {{domain}} as placeholder): {RESET}", end="")
            custom = input().strip().replace("{domain}", domain)
            print(f"\n  {GREEN}Dork  :{RESET} {custom}")
            url = generate_google_url(custom)
            print(f"  {GREEN}URL   :{RESET} {DIM}{url}{RESET}")
            results.append(("Custom", custom, url))
            if open_browser:
                webbrowser.open(url)
        elif choice in DORK_CATEGORIES:
            run_category(domain, choice, open_browser, results)
        else:
            print(f"{RED}[!] Invalid choice.{RESET}")
            continue

        print(f"\n{CYAN}[?] Continue? (y/n): {RESET}", end="")
        if input().strip().lower() != "y":
            break

    # ─── SAVE ────────────────────────────────────────
    if results:
        print(f"\n{GREEN}[✔] Generated {len(results)} dorks total.{RESET}")
        print(f"{CYAN}[?] Save all dorks to file? (y/n): {RESET}", end="")
        if input().strip().lower() == "y":
            fname = f"dorks_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            save_dorks(domain, results, fname)

    print(f"\n{YELLOW}[!] Always investigate findings ethically. Happy hunting! 🎯{RESET}\n")

if __name__ == "__main__":
    main()
