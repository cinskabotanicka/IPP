"""Tento skript slouží k analýze kódu v IPPcode24 a generování XML reprezentace.

    Název skriptu: parse.py
    Datum: 18. 2. 2024
    Autor: Martina Hromadkova
    Login: xhroma15
"""

import re
import sys
import argparse
from typing import Union
import xml.etree.ElementTree as ET
import xml.dom.minidom
from xml.etree.ElementTree import tostring

# Konstanty

GINFO = {'lines': 0, 'header': False, 'i_lines': 0, 'c_lines': 0}

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
    'SUCCESS': 0,
    'ERPARAM': 10,
    'ERNOENT': 11,
    'ERWRITE': 12,
    'ERNOHEAD': 21,
    'EROPCODE': 22,
    'ERANLYS': 23,
    'ERINT': 99,
}

#
# Funkce pro generování XML reprezentace kódu
#

# Funkce pro vrácení XML jako řetězce, volitelně formátovaného jako dokument XML
def XML_asXML(format: bool = False) -> str:
    global XML

    xml_string = tostring(XML, encoding='unicode')

    if not format:
        return xml_string

    # Parse XML a formátování
    xml_dom = xml.dom.minidom.parseString(xml_string)
    pretty_xml_string = xml_dom.toprettyxml(indent="  ")

    # Odstranění prvního řádku pro formátování
    pretty_xml_lines = pretty_xml_string.split('\n')[1:]
    pretty_xml_string = '\n'.join(pretty_xml_lines)

    return '<?xml version="1.0" encoding="UTF-8"?>\n' + pretty_xml_string

# Funkce pro vytvoření kořenového elementu XML 
def XML_new_root() -> ET.Element:
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>'
    root = ET.Element('program', {'language': 'IPPcode24'})
    xml_string = xml_declaration + ET.tostring(root, encoding='unicode')
    return ET.fromstring(xml_string)

# Funkce pro přidání instrukce do XML
def XML_add_instruction(name: str) -> ET.Element:

    global GINFO
    global XML

    instruction = ET.Element('instruction')
    instruction.set('order', str(GINFO['i_lines']))
    instruction.set('opcode', name)

    # Instrukce nemá žádné argumenty
    if not INSTR[name]['argt']:
        XML.append(instruction)
        return instruction

    # Přidání instrukce do XML
    XML.append(instruction)

    return instruction


# Funkce pro přidání argumentu do instrukce
def XML_add_argument(instruction: ET.Element, order: int) -> ET.Element:
    return ET.SubElement(instruction, f'arg{order}')

# Funkce pro vytvoření XML reprezentace proměnné
def XML_make_variable(arg_xml: ET.Element, value: str) -> ET.Element:
    arg_xml.set('type', 'var')
    arg_xml.text = value
    return arg_xml

# Funkce pro vytvoření XML reprezentace konstanty
def XML_make_constant(arg_xml: ET.Element, type: str, value: str) -> ET.Element:
    arg_xml.set('type', type.lower())
    arg_xml.text = value
    return arg_xml

# Funkce pro vytvoření XML reprezentace návěští
def XML_make_label(arg_xml: ET.Element, name: str) -> ET.Element:
    arg_xml.set('type', 'label')
    arg_xml.text = name
    return arg_xml

# Funkce pro vytvoření XML reprezentace typu                        
def XML_make_type(arg_xml: ET.Element, type_str: str) -> ET.Element:
    arg_xml.set('type', 'type')
    arg_xml.text = type_str
    return arg_xml

# Funkce provádí předzpracování kódu
def preparse(line: str) -> Union[str, None]:
    global GINFO

    # Celý řádek je komentář
    if is_comment(line):
        GINFO['c_lines'] += 1
        return None

    # Odstranění komentářů
    if has_comment(line):
        GINFO['c_lines'] += 1
        line = remove_comments(line)

    # Odstranění nadbytečných bílých znaků
    line = re.sub(r'\s+', ' ', line).strip()

    # Prázdný řádek
    if is_empty_line(line):
        return None

    return line

# Funkce zpracovává řádek kódu
def parse_line(line: str) -> None:
    global GINFO
    global XML

    # Odstranění komentářů a ignorování prázdných řádků
    line = preparse(line)
    if not line:
        return

    # První neprázdný řádek musí být záhlaví
    if not GINFO['header']:
        # Pokud aktuální řádek je hlavička
        if is_header(line):
            GINFO['header'] = True
        else:
            # Pokud není hlavička, zobrazíme chybovou zprávu a ukončíme program
            sys.exit(RETCODE['ERNOHEAD'])
        return

    # Inkrementace čítače řádků        
    GINFO['i_lines'] += 1
    
    # Rozdělení řádku na instrukci a argumenty
    instr_args = line.split(' ')
    instr = instr_args.pop(0).upper() if instr_args else None
    if not instr:
        sys.exit(RETCODE['EROPCODE'])

    # Kontrola, zda je instrukce v seznamu
    instr_id = INSTR.get(instr, None) if INSTR else None
    if not instr_id:
        sys.exit(RETCODE['EROPCODE'])

    # XML prvek instrukce
    instr_xml = XML_add_instruction(instr)

    # Kontrola počtu argumentů
    instr_argc = len(instr_args)
    if instr_argc != len(instr_id['argt']):
        sys.exit(RETCODE['ERANLYS'])

    # Zpracování argumentů
    for i, arg in enumerate(instr_args):
        arg_type = instr_id['argt'][i]
        arg_xml = XML_add_argument(instr_xml, i + 1)
        if arg_type == 'OPERAND[var]':
            if not parse_var(arg, arg_xml):
                sys.exit(RETCODE['ERANLYS'])
        elif arg_type == 'OPERAND[symb]':
            if not (parse_var(arg, arg_xml) or parse_const(arg, arg_xml)):
                sys.exit(RETCODE['ERANLYS'])
        elif arg_type == 'OPERAND[label]':
            if not is_identifier(arg):
                sys.exit(RETCODE['ERANLYS'])
            else:
                XML_make_label(arg_xml, arg)
        elif arg_type == 'OPERAND[type]':
            if not is_type(arg):
                sys.exit(RETCODE['ERANLYS'])
            else:
                XML_make_type(arg_xml, arg)
        else:
            sys.exit(RETCODE['ERANLYS'])
            
