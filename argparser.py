import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Nut Cracker - Scanare și exploatare automată controlată de AI."
    )

    parser.add_argument(
        "--target",
        required=True,
        help="IP-ul sau domeniul țintă pentru scanare (ex: 192.168.1.1 sau example.com)."
    )


    parser.add_argument(
        "--context",
        type=str,
        default="Scanează serverul normal pentru vulnerabilități generale.",
        help="Context liber despre ce să prioritizeze AI-ul (ex: 'Caută vulnerabilități pe Telnet și FTP')."
    )

    parser.add_argument(
        "--learn",
        action="store_true",
        help="Dacă este setat, AI-ul va explica fiecare decizie pentru învățare."
    )

    return parser.parse_args()
