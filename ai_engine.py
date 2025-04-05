# ai_engine.py

from openai import OpenAI
import json
from dotenv import load_dotenv
import os
import re

# Încarcă cheia OpenAI
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key=api_key)

def fix_ai_json(raw_text):
    """
    Fixează problemele comune de formatare din răspunsul AI-ului.
    """
    match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    if not match:
        print("[-] Nu s-a găsit bloc JSON în outputul AI-ului.")
        return None

    json_text = match.group(0)

    # Repară ghilimelele simple (dacă există)
    json_text = json_text.replace("'", '"')

    # Repară lipsa de virgulă între obiecte consecutive
    json_text = re.sub(r'"}\s*{', '"}, {', json_text)

    return json_text

def analyze_nmap_result(nmap_result):
    """
    Trimite rezultatul brut Nmap la AI și returnează dict-ul JSON reparat automat.
    """
    prompt = f"""
Ești un expert în cybersecurity și penetration testing.

Primești output-ul brut de la o scanare Nmap asupra unui target.
Scopul tău este:

1. Să analizezi serviciile și porturile descoperite.
2. Să sugerezi posibile path-uri de exploatare pentru fiecare serviciu.
3. Să oferi link-uri utile pentru fiecare port (HackTricks, MITRE ATT&CK, CVEs, articole de pentesting).
4. Să recomanzi comenzi de enumerare suplimentară care pot fi rulate (ex: hydra, gobuster, nikto).
5. Dacă nu există exploatare directă, să propui metode de enumerare.

IMPORTANT: 
- Răspunde STRICT în format JSON în structura dată mai jos.
- Nu adăuga explicații în afara JSON-ului.

Structura JSON dorită:

{{
  "services": [
    {{
      "port": "22",
      "service": "ssh",
      "exploitation_paths": [
        "Brute force attack on SSH login",
        "Check for known vulnerabilities in OpenSSH 6.6.1p1"
      ],
      "links": [
        "https://book.hacktricks.xyz/network-services-pentesting/22-ssh",
        "https://attack.mitre.org/techniques/T1021/004/"
      ],
      "recommended_enumeration": [
        "hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://IP",
        "ssh-audit IP"
      ]
    }}
  ]
}}

Acesta este output-ul Nmap brut:

---
{nmap_result}
---
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Ești un expert în cybersecurity."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )
        
        ai_raw_response = response.choices[0].message.content

        # Aplicăm fix automat
        fixed_json = fix_ai_json(ai_raw_response)
        if not fixed_json:
            return None

        # Încercăm să parsăm
        try:
            strategy = json.loads(fixed_json)
            return strategy
        except json.JSONDecodeError as e:
            print(f"[-] Prima parsare a eșuat: {e}")

            # Dacă a eșuat, fallback - încercăm să cerem AI-ului să răspundă din nou
            print("[*] Reîncercăm să extragem JSON curat...")
            cleaned_text = fixed_json.replace('\\n', '').replace('\\', '')
            try:
                strategy = json.loads(cleaned_text)
                return strategy
            except Exception as e2:
                print(f"[-] Reîncercarea a eșuat: {e2}")
                return None

    except Exception as e:
        print(f"[-] Eroare la interogarea AI-ului: {e}")
        return None
