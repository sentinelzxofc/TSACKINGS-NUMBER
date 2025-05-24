#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

AUTHOR="sentinelzxofc"
REPO_URL="https://github.com/sentinelzxofc/TSACKINGS-NUMBER"
INSTAGRAM="@sentinelzxofc"

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%???}
        sleep $delay
        printf "\r"
    done
    printf "    \r"
}

print_header() {
    clear
    echo -e "${CYAN}"
    echo -e "  ████████╗███████╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗ ███████╗"
    echo -e "  ╚══██╔══╝██╔════╝██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝ ██╔════╝"
    echo -e "     ██║   ███████╗███████║██║     █FFFFE╔╝ ██║██╔██╗ ██║██║  ███╗███████╗"
    echo -e "     ██║   ╚════██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║╚════██║"
    echo -e "     ██║   ███████║██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝███████║"
    echo -e "     ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝"
    echo -e "                                       Installer by ${AUTHOR}${NC}"
    echo -e "${YELLOW}                                       Repo: ${REPO_URL}${NC}"
    echo -e "${BLUE}                                       Instagram: ${INSTAGRAM}${NC}"
    echo
}

print_step() {
    echo -e "${GREEN}[*] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[!] $1${NC}"
}

print_error() {
    echo -e "${RED}[X] $1${NC}"
}

check_command() {
    command -v $1 >/dev/null 2>&1
}

print_header

print_step "Exibindo Aviso Legal e Termos de Uso (Português)"
sleep 1
if [ -f "DISCLAIMER_PT.md" ]; then
    cat DISCLAIMER_PT.md
else
    print_error "Arquivo DISCLAIMER_PT.md não encontrado!"
    exit 1
fi
echo

print_step "Displaying Disclaimer and Terms of Use (English)"
sleep 1
if [ -f "DISCLAIMER_EN.md" ]; then
    cat DISCLAIMER_EN.md
else
    print_error "DISCLAIMER_EN.md file not found!"
    exit 1
fi
echo

print_warning "Ao continuar, você confirma que leu, entendeu e concorda com os termos acima."
print_warning "By continuing, you confirm that you have read, understood, and agree to the terms above."
read -p "Você concorda em continuar? (s/N) / Do you agree to continue? (y/N): " confirm

if [[ ! "$confirm" =~ ^[SsYy]$ ]]; then
    print_error "Instalação cancelada pelo usuário."
    print_error "Installation cancelled by user."
    exit 1
fi

print_header
print_step "Iniciando a instalação... / Starting installation..."
sleep 1

PKG_MANAGER=""
if check_command apt-get; then
    PKG_MANAGER="apt-get"
elif check_command pkg; then
    PKG_MANAGER="pkg"
elif check_command yum; then
    PKG_MANAGER="yum"
elif check_command dnf; then
    PKG_MANAGER="dnf"
elif check_command pacman; then
    PKG_MANAGER="pacman"
else
    print_error "Gerenciador de pacotes não suportado. Instale as dependências manualmente: python3, pip3, git, curl"
    print_error "Unsupported package manager. Please install dependencies manually: python3, pip3, git, curl"
    exit 1
fi

DEPENDENCIES=("python3" "python3-pip" "git" "curl")
if [ "$PKG_MANAGER" == "pkg" ]; then
    DEPENDENCIES=("python" "git" "curl")
fi

print_step "Verificando e instalando dependências do sistema... / Checking and installing system dependencies... ($PKG_MANAGER)"
for dep in "${DEPENDENCIES[@]}"; do
    if ! check_command ${dep//3-pip/}; then
        print_warning "Instalando $dep... / Installing $dep..."
        sudo $PKG_MANAGER update -y > /dev/null 2>&1 &
        spinner $!
        sudo $PKG_MANAGER install $dep -y > /dev/null 2>&1 &
        spinner $!
        if ! check_command ${dep//3-pip/}; then
            print_error "Falha ao instalar $dep. Verifique seu gerenciador de pacotes e tente novamente."
            print_error "Failed to install $dep. Check your package manager and try again."
            exit 1
        fi
        print_step "$dep instalado com sucesso. / $dep installed successfully."
    else
        print_step "$dep já está instalado. / $dep is already installed."
    fi
done

print_step "Instalando dependências Python via pip... / Installing Python dependencies via pip..."
PYTHON_DEPS=("requests" "phonenumbers" "beautifulsoup4")

pip3 install --upgrade pip > /dev/null 2>&1 &
spinner $!

for pdep in "${PYTHON_DEPS[@]}"; do
    print_step "Instalando $pdep... / Installing $pdep..."
    pip3 install $pdep > /dev/null 2>&1 &
    spinner $!
    print_step "$pdep instalado (ou já estava instalado). / $pdep installed (or already installed)."
done

echo
print_step "Instalação concluída com sucesso! / Installation completed successfully!"
print_step "Execute o script principal com: python3 main.py / Run the main script with: python3 main.py"
echo -e "${YELLOW}Lembre-se de usar esta ferramenta de forma ética e legal!${NC}"
echo -e "${YELLOW}Remember to use this tool ethically and legally!${NC}"
echo

exit 0