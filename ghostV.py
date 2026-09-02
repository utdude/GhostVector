import requests
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-l",
    "--list",
    required=True,
    help="File containing URLs"
)

args = parser.parse_args()

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
    
# print(f.readline())
