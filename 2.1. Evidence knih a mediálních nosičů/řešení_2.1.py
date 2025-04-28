#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: pstaif
"""
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

DB_NAME = 'media_records.db'

class MediaDB:
    """
    MediaDB je helper class, ve které se nacházi v
    šechny operace s databazí SQLite. 
    """
    def __init__(self, db_name=DB_NAME):
        """
        Konstrukor bere 
        jméno databáze jako dobrovolný argument, jinak defaultuje 
        ke jménu media_records.db. conn spouští SQLite databázi a vytváří tabulku
        """
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """
        Funkce sqlite object a posílá sql příkaz na 
        vytvoření tabulky s příslušnými sloupci 
        (ID = je povinný primarní klíč DB). Poté funkcí 
        commit() Ukládá transakci vytvoření tabulky na disk.
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_type TEXT NOT NULL,
                title TEXT NOT NULL,
                creator TEXT,
                acquisition_date TEXT,
                description TEXT,
                borrower TEXT,
                loan_date TEXT
            )
        ''')
        self.conn.commit()

    def add_item(self, media_type, title, creator, acq_date, description):
        """
        Funcke s parametry pro přídání nového řádku do tabulky.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO items (media_type, title, creator, acquisition_date, description) VALUES (?, ?, ?, ?, ?)',
            (media_type, title, creator, acq_date, description)
        )
        self.conn.commit()

    def update_item(self, item_id, media_type, title, creator, acq_date, description):
        """
        Funcke s parametry pro uprávu existujícího řádku v tabulce.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            '''UPDATE items SET media_type=?, title=?, creator=?, acquisition_date=?, description=? WHERE id=?''',
            (media_type, title, creator, acq_date, description, item_id)
        )
        self.conn.commit()

    def delete_item(self, item_id):
        """
        Funcke s parametrem ID pro smzáni řádku z tabulky.
        """
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM items WHERE id=?', (item_id,))
        self.conn.commit()

    def loan_item(self, item_id, borrower):
        """
        Funcke s parametry ID položky a jmémen osoby ktéra 
        si zapučuje položku, která vytváří záznam o vpujčení položky tím, 
        že populuje řádek borrower s jeho jménem, která tato funcke 
        dostala jako argument. Funkce také invokuje datetime.now(),
        což zaznaména přítomný čas, ktery je poté zapsán do slouoce 
        loan_date v tabulce.
        """
        cursor = self.conn.cursor()
        loan_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute(
            'UPDATE items SET borrower=?, loan_date=? WHERE id=?',
            (borrower, loan_date, item_id)
        )
        self.conn.commit()

    def return_item(self, item_id):
        """
        Funkce, která slouží k zaznamenání vrácení položky. 
        Jako parametry bere jen ID položky. Položka je dle ID vyhledaná a sloupce
        borrower a loan_date nabyjí hodnotu NULL.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE items SET borrower=NULL, loan_date=NULL WHERE id=?',
            (item_id,)
        )
        self.conn.commit()

    def fetch_items(self, media_type=None, only_loaned=False):
        """
        Funkce k vyhledání položek v tabulce s použitím filtrů. 
        Tyto dva filtry týkající se sloupců media_type a only_loaned, 
        které mají defaultní hodnotu none a false. Pokud je je hodnota 
        těchto parametrů změněna, příslušné řádky z tabulky budou zobrazeny. 
        """
        cursor = self.conn.cursor()
        query = 'SELECT * FROM items'
        conditions = []
        params = []
        if media_type and media_type != 'All':
            conditions.append('media_type=?')
            params.append(media_type)
        if only_loaned:
            conditions.append('borrower IS NOT NULL')
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        query += ' ORDER BY title'
        cursor.execute(query, params)
        return cursor.fetchall()

class MediaApp(tk.Tk):
    """ 
    Class MediaApp je definovaná jako subclass tk.Tk a slouží k definici 
    uživatelského interfacu a jeho integrace s funkcemi classu MediaDB.
    """
    def __init__(self):
        """ 
        Konstruktor pro okenko aplikace, 
        instanciován funkci title() a proporce nastaveny na
        800x500 pixelů. Také pomocí self.db = MediaDB() ytvoří 
        instanci databázového pomocníka, aby grafické uživatelské 
        rozhraní mohlo volat metody CRUD a dotazování. 
        """
        super().__init__()
        self.title('Home Media Record Keeper')
        self.geometry('800x500')

        self.db = MediaDB()
        self.create_widgets()
        self.populate_tree()

    def create_widgets(self):
        """ 
        Tato metoda slouží ke konstrukci widgetů v grafickém 
        uživatelském rozhraní (Tkinter). 
        """
        
        # Filter frame
        """
        Vytvoří horizontální panel s rozbalovacím 
        seznamem pro výběr typu média (Vše, Kniha, CD, DVD) a 
        zaškrtávací políčko „Zobrazit pouze půjčené“. Při změně 
        filtru se automaticky znovu načte seznam položek.
        """
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill=tk.X, pady=5)

        ttk.Label(filter_frame, text='Filter by type:').pack(side=tk.LEFT, padx=5)
        self.type_var = tk.StringVar(value='All')
        self.type_combo = ttk.Combobox(filter_frame, textvariable=self.type_var, state='readonly')
        self.type_combo['values'] = ['All', 'Book', 'CD', 'DVD']
        self.type_combo.pack(side=tk.LEFT)
        self.type_combo.bind('<<ComboboxSelected>>', lambda e: self.populate_tree())

        self.loaned_var = tk.BooleanVar()
        ttk.Checkbutton(filter_frame, text='Show only loaned', variable=self.loaned_var, command=self.populate_tree).pack(side=tk.LEFT, padx=10)

        # Treeview
        """
        Tabulka s hlavičkami sloupců ID, Typ, Název, 
        Autor/Režisér, Datum pořízení, Půjčeno komu, 
        Datum půjčení. Sloupce se nastaví na šířku 100 px 
        (sloupec Název na 200 px) a tabulka se rozprostře 
        přes dostupnou plochu okna.
        """
        columns = ('ID', 'Type', 'Title', 'Creator', 'Acquired', 'Borrower', 'Loan Date')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.W)
        self.tree.column('Title', width=200)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        # Buttons
        """
        Vytvoří se nový frame s 5px odsazením. 
        Uvnitř vytvoří tlačítko s popiskem ('Add', 'Edit' atd.) a 
        při kliknutí spustí odpovídající metodu.
        """
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=5)
        for text, cmd in (
            ('Add', self.add_item),
            ('Edit', self.edit_item),
            ('Delete', self.delete_item),
            ('Loan', self.loan_item),
            ('Return', self.return_item)
        ):
            ttk.Button(btn_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=5)

    def populate_tree(self):
        """ 
        Vyčistí všechny existující řádky v Treeview a znovu načte
        a zobrazí položky z databáze podle aktuálně zvolených filtrů
        (typ média a stav půjčení).
        """
        for row in self.tree.get_children():
            self.tree.delete(row)
        items = self.db.fetch_items(self.type_var.get(), self.loaned_var.get())
        for it in items:
            self.tree.insert('', tk.END, values=it)

    def add_item(self):
        """ 
        Otevře dialog pro přidání nové položky. 
        Po potvrzení dialogu vloží zadaná data do databáze
        a aktualizuje zobrazení.
        """
        dialog = ItemDialog(self, 'Add Item')
        if dialog.result:
            media_type, title, creator, acq_date, desc = dialog.result
            self.db.add_item(media_type, title, creator, acq_date, desc)
            self.populate_tree()

    def edit_item(self):
        """ 
        Pokud je vybraná položka, otevře dialog předvyplněný jejími hodnotami.
        Po úpravě uloží změny do databáze a znovu načte seznam.
        Pokud není nic vybráno, zobrazí varování.
        """
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Select item', 'Please select an item to edit.')
            return
        item_vals = self.tree.item(sel[0], 'values')
        dialog = ItemDialog(self, 'Edit Item', prefill=item_vals)
        if dialog.result:
            media_type, title, creator, acq_date, desc = dialog.result
            self.db.update_item(item_vals[0], media_type, title, creator, acq_date, desc)
            self.populate_tree()

    def delete_item(self):
        """ 
        Zkontroluje, že je položka vybraná, a zeptá se na potvrzení smazání.
        Pokud uživatel potvrdí, odstraní záznam z databáze
        a obnoví zobrazení seznamu.
        """
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Select item', 'Please select an item to delete.')
            return
        if messagebox.askyesno('Confirm Delete', 'Are you sure you want to delete the selected item?'):
            item_id = self.tree.item(sel[0], 'values')[0]
            self.db.delete_item(item_id)
            self.populate_tree()

    def loan_item(self):
        """ 
        Zkontroluje výběr položky a zda už není půjčená.
        Pokud je k dispozici, otevře dialog pro zadání jména dlužníka,
        uloží půjčku do databáze a znovu načte seznam.
        """
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Select item', 'Please select an item to loan.')
            return
        item_vals = self.tree.item(sel[0], 'values')
        if item_vals[5]:
            messagebox.showinfo('Already Loaned', 'This item is already loaned.')
            return
        borrower = simpledialog.askstring('Loan Item', 'Enter borrower name:')
        if borrower:
            self.db.loan_item(item_vals[0], borrower)
            self.populate_tree()

    def return_item(self):
        """ 
        Zkontroluje výběr položky a ověří, že je skutečně půjčená.
        Pokud ano, vrátí položku (vymaže údaje o dlužníkovi)
        a obnoví zobrazení.
        """
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Select item', 'Please select an item to return.')
            return
        item_vals = self.tree.item(sel[0], 'values')
        if not item_vals[5]:
            messagebox.showinfo('Not Loaned', 'This item is not currently loaned.')
            return
        self.db.return_item(item_vals[0])
        self.populate_tree()

class ItemDialog(simpledialog.Dialog):
    """
    Dialog pro přidání nebo úpravu položky médií.
    Zajišťuje vstup všech potřebných polí: typ média, název,
    autor/režisér, datum pořízení a popis.
    """
    def __init__(self, parent, title, prefill=None):
        self.prefill = prefill
        super().__init__(parent, title)

    def body(self, master):
        """ 
        Vytvoří a rozmístí widgety pro zadání údajů o položce:
        - Kombobox pro volbu typu média
        - Textová pole pro název a autora/režiséra
        - Vstup pro datum pořízení (YYYY-MM-DD)
        - Víceřádkové Text pole pro popis
        Vrací widget, na který se zaměří kurzor po otevření dialogu.
        parametr master: rodičovský kontejner uvnitř dialogu
        """
        ttk.Label(master, text='Type:').grid(row=0, column=0, sticky=tk.W)
        self.type_var = tk.StringVar(value=(self.prefill[1] if self.prefill else 'Book'))
        self.type_combo = ttk.Combobox(master, textvariable=self.type_var, state='readonly')
        self.type_combo['values'] = ['Book', 'CD', 'DVD']
        self.type_combo.grid(row=0, column=1)

        ttk.Label(master, text='Title:').grid(row=1, column=0, sticky=tk.W)
        self.title_var = tk.StringVar(value=(self.prefill[2] if self.prefill else ''))
        ttk.Entry(master, textvariable=self.title_var).grid(row=1, column=1)

        ttk.Label(master, text='Author/Director:').grid(row=2, column=0, sticky=tk.W)
        self.creator_var = tk.StringVar(value=(self.prefill[3] if self.prefill else ''))
        ttk.Entry(master, textvariable=self.creator_var).grid(row=2, column=1)

        ttk.Label(master, text='Acquisition Date (YYYY-MM-DD):').grid(row=3, column=0, sticky=tk.W)
        self.acq_var = tk.StringVar(value=(self.prefill[4] if self.prefill else datetime.now().strftime('%Y-%m-%d')))
        ttk.Entry(master, textvariable=self.acq_var).grid(row=3, column=1)

        ttk.Label(master, text='Description:').grid(row=4, column=0, sticky=tk.W)
        self.desc_var = tk.Text(master, width=40, height=4)
        self.desc_var.grid(row=4, column=1)
        if self.prefill:
            self.desc_var.insert('1.0', self.prefill[5])
        return self.type_combo

    def apply(self):
        """ 
        Po potvrzení dialogu načte hodnoty ze všech widgetů,
        uloží je do n-tice a přidělí do self.result pro další zpracování.
        """
        media_type = self.type_var.get()
        title = self.title_var.get()
        creator = self.creator_var.get()
        acq_date = self.acq_var.get()
        description = self.desc_var.get('1.0', tk.END).strip()
        self.result = (media_type, title, creator, acq_date, description)

if __name__ == '__main__':
    app = MediaApp()
    app.mainloop()

