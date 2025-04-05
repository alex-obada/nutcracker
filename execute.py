import subprocess



#nmap target -sV -sC -Pn"
def nmap_scan(target):
    command = f"nmap {target} -sV -sC -Pn"
    print(f"[+] Executăm comanda: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout;

    except Exception as e:
        print(f"[-] Eroare la executarea comenzii: {e}")


def execute_command(command):
    print(f"[+] Executăm comanda: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print("[+] Comanda a fost executată.")
        return result.stdout
    except Exception as e:
        print(f"[-] Eroare la executarea comenzii: {e}")
        return None