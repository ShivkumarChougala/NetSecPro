import socket, ipaddress, nmap, time, sys, os
from datetime import datetime
from modules.utils import Colors, clear_screen

# Create logs directory if not exists
if not os.path.exists("logs"):
    os.makedirs("logs")

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

def log_scan(host, open_ports, vuln_results):
    filename = f"logs/network_scan.txt"
    with open(filename,"a") as f:
        f.write(f"\n--- Scan on {host} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        f.write("Open Ports:\n")
        for port, desc in open_ports.items():
            f.write(f"{port}: {desc}\n")
        f.write("Vulnerability Assessment:\n")
        if vuln_results:
            for port, results in vuln_results.items():
                f.write(f"{port}:\n")
                for name, res in results.items():
                    f.write(f"  {name}: {res}\n")
        else:
            f.write("No vulnerabilities found.\n")
        f.write("\n---------------------------\n")

def vulnerability_scan(host_ip, open_ports):
    print(f"\n{Colors.MAGENTA}Starting Vulnerability Assessment on {host_ip}...{Colors.RESET}")
    nm = nmap.PortScanner()
    vuln_results = {}
    
    for port in open_ports:
        print(f"\nScanning port {port} for vulnerabilities...")
        nm.scan(host_ip, str(port), arguments='--script vuln -Pn')
        for host in nm.all_hosts():
            if nm[host].has_tcp(port):
                scripts = nm[host]['tcp'][port].get('script', {})
                if scripts:
                    vuln_results[port] = scripts
                    for name, result in scripts.items():
                        print(f"{Colors.YELLOW}[{port}] {name}:{Colors.RESET} {result}")
                else:
                    print(f"{Colors.GREEN}[{port}] No known vulnerabilities found.{Colors.RESET}")
        progress_bar(f"Completed port {port}", duration=0.005, length=20)
    return vuln_results

def run():
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}NETWORK & PORT SCANNER{Colors.RESET}")

    nm = nmap.PortScanner()
    network_range = get_network_range()
    print(f"Scanning network range: {network_range} ...")
    
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

    for i, (host, name) in enumerate(hosts_list,1):
        print(f"{i}. {name} ({host})")

    choice = input("\nSelect a device number to scan ports or press Enter to return: ")
    if choice.strip() == '':
        return
    try:
        index = int(choice)-1
        host_ip = hosts_list[index][0]
        name = hosts_list[index][1]
        print(f"\nScanning open ports for {name} ({host_ip}) ...")
        
        progress_bar("Scanning ports", duration=0.01, length=40)
        nm.scan(host_ip, arguments='-Pn -T4 -sV')  # Detect version info
        open_ports = {}
        for proto in nm[host_ip].all_protocols():
            ports = nm[host_ip][proto].keys()
            for port in sorted(ports):
                if nm[host_ip][proto][port]['state']=='open':
                    desc = PORT_DESCRIPTIONS.get(port, nm[host_ip][proto][port]['name'].capitalize())
                    open_ports[port] = desc
                    color = Colors.GREEN if desc != "Unknown" else Colors.YELLOW
                    print(f"{color}{port} ({desc}){Colors.RESET}")

        if not open_ports:
            print(Colors.YELLOW+"No open ports found."+Colors.RESET)
            input("\nPress Enter to return to menu...")
            return

        vuln_results = {}
        vuln_choice = input("\nDo you want to run vulnerability assessment on these ports? (y/n): ")
        if vuln_choice.lower() == 'y':
            vuln_results = vulnerability_scan(host_ip, open_ports.keys())

        # Log the results
        log_scan(host_ip, open_ports, vuln_results)

    except Exception as e:
        print(Colors.RED+f"Error: {e}"+Colors.RESET)

    input("\nPress Enter to return to menu...")

