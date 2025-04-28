# Word Search in Matrix

## Popis
Interaktivní webová aplikace Osmisměrky vytvořená pomocí Streamlitu, která umožňuje uživatelům zadat matici písmen a seznam slov k vyhledání. Aplikace vizuálně zvýrazní nalezená slova v matici a zobrazí seznam nalezených slov. Navíc dokáže najít a zobrazit slovo složené ze zbývajících nepoužitých písmen.

## Funkce
- **Vložení matice písmen:** zadejte matici tak, že každý řádek píšete na nový řádek.
- **Vložení seznamu slov:** seznam slov oddělte mezerami.
- **Vyhledání slov:** tlačítko **Find Words** prohledá matici a zvýrazní nalezená slova.
- **Zobrazení zbývajících písmen:** tlačítko **Find Remaining Letters** vytvoří a zobrazí slovo ze všech písmen, která nebyla použita.

## Požadavky
- Python 3.7+
- Knihovny:
  - `streamlit`

## Spuštění
V kořenovém adresáři projektu spusťte:
```bash
streamlit run řešení_2.3.py
```

## Struktura projektu
```
řešení_2.3.py    # Hlavní skript se Streamlit rozhraním
README.md       # Dokumentace projektu
``` 
