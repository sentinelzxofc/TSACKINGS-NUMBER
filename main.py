import os
import sys
import time
import json
import urllib.parse
import re
import csv
try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("\033[91m[!] Erro: Algumas bibliotecas necessárias não estão instaladas.\033[0m")
    print("\033[93m[*] Execute 'pip install phonenumbers requests beautifulsoup4' no Termux.\033[0m")
    sys.exit(1)

C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BLUE = '\033[94m'
C_MAGENTA = '\033[95m'
C_CYAN = '\033[96m'
C_WHITE = '\033[97m'
C_BOLD = '\033[1m'
C_UNDERLINE = '\033[4m'
C_RESET = '\033[0m'

AUTHOR = "sentinelzxofc"
PROJECT_NAME = "TSACKINGS-NUMBER"
REPO_URL = "https://github.com/sentinelzxofc/TSACKINGS-NUMBER"
INSTAGRAM = "@sentinelzxofc"

BRAZIL_DDD = {
    '11': 'São Paulo, SP', '21': 'Rio de Janeiro, RJ', '31': 'Belo Horizonte, MG',
    '91': 'Belém, PA'
}

def print_banner():
    banner = f"""{C_CYAN}{C_BOLD}
    ████████╗███████╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ███████╗ ███████╗███╗   ███╗
    ╚══██╔══╝██╔════╝██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝ ██╔════╝████╗ ████║
       ██║   ███████╗███████║██║     █████╔╝ ██║██╔██╗ ██║███████╗ ███████╗██╔████╔██║
       ██║   ╚════██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║╚════██║ ╚════██║██║╚██╔╝██║
       ██║   ███████║██║  ██║╚██████╗██║  ██╗██║██║ ╚████║███████║ ███████║██║ ╚═╝ ██║
       ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝ ╚══════╝╚═╝     ╚═╝
    {C_RESET}
          {C_WHITE}Ultimate Phone Number Tracker by {C_YELLOW}{AUTHOR}{C_RESET}
          {C_MAGENTA}Project: {PROJECT_NAME}{C_RESET}
          {C_BLUE}Repo: {REPO_URL}{C_RESET}
          {C_GREEN}Instagram: {INSTAGRAM}{C_RESET}
    """
    print(banner)

def print_disclaimer():
    print(f"{C_YELLOW}{C_BOLD}--- AVISO LEGAL / LEGAL DISCLAIMER ---{C_RESET}")
    print(f"{C_WHITE}This tool is for educational and OSINT purposes ONLY in a controlled environment.{C_RESET}")
    print(f"{C_RED}{C_BOLD}DO NOT use for illegal activities or to invade privacy. Respect the laws.{C_RESET}")
    try:
        input(f"{C_GREEN}[?] Pressione Enter para concordar / Press Enter to agree...{C_RESET}")
    except KeyboardInterrupt:
        print(f"\n{C_RED}[X] Cancelado / Cancelled. Saindo / Exiting...{C_RESET}")
        sys.exit(0)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_to_file(info, filename="phone_info", formats=["json"]):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    try:
        if "json" in formats:
            with open(f"{filename}_{timestamp}.json", 'a') as f:
                json.dump(info, f, indent=4, ensure_ascii=False)
                f.write('\n')
            print(f"{C_GREEN}[*] Informações salvas em / Saved to {filename}_{timestamp}.json{C_RESET}")
        if "csv" in formats:
            with open(f"{filename}_{timestamp}.csv", 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=info.keys())
                writer.writeheader()
                writer.writerow(info)
            print(f"{C_GREEN}[*] Informações salvas em / Saved to {filename}_{timestamp}.csv{C_RESET}")
        if "txt" in formats:
            with open(f"{filename}_{timestamp}.txt", 'a') as f:
                for key, value in info.items():
                    f.write(f"{key.replace('_', ' ').title()}: {value}\n")
            print(f"{C_GREEN}[*] Informações salvas em / Saved to {filename}_{timestamp}.txt{C_RESET}")
    except Exception as e:
        print(f"{C_RED}[X] Erro ao salvar arquivo / Error saving file: {e}{C_RESET}")

def load_cache():
    try:
        with open('phone_cache.json', 'r') as f:
            cache = json.load(f)
            current_time = time.time()
            return {k: v for k, v in cache.items() if current_time - v.get('timestamp_epoch', 0) < 86400}
    except FileNotFoundError:
        return {}

def save_cache(cache):
    with open('phone_cache.json', 'w') as f:
        json.dump(cache, f, indent=4)

def is_basic_format_valid(phone_number_str):
    pattern = r'^\+?\d{1,15}$'
    return bool(re.match(pattern, phone_number_str))

