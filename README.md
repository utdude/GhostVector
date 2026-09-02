# 🔎 ENV File Exposure Checker

A lightweight Python security-testing tool that checks whether a web application's **`.env` file is publicly accessible**.

The tool reads a list of URLs, automatically targets `/.env`, sends an HTTP request, checks the returned status code, and reports potentially exposed endpoints.

> ⚠️ **For authorized security testing only.** Use this tool only against websites and systems you own or have explicit permission to test.

---

## ✨ Features

* 📄 Read multiple targets from a file
* 🔍 Automatically checks `/.env`
* 🌐 Supports HTTP/HTTPS URLs
* ⚡ Uses Python `requests` for HTTP requests
* 📊 Displays the HTTP status code
* 🟢 Highlights `200 OK` responses
* 🟡 Detects request timeouts
* 🔴 Reports other HTTP responses
* 🛡️ Handles missing and inaccessible input files
* 💻 Simple command-line interface

---

## 📦 Requirements

Before using the tool, make sure you have:

* **Python 3.x**
* **`requests`**

Check your Python installation:

```bash
python --version
```

### Install the dependency

The required Python packages are listed in `requirements.txt`.

Install them with:

```bash
pip install -r requirements.txt
```

Or install `requests` directly:

```bash
pip install requests
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/utdude/testENV.git
```

### 2. Enter the project directory

```bash
cd testENV
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The tool is now ready to use.

---

## 🎯 Usage

The tool requires a file containing the URLs you want to test.

Use the `-l` or `--list` option:

```bash
python script.py -l urls.txt
```

Or:

```bash
python script.py --list urls.txt
```

### URL List Format

Create a file such as `urls.txt`:

```text
https://example.com
https://example.org
https://test.example.com
```

Put **one URL per line**.

The tool will automatically append:

```text
/.env
```

to each target.

For example:

```text
https://example.com
```

becomes:

```text
https://example.com/.env
```

---

## 🖥️ Example

Run:

```bash
python script.py -l urls.txt
```

The tool may produce output such as:

```text
[VULNERABLE] -> 200 OK  https://example.com/.env

[NOT VULNERABLE] -> 404 https://example.org/.env

[TIMEOUT] -> https://test.example.com/.env
```

### Status Indicators

| Output          | Meaning                                                   |
| --------------- | --------------------------------------------------------- |
| 🟢 `200 OK`     | The endpoint returned HTTP 200 and should be investigated |
| 🔴 `404`        | The requested resource was not found                      |
| 🔴 `403`        | Access to the resource was forbidden                      |
| 🟡 `TIMEOUT`    | The request did not complete within the timeout           |
| 🔴 Other status | The server returned another HTTP response                 |

---

## 🔬 How It Works

The tool follows a simple workflow:

```text
             URL List
                │
                ▼
        Read each URL
                │
                ▼
         Append /.env
                │
                ▼
       Send HTTP Request
                │
                ▼
        Get Status Code
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
      200    Timeout   Other
       │        │        │
       ▼        ▼        ▼
   Potential  Timeout  Not 200
   Exposure
```

For example:

```text
https://example.com
        │
        ▼
https://example.com/.env
        │
        ▼
     HTTP 200
        │
        ▼
Potentially exposed
```

---

## ⚠️ Important: `200 OK` ≠ Confirmed `.env` Exposure

A `200 OK` response **does not automatically mean that an actual `.env` file has been exposed**.

Some applications return `200 OK` for:

* Custom error pages
* Login pages
* SPA fallback pages
* Generic application responses
* Reverse-proxy responses
* Catch-all routes

Therefore, a `200` result should be **manually verified** before reporting it as a confirmed vulnerability.

A confirmed exposure should be based on the response actually containing `.env`-style configuration data, rather than the status code alone.

---

## 📁 Project Structure

```text
testENV/
│
├── script.py
├── requirements.txt
├── urls.txt
├── README.md
└── .gitignore
```

### `script.py`

Main Python script responsible for reading targets and checking `/.env`.

### `requirements.txt`

Contains the Python dependencies required by the project.

### `urls.txt`

Example input file containing URLs to test.

> Avoid committing real targets or sensitive information to a public repository.

### `.gitignore`

Prevents files such as local `.env` files, Python cache files, and virtual environments from being committed.

---

## 🛠️ Command Reference

### Show help

```bash
python script.py -h
```

### Provide a URL list

```bash
python script.py -l urls.txt
```

### Long-form option

```bash
python script.py --list urls.txt
```

---

## 🧪 Example Test Flow

```bash
# Clone
git clone https://github.com/utdude/testENV.git

# Enter directory
cd testENV

# Install dependencies
pip install -r requirements.txt

# Create your target list
nano urls.txt

# Run
python script.py -l urls.txt
```

---

## ⚠️ Responsible Use

This project is intended for **authorized security research and testing**.

Appropriate uses include:

* 🛡️ Testing your own applications
* 🐛 Authorized bug bounty programs
* 🔐 Penetration testing with permission
* 🧪 Local security labs
* 📚 Security research and learning

**Do not scan websites, servers, or infrastructure without authorization.**

Always verify that your testing is permitted and within the target's defined scope.

---

## 📜 License

This project is provided for educational and authorized security-testing purposes.

Use it responsibly.
