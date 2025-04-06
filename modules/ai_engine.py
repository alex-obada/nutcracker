from openai import OpenAI
import json
import os
import sys
from dotenv import load_dotenv

# Încarcă cheia OpenAI
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key=api_key)

def analyze_nmap_result(nmap_result):
    """
    Trimite output-ul brut de la Nmap la AI și returnează strict un dict JSON.
    """

    prompt = f"""
Ești un expert în cybersecurity și penetration testing.

Primești output-ul brut de la o scanare Nmap asupra unui target.

Scopul tău este:

1. Să analizezi TOATE serviciile și porturile descoperite în scanarea Nmap.
2. Pentru FIECARE port deschis, să creezi un obiect individual în lista "services".
3. Pentru fiecare port, să sugerezi posibile path-uri de exploatare.
4. Dacă există vulnerabilități cunoscute (ex: versiuni vechi de software sau CVE-uri publice), să propui exploituri concrete, inclusiv comenzi Metasploit sau payloaduri funcționale dacă sunt publice.
5. Dacă nu se poate exploata direct, să recomanzi metode de enumerare și investigare suplimentară.
6. Să oferi link-uri utile pentru fiecare port (HackTricks, MITRE ATT&CK, CVEs, articole de pentesting).
7. Pentru fiecare serviciu, să adaugi versiunea descoperită după două puncte în câmpul "service" (ex: "http: Apache 2.4.7").

IMPORTANT:

- Pentru fiecare port detectat, creează un obiect separat în JSON.
- Nu ignora niciun port deschis. Dacă Nmap a găsit portul, trebuie să îl analizezi.
- Comenzile sugerate trebuie să fie 100% reale, exacte conform documentației oficiale.
- NU inventa flaguri sau tool-uri care nu există.
- Unde vezi IP în comenzi, înlocuiește corect cu IP-ul targetului scanat.
- În comenzi sau sugestii, folosește tool-uri practice: hydra, gobuster, nikto, nmap (scripting), ssh-audit, searchsploit, msfconsole.
- Dacă identifici un CVE asociat unui serviciu, propune exploit concret folosind searchsploit sau modul Metasploit.
- NU repeta aceleași comenzi între porturi dacă nu este necesar.
- Fii concis și direct: doar JSON, fără explicații, introduceri sau comentarii suplimentare.
- Ghilimelele trebuie să fie duble " pentru compatibilitate JSON.

Structura JSON dorită:

{{
  "services": [
    {{
      "port": "22",
      "service": "ssh: OpenSSH 6.6.1p1",
      "exploitation_paths": [
        "Brute force SSH login with Hydra",
        "Check known vulnerabilities in OpenSSH 6.6.1p1"
      ],
      "links": [
        "https://book.hacktricks.xyz/network-services-pentesting/22-ssh",
        "https://attack.mitre.org/techniques/T1021/004/",
        "https://www.cvedetails.com/vulnerability-list/vendor_id-97/product_id-585/version_id-165479/Openssh-Openssh-6.6.1p1.html"
      ],
      "recommended_enumeration": [
        "hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://IP",
        "ssh-audit IP",
        "nmap -sV --script=ssh2-enum-algos -p 22 IP",
        "searchsploit OpenSSH 6.6.1p1"
      ]
    }}
  ]
}}

Acesta este output-ul brut de la scanarea Nmap:

---
{nmap_result}
---

⚠️ IMPORTANT:
- Returnează DOAR JSON-ul complet și valid.
- Nu adăuga alt text înainte sau după JSON.
- Respectă strict structura cerută.

"""

    try:
        # Trimitem promptul
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Răspunzi strict în JSON valid."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=1500
        )

        ai_raw_response = response.choices[0].message.content
        if ai_raw_response is None:
            print("[!] Eroare: Content-ul primit de la AI este None. Ieșim din aplicație...")
            sys.exit(1)
            

        # Parsăm direct JSON-ul primit
        return json.loads(ai_raw_response)

    except Exception as e:
        print(f"[-] Eroare la analiza rezultatului Nmap: {e}")
        return None


def analyze_enumeration_outputs(enumeration_output: str) -> dict | None:
    """
    Trimite output-ul combinat de la enumerare către AI și returnează strict un dict JSON.
    """

    prompt = f"""
Ești un expert ofensiv în cybersecurity și penetration testing.

Primești un output brut rezultat din rularea unor comenzi de enumerare (ex: hydra, ssh-audit, nmap scripts, gobuster, telnet, searchsploit) asupra unui target.

Scopul tău este:

1. Analizează toate informațiile primite în output-ul de enumerare.
2. Identifică vulnerabilitățile reale detectabile din output.
3. Pentru fiecare vulnerabilitate descoperită, propune comenzi concrete și reale pentru exploatare sau atac.
4. Comenzile trebuie să fie corecte, funcționale și să poată fi executate direct în terminal (ex: folosind hydra, msfconsole, searchsploit, scripturi de exploit, brute-force SSH etc.).
5. Dacă există mai multe metode de atac pentru aceeași vulnerabilitate, listează-le.
6. Oferă și linkuri utile (HackTricks, Exploit-DB, MITRE ATT&CK) dacă există informații relevante.
7. Nu propune exploaturi care sunt fictive sau foarte improbabile.

IMPORTANT:
- Ghilimelele folosite trebuie să fie duble ("), nu simple (').
- Fără explicații suplimentare sau comentarii în afara JSON-ului.
- Output-ul final trebuie să fie strict un JSON valid conform structurii de mai jos.
- Când generezi comenzi de bruteforce sau de directory enumeration, folosește wordlist-uri din `/usr/share/seclists/`, cum ar fi:
- `/usr/share/seclists/Passwords/rockyou.txt` pentru parole
- `/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt` pentru directoare si asa mai departe.

Structură JSON dorită:

{{
  "attacks": [
    {{
      "vulnerability": "Descriere clară a vulnerabilității foarte detaliată",
      "attack_commands": [
        "comandă 1 de exploatare",
        "comandă 2 de exploatare"
      ],
      "additional_resources": [
        "link 1 către documentație sau CVE",
        "link 2 către exploit relevant"
      ]
    }}
  ]
}}

Acesta este output-ul brut de enumerare:

---
{enumeration_output}
---

⚠️ IMPORTANT:
- Returnează DOAR JSON-ul cerut.
- Nu adăuga introduceri, explicații sau alte texte suplimentare înainte sau după JSON.
- JSON-ul trebuie să înceapă și să se termine strict cu {{ și }}.
- Când generezi comenzi de bruteforce sau de directory enumeration, folosește wordlist-uri din `/usr/share/seclists/`, cum ar fi:
- `/usr/share/seclists/Passwords/rockyou.txt` pentru parole
- `/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt` pentru directoare si asa mai departe.
"""


    try:
        # Trimitem promptul către AI
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Răspunzi strict în JSON valid."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=2000
        )

        ai_raw_response = response.choices[0].message.content
        if ai_raw_response is None:
            print("[!] Eroare: Content-ul primit de la AI este None. Ieșim din aplicație...")
            sys.exit(1)
            
        ai_raw_response = ai_raw_response.strip()

        # Parsăm direct răspunsul primit
        return json.loads(ai_raw_response)

    except Exception as e:
        print(f"[-] Eroare la analiza outputului de enumerare: {e}")
        return None