def guess_country_code(phone_number_str):
    common_ddis = ['+55', '+1', '+44', '+33']
    for ddi in common_ddis:
        try:
            parsed = phonenumbers.parse(ddi + phone_number_str, None)
            if phonenumbers.is_valid_number(parsed):
                return parsed
        except phonenumbers.NumberParseException:
            continue
    return None

def check_regional_format(parsed_number):
    if phonenumbers.region_code_for_number(parsed_number) == 'BR':
        national = str(parsed_number.national_number)
        if len(national) == 11 and national.startswith(('9', '8', '7')):
            return "Número móvel válido para o Brasil / Valid mobile number for Brazil"
        elif len(national) == 10:
            return "Número fixo válido para o Brasil / Valid fixed number for Brazil"
        else:
            return "Formato inválido para o Brasil / Invalid format for Brazil"
    return "Verificação de formato regional não disponível / Regional format verification not available"

def get_ddd_info(parsed_number):
    if phonenumbers.region_code_for_number(parsed_number) == 'BR':
        national = str(parsed_number.national_number)
        ddd = national[:2]
        return BRAZIL_DDD.get(ddd, 'DDD não encontrado / DDD not found')
    return 'N/A'

def check_portability(parsed_number, carrier_name):
    if phonenumbers.region_code_for_number(parsed_number) == 'BR':
        ddd = str(parsed_number.national_number)[:2]
        if ddd == '91' and carrier_name not in ['TIM', 'Claro', 'Vivo']:
            return "Possível número portado (operadora não comum para o DDD) / Possible ported number (uncommon carrier for DDD)"
        return "Nenhuma indicação de portabilidade / No indication of portability"
    return "Verificação de portabilidade não disponível / Portability verification not available"

def check_voip_status(parsed_number, carrier_name):
    if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.VOIP:
        return "Número identificado como VoIP / Number identified as VoIP"
    if carrier_name in ['Skype', 'Google Voice', 'TextNow']:
        return "Possível número VoIP (baseado na operadora) / Possible VoIP number (based on carrier)"
    return "Sem indicação de VoIP / No VoIP indication"

