import os

def generate_ai_report(strategy):
    """
    Primește un dict JSON de la AI și:
    - Afișează raport modernizat în CLI.
    - Salvează raportul și în format Markdown.
    """
    if not strategy or "services" not in strategy:
        print("[-] Nu există date valide pentru raport.")
        return

    # ====== Pregătire pentru Markdown ======
    markdown_lines = [
        "# 🔍 Raport AI de Analiză a Targetului",
        "",
        "| Port | Serviciu | Path-uri de Exploatare | Link-uri Utile | Comenzi Recomandate |",
        "|:----:|:--------:|:----------------------:|:--------------:|:-------------------:|"
    ]

    print("\n" + "="*100)
    print("🔍 RAPORT DE ANALIZĂ AI PENTRU TARGET")
    print("="*100)

    for service in strategy["services"]:
        port = service.get("port", "N/A")
        servicename = service.get("service", "N/A")
        paths = service.get("exploitation_paths", [])
        links = service.get("links", [])
        enumeration_cmds = service.get("recommended_enumeration", [])

        # ====== Afișare modernă în CLI ======
        print(f"\n🛡️  PORT: {port}  |  SERVICIU: {servicename}")
        print("-" * 100)

        if paths:
            print("🔥 PATH-URI DE EXPLOATARE:")
            for path in paths:
                print(f"    - {path}")

        if links:
            print("\n🔗 LINK-URI UTILE:")
            for link in links:
                print(f"    - {link}")

        if enumeration_cmds:
            print("\n🛠️ COMENZI RECOMANDATE:")
            for cmd in enumeration_cmds:
                print(f"    - {cmd}")

        print("=" * 100)

        # ====== Construim rând pentru Markdown ======
        markdown_lines.append(
            f"| {port} | {servicename} | {'<br>'.join(paths)} | {'<br>'.join(links)} | {'<br>'.join(enumeration_cmds)} |"
        )

    print("\n✅ Sfârșitul raportului.")
    print("="*100)

    # ====== Salvare Markdown ======
    os.makedirs("Reports", exist_ok=True)
    markdown_path = os.path.join("Reports", "report.md")
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_lines))

    print(f"[+] Raportul Markdown a fost salvat în '{markdown_path}'.")



def display_findings_report(findings: dict):
    """
    Afișează în consolă un raport frumos cu findings sau attacks AI.
    """
    findings_list = findings.get("findings", []) or findings.get("attacks", [])

    print("\n" + "="*60)
    print("📋 Raport AI: Vulnerabilități și sugestii de exploatare")
    print("="*60 + "\n")

    if not findings_list:
        print("⚠️  Nu s-au identificat vulnerabilități exploatabile.\n")
        return

    for idx, item in enumerate(findings_list, 1):
        vuln = item.get("vulnerability", "Vulnerabilitate necunoscută")
        print(f"🔹 {idx}. {vuln}\n")

        # În funcție de ce există
        recommended = item.get("recommended_exploitation", item.get("attack_commands", []))
        if recommended:
            print("   ✅ Comenzi recomandate:")
            for cmd in recommended:
                print(f"     └─ 🛠 {cmd}")

        resources = item.get("additional_resources", [])
        if resources:
            print("\n   🔗 Resurse utile:")
            for link in resources:
                print(f"     └─ {link}")
        
        print("\n" + "-"*50 + "\n")

    print("✅ Sfârșitul raportului AI.\n")

def generate_final_markdown_report(nmap_json: dict, findings_json: dict, output_file: str = "Reports/final_report.md"):
    """
    Generează un raport final Markdown cu toate informațiile:
    - Rezultatul scanării Nmap și analiza inițială
    - Vulnerabilități suplimentare detectate după recon
    - Mesaj de contact Zerotak
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 📄 Raport Final de Analiză Nutcracker\n\n")

        # Secțiunea Nmap + analiza inițială
        f.write("## 🔍 Rezultatele scanării Nmap și analiza inițială\n\n")

        services = nmap_json.get("services", [])
        for service in services:
            port = service.get("port", "N/A")
            service_name = service.get("service", "Unknown")
            exploitation_paths = service.get("exploitation_paths", [])
            links = service.get("links", [])
            enumeration_cmds = service.get("recommended_enumeration", [])

            f.write(f"<details>\n<summary>🚪 Port {port} - {service_name}</summary>\n\n")
            
            f.write("**Path-uri de Exploatare:**\n")
            for path in exploitation_paths:
                f.write(f"- {path}\n")
            f.write("\n")

            if links:
                f.write("**Link-uri Utile:**\n")
                for link in links:
                    f.write(f"- [{link}]({link})\n")
                f.write("\n")

            if enumeration_cmds:
                f.write("**Comenzi Recomandate:**\n")
                for cmd in enumeration_cmds:
                    f.write(f"- `{cmd}`\n")
                f.write("\n")

            f.write("</details>\n\n---\n\n")

        # Secțiunea Findings suplimentare
        f.write("## 🛡️ Vulnerabilități suplimentare identificate după Recon\n\n")

        attacks = findings_json.get("attacks", [])
        if attacks:
            for attack in attacks:
                vuln = attack.get("vulnerability", "Vulnerabilitate necunoscută")
                attack_cmds = attack.get("attack_commands", [])
                resources = attack.get("additional_resources", [])

                f.write(f"<details>\n<summary>🔹 {vuln}</summary>\n\n")

                if attack_cmds:
                    f.write("**Comenzi de Atac Recomandate:**\n")
                    for cmd in attack_cmds:
                        f.write(f"- `{cmd}`\n")
                    f.write("\n")

                if resources:
                    f.write("**Link-uri Suplimentare:**\n")
                    for link in resources:
                        f.write(f"- [{link}]({link})\n")
                    f.write("\n")

                f.write("</details>\n\n---\n\n")
        else:
            f.write("⚠️  Nu s-au identificat vulnerabilități suplimentare.\n\n")

        # Secțiunea Finală - Mesajul Nutcracker & Zerotak
        final_message = """
---

## 📢 Asistență Suplimentară

Dacă aveți nevoie de ajutor suplimentar în soluționarea problemelor dumneavoastră,  
echipa **Nutcracker** vă recomandă să îi contactați pe experții de la **Zerotak**.

📧 **Email de contact:** [collaboration@zerotak.com](mailto:collaboration@zerotak.com)

---
"""
        f.write(final_message)