import os
import time
import random
import socket
import ipaddress
import nmap
import uuid
import platform
import subprocess
import requests
from urllib.parse import urljoin
import re

# ------------------ Color & Style Functions ------------------
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_title(text):
    print(Colors.CYAN + Colors.BOLD + "\n" + text + "\n" + Colors.RESET)

def print_option(number, text):
    print(f"{Colors.YELLOW}[{number}]{Colors.RESET} {text}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ------------------ Module 1: Network & Port Scanner ------------------
PORT_DESCRIPTIONS = {
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP",
}

def get_network_range():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        network = ipaddress.IPv4Network(local_ip + '/24', strict=False)
        return str(network)
    except:
        print(Colors.RED + "Could not detect network range." + Colors.RESET)
        return None

def network_scanner():
    clear_screen()
    print_title("NETWORK & PORT SCANNER")
    nm = nmap.PortScanner()
    network_range = get_network_range()
    if not network_range:
        input("Press Enter to return to main menu...")
        return
    print(f"Scanning network range: {network_range} ...")
    try:
        nm.scan(hosts=network_range, arguments='-sn')
        hosts_list = []
        for host in nm.all_hosts():
            if nm[host].state() == 'up':
                try:
                    hostname = socket.gethostbyaddr(host)[0]
                except:
                    hostname = "Unknown"
                hosts_list.append((host, hostname))
        if not hosts_list:
            print(Colors.RED + "No active devices found." + Colors.RESET)
        for i, (host, hostname) in enumerate(hosts_list, 1):
            print(f"{i}. {host} ({hostname})")
        # Optional: scan open ports for first device
        if hosts_list:
            choice = input("Scan ports for a device? Enter number or 'n': ")
            if choice.lower() != 'n':
                try:
                    index = int(choice) - 1
                    host_ip = hosts_list[index][0]
                    nm.scan(host_ip, arguments='-Pn -T4 -F')
                    open_ports = []
                    for proto in nm[host_ip].all_protocols():
                        ports = nm[host_ip][proto].keys()
                        for port in ports:
                            if nm[host_ip][proto][port]['state'] == 'open':
                                open_ports.append(f"{port} ({PORT_DESCRIPTIONS.get(port,'Unknown')})")
                    if open_ports:
                        print(Colors.RED + f"Open ports: {open_ports}" + Colors.RESET)
                    else:
                        print(Colors.GREEN + "No open ports found." + Colors.RESET)
                except:
                    print(Colors.RED + "Invalid selection." + Colors.RESET)
    except Exception as e:
        print(Colors.RED + f"Network scan failed: {e}" + Colors.RESET)
    input("Press Enter to return to main menu...")

# ------------------ Module 2: MAC Changer Simulator ------------------
def get_mac():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

def random_mac():
    mac = [ 0x00, 0x16, 0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def mac_changer():
    clear_screen()
    print_title("MAC CHANGER SIMULATOR")
    print(f"Current MAC: {Colors.GREEN}{get_mac()}{Colors.RESET}")
    interface = input("Network Interface (Linux only, default eth0): ") or "eth0"
    choice = input("Generate Random MAC / Apply? (y/n): ").lower()
    if choice == 'y':
        new_mac = random_mac()
        if platform.system() == "Linux":
            try:
                subprocess.call(["sudo", "ifconfig", interface, "down"])
                subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
                subprocess.call(["sudo", "ifconfig", interface, "up"])
                print(Colors.GREEN + f"MAC changed to: {new_mac}" + Colors.RESET)
            except:
                print(Colors.RED + "Failed to change MAC." + Colors.RESET)
        else:
            print(Colors.YELLOW + f"Simulation: MAC changed to {new_mac}" + Colors.RESET)
    input("Press Enter to return to main menu...")

# ------------------ Module 3: Web Vulnerability & Risk Scorer ------------------
DEFAULT_PAGES = ["/admin", "/login", "/administrator", "/wp-admin"]

def web_risk_scanner():
    clear_screen()
    print_title("WEB VULNERABILITY / RISK SCORER")
    url = input("Enter your website URL or local server: ").strip()
    if not url.startswith("http"):
        url = "http://" + url
    results = []
    risk_score = 0

    # HTTPS check
    if url.startswith("http://"):
        results.append("Site is HTTP only (not secure).")
        risk_score += 2
    else:
        results.append("Site uses HTTPS (secure).")

    try:
        response = requests.get(url, timeout=5)
    except:
        print(Colors.RED + "Failed to reach site." + Colors.RESET)
        input("Press Enter to return to main menu...")
        return

    # Default pages
    open_pages = []
    for page in DEFAULT_PAGES:
        full_url = urljoin(url, page)
        try:
            r = requests.get(full_url, timeout=3)
            if r.status_code == 200:
                open_pages.append(page)
                risk_score += 2
        except:
            pass
    if open_pages:
        results.append(f"Default admin pages found: {open_pages}")
    else:
        results.append("No common admin pages detected.")

    # Weak headers
    headers = response.headers
    weak_headers = []
    if "X-Frame-Options" not in headers:
        weak_headers.append("X-Frame-Options missing")
        risk_score += 1
    if "Content-Security-Policy" not in headers:
        weak_headers.append("Content-Security-Policy missing")
        risk_score += 1
    if weak_headers:
        results.append(f"Weak headers: {weak_headers}")
    else:
        results.append("All recommended security headers found.")

    # Risk score display
    if risk_score >= 6:
        color = Colors.RED
        level = "High Risk"
    elif risk_score >= 3:
        color = Colors.YELLOW
        level = "Medium Risk"
    else:
        color = Colors.GREEN
        level = "Low Risk"
    results.append(f"Risk Score: {risk_score} ({level})")
    print(color + "\n".join(results) + Colors.RESET)
    input("Press Enter to return to main menu...")

# ------------------ Main Menu ------------------
def main_menu():
    while True:
        clear_screen()
        print_title("CYBER SECURITY AWARENESS PLATFORM (RETRO STYLE)")
        print_option(1, "Network & Port Scanner")
        print_option(2, "MAC Changer Simulator")
        print_option(3, "Web Vulnerability / Risk Scorer")
        print_option(4, "Exit")
        choice = input("\nEnter your choice: ")
        if choice == '1':
            network_scanner()
        elif choice == '2':
            mac_changer()
        elif choice == '3':
            web_risk_scanner()
        elif choice == '4':
            print(Colors.CYAN + "\nExiting platform. Stay safe!" + Colors.RESET)
            break
        else:
            print(Colors.RED + "Invalid choice. Try again." + Colors.RESET)
            time.sleep(1)

# ------------------ Run ------------------
if __name__ == "__main__":
    main_menu()
