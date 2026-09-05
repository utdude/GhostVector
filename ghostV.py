import requests
import argparse
import sys
import os
import re


ghostu_art = r"""
     ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗██╗   ██╗
    ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██║   ██║
    ██║  ███╗███████║██║   ██║███████╗   ██║   ██║   ██║
    ██║   ██║██╔══██║██║   ██║╚════██║   ██║   ██║   ██║
    ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║  ╚██████╔╝
     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝    ╚═════╝

                         👻 GhostV
              ─────────────────────────────
                 Hunt the hidden, Map the vector.
                 Created by: Utkarsh Rai
              ─────────────────────────────
"""

SENSITIVE_FILES = [
    ".env", ".env.local", ".env.production", ".env.development", ".env.staging",
    ".env.backup", ".env.old", ".env.bak", ".git/config", ".git/HEAD", ".git/index",
    ".htaccess", ".htpasswd", "web.config", "config.php", "configuration.php",
    "settings.py", "config.py", "database.yml", "database.yaml", "docker-compose.yml",
    "docker-compose.yaml", "Dockerfile", "package.json", "package-lock.json",
    "yarn.lock", "composer.json", "composer.lock", "requirements.txt", "wp-config.php",
    "database.sql", "dump.sql", "backup.sql", "db.sql", "database.db", "database.sqlite",
    "database.sqlite3", "backup.zip", "backup.tar", "backup.tar.gz", "site.zip",
    "www.zip", "credentials.json", "secrets.json", "service-account.json",
    "firebase-adminsdk.json", "id_rsa", "id_rsa.pub", ".pem", ".key", ".p12", ".pfx",
    "phpinfo.php", "info.php", "debug.log", "error.log", "access.log",
    ".env.example", ".gitignore", ".editorconfig", "tsconfig.json",
]


class GhostV:
    """Container for all scan logic: normalizing targets, making requests,
    and reporting results. Keeping this as a class (like you started)
    makes it easy to add new scan modes later without touching option()."""

    def __init__(self, cookie=None, full=False, timeout=5):
        self.cookie = cookie
        self.full = full
        self.timeout = timeout
        self.headers = {"Cookie": cookie} if cookie else {}

    # ---------- helpers ----------

    def normalize_base(self, target):
        """Make sure target has a scheme and no trailing slash."""
        t = target.strip()
        if not t:
            return None
        if not t.startswith(("http://", "https://")):
            t = "https://" + t
        t = t.replace(" ", "")
        if t.endswith("/"):
            t = t[:-1]
        return t

    def build_urls(self, base):
        """Return list of (filename, full_url) to check for a given base."""
        files_to_check = SENSITIVE_FILES if self.full else [".env"]
        return [(f, f"{base}/{f}") for f in files_to_check]

    def build_non_persistant_urls(self, base):
        """Return a non-persistant version of the URLs to check for a given base."""
        return base+"/.ghostV-non-persistant-check"

    def check_url(self, url):
        try:
            res = requests.get(url, headers=self.headers, timeout=self.timeout)
            return res
        except requests.Timeout:
            return "TIMEOUT"
        except requests.RequestException:
            return "REQUEST ERROR"
        

    def report(self, label, status, url):
        if status == 200:
            print(f"\033[32m[VULNERABLE] {label} -> 200 OK  {url}\033[0m")
        elif status == "TIMEOUT":
            print(f"\033[33m[TIMEOUT] {label} ->  {url}\033[0m")
        else:
            print(f"\033[31m[NOT VULNERABLE] {label} ->  {status} {url}\033[0m")

    # ---------- scan modes ----------

    def scan_base(self, base):
        """Run every sensitive-file check against a single normalized base URL."""
        print(f"\033[36m[SCANNING] ->  {base}\033[0m\n")
        non_persistant_url = self.build_non_persistant_urls(base)
        non_persistant_response = self.check_url(non_persistant_url)
        for fname, url in self.build_urls(base):
            status = self.check_url(url)
            if non_persistant_response.text == status.text:
                self.report(f"/{fname}", 404, url)
            else:
                self.report(f"/{fname}", status.status_code, url)
                     

    def domain_target(self, domain):
        """Entry point for -d / --domain: a single target string."""
        base = self.normalize_base(domain)
        if base is None:
            print("Error: empty domain provided.")
            return
        self.scan_base(base)

    def target_file(self, list_path):
        """Entry point for -l / --list: a file containing one target per line."""
        try:
            with open(list_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    base = self.normalize_base(line)
                    if base:
                        self.scan_base(base)
        except FileNotFoundError:
            print(f"Error: File not found: {list_path}")
        except PermissionError:
            print(f"Error: Permission denied: {list_path}")
        except OSError as e:
            print(f"Error opening file: {e}")


DOMAIN_RE = re.compile(
    r"^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|"
    r"([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))"
    r"\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$"
)


def option():
    parser = argparse.ArgumentParser(description="Secret/sensitive file exposure scanner.")
    parser.add_argument("-l", "--list", help="File containing target URLs (one per line)")
    parser.add_argument("-d", "--domain", help="Single domain target, e.g. target.com (no http/https)")
    parser.add_argument("-c", "--cookie", help="Send requests with a cookie header (helps bypass Cloudflare/WAF)")
    parser.add_argument("-f", "--full", action="store_true", help="Full scan for all known sensitive files (default: .env only)")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    scanner = GhostV(cookie=args.cookie, full=args.full)

    if args.domain:
        if DOMAIN_RE.match(args.domain):
            scanner.domain_target(args.domain)
        else:
            print("Domain error: please provide the domain target like this: target.com (without http/https)")
    elif args.list:
        scanner.target_file(args.list)
    else:
        print("Error: you must provide either -d/--domain or -l/--list")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    print(ghostu_art)
    try:
        option()
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("exit success!")
        sys.exit(0)