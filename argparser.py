import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Nut Cracker - Scanare și exploatare automată controlată de AI."
    )

    parser.add_argument(
        "target",
        help="IP-ul sau domeniul țintă pentru scanare (ex: 192.168.1.1 sau example.com)."
    )

    
    return parser.parse_args()
