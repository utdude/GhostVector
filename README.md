# 👻 GhostVector

> **Hunt the hidden, Map the vector.**

GhostVector is a lightweight Python security tool for checking whether potentially sensitive files are publicly accessible on web servers.

It supports scanning a single domain or a list of URLs and can check for `/.env` or a broader list of commonly sensitive files.

> ⚠️ **For authorized security testing only.**

---

## ✨ Features

* 🎯 Scan a single domain directly with `-d`
* 📄 Scan multiple URLs from a file with `-l`
* 🔗 Automatically check `/.env`
* 🔥 Full scan mode for commonly sensitive files
* 🔍 Checks multiple sensitive file paths
* 🍪 Send an authorized custom cookie header with `-c`
* 🌐 Supports HTTP and HTTPS URLs
* ⚡ HTTP requests using Python `requests`
* 📊 HTTP status code detection
* 🟢 Highlights `200 OK` responses
* 🟡 Detects request timeouts
* 🔴 Displays other HTTP status codes
* 🛡️ Handles file and request errors
* ⌨️ Supports `Ctrl+C` to stop a scan
* 💻 Simple command-line interface using `argparse`

---

## 🎯 Scanning Modes

GhostVector currently has two scanning modes.

### Normal Scan

The default mode checks each URL for:

```text
/.env
```

Example:

```bash
python ghostV.py -l urls.txt
```

### Full Scan

The `-f` / `--full` option checks each URL against a list of commonly sensitive files.

Example:

```bash
python ghostV.py -l urls.txt -f
```

The full scan can take longer because each URL is tested against multiple files.

---

## 🔎 How It Works

### Normal `.env` Scan

```text
URL List
   │
   ▼
Read URL
   │
   ▼
Add /.env
   │
   ▼
Send HTTP Request
   │
   ▼
Check Status Code
   │
   ├── 200 ──► Potential Finding
   ├── Timeout
   └── Other Status
```

### 🔥 Full Scan

```text
URL List
   │
   ▼
Read URL
   │
   ▼
Load Sensitive File List
   │
   ▼
Check Each File
   │
   ▼
Send HTTP Request
   │
   ▼
Check Status Code
   │
   ├── 200 ──► Potential Finding
   ├── Timeout
   └── Other Status
```

---

## 📂 Sensitive Files

The full scan currently checks files such as:

```text
.env
.env.local
.env.production
.env.development
.env.staging
.env.backup
.env.old
.env.bak

.git/config
.git/HEAD
.git/index

.htaccess
.htpasswd

web.config

config.php
configuration.php
settings.py
config.py

database.yml
database.yaml

docker-compose.yml
docker-compose.yaml
Dockerfile

package.json
package-lock.json
yarn.lock

composer.json
composer.lock
requirements.txt

wp-config.php

database.sql
dump.sql
backup.sql
db.sql
database.db
database.sqlite
database.sqlite3

backup.zip
backup.tar
backup.tar.gz
site.zip
www.zip

credentials.json
secrets.json
service-account.json
firebase-adminsdk.json

id_rsa
id_rsa.pub
.pem
.key
.p12
.pfx

phpinfo.php
info.php
debug.log
error.log
access.log

.env.example
.gitignore
.editorconfig
tsconfig.json
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/utdude/GhostVector.git
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

* 🐍 Python 3.x
* 📦 Requests

---

## 🎯 Usage

```text
usage: ghostV.py [-h] [-l LIST] [-d DOMAIN] [-c COOKIE] [-f]

options:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  File containing target URLs (one per line)
  -d DOMAIN, --domain DOMAIN
                        Single domain target, e.g. target.com (no http/https)
  -c COOKIE, --cookie COOKIE
                        Send requests with a cookie header
  -f, --full            Full scan for all known sensitive files (default: .env only)
