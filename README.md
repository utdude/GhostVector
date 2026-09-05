# 👻 GhostVector

### Hunt the hidden. Map the vector.

A lightweight Python tool for detecting potentially exposed `.env` files (and other sensitive files) on web applications.

GhostVector can take a single domain **or** a list of URLs, automatically checks their `/.env` endpoint (or a full list of known sensitive files), analyzes the HTTP response, and highlights targets that return `200 OK`.

> ⚠️ **For authorized security testing only.**

---

## ✨ Features

- 🎯 Scan a single domain directly with `-d`
- 📄 Check multiple URLs from a file with `-l`
- 🔗 Automatically append `/.env` (or the full sensitive-file list with `-f`)
- 🍪 Send a custom cookie header with `-c` to help bypass Cloudflare/WAF checks
- 🌐 Supports HTTP/HTTPS targets
- ⚡ Fast HTTP requests using Python `requests`
- 📊 HTTP status code detection
- 🟢 Highlights `200 OK` responses
- 🟡 Detects request timeouts
- 🔴 Displays other HTTP status codes
- 🛡️ Handles file-related errors
- 💻 Simple CLI interface

---

## 🔎 How It Works

```text
              Domain (-d)  or  URL List (-l)
                         │
                         ▼
                  Normalize target
                         │
                         ▼
             Append /.env (or full list)
                         │
                         ▼
        Send HTTP Request (+ cookie, if -c set)
                         │
                         ▼
                Check Status Code
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
             200      Timeout      Other
              │          │          │
              ▼          ▼          ▼
          Potential   Request     Not 200
          Exposure    Timeout
```

### Example

Input (domain mode):

```text
example.com
```

GhostVector checks:

```text
https://example.com/.env
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/utkarshrai369/GhostVector.git
```

### 2. Enter the directory

```bash
cd GhostVector
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### Requirements

- 🐍 Python 3.x
- 📦 `requests`

---

## 🎯 Usage

```text
usage: ghostv.py [-h] [-l LIST] [-d DOMAIN] [-c COOKIE] [-f]

options:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  File containing target URLs (one per line)
  -d DOMAIN, --domain DOMAIN
                        Single domain target, e.g. target.com (no http/https)
  -c COOKIE, --cookie COOKIE
                        Send requests with a cookie header (helps bypass Cloudflare/WAF)
  -f, --full            Full scan for all known sensitive files (default: .env only)
```

### 🔹 Scan a single domain directly

No need to build a file for one-off checks — just pass the domain straight in (no `http://` or `https://` prefix):

```bash
python ghostv.py -d example.com
```

### 🔹 Scan a list of URLs from a file

Create a file such as `urls.txt`, **one URL per line**:

```text
https://example.com
https://example.org
https://test.example.com
```

Run:

```bash
python ghostv.py -l urls.txt
```

Or:

```bash
python ghostv.py --list urls.txt
```

### 🔹 Full sensitive-file scan

By default GhostVector only checks `/.env`. Add `-f` / `--full` to also check a broader list of commonly exposed files (`.git/config`, `wp-config.php`, `docker-compose.yml`, `id_rsa`, backup dumps, etc.):

```bash
python ghostv.py -d example.com -f
python ghostv.py -l urls.txt -f
```

### 🔹 Sending a cookie (bypass Cloudflare / WAF)

Some targets sit behind Cloudflare or an application WAF that blocks unauthenticated/anonymous requests. If you have an authorized session cookie for the target, pass it with `-c` / `--cookie` so requests are sent with that cookie attached:

```bash
python ghostv.py -d example.com -c "cf_clearance=xxxx; session=yyyy"
```

This also works combined with `-l` and `-f`:

```bash
python ghostv.py -l urls.txt -f -c "session=yyyy"
```

> 🔐 Only use cookies from sessions you are authorized to test with. Never reuse cookies harvested from third parties or sessions you don't own/control.

### Show help

```bash
python ghostv.py -h
```

---

## 🖥️ Example Output

```text
[SCANNING] ->  https://example.com

[VULNERABLE] /.env -> 200 OK  https://example.com/.env

[NOT VULNERABLE] /.env ->  404 https://example.org/.env

[TIMEOUT] /.env ->  https://test.example.com/.env

[NOT VULNERABLE] /.env ->  403 https://test.example.net/.env
```

### Status Indicators

| Status | Result |
|:---:|---|
| 🟢 `200 OK` | Potential exposure — investigate further |
| 🟡 `TIMEOUT` | Request exceeded the timeout limit |
| 🔴 `403` | Access to the endpoint was forbidden |
| 🔴 `404` | Endpoint was not found |
| 🔴 Other | Server returned another HTTP status |

---

## ⚠️ Important: 200 Does Not Mean Confirmed Exposure

A `200 OK` response **does not automatically confirm that a `.env` file is exposed**.

Some applications return `200` for:

- Custom error pages
- Login pages
- SPA fallback pages
- Catch-all routes
- Reverse-proxy responses
- Generic application pages

Therefore, GhostVector's `200 OK` result should be considered a **potential finding**, not a confirmed vulnerability.

### 🔬 Always verify

If a target returns:

```text
200 OK
```

manually inspect the response and confirm that the returned content is actually an exposed sensitive file.

---

## 💡 Why Check `.env`?

Environment files can contain sensitive application configuration such as:

```text
DATABASE_URL=...
API_KEY=...
SECRET_KEY=...
DB_PASSWORD=...
```

If these values are publicly accessible, they could potentially expose:

- 🔑 Application secrets
- 🗄️ Database credentials
- 🔐 API keys
- ⚙️ Internal configuration
- 🛠️ Service credentials

The severity depends on the information contained within the exposed file.

---

## 📁 Project Structure

```text
GhostVector/
│
├── 👻 ghostv.py
├── 📦 requirements.txt
└── 📖 README.md
```

### `ghostv.py`

The main GhostVector script. Supports:

- `-d` / `--domain` — scan a single domain
- `-l` / `--list` — scan a file of targets
- `-f` / `--full` — check the full list of known sensitive files instead of just `.env`
- `-c` / `--cookie` — attach a cookie header to every request

### `requirements.txt`

Contains the Python dependencies required by the project.

### `README.md`

Project documentation and usage guide.

---

## 🧠 Built With

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming language |
| 🌐 Requests | HTTP requests |
| ⚙️ Argparse | Command-line arguments |

---

## 🛡️ Responsible Use

GhostVector is designed for **authorized security testing and research**.

Use it only against:

- 🏠 Applications you own
- 🐛 Authorized bug-bounty targets
- 🔐 Penetration-testing targets
- 🧪 CTFs and security labs
- 📚 Systems where you have explicit permission to test

**Never scan or test systems without authorization**, and never use `-c`/`--cookie` with credentials you are not authorized to use.

Always verify that your target is within the permitted scope of the security program or engagement.

---

## 📜 Disclaimer

GhostVector is provided for **educational and authorized security-testing purposes**.

The author is not responsible for misuse of this tool or any damage resulting from unauthorized testing.

---

<div align="center">

## 👻 GhostVector

### Hunt the hidden. Map the vector.

**Built for security research.**

</div>