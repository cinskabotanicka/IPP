"""
Název skriptu: parse.py
Autor: Martina Hromadkova
Login: xhroma15
Datum: 18. 2. 2024
Popis: Tento skript slouží k analýze kódu v IPPcode24 a generování XML reprezentace.
"""

import re
import sys
import argparse
from xml.etree.ElementTree import Element, SubElement, tostring

# Konstanty a výčty

# Výčet datových typů
DTYPE = {
    'int': 0,
    'bool': 1,
    'string': 2,
    'nil': 3,
    'float': 4,
}

# Výčet operandů
OPERAND = {
    'var': 1,
    'symb': 2,
    'label': 3,
    'type': 4,
}

# Instrukční sada IPPcode24
INSTR = {
    # Instrukce programových rámců
    'MOVE': {
        'id': 1,
        'argt': ['OPERAND[var]', 'OPERAND[symb]'],
    },
    'CREATEFRAME': {
        'id': 2,
        'argt': [],
    },
    'PUSHFRAME': {
        'id': 3,
        'argt': [],
    },
    'POPFRAME': {
        'id': 4,
        'argt': [],
    },
    'DEFVAR': {
        'id': 5,
        'argt': ['OPERAND[var]'],
    },
    'CALL': {
        'id': 6,
        'argt': ['OPERAND[label]'],
    },
    'RETURN': {
        'id': 7,
        'argt': [],
    },
    # Instrukce datového zásobníku
    'PUSHS': {
        'id': 8,
        'argt': ['OPERAND[symb]'],
    },
    'POPS': {
        'id': 9,
        'argt': ['OPERAND[var]'],
    },
    # Aritmetické a datové instrukce
    'ADD': {
        'id': 10,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'SUB': {
        'id': 11,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'MUL': {
        'id': 12,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'IDIV': {
        'id': 13,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'LT': {
        'id': 14,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'GT': {
        'id': 15,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'EQ': {
        'id': 16,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'AND': {
        'id': 17,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'OR': {
        'id': 18,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'NOT': {
        'id': 19,
        'argt': ['OPERAND[var]', 'OPERAND[symb]'],
    },
    'INT2CHAR': {
        'id': 20,
        'argt': ['OPERAND[var]', 'OPERAND[symb]'],
    },
    'STRI2INT': {
        'id': 21,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    # Vstupno-výstupní instrukce
    'READ': {
        'id': 22,
        'argt': ['OPERAND[var]', 'OPERAND[type]'],
    },
    'WRITE': {
        'id': 23,
        'argt': ['OPERAND[symb]'],
    },
    # Instrukce pro práci s řetězci
    'CONCAT': {
        'id': 24,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'STRLEN': {
        'id': 25,
        'argt': ['OPERAND[var]', 'OPERAND[symb]'],
    },
    'GETCHAR': {
        'id': 26,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'SETCHAR': {
        'id': 27,
        'argt': ['OPERAND[var]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    # Instrukce typů
    'TYPE': {
        'id': 28,
        'argt': ['OPERAND[var]', 'OPERAND[symb]'],
    },
    # Instrukce na řízení toku programu
    'LABEL': {
        'id': 29,
        'argt': ['OPERAND[label]'],
    },
    'JUMP': {
        'id': 30,
        'argt': ['OPERAND[label]'],
    },
    'JUMPIFEQ': {
        'id': 31,
        'argt': ['OPERAND[label]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'JUMPIFNEQ': {
        'id': 32,
        'argt': ['OPERAND[label]', 'OPERAND[symb]', 'OPERAND[symb]'],
    },
    'EXIT': {
        'id': 33,
        'argt': ['OPERAND[symb]'],
    },
    # Instrukce na ladění
    'DPRINT': {
        'id': 34,
        'argt': ['OPERAND[symb]'],
    },
    'BREAK': {
        'id': 35,
        'argt': [],
    },

}

# Nastavení výstupu chybových hlášek

# Návratový kód
RETCODE = {
    'OK': 0,
    'EPARAM': 10,
    'ENOENT': 11,
    'EWRITE': 12,
    'ENOHEAD': 21,
    'EOPCODE': 22,
    'EANLYS': 23,
    'EINT': 99,
}

# Funkce pro zpracování vstupního kódu a generování XML reprezentace
def parse_code(input_code):
    # Zde bude implementace zpracování kódu a generování XML reprezentace
    pass

# Funkce pro výpis nápovědy
def print_help():
    help_message = """
    Použití: parse.py [--help || -h]

    IPPcode24 Parser
    Zpracuje kód (IPPcode24) ze standardního vstupu.
    Pokud nenajde žádné syntaktické nebo lexikální chyby,
    vypíše jeho XML reprezentaci na standardní výstup.

    Volby:
      --help nebo -h          Zobrazí tuto nápovědu a ukončí program
    """
    print(help_message)
    sys.exit(RETCODE['OK'])

# Hlavní funkce pro analýzu přepínačů a volání odpovídajících funkcí
def main():
    # Inicializace parseru argumentů s popisem programu a bez automatického přidání help přepínače
    parser = argparse.ArgumentParser(description='IPPcode24 Parser', add_help=False)
    
    # Přidání možnosti --help pro zobrazení nápovědy
    parser.add_argument('--help', '-h', action='store_true', help='Zobrazí tuto nápovědu a ukončí program')

    # Zpracování předaných argumentů
    args = parser.parse_args()

    # Kontrola, zda byly předány další argumenty kromě přepínače --help
    if len(sys.argv) > 2:
        print("Chyba: Přepínač --help nelze kombinovat s žádným jiným parametrem.", file=sys.stderr)
        sys.exit(RETCODE['EPARAM'])    
        
    # Pokud byl předán argument --help
    if args.help:
        print_help()

# Zavolání hlavní funkce
if __name__ == "__main__":
    main()