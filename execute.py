import subprocess
import shutil

#nmap target -sV -sC -Pn"
def nmap_scan(target):
    command = f"nmap {target} -sV -sC -Pn"
    print(f"[+] Executăm comanda: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout;

    except Exception as e:
        print(f"[-] Eroare la executarea comenzii: {e}")


def extract_enumeration_commands(strategy, target):
    """
    Extrage comenzile de enumerare recomandate din output-ul AI și înlocuiește placeholder-ul IP.
    Ignoră comenzile care folosesc nikto (deoarece targetul este întotdeauna IP și nikto are probleme).
    """
    commands = []

    if not strategy or "services" not in strategy:
        print("[-] Structura JSON este invalidă sau lipsesc serviciile.")
        return commands

    for service in strategy["services"]:
        recommended = service.get("recommended_enumeration", [])
        for cmd in recommended:
            if "nikto" in cmd.lower():
                continue  # Ignorăm complet comenzile nikto
            full_cmd = cmd.replace("IP", target)
            commands.append(full_cmd)

    return commands


def check_and_install_tool(tool):
    """
    Verifică dacă un tool există. Dacă nu există, încearcă să îl instaleze automat cu apt.
    """
    if shutil.which(tool) is not None:
        return True  # Tool-ul există deja

    print(f"[!] Tool-ul '{tool}' nu este instalat. Încerc să îl instalez automat...")

    try:
        subprocess.run(f"sudo apt-get update && sudo apt-get install -y {tool}", shell=True, check=True)
        if shutil.which(tool) is not None:
            print(f"[+] Tool-ul '{tool}' a fost instalat cu succes.")
            return True
        else:
            print(f"[-] Nu am reușit să instalez tool-ul '{tool}'. Comanda va fi sărită.")
            return False
    except Exception as e:
        print(f"[-] Eroare la instalarea tool-ului '{tool}': {e}")
        return False

def execute_command(cmd, timeout=300):
    """
    Execută o comandă shell după ce verifică dacă tool-ul principal există.
    Dacă tool-ul lipsește și nu poate fi instalat, sarim comanda.
    """
    try:
        # Extragem primul cuvânt din comandă (ex: "hydra", "gobuster")
        tool = cmd.split()[0]

        # Verificăm și instalăm dacă lipsește
        if not check_and_install_tool(tool):
            print(f"[!] Sărim comanda pentru că tool-ul '{tool}' lipsește.")
            return ""

        # Executăm comanda normal
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout

    except subprocess.TimeoutExpired:
        print(f"[-] Comanda a fost oprită după {timeout} secunde: {cmd}")
        return ""
    except Exception as e:
        print(f"[-] Eroare la executarea comenzii {cmd}: {e}")
        return ""