#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: pstaif
"""

import streamlit as st
import zipfile
import io 
import os

st.set_page_config(page_title="Prohlížeč ZIP", layout="wide")


st.title(" Prohlížeč obsahu ZIP archivu")
st.write("Nahrajte ZIP soubor a aplikace zobrazí seznam souborů a složek, které obsahuje. Jednotlivé soubory můžete rovnou stáhnout.")


#Widget pro nahrání souboru s omezením na typ .zip a
#jen jeden soubor na jednou. 
uploaded_file = st.file_uploader(
    "Vyberte ZIP soubor",
    type="zip",
    accept_multiple_files=False
)


#Zpracování nahraného souboru
if uploaded_file is not None:
    st.markdown("---")
    st.subheader(f" Obsah archivu: `{uploaded_file.name}`")

    try:
        #Načtení celého obsahu souboru do paměti pro spolehlivost při rerunech
        zip_data = io.BytesIO(uploaded_file.getvalue())

        #Práce s kopií ZIP dat v paměti
        with zipfile.ZipFile(zip_data, 'r') as zip_ref:
            file_list = zip_ref.namelist()

            if not file_list:
                st.info("Tento ZIP archiv je prázdný.")
            else:
                st.write(f"Archiv obsahuje {len(file_list)} položek:")
                
                #Procházení položek a zobrazení s tlačítky pro soubory
                for item in file_list:
                    #Rozdělení řádku na sloupce pro název a tlačítko
                    col1, col2 = st.columns([4, 1]) #Poměr šířky sloupců

                    is_folder = item.endswith('/')

                    with col1:
                        if is_folder:
                            st.text(f" {item}")
                            st.caption("Složka")
                        else:
                            st.text(f" {item}")
                            st.caption("Soubor")

                    with col2:
                        if not is_folder:
                            try:
                                #Získání obsahu konkrétního souboru z archivu
                                file_content = zip_ref.read(item)

                                #Získání pouze názvu souboru (bez cesty)
                                download_filename = os.path.basename(item)

                                #Zobrazení tlačítka pro stažení
                                st.download_button(
                                    label="Stáhnout",
                                    data=file_content,
                                    file_name=download_filename,
                                    #'application/octet-stream' obecný typ pro binární data
                                    mime='application/octet-stream',
                                    #Unikátní klíč pro každý widget ve smyčce
                                    key=f"download_{item}"
                                )
                            except Exception as read_err:
                                #Zobrazení chyby, pokud nelze soubor z archivu přečíst
                                st.error(f"Chyba čtení", icon="⚠️")


                st.markdown("---")
                #stažení celého seznamu souborů
                list_str = "\n".join(file_list)
                st.download_button(
                    label=" Stáhnout celý seznam souborů (.txt)",
                    data=list_str,
                    file_name=f"obsah_{uploaded_file.name}.txt",
                    mime="text/plain",
                    key="download_all_list"
                )


    except zipfile.BadZipFile:
        st.error(f"Chyba: Soubor '{uploaded_file.name}' není platný nebo je poškozený ZIP archiv.")
    except Exception as e:
        #Zachycení obecných chyb 
        st.error(f"Nastala neočekávaná chyba při zpracování souboru: {e}")

else:
    st.info(" Nahrajte ZIP soubor pomocí tlačítka výše pro zobrazení jeho obsahu.")

st.markdown("---")
st.caption("Autor: Petr Štaif")