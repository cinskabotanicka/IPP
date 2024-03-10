Implementační dokumentace k 1. úloze do IPP 2023/2024
Jméno a příjmení: Martina Hromádková
Login: xhroma15

## Úvod

Tento dokument slouží k popisu implementace skriptu `parse.py`, který slouží k analýze kódu v IPPcode24 a generování XML reprezentace. Skript byl vytvořen v rámci první úlohy v předmětu IPP.

## Filozofie návrhu

Cílem skriptu `parse.py` je zpracování kódu v IPPcode24 a vytvoření jeho XML reprezentace. Implementace se zaměřuje na efektivní a přesné zpracování instrukcí, zachování správné struktury XML a identifikaci chyb v kódu.

## Interní reprezentace

Interně skript pracuje s různými datovými strukturami pro reprezentaci instrukcí, operandů a konstant. Používá se kombinace slovníků a seznamů pro efektivní manipulaci s daty a generování XML reprezentace.

## Způsob řešení

Skript postupuje následovně:

1. Načte vstupní kód z IPPcode24.
2. Předzpracuje kód a odstraní komentáře.
3. Zpracuje každou instrukci a její argumenty.
4. Provádí syntaktickou kontrolu instrukcí a operandů.
5. Generuje XML reprezentaci zpracovaného kódu.
6. Vypisuje XML reprezentaci na standardní výstup.

## Specifické postupy

- **Předzpracování kódu:** Skript odstraňuje komentáře a zpracovává prázdné řádky.
- **Zpracování instrukcí:** Každá instrukce je zpracována podle definovaných pravidel pro IPPcode24. Skript kontroluje správnost operandů a instrukcí.
- **Generování XML:** XML reprezentace je vytvářena pomocí knihovny `xml.etree.ElementTree`. Skript pečlivě vytváří strukturu XML podle specifikace.

## Závěr

Skript `parse.py` poskytuje robustní a spolehlivé zpracování kódu v IPPcode24 a generuje přesnou XML reprezentaci. Jeho implementace se řídí specifikací IPPcode24 a dbá na správnost a přesnost výstupu.

Tím končí dokumentace k skriptu `parse.py`.
