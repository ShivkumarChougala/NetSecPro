import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import ssl
import socket
import json
from modules.utils import Colors, clear_screen

MAX_DEPTH = 2

def print_banner():
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔═════════════════════════════╗")
    print("║   WEB VULNERABILITY SCAN    ║")
    print("╚═════════════════════════════╝")
    print(f"{Colors.RESET}")

# ---- HTTP Headers ----
def check_headers(url):
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        results = {}
        for header in ["X-Frame-Options", "X-Content-Type-Options",
                       "Strict-Transport-Security", "Content-Security-Policy", "Server"]:
            results[header] = headers.get(header, None)
        return results
    except:
        return {}

# ---- Form Detection ----
def scan_forms(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        forms = []
        for form in soup.find_all("form"):
            forms.append({
                "action": form.get("action"),
                "method": form.get("method", "get").lower(),
                "has_file_upload": bool(form.find("input", {"type": "file"}))
            })
        return forms
    except:
        return []

# ---- Safe XSS Test ----
def test_payload(url, param_name, payload):
    try:
        data = {param_name: payload}
        response = requests.post(url, data=data)
        if payload in response.text or "error" in response.text.lower():
            return True
    except:
        return False
    return False

# ---- SSL/TLS Check ----
def check_ssl(url):
    parsed = urlparse(url)
    host = parsed.hostname
    port = 443
    ssl_info = {"https": url.startswith("https"), "valid_cert": False}
    if ssl_info["https"]:
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
                s.settimeout(3)
                s.connect((host, port))
                cert = s.getpeercert()
                ssl_info["valid_cert"] = True
                ssl_info["issuer"] = dict(x[0] for x in cert['issuer'])['organizationName']
        except Exception as e:
            ssl_info["error"] = str(e)
    return ssl_info

# ---- Crawl Site ----
def crawl_site(base_url, depth=0, visited=None):
    if visited is None:
        visited = set()
    if depth > MAX_DEPTH or base_url in visited:
        return visited
    visited.add(base_url)
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a", href=True):
            href = urljoin(base_url, link['href'])
            if urlparse(href).netloc == urlparse(base_url).netloc:
                crawl_site(href, depth+1, visited)
    except:
        pass
    return visited

# ---- Main Scanner ----
def main():
    print_banner()
    base_url = input("Enter website URL (include http/https): ").strip()
    if not base_url.startswith("http"):
        base_url = "http://" + base_url

    print(f"{Colors.CYAN}\n[*] Crawling site and scanning pages...{Colors.RESET}")
    pages = crawl_site(base_url)
    full_report = []

    for page in pages:
        page_report = {"url": page, "headers": {}, "forms": [], "ssl": {}}
        print(f"{Colors.YELLOW}\nScanning page: {page}{Colors.RESET}")

        # Headers
        headers = check_headers(page)
        page_report["headers"] = headers
        for h, val in headers.items():
            if val:
                print(f"{Colors.GREEN}[+] {h}: {val}{Colors.RESET}")
            else:
                print(f"{Colors.RED}[-] {h} missing{Colors.RESET}")

        # SSL
        ssl_info = check_ssl(page)
        page_report["ssl"] = ssl_info
        if not ssl_info.get("https", False):
            print(f"{Colors.RED}[-] HTTPS not enabled{Colors.RESET}")
        elif not ssl_info.get("valid_cert", False):
            print(f"{Colors.RED}[-] SSL certificate invalid{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}[+] SSL certificate valid, issuer: {ssl_info.get('issuer','Unknown')}{Colors.RESET}")

        # Forms
        forms = scan_forms(page)
        page_report["forms"] = forms
        if forms:
            print(f"{Colors.RED}[!] Found {len(forms)} forms! Potential XSS/SQLi/File Upload points{Colors.RESET}")
            for form in forms:
                # safe XSS test
                if test_payload(urljoin(page, form['action']), 'testinput', "<script>alert('XSS')</script>"):
                    print(f"{Colors.RED}[!] Potential XSS detected in {form['action']}{Colors.RESET}")
                    form["xss"] = True
                else:
                    print(f"{Colors.GREEN}[+] No XSS detected in {form['action']}{Colors.RESET}")
                    form["xss"] = False
                if form["has_file_upload"]:
                    print(f"{Colors.RED}[!] Form has file upload input{Colors.RESET}")
                    form["file_upload"] = True
        else:
            print(f"{Colors.GREEN}[+] No forms found on page{Colors.RESET}")

        full_report.append(page_report)

    # Save full report as JSON
    with open("web_scan_report.json", "w") as f:
        json.dump(full_report, f, indent=4)
    print(f"{Colors.CYAN}\nScan complete! Full report saved to web_scan_report.json{Colors.RESET}")
    input("Press Enter to return to menu...")

