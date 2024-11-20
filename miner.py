import os
import time
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
import pyfiglet
import requests
from mnemonic import Mnemonic
from bip32utils import BIP32Key

API_URL = "https://blockchain.info/balance"
found_count = 0
attempt_count = 0

def check_balance(address, mnemonic):
    global found_count
    try:
        response = requests.get(API_URL, params={"active": address})
        response.raise_for_status()
        data = response.json()
        balance = float(data[address]["final_balance"]) / 1e8
        if balance > 0:
            found_count += 1
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            output = f"{current_time} | Found: {colored(found_count, 'green')} | Attempt: {colored(attempt_count, 'yellow')} | Address: {colored(address, 'cyan')} | Balance: {colored(balance, 'red')} BTC"
            print(output)
            save_to_file(mnemonic, address, balance)
            return True
    except Exception:
        pass
    return False

def mnemonic_to_address(mnemonic):
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic)
    bip32_key = BIP32Key.fromEntropy(seed)
    address = bip32_key.Address()
    return address

def generate_mnemonic(word_count=12):
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=128)

def save_to_file(mnemonic, address, balance):
    with open("founds.txt", "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | Mnemonic: {mnemonic}\n")
        f.write(f"Address: {address}\nBalance: {balance} BTC\n\n")

def process_mnemonic(mnemonic):
    global attempt_count
    attempt_count += 1
    address = mnemonic_to_address(mnemonic)
    found = check_balance(address, mnemonic)
    if not found:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"{current_time} | Found: {colored(found_count, 'green')} | Attempt: {colored(attempt_count, 'yellow')} | Address: {colored(address, 'cyan')} | Balance: {colored(0, 'red')} BTC")

def wallet_checker():
    print(colored("Wallet Checker başlatılıyor...\n", "cyan"))
    time.sleep(1)
    num_workers = 15
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        while True:
            mnemonics = [generate_mnemonic(12) for _ in range(num_workers)]
            executor.map(process_mnemonic, mnemonics)

def view_wallets():
    print(colored("\nBulunan Cüzdanlar:\n", "cyan", attrs=["bold"]))
    try:
        with open("founds.txt", "r") as f:
            content = f.read()
            if content.strip():
                print(colored(content, "yellow"))
            else:
                print(colored("Henüz hiçbir cüzdan bulunamadı.", "red"))
    except FileNotFoundError:
        print(colored("Henüz hiçbir cüzdan bulunamadı.", "red"))
    input(colored("\nDevam etmek için bir tuşa basın...", "green"))

def exit_program():
    print(colored("\nÇıkış yapılıyor...", "red"))
    time.sleep(1)
    exit()

def main_menu():
    while True:
        os.system("clear")
        logo = pyfiglet.figlet_format("Wallet Checker")
        print(colored(logo, "blue", attrs=["bold"]))
        print(colored("Developed by Yuşa\n", "yellow", attrs=["bold"]))
        print(colored("1. Wallet Checker'ı Başlat", "cyan"))
        print(colored("2. Bulunan Cüzdanları Görüntüle", "cyan"))
        print(colored("3. Çıkış", "red"))
        choice = input(colored("\nSeçiminizi yapın (1/2/3): ", "green"))
        if choice == "1":
            wallet_checker()
        elif choice == "2":
            view_wallets()
        elif choice == "3":
            exit_program()
        else:
            print(colored("Geçersiz seçim. Lütfen tekrar deneyin.", "red"))
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
