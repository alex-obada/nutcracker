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


def extract_enumeration_commands(strategy, target):
    """
    Extrage comenzile de enumerare recomandate din output-ul AI și înlocuiește placeholder-ul IP.
    Returnează o listă de comenzi pregătite de execuție.
    """
    commands = []

    if not strategy or "services" not in strategy:
        print("[-] Structura JSON este invalidă sau lipsesc serviciile.")
        return commands

    for service in strategy["services"]:
        recommended = service.get("recommended_enumeration", [])
        for cmd in recommended:
            # Înlocuim 'IP' cu target-ul real
            full_cmd = cmd.replace("IP", target)
            commands.append(full_cmd)

    return commands