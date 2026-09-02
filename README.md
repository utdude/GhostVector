# 👻 GhostVector

### Hunt the hidden. Map the vector.

A lightweight Python tool for detecting potentially exposed `.env` files on web applications.

GhostVector takes a list of URLs, automatically checks their `/.env` endpoint, analyzes the HTTP response, and highlights targets that return `200 OK`.

> ⚠️ **For authorized security testing only.**

---

## ✨ Features

- 📄 Check multiple URLs from a file
- 🔗 Automatically append `/.env`
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

GhostVector keeps the initial check simple:

```text
                 URL List
                    │
                    ▼
               Read URL
                    │
                    ▼
              Append /.env
                    │
                    ▼
            Send HTTP Request
                    │
                    ▼
             Check Status Code
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
         200      Timeout    Other
          │         │         │
          ▼         ▼         ▼
      Potential   Request    Not 200
      Exposure    Timeout
```

### Example

Input:

```text
https://example.com
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

GhostVector accepts a file containing URLs using the `-l` / `--list` option.

### Create your URL list

Create a file such as `urls.txt`:

```text
https://example.com
https://example.org
https://test.example.com
```

Use **one URL per line**.

### Run GhostVector

```bash
python ghostv.py -l urls.txt
```

Or:

```bash
python ghostv.py --list urls.txt
```

### Show help

```bash
python ghostv.py -h
```

---

## 🖥️ Example Output

```text
[VULNERABLE] -> 200 OK  https://example.com/.env

[NOT VULNERABLE] -> 404 https://example.org/.env

[TIMEOUT] -> https://test.example.com/.env

[NOT VULNERABLE] -> 403 https://test.example.net/.env
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

manually inspect the response and confirm that the returned content is actually an exposed `.env` file.

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

The main GhostVector script.

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

**Never scan or test systems without authorization.**

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