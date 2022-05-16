import tkinter as tk
from tkinter import filedialog


import pandas as pd
import pathlib
import prace_s_db

import openpyxl


def import_sl(self):
    file_path = filedialog.askopenfilename()
    try:
        soubor_typ = pathlib.Path(file_path).suffix       
        if "xl" in soubor_typ:
            seznam_slov = pd.read_excel(file_path, engine = 'openpyxl')

        elif "csv" or "txt" in soubor_typ:
            seznam_slov = pd.read_csv(file_path, delimiter='/', usecols=(0,1))
    
    except ValueError:
        tk.messagebox.showwarning("ERROR", "Nepodporovaný typ souboru\naplikace podporuje pouze soubory typu\ncsv, txt, xls")
        return
    except FileNotFoundError:
        return
    seznam_slov = seznam_slov.values.tolist()
    akt_prostredi = [self.akt_Lekce]
    export = akt_prostredi + seznam_slov
    pocet = prace_s_db.pridej_slovicka(export)
    tk.messagebox.showwarning("ULOŽENO", "V databáti je uloženo " + str(pocet) + "\nslovíček pro tuto lekci.")
    
