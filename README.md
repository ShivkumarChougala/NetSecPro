# NetSecPro

**NetSecPro** is a multi-module cybersecurity tool for ethical testing and learning. It combines network scanning, web vulnerability assessment, offline LAN chat, and WiFi penetration testing in one platform.

> ⚠️ **Warning:** Use only on networks you own or have explicit permission to test.

---

## Modules

### 1. Network & Port Scanner
- Scan LAN devices and list hostnames, IP addresses, and open ports.
- Identify basic vulnerabilities.

### 2. LAN Chat (Offline)
- Chat with devices on the same network without Internet.
- Secure and easy-to-use messaging.

### 3. Web Vulnerability Scanner
- Check HTTP headers for security configurations.
- Detect forms and potential XSS/SQL injection points.

### 4. WiFi Pentest Tool
- Detect WiFi interfaces and scan available networks.
- Enable monitor mode for testing.
- Perform optional deauthentication attacks (dry-run available).

---

## Installation

```bash
git clone https://github.com/ShivkumarChougala/NetSecPro
cd NetSecPro
source venv/bin/activate
pip install -r requirements.txt
python3 main.py


## Usage
- Run main.py.
- Select a module from the menu.
- Follow on-screen instructions:
- Network Scanner: choose interface → scan → view ports → check vulnerabilities.
- LAN Chat: start server → connect clients → chat.
- Web Scanner: enter website URL → scan headers/forms → view potential vulnerabilities.
- WiFi Pentest: select WiFi interface → enable monitor mode → scan networks → optional deauth attack → save report.
