"""
Název skriptu: parse.py
Autor: Martina Hromadkova
Login: xhroma15
Datum: 18. 2. 2024
Popis: Tento skript slouží k analýze kódu v IPPcode24 a generování XML reprezentace.
"""

import sys
import argparse

# Chybové návratové kódy
ERROR_INVALID_COMBINATION = 10
ERROR_DUPLICATE_STATS_FILE = 12
ERROR_INVALID_HEADER = 21
ERROR_INVALID_OPCODE = 22
ERROR_LEXICAL_SYNTAX = 23

# Návratový kód pro úspěšné ukončení
SUCCESS = 0

# Slovník pro uchování statistik
statistics = {
    '--loc': 0,
    '--comments': 0,
    '--labels': 0,
    '--jumps': 0,
    '--fwjumps': 0,
    '--backjumps': 0,
    '--badjumps': 0,
    '--frequent': set(),
    '--print': [],
    '--eol': 0
}

# Funkce pro zpracování vstupního kódu a generování XML reprezentace
def parse_code(input_code):
    # Zde bude implementace zpracování kódu a generování XML reprezentace
    pass

# Funkce pro výpis nápovědy
def print_help():
    help_message = """
    Použití: parse.py [--help] [--stats=file] [--loc] [--comments] [--labels] [--jumps] [--fwjumps] [--backjumps] [--badjumps] [--frequent] [--print=string] [--eol]

    IPPcode24 Parser

    Volby:
      --help           Zobrazí tuto nápovědu a ukončí program
      --stats=file     Zadání souboru pro uložení statistik
      --loc            Vypíše počet řádků s instrukcemi
      --comments       Vypíše počet řádků obsahujících komentáře
      --labels         Vypíše počet definovaných návěští
      --jumps          Vypíše počet všech instrukcí návratů, skoků a volání
      --fwjumps        Vypíše počet dopředných skoků
      --backjumps      Vypíše počet zpětných skoků
      --badjumps       Vypíše počet skoků na neexistující návěští
      --frequent       Vypíše nejčastější operační kódy
      --print=string   Vypíše řetězec string
      --eol            Vypíše odřádkování
    """
    print(help_message)
    sys.exit(SUCCESS)
      
# Funkce pro zpracování statistik
def process_stats(filename):
    # Zde proběhne zpracování a zápis statistik do souboru
    pass

# Hlavní funkce pro analýzu přepínačů a volání odpovídajících funkcí
def main():
    # Inicializace argument parseru s popisem programu a bez automatického přidání help přepínače
    parser = argparse.ArgumentParser(description='IPPcode24 Parser', add_help=False)
    
    # Přidání možnosti --help pro zobrazení nápovědy
    parser.add_argument('--help', action='store_true', help='Zobrazí tuto nápovědu a ukončí program')
    parser.add_argument('--stats', metavar='filename', help='Zadání souboru pro uložení statistik')
    parser.add_argument('--loc', action='store_true', help='Vypíše počet řádků s instrukcemi')
    parser.add_argument('--comments', action='store_true', help='Vypíše počet řádků obsahujících komentáře')
    parser.add_argument('--labels', action='store_true', help='Vypíše počet definovaných návěští')
    parser.add_argument('--jumps', action='store_true', help='Vypíše počet všech instrukcí návratů, skoků a volání')
    parser.add_argument('--fwjumps', action='store_true', help='Vypíše počet dopředných skoků')
    parser.add_argument('--backjumps', action='store_true', help='Vypíše počet zpětných skoků')
    parser.add_argument('--badjumps', action='store_true', help='Vypíše počet skoků na neexistující návěští')
    parser.add_argument('--frequent', action='store_true', help='Vypíše nejčastější operační kódy')
    parser.add_argument('--print', metavar='string', help='Vypíše řetězec string')
    parser.add_argument('--eol', action='store_true', help='Vypíše odřádkování')

    # Zpracování předaných argumentů
    args = parser.parse_args()

    # Kontrola, zda byly předány další argumenty kromě přepínače --help
    if len(sys.argv) > 2:
        print("Chyba: Přepínač --help nelze kombinovat s žádným jiným parametrem.", file=sys.stderr)
        sys.exit(ERROR_INVALID_COMBINATION)    
        
    # Pokud byl předán argument --help
    if args.help:
        print_help()
        
    # Kontrola chyby 10 pro statistiky
    if any([args.loc, args.comments, args.labels, args.jumps, args.fwjumps, args.backjumps, args.badjumps, args.frequent, args.print, args.eol]) and not args.stats:
        print("Chyba: Parametry statistik nelze zadat bez předchozího zadání parametru --stats.", file=sys.stderr)
        sys.exit(ERROR_INVALID_COMBINATION)

    # Kontrola chyby 12 pro statistiky
    if args.stats and (args.loc or args.comments or args.labels or args.jumps or args.fwjumps or args.backjumps or args.badjumps or args.frequent or args.print or args.eol):
        print("Chyba: Nelze zapisovat více skupin statistik do stejného souboru během jednoho spuštění.", file=sys.stderr)
        sys.exit(ERROR_DUPLICATE_STATS_FILE)
        
    if args.stats:
        process_stats(args.stats)

# Zavolání hlavní funkce
if __name__ == "__main__":
    main()