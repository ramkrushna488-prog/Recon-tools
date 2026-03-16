# 🎩 Grey Hat Recon Toolkit

A beginner-friendly set of recon scripts for learning ethical hacking, bug bounty hunting, and security research.

---

## ⚠️ DISCLAIMER

These tools are strictly for **educational purposes** and **authorized security testing only**.
- Only use on systems **you own** or have **explicit written permission** to test
- Never access, download, or store sensitive data you discover
- Always follow responsible disclosure practices
- Unauthorized use may be **illegal** in your jurisdiction

---

## 🛠️ Tools Included

| Script | Description |
|---|---|
| `subdomain_finder.py` | DNS brute-force subdomain enumeration |
| `port_scanner.py` | Multi-threaded TCP port scanner with service detection |
| `google_dork_generator.py` | Google dork query generator for OSINT recon |

---

## 🚀 Setup

```bash
# Python 3.7+ required, no extra installs needed — uses stdlib only!
python3 --version

# Make scripts executable
chmod +x subdomain_finder.py port_scanner.py google_dork_generator.py
```

---

## 📖 Usage

### 1. Subdomain Finder
```bash
python3 subdomain_finder.py
```
- Resolves subdomains using DNS
- Comes with a built-in wordlist of 80+ common subdomains
- Supports custom wordlists (one subdomain per line)
- Multi-threaded (default: 50 threads)
- Saves results to `.txt`

### 2. Port Scanner
```bash
python3 port_scanner.py
```
- Scan profiles: Quick (1-1024), Common, Full (1-10000), Web, Database
- Identifies 30+ well-known services with risk ratings
- Custom port ranges supported
- Saves results to `.txt`

### 3. Google Dork Generator
```bash
python3 google_dork_generator.py
```
Categories:
- 🔐 Login Pages & Admin Panels
- 📄 Sensitive Files & Documents  
- 🔑 Exposed Credentials & API Keys
- ⚙️ Technology & Infrastructure
- 📋 Open Redirects & Injection Points
- 🌐 Subdomains & Infrastructure
- 📧 Email & User Data

Generates ready-to-use Google/Bing search URLs and can auto-open them in browser.

---

## 📚 Learning Path

1. Practice on **your own machines** or lab environments first
2. Use **TryHackMe** / **HackTheBox** for legal targets
3. Join **bug bounty programs** (HackerOne, Bugcrowd) before targeting real sites
4. Always read the **program scope** before scanning anything

---

## 🔗 Useful Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [HackerOne Programs](https://hackerone.com/bug-bounty-programs)
- [Exploit-DB Google Hacking DB](https://www.exploit-db.com/google-hacking-database)
- [TryHackMe](https://tryhackme.com)
- [HackTheBox](https://hackthebox.com)
