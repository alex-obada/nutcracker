import subprocess
import shutil

#nmap target -sV -sC -Pn -p 1-100"
def nmap_scan(target):
    command = f"nmap {target} -sV -sC -Pn -p 1-100"
    print(f"[+] Executăm comanda: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout;

    except Exception as e:
        print(f"[-] Eroare la executarea comenzii: {e}")


def extract_attack_commands(findings: dict) -> list:
    """
    Primește findings (dict) și extrage toate comenzile de atac din findings["attacks"].
    """
    attack_commands = []

    if "attacks" in findings:
        for vuln in findings["attacks"]:
            attack_commands.extend(vuln.get("attack_commands", []))

    return attack_commands

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


def is_tool_installed(tool_name):
    return shutil.which(tool_name) is not None

def install_tool(tool_name):
    try:
        subprocess.run(["sudo", "apt", "install", "-y", tool_name], check=True)
        return is_tool_installed(tool_name)
    except Exception as e:
        print(f"[-] Eroare la instalarea tool-ului {tool_name}: {e}")
        return False

def execute_command(command, allow_install=False):
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300
        )
        return result.stdout + "\n" + result.stderr

    except FileNotFoundError:
        if allow_install:
            tool_name = command.split()[0]  # Extrage tool-ul din comandă (ex: "hydra")
            print(f"[!] Tool-ul {tool_name} nu este instalat. Încercăm să îl instalăm...")

            if install_tool(tool_name):
                print(f"[+] Tool-ul {tool_name} a fost instalat cu succes. Reîncercăm comanda...")
                try:
                    result = subprocess.run(
                        command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        timeout=300
                    )
                    return result.stdout + "\n" + result.stderr
                except Exception as e2:
                    return f"[-] Eroare după instalare: {e2}"
            else:
                return f"[-] Nu s-a putut instala tool-ul {tool_name}."
        else:
            return "[-] Comanda nu a fost găsită și instalarea automată este dezactivată."

    except subprocess.TimeoutExpired:
        return "[-] Timeout atins pentru această comandă."
    except Exception as e:
        return f"[-] Eroare la rularea comenzii: {e}"