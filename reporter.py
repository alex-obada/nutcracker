def generate_ai_report(strategy):
    """
    Primește un dict JSON de la AI și afișează un raport frumos în CLI.
    """
    if not strategy or "services" not in strategy:
        print("[-] Nu există date valide pentru raport.")
        return

    print("\n" + "="*60)
    print("🔍 RAPORT DE ANALIZĂ AI PENTRU TARGET")
    print("="*60)

    for service in strategy["services"]:
        port = service.get("port", "N/A")
        servicename = service.get("service", "N/A")
        paths = service.get("exploitation_paths", [])
        links = service.get("links", [])
        enumeration_cmds = service.get("recommended_enumeration", [])

        print(f"\n[+] Port: {port} / Serviciu: {servicename}")

        if paths:
            print("    🔥 Path-uri de exploatare sugerate:")
            for path in paths:
                print(f"      - {path}")

        if links:
            print("    🔗 Link-uri utile:")
            for link in links:
                print(f"      - {link}")

        if enumeration_cmds:
            print("    🛠 Comenzi de enumerare recomandate:")
            for cmd in enumeration_cmds:
                print(f"      - {cmd}")

        print("-"*60)

    print("\n✅ Sfârșitul raportului.")
    print("="*60)