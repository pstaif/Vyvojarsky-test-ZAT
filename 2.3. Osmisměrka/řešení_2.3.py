#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: pstaif
"""

import streamlit as st

def text_to_matrix(text_input):
    # Funcke která bere text jako input, poté ho rozdelí
    # na řádky na základě '\n' indikátoru nového řádku. Individualní
    # písmena jsou populována do matice, ktera je poté funkcí vrácena. 
    rows = text_input.strip().split('\n')
    matrix = [list(row.strip()) for row in rows]
    return matrix

def find_words_in_matrix(matrix, word_list):
    # Tato funkce slouží ke hledáni slov v matici (osmisměrky). 
    # Hledá v ní všechna slova ze zadaného seznamu slov (word_list). 
    # Hledání probíhá horizontálně, vertikálně a diagonálně ve 
    # všech osmi směrech.  
    found_words = {}
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    
    def search(r, c, word, index, direction):
        # Tato vnitřní funkce je rekurzivní a slouží k prohledání 
        # jednoho konkrétního slova (word) z dané počáteční pozice (r, c) 
        # v zadaném směru z tuplu direction.
        
        if index == len(word):
          return True, []
      
        if not (0 <= r < rows and 0 <= c < cols and matrix[r][c] == word[index]):
          return False, None
      
        next_r, next_c = r + direction[0], c + direction[1]
        found, rest_of_path = search(next_r, next_c, word, index + 1, direction)
        if found:
          return True, [(r, c)] + rest_of_path
        return False, None
    
    directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, 1), (-1, -1)]


    # Následující loop na začátku pro každé hledané word se 
    # inicializuje prázdný seznam found_word_locations, který 
    # ukládá všechny nalezené cesty (sekvence souřadnic) pro dané 
    # slovo v matici. Pro každé slovo iteruje přes všechny buňky matice 
    # jako potenciální počátek a pro každý směr volá rekurzivní funkci 
    # search, která ověřuje existenci slova. Pokud se slovo najde, uloží se
    # seznam souřadnic jeho písmen do seznamu found_word_locations pro 
    # dané slovo. Nakonec, pokud pro dané slovo existují nějaké nalezené pozice, 
    # uloží se toto slovo jako klíč a seznam jeho pozic jako hodnota do 
    # slovníku found_words, který je na konci funkce vrácen.
  
    for word in word_list:
        found_word_locations = []
        for r in range(rows):
          for c in range(cols):
            for direction in directions:
              found, path = search(r, c, word, 0, direction)
              if found:
                found_word_locations.append(path)
        if found_word_locations:
          found_words[word] = found_word_locations
    
    return found_words

def find_remaining_letters(matrix, found_words): 
    # Tato funkce má za úkol najít všechna písmena v původní 
    # matici, která nejsou součástí žádného z nalezených slov. 
    # Poté tato zbývající písmena spojí do jednoho slova.
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    colored_cells = set()
    remaining_letters = []
    
    
    # Tento trojitý for loop iteruje přes všechny nalezené pozice 
    # písmen, které tvoří hledaná slova. Začíná procházením všech 
    # seznamů pozic (locations_list) uložených jako hodnoty ve 
    # slovníku found_words. Pro každý takový seznam 
    # (který reprezentuje všechny výskyty jednoho slova) 
    # iteruje přes jednotlivé nalezené cesty (locations), 
    # kde každá cesta je seznamem souřadnic (r, c) písmen 
    # tvořících daný výskyt slova. V nejvnitřnější smyčce se 
    # pak pro každou souřadnici (r, c) písmene, které je 
    # součástí nalezeného slova, tato souřadnice přidá do 
    # množiny colored_cells. Množina je použita proto, aby 
    # se zajistilo, že každá souřadnice je uložena pouze jednou, 
    # i když se dané písmeno může vyskytovat ve více nalezených slovech.
    for locations_list in found_words.values():
      for locations in locations_list:
        for r, c in locations:
          colored_cells.add((r, c))
    
    
    # Tento loop iteruje matici po řádcích a sloupcích. Pro 
    # každou buňku zkontroluje, zda její souřadnice nejsou v 
    # colored_cells (souřadnice písmen nalezených slov). 
    # Pokud nejsou, písmeno z této buňky se přidá do 
    # seznamu remaining_letters.
    for r in range(rows):
      for c in range(cols):
        if (r, c) not in colored_cells:
          remaining_letters.append(matrix[r][c])
    
    return "".join(remaining_letters)

def visualize_matrix_streamlit(matrix, found_words):
    # Tato funkce je zodpovědná za vizualizaci matice 
    # písmen a zvýraznění nalezených slov v Streamlit 
    # aplikaci pomocí HTML. 
    st.subheader("Letter Matrix")
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    
    word_colors = {}
    color_palette = ["lightblue", "lightgreen", "lightcoral", "lightsalmon", "lightseagreen", "lightskyblue", "lightgoldenrodyellow", "lightpink"]
    color_index = 0
    

    #Tento loop prochází všechna unikátní slova nalezených 
    #slovech (found_words). Pro každé slovo, které ještě nemá 
    #přiřazenou barvu ve slovníku word_colors, se přiřadí barva 
    #z color_palette pomocí indexu color_index. Operátor modulo % 
    #zajišťuje cyklické procházení palety barev, pokud je nalezeno 
    #více slov než barev v paletě. Tímto způsobem každé nalezené 
    #slovo získá unikátní barvu pro vizualizaci.

    for word in found_words:
      if word not in word_colors:
        word_colors[word] = color_palette[color_index % len(color_palette)]
        color_index += 1
    
   
    #Tento nested loop  prochází všechna nalezená slova a jejich 
    #seznamy souřadnic. Pro každé písmeno tvořící nalezené slovo 
    #získá jeho souřadnice (r, c) a přiřadí mu barvu daného slova 
    #(získanou z word_colors) jako hodnotu ve slovníku highlighted_cells, 
    #kde klíčem jsou tyto souřadnice. Tímto způsobem se vytvoří mapování 
    #mezi souřadnicemi písmen nalezených slov a jejich barvami pro účely 
    #zvýraznění ve vizualizaci.
   
    highlighted_cells = {}
    for word, locations_list in found_words.items():
      color = word_colors[word]
      for locations in locations_list:
        for r, c in locations:
          highlighted_cells[(r, c)] = color
    
    
    #Tento kód vytváří HTML řetězec reprezentující tabulku matice. 
    #Prochází každý řádek a sloupec matice a pro každé písmeno vytváří 
    #HTML buňku (<td>). Pokud se souřadnice aktuální buňky nacházejí ve 
    #slovníku highlighted_cells, aplikuje na buňku inline CSS styl pro 
    #podbarvení a tučné písmo. Nakonec je kompletní HTML tabulka zobrazena 
    #ve Streamlit aplikaci pomocí st.markdown s povoleným unsafe_allow_html, 
    #aby se HTML správně interpretovalo.
    
    html_table = "<table>"
    for r in range(rows):
      html_table += "<tr>"
      for c in range(cols):
        char = matrix[r][c]
        style = ""
        if (r, c) in highlighted_cells:
          style = f'background-color: {highlighted_cells[(r, c)]}; font-weight: bold;'
        html_table += f'<td style="{style}">{char}</td>'
      html_table += "</tr>"
    html_table += "</table>"
    
    st.markdown(html_table, unsafe_allow_html=True)
    
   
    #Tento kód nejprve zobrazí nadpis "Found Words". Poté zkontroluje, 
    #zda slovník found_words obsahuje nějaká nalezená slova. Pokud ano, 
    #vytvoří HTML seznam (<ul>) a pro každé nalezené slovo v 
    #tomto seznamu (word_colors) vytvoří položku (<li>) s tímto slovem, 
    #přičemž text slova je obarven příslušnou barvou. Pokud 
    #nebyla nalezena žádná slova, zobrazí se informační zpráva pomocí st.info().
    
    st.subheader("Found Words")
    if found_words:
      found_words_list_html = "<ul>"
      for word, color in word_colors.items():
        found_words_list_html += f'<li style="color: {color}; font-weight: bold;">{word}</li>'
      found_words_list_html += "</ul>"
      st.markdown(found_words_list_html, unsafe_allow_html=True)
    else:
      st.info("No words from the list were found in the matrix.")

def main():
    """
    # Funkce main() definuje uživatelské rozhraní Streamlit aplikace a řídí její logiku. 
    # Zahrnuje vstupní pole pro matici a hledaná slova, tlačítka pro spuštění hledání a 
    # zobrazení zbývajících písmen, a také zobrazení výsledků. Používá st.session_state 
    # pro uchování stavu aplikace mezi jednotlivými interakcemi uživatele.
    """
    st.title("Word Search in Matrix")

    if "matrix" not in st.session_state:
        st.session_state["matrix"] = None
    if "found_words" not in st.session_state:
        st.session_state["found_words"] = {}
    if "words_found" not in st.session_state:
        st.session_state["words_found"] = False

    text_input = st.text_area("Enter the letter matrix (each row on a new line):", """KALTJSHODA
