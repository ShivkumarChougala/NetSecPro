import os
import time
from modules import wifi_attack,  network_scanner, mac_changer, web_risk_scanner, blechat

# ------------------ Retro Colors & Styles ------------------
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(f"""{Colors.CYAN}{Colors.BOLD}
   ██████╗ ██╗   ██╗██████╗ ███████╗██████╗ ██╗   ██╗███████╗
  ██╔═══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝
  ██║   ██║██║   ██║██████╔╝█████╗  ██████╔╝██║   ██║█████╗  
  ██║   ██║██║   ██║██╔═══╝ ██╔══╝  ██╔═══╝ ██║   ██║██╔══╝  
  ╚██████╔╝╚██████╔╝██║     ███████╗██║     ╚██████╔╝███████╗
   ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝╚═╝      ╚═════╝ ╚══════╝
{Colors.RESET}""")

def print_option(number, text):
    print(f"{Colors.YELLOW}[{number}]{Colors.RESET} {text}")

def main_menu():
    while True:
        clear_screen()
        print_banner()
        print_option(1, "Network & Port Scanner")
        print_option(2, "MAC Changer Simulator")
        print_option(3, "Web Vulnerability ")
        print_option(4, "blechat")
        print_option(5, "Wifi Pentest")
        print_option(6, "Exit")
        choice = input("\nEnter your choice: ")
        if choice == '1':
            network_scanner.run()
        elif choice == '2':
            mac_changer.run()
        elif choice == '3':
            web_risk_scanner.main()
        elif choice == '4':
            blechat.main()
        elif choice == '5':
            wifi_attack.main()
        elif choice == '6':
            print(Colors.CYAN + "\nExiting platform. Stay safe!" + Colors.RESET)
            break
        else:
            print(Colors.RED + "Invalid choice. Try again." + Colors.RESET)
            time.sleep(1)

if __name__ == "__main__":
    main_menu()

