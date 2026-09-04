print(r"""
     ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗██╗   ██╗
    ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██║   ██║
    ██║  ███╗███████║██║   ██║███████╗   ██║   ██║   ██║
    ██║   ██║██╔══██║██║   ██║╚════██║   ██║   ██║   ██║
    ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ╚██████╔╝
     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝    ╚═════╝

                         👻 GhostV
              ─────────────────────────────
                 Hunt the hidden, Map the vector.
                 Created by: Utkarsh Rai
              ─────────────────────────────
""")

import requests
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-l",
    "--list",
    required=True,
    help="File containing URLs"
)
parser.add_argument(
    "-f",
    "--full",
    help="Full scan for all restricted files (may take longer)",
    action="store_true"
)
args = parser.parse_args()

if args.list and args.full:

    SENSITIVE_FILES=[".env",".env.local",".env.production",".env.development",".env.staging",".env.backup",".env.old",".env.bak",".git/config",".git/HEAD",".git/index",".htaccess",".htpasswd","web.config","config.php","configuration.php","settings.py","config.py","database.yml","database.yaml","docker-compose.yml","docker-compose.yaml","Dockerfile","package.json","package-lock.json","yarn.lock","composer.json","composer.lock","requirements.txt","wp-config.php","database.sql","dump.sql","backup.sql","db.sql","database.db","database.sqlite","database.sqlite3","backup.zip","backup.tar","backup.tar.gz","site.zip","www.zip","credentials.json","secrets.json","service-account.json","firebase-adminsdk.json","id_rsa","id_rsa.pub",".pem",".key",".p12",".pfx","phpinfo.php","info.php","debug.log","error.log","access.log",".env.example",".gitignore",".editorconfig","tsconfig.json"]

    try:
            with open(args.list, "r") as f:
                for x in f:
                    print("\033[36m[SCANNING] ->  " + x.strip() + "\033[0m")
                    print("\n")
                    for sensitive_file in SENSITIVE_FILES:
                        t = x.strip()
                        if not t.startswith(("http://", "https://")):
                            t = "https://" + t
                        if t[-1] == "/":
                            t = t+sensitive_file
                        else:
                            t = t+"/"+sensitive_file
                        t = t.replace(" ", "")
                        try:
                            res = requests.get(t, timeout=5).status_code
                        except requests.Timeout:
                            res = "TIMEOUT"
                        except requests.RequestException as e:
                            res = "REQUEST ERROR"
                        if res == 200:
                            print("\033[32m[VULNERABLE] /" + sensitive_file + " -> 200 OK  " + t + "\033[0m")
                        elif res == "TIMEOUT":
                            print("\033[33m[TIMEOUT] /" + sensitive_file + " ->  " + t + "\033[0m")
                        else:
                            print("\033[31m[NOT VULNERABLE] /" + sensitive_file + "->  " + str(res) + " " + t + "\033[0m")
    
    except FileNotFoundError:
        print(f"Error: File not found: {args.list}")
    
    except PermissionError:
        print(f"Error: Permission denied: {args.list}")
    
    except OSError as e:
        print(f"Error opening file: {e}")

    except KeyboardInterrupt:
            print("\n[!] Scan stopped by user.")

    
elif args.list:
    try:
        with open(args.list, "r") as f:
            for x in f:
                t = x.strip()
                if not t.startswith(("http://", "https://")):
                    t = "https://" + t
                if t[-1] == "/":
                    t = t+".env"
                else:
                    t = t+"/.env"
                t = t.replace(" ", "")
                try:
                    res = requests.get(t, timeout=5).status_code
                except requests.Timeout:
                    res = "TIMEOUT"
                except requests.RequestException as e:
                    res = "REQUEST ERROR"
                if res == 200:
                    print("\033[32m[VULNERABLE] -> 200 OK  " + t + "\033[0m")
                elif res == "TIMEOUT":
                    print("\033[33m[TIMEOUT] ->  " + t + "\033[0m")
                else:
                    print("\033[31m[NOT VULNERABLE] ->  " + str(res) + " " + t + "\033[0m")

    except FileNotFoundError:
        print(f"Error: File not found: {args.list}")

    except PermissionError:
        print(f"Error: Permission denied: {args.list}")

    except OSError as e:
        print(f"Error opening file: {e}")
                   
    except KeyboardInterrupt:
        print("\n[!] Scan stopped by user.")
