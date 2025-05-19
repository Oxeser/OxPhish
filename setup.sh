#!/bin/bash

RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BLUE='\033[94m'
PURPLE='\033[95m'
CYAN='\033[96m'
WHITE='\033[97m'
BOLD='\033[1m'
END='\033[0m'

clear

print_banner() {
    echo -e "${RED}   ▒█████  ▒██   ██▒${WHITE}  ${BOLD}██▓███   ██░ ██  ██▓  ██████  ██░ ██ ${END}"
    echo -e "${RED}  ▒██▒  ██▒▒▒ █ █ ▒░${WHITE}  ${BOLD}▓██░  ██▒▓██░ ██▒▓██▒▒██    ▒ ▓██░ ██▒${END}"
    echo -e "${RED}  ▒██░  ██▒░░  █   ░${WHITE}  ${BOLD}▓██░ ██▓▒▒██▀▀██░▒██▒░ ▓██▄   ▒██▀▀██░${END}"
    echo -e "${RED}  ▒██   ██░ ░ █ █ ▒ ${WHITE}  ${BOLD}▒██▄█▓▒ ▒░▓█ ░██ ░██░  ▒   ██▒░▓█ ░██ ${END}"
    echo -e "${RED}  ░ ████▓▒░▒██▒ ▒██▒${WHITE}  ${BOLD}▒██▒ ░  ░░▓█▒░██▓░██░▒██████▒▒░▓█▒░██▓${END}"
    echo -e "${RED}  ░ ▒░▒░▒░ ▒▒ ░ ░▓ ░${WHITE}  ${BOLD}▒▓▒░ ░  ░ ▒ ░░▒░▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒${END}"
    echo -e "${RED}    ░ ▒ ▒░ ░░   ░▒ ░${WHITE}  ${BOLD}░▒ ░      ▒ ░▒░ ░ ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░${END}"
    echo -e "${RED}  ░ ░ ░ ▒   ░    ░  ${WHITE}  ${BOLD}░░        ░  ░░ ░ ▒ ░░  ░  ░   ░  ░░ ░${END}"
    echo -e "${RED}      ░ ░   ░    ░  ${WHITE}  ${BOLD}          ░  ░  ░ ░        ░   ░  ░  ░${END}"
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗"
    echo -e "║ ${YELLOW}Tool        ${WHITE}: OxPhish - Advanced Phishing Tool Setup          ║"
    echo -e "║ ${YELLOW}Version     ${WHITE}: 2.1.0                                           ║"
    echo -e "║ ${YELLOW}GitHub      ${WHITE}: https://github.com/Oxeser/OxPhish               ║"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${END}"
    echo ""
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

handle_error() {
    echo -e "\n${RED}[!] Error: $1${END}"
    exit 1
}

success_message() {
    echo -e "${GREEN}[+] $1${END}"
}

info_message() {
    echo -e "${YELLOW}[*] $1${END}"
}

warning_message() {
    echo -e "${YELLOW}[!] $1${END}"
}

check_directory() {
    if [ ! -f "main.py" ]; then
        handle_error "main.py not found! Please run this script from the OxPhish directory."
    fi
    
    if [ ! -d ".git" ]; then
        warning_message "Git repository not found. Skipping update check."
        return 1
    fi
    
    return 0
}

update_tool() {
    info_message "Checking for updates..."
    
    if ! ping -c 1 google.com &> /dev/null; then
        warning_message "No internet connection. Skipping update."
        return 1
    fi
    
    if ! git diff-index --quiet HEAD --; then
        warning_message "Local changes detected. Skipping update to prevent conflicts."
        info_message "Commit or stash your changes if you want to update."
        return 1
    fi
    
    local current_commit=$(git rev-parse HEAD)
    
    git fetch origin main &> /dev/null
    
    local latest_commit=$(git rev-parse origin/main)
    
    if [ "$current_commit" = "$latest_commit" ]; then
        success_message "OxPhish is already up to date!"
        return 0
    fi
    
    info_message "Update available. Updating OxPhish..."
    
    if git pull origin main; then
        success_message "OxPhish updated successfully!"
        return 0
    else
        warning_message "Failed to update OxPhish. Please check manually."
        return 1
    fi
}

install_packages() {
    info_message "Installing required Python packages..."
    
    if ! command_exists "python3"; then
        handle_error "Python 3 is not installed. Please install Python 3 first."
    fi
    
    if ! command_exists "pip3" && ! command_exists "pip"; then
        handle_error "pip is not installed. Please install pip first."
    fi
    
    local pip_cmd="pip3"
    if ! command_exists "pip3"; then
        pip_cmd="pip"
    fi
    
    local packages=("flask" "qrcode[pil]")
    
    for package in "${packages[@]}"; do
        info_message "Installing $package..."
        
        if $pip_cmd install "$package" --user --quiet; then
            success_message "$package installed successfully"
        elif command_exists "sudo" && sudo $pip_cmd install "$package" --quiet; then
            success_message "$package installed successfully (with sudo)"
        else
            warning_message "Failed to install $package. You may need to install it manually."
        fi
    done
    
    if [ -f "requirements.txt" ]; then
        info_message "Installing packages from requirements.txt..."
        if $pip_cmd install -r requirements.txt --user --quiet; then
            success_message "Additional packages installed from requirements.txt"
        elif command_exists "sudo" && sudo $pip_cmd install -r requirements.txt --quiet; then
            success_message "Additional packages installed from requirements.txt (with sudo)"
        else
            warning_message "Some packages from requirements.txt may not have been installed"
        fi
    fi
}

verify_installation() {
    info_message "Verifying installation..."
    
    local python_test="
try:
    import flask
    import qrcode
    print('SUCCESS')
except ImportError as e:
    print(f'MISSING: {e}')
"
    
    local result=$(python3 -c "$python_test" 2>&1)
    
    if [[ "$result" == "SUCCESS" ]]; then
        success_message "All required packages are installed correctly"
    else
        warning_message "Some packages may be missing: $result"
        warning_message "Try running the script again or install packages manually"
    fi
    
    if [ -x "main.py" ]; then
        success_message "main.py has execute permissions"
    else
        info_message "Setting execute permissions for main.py..."
        chmod +x main.py
        success_message "Execute permissions set"
    fi
}

show_menu() {
    echo -e "${CYAN}╔══════════════════════════════════╗"
    echo -e "║         ${YELLOW}SETUP OPTIONS${CYAN}            ║"
    echo -e "╠══════════════════════════════════╣"
    echo -e "║ ${WHITE}[1] Update Tool               ${CYAN}   ║"
    echo -e "║ ${WHITE}[2] Install Packages          ${CYAN}   ║"
    echo -e "║ ${WHITE}[3] Both (Update + Install)   ${CYAN}   ║"
    echo -e "║ ${WHITE}[4] Run OxPhish               ${CYAN}   ║"
    echo -e "║ ${WHITE}[5] Exit                      ${CYAN}   ║"
    echo -e "╚══════════════════════════════════╝${END}"
    echo ""
}

main() {
    print_banner
    
    check_directory
    local git_available=$?
    
    if [ $# -eq 0 ]; then
        while true; do
            show_menu
            read -p "$(echo -e "${YELLOW}[?] Select an option (1-5): ${END}")" choice
            echo ""
            
            case $choice in
                1)
                    if [ $git_available -eq 0 ]; then
                        update_tool
                    else
                        warning_message "Git repository not found. Cannot update."
                    fi
                    echo ""
                    read -p "Press Enter to continue..."
                    ;;
                2)
                    install_packages
                    verify_installation
                    echo ""
                    read -p "Press Enter to continue..."
                    ;;
                3)
                    if [ $git_available -eq 0 ]; then
                        update_tool
                    fi
                    install_packages
                    verify_installation
                    echo ""
                    read -p "Press Enter to continue..."
                    ;;
                4)
                    info_message "Starting OxPhish..."
                    python3 main.py
                    break
                    ;;
                5)
                    info_message "Exiting setup..."
                    exit 0
                    ;;
                *)
                    warning_message "Invalid option. Please select 1-5."
                    echo ""
                    read -p "Press Enter to continue..."
                    ;;
            esac
        done
    else
        case $1 in
            --update|-u)
                if [ $git_available -eq 0 ]; then
                    update_tool
                else
                    warning_message "Git repository not found. Cannot update."
                fi
                ;;
            --install|-i)
                install_packages
                verify_installation
                ;;
            --all|-a)
                if [ $git_available -eq 0 ]; then
                    update_tool
                fi
                install_packages
                verify_installation
                ;;
            --run|-r)
                python3 main.py
                ;;
            --help|-h)
                echo "OxPhish Setup Script"
                echo "Usage: $0 [option]"
                echo ""
                echo "Options:"
                echo "  --update,  -u    Update tool from GitHub"
                echo "  --install, -i    Install required packages"
                echo "  --all,     -a    Update and install packages"
                echo "  --run,     -r    Run OxPhish directly"
                echo "  --help,    -h    Show this help message"
                echo ""
                echo "Run without arguments for interactive menu."
                ;;
            *)
                warning_message "Unknown option: $1"
                echo "Use --help for available options."
                exit 1
                ;;
        esac
    fi
}

trap 'echo -e "\n${RED}[!] Setup interrupted by user${END}"; exit 1' INT

main "$@"