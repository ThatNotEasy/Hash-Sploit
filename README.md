# 🔐 Hash-Sploit

**Hash-Sploit** is a powerful and lightweight Python tool designed to detect and crack cryptographic hashes using a wordlist. Whether you're analyzing unknown hash strings or performing dictionary attacks, HashHunter provides a user-friendly, terminal-based experience with progress tracking, threading, and algorithm awareness.

---

## 🚀 Features

- 🧠 **Smart Hash Detection** — Automatically detects popular hash algorithms based on input string.
- 🛠️ **Modular Design** — Easily extend or integrate with custom modules.
- 🔄 **Multithreaded Cracking** — Speed up brute-force attempts using multiple threads.
- 📈 **Live Progress Display** — Real-time feedback on cracking progress.
- 📂 **Wordlist Support** — Use any custom dictionary file to crack hashes.
- 🧪 **Algorithm-aware Cracker** — Adapts its approach depending on hash type (MD5, SHA1, SHA256, bcrypt, etc).
- 💾 **Output Logging** — Optionally save cracked hashes to a file.

---

## 🧰 Supported Hashes

- MD5
- SHA1
- SHA224 / SHA256 / SHA384 / SHA512
- bcrypt
- More coming soon...

---

## 📦 Installation

```bash
git clone https://github.com/ThatNotEasy/Hash-Sploit.git
cd Hash-Sploit
pip install -r requirements.txt
```

> ✅ Python 3.8+ recommended

---

## ⚙️ Usage

```bash
python main.py -i <HASH> -w <WORDLIST> -t <THREADS> [-o <OUTPUT_FILE>]
```

### 🔍 Example:

```bash
python main.py -i 5f4dcc3b5aa765d61d8327deb882cf99 -w rockyou.txt -t 4
```

### 🧾 Arguments:

| Flag            | Description                             |
|-----------------|-----------------------------------------|
| `-i`, `--input` | 🔢 The hash string to analyze/crack     |
| `-w`, `--wordlist` | 📚 Path to the wordlist file        |
| `-t`, `--threads` | ⚙️  Number of threads to use         |
| `-o`, `--output` | 💾 File to save cracked results (opt) |

---

## 🖼️ Sample Output

```bash
[🔍] Hash Analysis:

 - Input: 5f4dcc3b5aa765d61d8327deb882cf99
 - Algorithm: MD5
 - Length: 32

[⚡] Starting cracking process:
 - Algorithm: MD5
 - Wordlist: rockyou.txt (14,344,391 passwords)
 - Threads: 4

[✅] SUCCESS: Password found - password
[📁] Results saved to: cracked_hashes.txt

[⏱️] Total processing time: 2.84 seconds
```

---

## 🛑 Notes & Warnings

- ⚠️ Cracking hashes like **bcrypt** can be significantly slower due to computational cost.
- ⚠️ Always ensure you have legal permission before attempting to crack any hash.
- 🚫 This tool is for **educational** and **authorized testing** purposes only.

---

## 🤝 Contributing

PRs and issues are welcome! Feel free to fork the repo and submit suggestions, bug reports, or feature requests.
