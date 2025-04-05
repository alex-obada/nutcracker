# reporter.py

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

