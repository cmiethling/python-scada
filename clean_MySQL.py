from  sql_connector import SQLConnector
import Tkinter as tk
import tkMessageBox as messagebox


def loesche_Eintraege():
    sql_object = SQLConnector()
    # 7200s = 2h, 604800s = 1 Woche -> 1mil fast 2Wochen
    sql_object.loesche_Zeilen_unterhalb('messwerte_1s',int(1e6))
    sql_object.loesche_Zeilen_unterhalb('stoermeldungen', 100)
    sql_object.loesche_Zeilen_unterhalb('befehle', 1000)
    sql_object.loesche_Zeilen_unterhalb('meldungen', 1000)
    sql_object.loesche_Zeilen_unterhalb('sollwerte', 1000)
    return None


def Message(title, text):
    tk.Tk().withdraw()  # hide the root window

    messagebox.showinfo(title, text)  # show the messagebox


if __name__ == "__main__":
    loesche_Eintraege()