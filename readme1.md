Implementační dokumentace k 1. úloze do IPP 2023/2024
Jméno a příjmení: Martina Hromádková
Login: xhroma15

## Úvod

Tento dokument slouží k popisu implementace skriptu `parse.py`, který slouží k analýze kódu v IPPcode24 a k následnému generování XML reprezentace. Skript byl vytvořen v rámci první úlohy v předmětu IPP.

## Filozofie návrhu

Cílem skriptu `parse.py` je zpracování kódu v IPPcode24 a vytvoření jeho XML reprezentace. Implementace se zaměřuje na efektivní a přesné zpracování instrukcí, zachování správné struktury XML a identifikaci chyb v kódu s navracením správných chybových návratových hodnot podle zadání.

## Interní reprezentace

Interně skript pracuje s různými datovými strukturami pro reprezentaci instrukcí, operandů a konstant. Používám kombinaci slovníků a seznamů pro efektivní manipulaci s daty a generování XML reprezentace.

## Způsob řešení

Skript postupuje následovně:

1. Načte vstupní kód v IPPcode24.
2. Předzpracuje kód a odstraní komentáře.
3. Zpracuje každou instrukci a její argumenty.
4. Provádí syntaktickou kontrolu instrukcí a operandů.
5. Generuje XML reprezentaci zpracovaného kódu.
6. Vypisuje XML reprezentaci na standardní výstup.

## Specifické postupy

- **Předzpracování kódu:** Skript odstraňuje komentáře a zpracovává prázdné řádky.
- **Zpracování instrukcí:** Každá instrukce je zpracována podle definovaných pravidel pro IPPcode24. Skript kontroluje správnost operandů a instrukcí.
- **Generování XML:** XML reprezentace je vytvářena pomocí knihovny `xml.etree.ElementTree`. Skript pečlivě vytváří strukturu XML podle specifikace.

## Závěr a upřesnění výstupu

Skript `parse.py` poskytuje spolehlivé zpracování kódu v IPPcode24 a generuje přesnou XML reprezentaci. Tato reprezentace je formátována stejně jako ve výstupu zadaných testů, navíc pokud instrukce nemá argumenty, vypíše se pouze jako nepárový tag.