def scrape_search_results(phone_number_e164):
    results = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Android; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0'}
    try:
        url = f"https://www.google.com/search?q={urllib.parse.quote(phone_number_e164)}"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            snippets = [div.text[:100] + '...' for div in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')[:3]]
            results['google'] = snippets if snippets else ["Nenhuma menção encontrada / No mentions found"]
        else:
            results['google'] = ["Erro ao acessar Google / Error accessing Google"]
    except requests.RequestException:
        results['google'] = ["Erro ao acessar Google / Error accessing Google"]

    try:
        url = f"https://www.reclameaqui.com.br/busca/?q={urllib.parse.quote(phone_number_e164)}"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            complaints = [a.text[:100] + '...' for a in soup.find_all('a', class_='link-ng')[:3]]
            results['reclame_aqui'] = complaints if complaints else ["Nenhuma reclamação encontrada / No complaints found"]
        else:
            results['reclame_aqui'] = ["Erro ao acessar Reclame Aqui / Error accessing Reclame Aqui"]
    except requests.RequestException:
        results['reclame_aqui'] = ["Erro ao acessar Reclame Aqui / Error accessing Reclame Aqui"]

    try:
        url = f"https://www.google.com/search?q={urllib.parse.quote(phone_number_e164 + ' spam OR scam')}"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            snippets = [div.text[:100] + '...' for div in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')[:3]]
            results['spam_check'] = snippets if snippets else ["Nenhuma menção de spam/scam / No spam/scam mentions"]
        else:
            results['spam_check'] = ["Erro ao verificar spam / Error checking spam"]
    except requests.RequestException:
        results['spam_check'] = ["Erro ao verificar spam / Error checking spam"]

    return results

def generate_search_links(phone_number_e164):
    encoded_number = urllib.parse.quote(phone_number_e164)
    links = {
        "Google": f"https://www.google.com/search?q={encoded_number}",
        "Google (Intext)": f"https://www.google.com/search?q=intext%3A%22{encoded_number}%22",
        "DuckDuckGo": f"https://duckduckgo.com/?q={encoded_number}",
        "Bing": f"https://www.bing.com/search?q={encoded_number}",
        "Reclame Aqui (BR)": f"https://www.reclameaqui.com.br/busca/?q={encoded_number}",
        "Spam Check": f"https://www.google.com/search?q={encoded_number}+spam+OR+scam",
        "Google (Contato)": f"https://www.google.com/search?q={urllib.parse.quote(phone_number_e164 + ' contato')}"
    }
    return links

def get_phone_info(phone_number_str):
    info = {}
    cache = load_cache()
    if phone_number_str in cache:
        print(f"{C_GREEN}[*] Usando dados do cache / Using cached data{C_RESET}")
        return cache[phone_number_str]

    if not is_basic_format_valid(phone_number_str):
        info['error'] = 'Formato inválido: use apenas dígitos e opcionalmente + / Invalid format: use only digits and optionally +'
        return info

    try:
        if not phone_number_str.startswith('+'):
            parsed_number = guess_country_code(phone_number_str)
            if not parsed_number:
                info['error'] = "Não foi possível inferir DDI / Unable to infer country code. Use +DDI..."
                return info
            print(f"{C_YELLOW}[!] Número analisado com DDI inferido / Number parsed with inferred country code{C_RESET}")
        else:
            parsed_number = phonenumbers.parse(phone_number_str, None)

        if not phonenumbers.is_valid_number(parsed_number):
            parsed_number_br = phonenumbers.parse(phone_number_str, "BR")
            if phonenumbers.is_valid_number(parsed_number_br):
                parsed_number = parsed_number_br
                print(f"{C_YELLOW}[!] Número analisado assumindo DDI do Brasil (+55) / Number parsed assuming Brazil DDI (+55){C_RESET}")
            else:
                info['error'] = "Número inválido ou formato não reconhecido / Invalid number or unrecognized format"
                return info

        info['international_format'] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        info['national_format'] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        info['e164_format'] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        info['country_code'] = str(parsed_number.country_code)
        info['national_number'] = str(parsed_number.national_number)
        info['location_en'] = geocoder.description_for_number(parsed_number, "en") or "N/A"
        info['location_pt'] = geocoder.description_for_number(parsed_number, "pt") or "N/A"
        info['carrier'] = carrier.name_for_number(parsed_number, "en") or "N/A"
        info['timezones'] = list(timezone.time_zones_for_number(parsed_number)) or ["N/A"]
        info['is_possible'] = str(phonenumbers.is_possible_number(parsed_number))
        info['is_valid'] = str(phonenumbers.is_valid_number(parsed_number))
        number_type = phonenumbers.number_type(parsed_number)
        type_map = {
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixo / Fixed Line",
            phonenumbers.PhoneNumberType.MOBILE: "Móvel / Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixo ou Móvel / Fixed or Mobile",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Gratuito / Toll Free",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Tarifa Premium / Premium Rate",
            phonenumbers.PhoneNumberType.SHARED_COST: "Custo Compartilhado / Shared Cost",
            phonenumbers.PhoneNumberType.VOIP: "VoIP",
            phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Número Pessoal / Personal Number",
            phonenumbers.PhoneNumberType.PAGER: "Pager",
            phonenumbers.PhoneNumberType.UAN: "Número de Acesso Universal / UAN",
            phonenumbers.PhoneNumberType.VOICEMAIL: "Correio de Voz / Voicemail",
            phonenumbers.PhoneNumberType.UNKNOWN: "Desconhecido / Unknown"
        }
        info['number_type'] = type_map.get(number_type, "Desconhecido / Unknown")
        info['regional_format'] = check_regional_format(parsed_number)
        info['ddd_info'] = get_ddd_info(parsed_number)
        info['portability'] = check_portability(parsed_number, info['carrier'])
        info['voip_status'] = check_voip_status(parsed_number, info['carrier'])
        info['search_links'] = generate_search_links(info['e164_format'])
        info['search_results'] = scrape_search_results(info['e164_format'])
        info['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
        info['timestamp_epoch'] = time.time()

        if 'error' not in info:
            cache[phone_number_str] = info
            save_cache(cache)

    except phonenumbers.NumberParseException as e:
        error_type = e.error_type
        if error_type == phonenumbers.NumberParseException.INVALID_COUNTRY_CODE:
            info['error'] = "Código do país inválido / Invalid country code. Use +DDI..."
        elif error_type == phonenumbers.NumberParseException.NOT_A_NUMBER:
            info['error'] = "Contém caracteres inválidos / Contains invalid characters"
        elif error_type == phonenumbers.NumberParseException.TOO_SHORT_AFTER_IDD or error_type == phonenumbers.NumberParseException.TOO_SHORT_NSN:
            info['error'] = "Número muito curto / Number too short"
        elif error_type == phonenumbers.NumberParseException.TOO_LONG:
            info['error'] = "Número muito longo / Number too long"
        else:
            info['error'] = f"Erro ao analisar número / Error parsing number: {e}"
    except Exception as e:
        info['error'] = f"Erro inesperado / Unexpected error: {e}"

    return info

def process_batch_file(filename):
    try:
        with open(filename, 'r') as f:
            numbers = [line.strip() for line in f if line.strip()]
        for number in numbers:
            print(f"\n{C_BLUE}[*] Processando / Processing: {number}{C_RESET}")
            info = get_phone_info(number)
            display_info(info)
            save_to_file(info, f"batch_results_{time.time()}", formats=["json", "csv", "txt"])
    except FileNotFoundError:
        print(f"{C_RED}[X] Arquivo não encontrado / File not found: {filename}{C_RESET}")
    except Exception as e:
        print(f"{C_RED}[X] Erro ao processar arquivo / Error processing file: {e}{C_RESET}")

def display_info(info):
    print(f"\n{C_GREEN}{C_BOLD}--- Informações Encontradas / Information Found ---{C_RESET}")
    if 'error' in info:
        print(f"{C_RED}[X] Erro / Error: {info['error']}{C_RESET}")
        return

    print(f"{C_CYAN}{C_BOLD}Informações Básicas / Basic Information:{C_RESET}")
    for key in ['international_format', 'national_format', 'e164_format', 'country_code', 'national_number', 'timestamp']:
        print(f"  {C_WHITE}{key.replace('_', ' ').title()}:{C_RESET} {C_YELLOW}{info.get(key, 'N/A')}{C_RESET}")

    print(f"\n{C_CYAN}{C_BOLD}Localização e Operadora / Location and Carrier:{C_RESET}")
    for key in ['location_en', 'location_pt', 'carrier', 'ddd_info']:
        print(f"  {C_WHITE}{key.replace('_', ' ').title()}:{C_RESET} {C_YELLOW}{info.get(key, 'N/A')}{C_RESET}")
    print(f"  {C_WHITE}Fuso Horário(s) / Time Zone(s):{C_RESET} {C_YELLOW}{', '.join(info.get('timezones', ['N/A']))}{C_RESET}")

    print(f"\n{C_CYAN}{C_BOLD}Detalhes Técnicos / Technical Details:{C_RESET}")
    for key in ['number_type', 'is_possible', 'is_valid', 'regional_format', 'portability', 'voip_status']:
        print(f"  {C_WHITE}{key.replace('_', ' ').title()}:{C_RESET} {C_YELLOW}{info.get(key, 'N/A')}{C_RESET}")

    if 'search_links' in info:
        print(f"\n{C_MAGENTA}{C_BOLD}OSINT - Links de Busca / Search Links:{C_RESET}")
        for engine, link in info['search_links'].items():
            print(f"  {C_GREEN} -> {engine}:{C_RESET} {C_BLUE}{C_UNDERLINE}{link}{C_RESET}")

    if 'search_results' in info:
        print(f"\n{C_MAGENTA}{C_BOLD}OSINT - Resultados de Busca / Search Results:{C_RESET}")
        for source, results in info['search_results'].items():
            print(f"  {C_GREEN} -> {source.replace('_', ' ').title()}:{C_RESET}")
            for result in results:
                print(f"    {C_YELLOW}{result}{C_RESET}")

    print(f"\n{C_GREEN}{C_BOLD}--- Fim das Informações / End of Information ---{C_RESET}")

def main():
    clear_screen()
    print_banner()
    print_disclaimer()
    clear_screen()
    print_banner()

    while True:
        try:
            mode = input(f"{C_YELLOW}[?] Modo interativo (i) ou arquivo em lote (b)? / Interactive mode (i) or batch file (b)? [i/b]: {C_RESET}").strip().lower()
            if mode == 'b':
                filename = input(f"{C_YELLOW}[?] Nome do arquivo com números / File name with numbers: {C_RESET}")
                process_batch_file(filename)
                break
            elif mode != 'i':
                print(f"{C_RED}[X] Modo inválido / Invalid mode. Use 'i' or 'b'.{C_RESET}")
                continue

            phone_input = input(f"{C_YELLOW}[?] Digite o número (+DDIxxxx) / Enter the number (+DDIxxxx): {C_RESET}").strip()
            if not phone_input:
                continue
            if phone_input.lower() in ['exit', 'quit', 'sair', '0']:
                print(f"\n{C_BLUE}Saindo / Exiting... Obrigado por usar / Thanks for using {PROJECT_NAME}!{C_RESET}")
                break

            print(f"\n{C_BLUE}[*] Analisando o número / Analyzing number: {phone_input}...{C_RESET}")
            time.sleep(0.5)
            info = get_phone_info(phone_input)
            display_info(info)
            save_option = input(f"{C_YELLOW}[?] Deseja salvar os resultados (json, csv, txt, ambos)? / Save results (json, csv, txt, all)? [j/c/t/a/n]: {C_RESET}").lower()
            formats = []
            if save_option in ['j', 'a']:
                formats.append("json")
            if save_option in ['c', 'a']:
                formats.append("csv")
            if save_option in ['t', 'a']:
                formats.append("txt")
            if formats:
                save_to_file(info, formats=formats)

        except KeyboardInterrupt:
            print(f"\n{C_RED}[X] Cancelado / Cancelled. Saindo / Exiting...{C_RESET}")
            break
        except Exception as e:
            print(f"{C_RED}[X] Erro no loop principal / Error in main loop: {e}{C_RESET}")

        print("\n" + "-" * 40)

if __name__ == "__main__":
    main()