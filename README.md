A multi-module cybersecurity tool for ethical testing and learning. It includes:

Network & Port Scanner: Scan LAN devices, show hostnames, IPs, open ports, and basic vulnerabilities.

LAN Chat (Offline): Chat with devices on the same network without Internet.

Web Vulnerability Scanner: Check HTTP headers, detect forms, and identify potential XSS/SQLi points.

WiFi Pentest Tool: Detect WiFi interfaces, scan networks, enable monitor mode, and perform deauth attacks (dry-run available).

⚠️ Use only on networks you own or have permission to test


git clone https://github.com/ShivkumarChougala/NetSecPro
cd NetSecPro
source venv/bin/activate
pip install -r requirements.txt
python3 main.py


Usage

Run main.py.

Select a module from the menu.

Follow on-screen instructions:

Network Scanner: choose interface → scan → view ports → vulnerability check.

LAN Chat: start server → connect clients → chat.

Web Scanner: enter website URL → scan headers/forms → view potential vulnerabilities.

WiFi Pentest: select WiFi interface → enable monitor mode → scan networks → optional deauth attack → save report.