# Funkce ověřuje a zpracovává proměnnou a přidává ji do XML
def parse_var(op, arg_xml):
    op_split = op.split('@', 1)
    
    # Kontrola formátu: FRAME@ID
    if len(op_split) != 2:
        return False
    
    var_frame, var_id = op_split
    
    # Kontrola FRAME = GF|LF|TF
    if not is_frame(var_frame):
        return False
    
    # Kontrola ID
    if not is_identifier(var_id):
        return False
    
    # Platná proměnná -> přidat do XML
    XML_make_variable(arg_xml, op)
    return True

# Funkce ověřuje a zpracovává konstantu a přidává ji do XML
def parse_const(op, arg_xml):
    op_split = op.split('@', 1)
    
    # Kontrola formátu: TYPE@VALUE
    if len(op_split) != 2:
        return False
    
    const_type, const_val = op_split
    
    # Kontrola TYPE
    if not is_type(const_type):
        return False
    
    const_typeid = DTYPE[const_type]
    
    # Kontrola VALUE
    if const_typeid == DTYPE['int']:
        if not re.match(r'^[+-]?\d+$', const_val):
            return False
    elif const_typeid == DTYPE['bool']:
        if const_val not in ['true', 'false']:
            return False
    elif const_typeid == DTYPE['string']:
        if re.search(r'[\s#]|(\\(?!\d{3}))', const_val):
            return False
    elif const_typeid == DTYPE['nil']:
        if const_val != 'nil':
            return False
    elif const_typeid == DTYPE['float']:
        if not re.match(r'^[+-]?0x[0-9a-fA-F]+(\.[0-9a-fA-F]+)?p[+-]?\d+$', const_val):
            return False
    else:
        return False
    
    # Platná konstanta -> přidat do XML
    XML_make_constant(arg_xml, const_type, const_val)
    return True

# Funkce pro kontrolu, zda je řetězec platným identifikátorem
def is_identifier(op):
    return bool(re.match(r'^[$&%!a-zA-Z_\-\*\?][$&%!\w\-\*\?]*$', op))

# Funkce pro kontrolu, zda je řetězec platným rámcem
def is_frame(op):
    return bool(re.match(r'^(GF|LF|TF)$', op))

# Funkce pro kontrolu, zda je řetězec komentářem
def is_comment(line):
    return bool(re.match(r'^\s*#.*', line))

# Funkce pro kontrolu, zda je řetězec prázdným řádkem
def is_empty_line(line):
    return bool(re.match(r'^\s*$', line))

# Funkce pro kontrolu, zda je řetězec komentářem
def has_comment(line):
    return bool(re.match(r'^.*#', line))

# Funkce pro odstranění komentářů
def remove_comments(line):
    return line.split('#', 1)[0]

# Funkce pro kontrolu, zda je řetězec hlavičkou
def is_header(line):
    return bool(re.match(r'^\.IPPcode24$', line))

# Funkce pro kontrolu, zda je řetězec platným typem
def is_type(op):
    return op in DTYPE

# Funkce pro výpis nápovědy
def print_help():
    help_message = """
    Použití: parse.py [--help || -h]

    IPPcode24 Parser
    Zpracuje kód (IPPcode24) ze standardního vstupu.
    PSUCCESSud nenajde žádné syntaktické nebo lexikální chyby,
    vypíše jeho XML reprezentaci na standardní výstup.

    Volby:
      --help nebo -h          Zobrazí tuto nápovědu a ukončí program
    """
    print(help_message)
    sys.exit(RETCODE['SUCCESS'])

# Hlavní funkce pro analýzu přepínačů a volání odpovídajících funkcí
def main():
    global GINFO
    global XML
    
    # Vytvoření XML reprezentace kódu
    XML = XML_new_root()

    # Inicializace parseru argumentů s popisem programu a bez automatického přidání help přepínače
    parser = argparse.ArgumentParser(description='IPPcode24 Parser', add_help=False)
    
    # Přidání možnosti --help pro zobrazení nápovědy
    parser.add_argument('--help', '-h', action='store_true', help='Zobrazí tuto nápovědu a ukončí program')

    # Zpracování předaných argumentů
    args = parser.parse_args()

    # Kontrola, zda byly předány další argumenty kromě přepínače --help
    if len(sys.argv) > 2:
        print("Chyba: Přepínač --help nelze kombinovat s žádným jiným parametrem.", file=sys.stderr)
        sys.exit(RETCODE['ERPARAM'])    
        
    # Pokud byl předán argument --help
    if args.help:
        print_help()

    # Zpracování vstupu
    for lineno, line in enumerate(sys.stdin):
        GINFO['lines'] = lineno + 1
        parse_line(line)

    # Kontrola chybějící hlavičky
    if not GINFO['header']:
        sys.exit(RETCODE['ERNOHEAD'])

    # Výpis XML reprezentace kódu
    print(XML_asXML(True))

    # Ukončení s úspěšným kódem
    sys.exit(RETCODE['SUCCESS'])

# Zavolání hlavní funkce
if __name__ == "__main__":
    main()