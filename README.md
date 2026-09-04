# 👻 GhostVector

> **Hunt the hidden, Map the vector.**

GhostVector is a lightweight Python security tool for checking whether potentially sensitive files are publicly accessible on web servers.

It currently supports two scanning modes:

- 🎯 **Normal scan** — checks for `/.env`
- 🔥 **Full scan** — checks a list of commonly sensitive/restricted files

> ⚠️ **For authorized security testing only.**

---

## ✨ Features

- 📄 Scan multiple URLs from a file
- 🎯 `.env` scanning
- 🔥 Full scan mode
- 🔍 Checks multiple sensitive file paths
- 🌐 Supports HTTP and HTTPS URLs
- ⚡ HTTP requests using Python `requests`
- 📊 HTTP status code detection
- 🟢 Highlights `200 OK` responses
- 🟡 Detects request timeouts
- 🔴 Displays other HTTP status codes
- 🛡️ Handles file errors and request errors
- ⌨️ Supports `Ctrl+C` to stop a scan
- 💻 Simple command-line interface using `argparse`

---

## 🎯 Scanning Modes

GhostV currently has two scanning modes.

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

The `-f` / `--full` option checks each URL against a list of sensitive files.

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

- 🐍 Python 3.x
- 📦 Requests

---

## 🎯 Usage

GhostV requires a URL list using the `-l` / `--list` option.

### Create a URL list

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

---

### 🎯 Normal Scan

Check for exposed `.env` files:

```bash
python ghostV.py -l urls.txt
```

Or:

```bash
python ghostV.py --list urls.txt
```

---

### 🔥 Full Scan

Check for multiple sensitive files:

```bash
python ghostV.py -l urls.txt -f
```

Or:

```bash
python ghostV.py --list urls.txt --full
```

---

### ❓ Show Help

```bash
python ghostV.py -h
```

---

## 🖥️ Output

### Normal Scan

```text
[VULNERABLE] -> 200 OK  https://example.com/.env

[NOT VULNERABLE] -> 404 https://example.org/.env

[TIMEOUT] -> https://test.example.com/.env
```

### Full Scan

```text
[SCANNING] -> https://example.com

[VULNERABLE] /.env -> 200 OK  https://example.com/.env

[NOT VULNERABLE] /config.php -> 404 https://example.com/config.php

[TIMEOUT] /backup.zip -> https://example.com/backup.zip
```

---

## 📊 Status Indicators

| Indicator | Meaning |
|---|---|
| 🟢 `VULNERABLE` | Server returned `200 OK` for the requested file |
| 🟡 `TIMEOUT` | Request exceeded the 5-second timeout |
| 🔴 `NOT VULNERABLE` | Server returned a status other than `200` |
| 🔵 `SCANNING` | Target is currently being scanned |

> **Important:** A `200 OK` response does **not automatically confirm a vulnerability**.

---

## ⚠️ Important: `200 OK` ≠ Confirmed Exposure

GhostV uses the HTTP status code to identify potentially accessible files.

A `200 OK` response means that the server successfully returned a response, but it does **not necessarily mean that the requested sensitive file exists or contains sensitive information**.

Possible false positives include:

- Custom error pages
- Login pages
- SPA fallback pages
- Catch-all routes
- Reverse proxy responses
- Generic application responses

Always manually verify potential findings.

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

- 🔑 API keys
- 🗄️ Database credentials
- 🔐 Application secrets
- ⚙️ Internal configuration
- 🛠️ Service credentials
- 📦 Application information

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

Main GhostV scanner containing the `.env` and full scanning functionality.

### `requirements.txt`

Contains the Python dependencies required by GhostV.

### `README.md`

Project documentation and usage instructions.

---

## 🧠 Built With

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming language |
| 🌐 Requests | HTTP requests |
| ⚙️ Argparse | Command-line arguments |

---

## 🛡️ Responsible Use

GhostVector is intended for **authorized security testing and educational purposes**.

Use GhostV only against systems where you have permission to perform security testing, such as:

- 🏠 Applications you own
- 🐛 Authorized bug-bounty targets
- 🔐 Authorized penetration-testing targets
- 🧪 CTFs and security labs
- 📚 Your own test environments

Do not scan systems without authorization.

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