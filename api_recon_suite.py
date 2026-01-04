import sys
import subprocess
import argparse
import time
import re
from urllib.parse import urljoin

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_and_import("requests")
install_and_import("colorama")

import requests
from colorama import Fore, Style, init

init(autoreset=True)

BANNER = f"""
{Fore.CYAN} █████╗ ██████╗ ██╗    ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
{Fore.CYAN}██╔══██╗██╔══██╗██║    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
{Fore.CYAN}███████║██████╔╝██║    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
{Fore.CYAN}██╔══██║██╔═══╝ ██║    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
{Fore.CYAN}██║  ██║██║     ██║    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
{Fore.CYAN}╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
{Style.BRIGHT}     API RECON & WEB SECURITY SUITE v1.2
"""

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-u", "--url")
args = parser.parse_args()

headers = {"User-Agent": "Security-Suite/1.2"}

api_paths = [
    "/api", "/api/v1", "/api/v2", "/api/v3",
    "/swagger", "/swagger-ui.html", "/v3/api-docs",
    "/openapi.json", "/actuator", "/admin/api"
]

hidden_paths = [
    "/admin", "/login", "/.git", "/.env", "/backup", "/config"
]

security_headers = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Strict-Transport-Security",
    "Referrer-Policy"
]

def label(level, text):
    color = {
        "INFO": Fore.CYAN,
        "POTENTIAL": Fore.YELLOW,
        "HIGH": Fore.RED
    }.get(level, Fore.WHITE)
    print(color + f"[{level}] {text}")

def api_scan():
    found = False
    for path in api_paths:
        try:
            r = requests.get(args.url.rstrip("/") + path, headers=headers, timeout=5)
            if r.status_code in [200, 401, 403]:
                label("POTENTIAL", f"API endpoint {path} ({r.status_code})")
                found = True
        except Exception:
            pass
    if not found:
        label("INFO", "No API endpoints discovered")

def health_check():
    try:
        start = time.time()
        r = requests.get(args.url, headers=headers, timeout=10)
        label("INFO", f"Status {r.status_code}, response {round(time.time() - start, 2)}s")
    except Exception:
        label("INFO", "Target unreachable")

def header_check():
    try:
        r = requests.get(args.url, headers=headers, timeout=5)
        missing = False
        for h in security_headers:
            if h not in r.headers:
                label("INFO", f"Missing header: {h}")
                missing = True
        if not missing:
            label("INFO", "All common security headers present")
    except Exception:
        label("INFO", "Failed to fetch headers")

def robots_and_hidden_scan():
    found_any = False
    try:
        robots_url = urljoin(args.url, "/robots.txt")
        r = requests.get(robots_url, headers=headers, timeout=5)
        if r.status_code == 200:
            label("INFO", "robots.txt accessible")
            disallows = re.findall(r"Disallow:\s*(/[^\\s]*)", r.text)
            for d in disallows:
                try:
                    rr = requests.get(urljoin(args.url, d), headers=headers, timeout=5)
                    if rr.status_code in [200, 401, 403]:
                        label("POTENTIAL", f"Disallowed path accessible: {d} ({rr.status_code})")
                        found_any = True
                except Exception:
                    pass
    except Exception:
        pass

    for path in hidden_paths:
        try:
            r = requests.get(args.url.rstrip("/") + path, headers=headers, timeout=5)
            if r.status_code in [200, 401, 403]:
                label("HIGH", f"Sensitive path exposed: {path} ({r.status_code})")
                found_any = True
        except Exception:
            pass

    if not found_any:
        label("INFO", "No sensitive or disallowed paths exposed")

def menu():
    print(BANNER)
    print(Fore.CYAN + "[1] API Recon Scan")
    print(Fore.CYAN + "[2] Endpoint Health Check")
    print(Fore.CYAN + "[3] Security Header Check")
    print(Fore.CYAN + "[4] Robots.txt & Hidden Path Scan")
    print(Fore.CYAN + "[5] Exit")

    choice = input(Fore.YELLOW + "\nSelect option: ")

    if choice in ["1", "2", "3", "4"] and not args.url:
        args.url = input(Fore.YELLOW + "Enter target URL: ")

    if choice == "1":
        api_scan()
    elif choice == "2":
        health_check()
    elif choice == "3":
        header_check()
    elif choice == "4":
        robots_and_hidden_scan()
    elif choice == "5":
        sys.exit(0)
    else:
        print(Fore.RED + "Invalid option")

if __name__ == "__main__":
    menu()
