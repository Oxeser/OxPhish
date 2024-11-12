import os
import sys
import time
import requests
import subprocess
from termcolor import colored
from pyfiglet import figlet_format

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

def display_main_menu():
    print(colored("=" * 50, 'yellow', attrs=['bold']))
    print(colored("              [01] Instagram Login", 'cyan', attrs=['bold']))
    print(colored("              [00] Exit", 'red', attrs=['bold']))
    print(colored("=" * 50, 'yellow', attrs=['bold']))
    print("\n")

def main_menu():
    clear_screen()
    display_logo()
    check_for_updates()
    while True:
        display_main_menu()
        choice = input(colored("Select an option: ", 'cyan', attrs=['bold']))
        
        if choice == '01':
            pass
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
