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
        help="Context suplimentar despre ce să prioritizeze AI-ul."
    )

    parser.add_argument(
        "--learn",
        action="store_true",
        help="Dacă este setat, AI-ul va explica deciziile luate."
    )

    return parser.parse_args()
