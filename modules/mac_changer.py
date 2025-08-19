import uuid, platform, subprocess
from modules.utils import Colors, clear_screen 
import random, re

def get_mac():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

def random_mac():
    mac = [0x00,0x16,0x3e, random.randint(0x00,0x7f), random.randint(0x00,0xff), random.randint(0x00,0xff)]
    return ':'.join(map(lambda x:"%02x"%x, mac))

def run():
    clear_screen()
    print(f"{Colors.CYAN}MAC CHANGER SIMULATOR{Colors.RESET}")
    print(f"Current MAC: {Colors.GREEN}{get_mac()}{Colors.RESET}")
    interface = input("Network Interface (Linux only, default eth0): ") or "eth0"
    choice = input("Generate Random MAC / Apply? (y/n): ").lower()
    if choice=='y':
        new_mac = random_mac()
        if platform.system()=="Linux":
            subprocess.call(["sudo","ifconfig",interface,"down"])
            subprocess.call(["sudo","ifconfig",interface,"hw","ether",new_mac])
            subprocess.call(["sudo","ifconfig",interface,"up"])
            print(Colors.GREEN+f"MAC changed to: {new_mac}"+Colors.RESET)
        else:
            print(Colors.YELLOW+f"Simulation: MAC changed to {new_mac}"+Colors.RESET)
    input("Press Enter to return to menu...")

