import socket, ipaddress, nmap, time, sys
from modules.utils import Colors, clear_screen

# Common port descriptions (extendable)
PORT_DESCRIPTIONS = {
    20:"FTP Data",21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",
    80:"HTTP",110:"POP3",111:"RPC",135:"MS RPC",139:"NetBIOS",
    143:"IMAP",443:"HTTPS",445:"SMB",993:"IMAPS",995:"POP3S",
    1723:"PPTP",3306:"MySQL",3389:"RDP",5000:"UPnP",7000:"AFS3-FileServer",
    8080:"HTTP-alt"
}

def get_network_range():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    network = ipaddress.IPv4Network(local_ip+'/24', strict=False)
    return str(network)

def progress_bar(task, duration=0.01, length=30):
    for i in range(length+1):
        percent = int((i/length)*100)
        bar = '█'*i + '-'*(length-i)
        sys.stdout.write(f"\r{task} |{bar}| {percent}%")
        sys.stdout.flush()
        time.sleep(duration)
    print()

def run():
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}NETWORK & PORT SCANNER{Colors.RESET}")

    nm = nmap.PortScanner()
    network_range = get_network_range()
    print(f"Scanning network range: {network_range} ...")
    
    # Ping scan first
    nm.scan(hosts=network_range, arguments='-sn')
    hosts_list = []
    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            try:
                hostname = socket.gethostbyaddr(host)[0]
            except:
                hostname = host
            hosts_list.append((host, hostname))

    if not hosts_list:
        print(Colors.RED+"No active devices found."+Colors.RESET)
        input("Press Enter to return to menu...")
        return

    # Display hosts
    for i, (host, name) in enumerate(hosts_list,1):
        print(f"{i}. {name} ({host})")

    # Select device
    choice = input("\nSelect a device number to scan ports or press Enter to return: ")
    if choice.strip() == '':
        return
    try:
        index = int(choice)-1
        host_ip = hosts_list[index][0]
        name = hosts_list[index][1]
        print(f"\nScanning open ports for {name} ({host_ip}) ...")
        
        # Full TCP port scan
        progress_bar("Scanning ports", duration=0.01, length=40)
        nm.scan(host_ip, arguments='-Pn -T4')
        open_ports=[]
        for proto in nm[host_ip].all_protocols():
            ports = nm[host_ip][proto].keys()
            for port in sorted(ports):
                if nm[host_ip][proto][port]['state']=='open':
                    # Use description from dictionary, else use nmap service name
                    desc = PORT_DESCRIPTIONS.get(port, nm[host_ip][proto][port]['name'].capitalize())
                    # Color-code
                    color = Colors.GREEN if desc != "Unknown" else Colors.YELLOW
                    open_ports.append(f"{color}{port} ({desc}){Colors.RESET}")

        if open_ports:
            print(Colors.CYAN+"\nOpen Ports:"+Colors.RESET)
            print("\n".join(open_ports))
        else:
            print(Colors.YELLOW+"No open ports found."+Colors.RESET)

    except Exception as e:
        print(Colors.RED+f"Error: {e}"+Colors.RESET)

    input("\nPress Enter to return to menu...")

