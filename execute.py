import subprocess

def execute_command(strategy):
    tool = strategy.get("tool")
    target = strategy.get("target")
    arguments = strategy.get("arguments")

    if not tool or not arguments:
        print("[-] Strategie incompletă. Lipsesc 'tool' sau 'arguments'.")
        return

    command = f"{tool} {target} {arguments}"
    print(f"[+] Executăm comanda: {command}")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print("[+] Output-ul comenzii:")
        print(result.stdout)

        if result.stderr:
            print("[-] Eroare:")
            print(result.stderr)

    except Exception as e:
        print(f"[-] Eroare la executarea comenzii: {e}")


        #o fucntie care sa execute comanda nmap cu flagurile -Pn si un target datgit 