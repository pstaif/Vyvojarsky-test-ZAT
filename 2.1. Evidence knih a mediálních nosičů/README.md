# Home Media Record Keeper

## Popis
Desktopová aplikace pro správu osobní sbírky médií (knihy, CD, DVD). Umožňuje evidovat položky, upravovat je, mazat, půjčovat a vracet, a filtrovat podle typu nebo stavu půjčení.

## Funkce
- Zobrazení všech položek nebo filtrování dle typu (All / Book / CD / DVD)
- CRUD operace: přidávání, úprava, mazání záznamů
- Evidence data pořízení a popisu každé položky
- Půjčování položek (zadání jména dlužníka + automatické zaznamenání data)
- Vrácení položky (vymazání informace o dlužníkovi)
- Zobrazení pouze půjčených položek pomocí zaškrtávacího políčka

## Požadavky
- Python 3.7+
- Moduly (součást standardní knihovny):
  - `sqlite3`
  - `tkinter`
  - `datetime`

## Spuštění
V kořenovém adresáři projektu spusťte:
```bash
python řešení_2.1.py
```

## Struktura projektu
```
řešení_2.1.py        # Hlavní skript s GUI i logikou databáze
media_records.db     # SQLite databáze (vytvoří se při prvním spuštění)
README.md            # Tento soubor s dokumentací
```