```

### 🔹 Scan a single domain

No need to create a file for one-off checks:

```bash
python ghostV.py -d example.com
```

### 🔹 Scan a list of URLs

Create a file such as:

```text
urls.txt
```

Add one URL per line:

```text
https://example.com
https://example.org
https://test.example.com
```

Run:

```bash
python ghostV.py -l urls.txt
```

Or:

```bash
python ghostV.py --list urls.txt
```

### 🔥 Full sensitive-file scan

By default GhostVector checks `/.env`. Use `-f` / `--full` to check the broader sensitive-file list:

```bash
python ghostV.py -d example.com -f
```

Or:

```bash
python ghostV.py -l urls.txt -f
```

### 🔹 Sending an authorized cookie

If you have an authorized session cookie for a target, you can provide it with `-c` / `--cookie`:

```bash
python ghostV.py -d example.com -c "session=yyyy"
```

This can also be combined with list and full-scan modes:

```bash
python ghostV.py -l urls.txt -f -c "session=yyyy"
```

> 🔐 Only use cookies from sessions you are authorized to test with. Never reuse cookies from third parties or sessions you do not own or control.

### ❓ Show Help

```bash
python ghostV.py -h
```

---

## 🖥️ Output

### Normal Scan

```text
[SCANNING] -> https://example.com

[VULNERABLE] /.env -> 200 OK https://example.com/.env

[NOT VULNERABLE] /.env -> 404 https://example.org/.env

[TIMEOUT] /.env -> https://test.example.com/.env

[NOT VULNERABLE] /.env -> 403 https://test.example.net/.env
```

### Full Scan

```text
[SCANNING] -> https://example.com

[VULNERABLE] /.env -> 200 OK https://example.com/.env

[NOT VULNERABLE] /config.php -> 404 https://example.com/config.php

[TIMEOUT] /backup.zip -> https://example.com/backup.zip
```

---

## 📊 Status Indicators

| Indicator           | Meaning                                         |
| ------------------- | ----------------------------------------------- |
| 🟢 `VULNERABLE`     | Server returned `200 OK` for the requested file |
| 🟡 `TIMEOUT`        | Request exceeded the 5-second timeout           |
| 🔴 `NOT VULNERABLE` | Server returned a status other than `200`       |
| 🔵 `SCANNING`       | Target is currently being scanned               |

> **Important:** A `200 OK` response does **not automatically confirm a vulnerability**.

---

## ⚠️ Important: `200 OK` ≠ Confirmed Exposure

GhostVector uses the HTTP status code to identify potentially accessible files.

A `200 OK` response means that the server successfully returned a response, but it does **not necessarily mean that the requested sensitive file exists or contains sensitive information**.

Possible false positives include:

* Custom error pages
* Login pages
* SPA fallback pages
* Catch-all routes
* Reverse proxy responses
* Generic application responses

Always manually inspect potential findings and confirm that the returned content is actually an exposed sensitive file.

---

## 💡 Why Sensitive Files Matter

Some configuration and backup files can contain sensitive information such as:

```text
DATABASE_URL=...
API_KEY=...
SECRET_KEY=...
DB_PASSWORD=...
```

Depending on the file, exposure could reveal:

* 🔑 API keys
* 🗄️ Database credentials
* 🔐 Application secrets
* ⚙️ Internal configuration
* 🛠️ Service credentials
* 📦 Application information

The actual impact depends on the contents of the exposed file.

---

## 📁 Project Structure

```text
GhostVector/
│
├── 👻 ghostV.py
├── 📦 requirements.txt
└── 📖 README.md
```

### `ghostV.py`

The main GhostVector scanner. It supports:

* `-d` / `--domain` — scan a single domain
* `-l` / `--list` — scan a file of targets
* `-f` / `--full` — check the full list of known sensitive files
* `-c` / `--cookie` — attach an authorized cookie header to requests

### `requirements.txt`

Contains the Python dependencies required by GhostVector.

### `README.md`

Project documentation and usage instructions.

---

## 🧠 Built With

| Technology  | Purpose                   |
| ----------- | ------------------------- |
| 🐍 Python   | Core programming language |
| 🌐 Requests | HTTP requests             |
| ⚙️ Argparse | Command-line arguments    |

---

## 🛡️ Responsible Use

GhostVector is intended for **authorized security testing and educational purposes**.

Use GhostVector only against systems where you have permission to perform security testing, such as:

* 🏠 Applications you own
* 🐛 Authorized bug-bounty targets
* 🔐 Authorized penetration-testing targets
* 🧪 CTFs and security labs
* 📚 Your own test environments
* 📚 Systems where you have explicit permission to test

**Never scan or test systems without authorization.**

Only use `-c` / `--cookie` with credentials from sessions you are authorized to use.

---

## 📜 Disclaimer

GhostVector is provided for educational and authorized security-testing purposes.

The author is not responsible for misuse of this tool or any damage resulting from unauthorized testing.

---

<div align="center">

### 👻 GhostVector

**Hunt the hidden, Map the vector.**

Created by **Utkarsh Rai**

</div>