LLPUKLTOAT
AKTAAKAARR
SAANLAKPEA
ARPOVPTOKK
RHOMOLICEA
KOLSPEKESR
ORAOCAALTP
SPOKVSTIAA
MATKAFTKAT
AIAKOSTKAY""")

    words_to_find = st.text_input("Enter words to search for (comma-separated):", "ALKA HORA JUTA KAPLE KARPATY KARTA KASA KAVKA KLAS KOSMONAUT KOST KROK LAPKA MATKA OKRASA OPAT OSMA PAKT PATKA PIETA POCEL POVLAK PROHRA SEKERA SHODA SOPKA TAKT TAKTIKA TLAK VOLHA")
    word_list = [word.strip().upper() for word in words_to_find.split(' ')]

    if st.button("Find Words"):
        if text_input:
            matrix = text_to_matrix(text_input.strip())
            if matrix and all(len(row) == len(matrix[0]) for row in matrix):
                st.session_state["matrix"] = matrix
                st.session_state["found_words"] = find_words_in_matrix(matrix, word_list)
                st.session_state["words_found"] = True  # Indicate that words have been found
            elif not matrix:
                st.error("Please enter a valid letter matrix.")
            else:
                st.error("The rows in the letter matrix must have the same length.")
        else:
            st.warning("Please enter the letter matrix.")

    if st.session_state["words_found"]:
        visualize_matrix_streamlit(st.session_state["matrix"], st.session_state["found_words"])

        if st.button("Find Remaining Letters"):
            remaining_word = find_remaining_letters(st.session_state["matrix"], st.session_state["found_words"])
            st.subheader("Remaining Letters Form:")
            st.markdown(f"**{remaining_word}**")
if __name__ == "__main__":
  main()


