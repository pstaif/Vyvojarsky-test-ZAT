# ZIP Archive Viewer in Streamlit

## Popis
Jednoduchá webová aplikace ve Streamlit pro nahrávání a interaktivní prohlížení obsahu ZIP archivů. Uživatel může procházet strukturu složek i souborů a stahovat buď jednotlivé položky, nebo celý seznam archivu najednou.

## Funkce
- **Nahrání ZIP souboru:** přes `st.file_uploader`.
- **Prohlížení obsahu:** přehledný výpis složek a souborů uvnitř archivu.
- **Stažení jednotlivých souborů:** tlačítka pro stažení jednoho souboru.
- **Stažení celého seznamu archivu:** stažení seznamu souborů a složek archivu .zip.
- **Práce v paměti:** ZIP se načítá a zpracovává přes `io.BytesIO` bez zápisu na disk.

## Požadavky
- Python 3.8+
- Knihovny:
  - `streamlit`
  - `io` (standardní knihovna)
  - `zipfile` (standardní knihovna)

## Spuštění
V kořenovém adresáři projektu spusťte:
```bash
streamlit run řešení_2.2.py
```

## Struktura projektu
```
řešení_2.2.py             # Hlavní skript aplikace
README.md                 # Tento soubor s dokumentací
``` 
