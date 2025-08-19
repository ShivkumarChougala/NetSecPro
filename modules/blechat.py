import socket
import threading
from datetime import datetime
import sys
import os
from modules.utils import Colors, clear_screen

# Config
PORT = 5555      # Chat TCP port
BROADCAST_PORT = 5556  # UDP broadcast port

clients = []
nickname = ""

def print_banner():
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔════════════════════════╗")
    print("║  RETRO OFFLINE CHAT    ║")
    print("╚════════════════════════╝")
    print(f"{Colors.RESET}")

def format_message(nick, msg):
    timestamp = datetime.now().strftime("%H:%M")
    return f"[{Colors.YELLOW}{timestamp}{Colors.RESET}] {Colors.CYAN}{nick}{Colors.RESET}: {Colors.GREEN}{msg}{Colors.RESET}"

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            break

def broadcast(message, sender):
    for c in clients:
        if c != sender:
            try:
                c.send(message.encode('utf-8'))
            except:
                clients.remove(c)
                c.close()
    print(message)

# ----------------- Broadcast Discovery -----------------
def start_broadcast():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        udp_sock.sendto(b"CHAT_SERVER_HERE", ('<broadcast>', BROADCAST_PORT))
        threading.Event().wait(2)  # send every 2 seconds

def discover_server(timeout=5):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_sock.bind(('', BROADCAST_PORT))
    udp_sock.settimeout(timeout)
    try:
        data, addr = udp_sock.recvfrom(1024)
        if data == b"CHAT_SERVER_HERE":
            return addr[0]
    except socket.timeout:
        return None
# -------------------------------------------------------

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', PORT))
    server.listen()
    print(Colors.YELLOW+f"Server started on port {PORT}. Waiting for clients..."+Colors.RESET)
    
    # Start broadcasting server presence
    threading.Thread(target=start_broadcast, daemon=True).start()
    
    while True:
        client, addr = server.accept()
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,)).start()

def start_client():
    print(Colors.YELLOW+"Searching for chat server on LAN..."+Colors.RESET)
    server_ip = discover_server()
    if not server_ip:
        print(Colors.RED+"No server found on LAN."+Colors.RESET)
        return
    print(Colors.GREEN+f"Server found at {server_ip}! Connecting..."+Colors.RESET)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, PORT))
    except:
        print(Colors.RED+"Failed to connect to server."+Colors.RESET)
        return
    print(Colors.YELLOW+"Connected! Type messages below. Type 'exit' to leave."+Colors.RESET)

    def receive():
        while True:
            try:
                msg = client.recv(1024).decode('utf-8')
                if msg:
                    print(msg)
            except:
                client.close()
                break

    threading.Thread(target=receive, daemon=True).start()

    while True:
        msg = input()
        if msg.lower() == "exit":
            client.close()
            break
        message = format_message(nickname, msg)
        client.send(message.encode('utf-8'))

def main():
    global nickname
    print_banner()
    nickname = input("Enter your nickname: ")
    print_banner()
    print(f"Hello {Colors.CYAN}{nickname}{Colors.RESET}!\n")
    print("1. Start Chat Server (Host)")
    print("2. Connect as Client")
    print("3. Exit")

    choice = input("\nSelect option: ")
    if choice == "1":
        threading.Thread(target=start_server, daemon=True).start()
        print(Colors.YELLOW+"Server running! Press Ctrl+C to stop."+Colors.RESET)
        print("You can also chat from this terminal.")
        while True:
            msg = input()
            if msg.lower() == "exit":
                print("Server stopped.")
                break
            message = format_message(nickname, msg)
            broadcast(message, None)
    elif choice == "2":
        start_client()
    else:
        return

if __name__ == "__main__":
    main()

