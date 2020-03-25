# -*- coding: utf-8 -*-
import datetime
from  sql_connector import SQLConnector
import Tkinter as tk
import tkMessageBox as messagebox
import pandas as pd #fuer geordnete Dict Ausgabe

def clear_list_val_if_last_val_eq_current_val(list):
    """
    Jeder einzelne Listenwert wird auf Wert-Wiederholung geprueft
    -> bei Gleichheit wird letzterer Wert = None (NULL) gesetzt
    out: list_new
    """
    # Hilfslisten initialisieren
    # Liste die den vorherigen Wert von besitzt
    l_prev_val = list[1:]
    # ersten Wert in neuer Tabelle schreiben, weil dieser nicht geschrieben werden kann 
    # (differenz = list2[0]-list1[0] -> list2[0] ~ list1[-1] = NAN) 
    l_new = [list[0]]

    # Laenge von Liste mit vorhergehenden Wert (l2) muss genommen werden, 
    # weil len(l2) < len(l1) -> ansonsten Error: index out of range
    for ind in range(0, len(l_prev_val)):
        dif = l_prev_val[ind] - list[ind]
        if dif == 0:
            # wenn vorhergehender Wert = jetziger Wert ->jetztiger Wert = None (NULL)
            new_val = None
        else:
            # ansonsten bleibt der Wert
            new_val = l_prev_val[ind]
        l_new.append(new_val)
    return l_new


def update_dict_in_list(dict_in_list):
    """
    laeuft nur mit messwerte_30s (und messwerte_1s) 
    -> TOC und N_ges werden direkt benutzt :(
    """
    # Hilfsliste -> alte Werte kommen hier rein
    l_TOC_old = []
    l_N_ges_old = []

    # Werte in eine Liste schreiben und aus sql_results loeschen 
    # -> besser nur einmal eine for-Schleife durchlaufen zu lassen     
    for dict_row in dict_in_list:
        l_TOC_old.append(dict_row.get('TOC'))
        dict_row.pop('TOC')    
        l_N_ges_old.append(dict_row.get('N_ges'))
        dict_row.pop('N_ges')

    l_TOC_new = clear_list_val_if_last_val_eq_current_val(l_TOC_old)
    l_N_ges_new = clear_list_val_if_last_val_eq_current_val(l_N_ges_old)
    # print l_N_ges_old
    # print l_N_ges_new

    # neue Werte in sql_results eintragen
    for row_nr in range(0, len(dict_in_list)):
        dict_in_list[row_nr].update({'TOC': l_TOC_new[row_nr]})
        dict_in_list[row_nr].update({'N_ges': l_N_ges_new[row_nr]})
    
    return sql_results

def write_csv_file(dict_in_list, header):  

    # letzten Monat anzeigen
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth = first - datetime.timedelta(days=1)
    zeit = lastMonth.strftime("%Y.%m")
    zeit += ' Erstellung '
    # Heute anzeige
    zeit += datetime.datetime.now().strftime("%y%m%d %H-%M-%S")


    # header_real = ['zeit', 'Re_Zul (m/h)', 'Re_pH1', 'Re_LF (mS/cm)', 'Re_TOC (mg/l)', 'Re_Nges (mg/l)', 
    # 'Re_Redox (mV)', 'Re_Trueb (FNU)', 
    # 'VB_pH2', 'VB_Vega1 (cm)', 'VB_Vega1 (l)', 'VB_c_TOC_Vorl (mg/l)', 
    # 'BR_pH3', 'BR_Vega2 (bar)', 'BR_Temp (C)', 'BR_Gas', 'Re_P1', 'P2', 'Re_Temp (C)']

    # columns gibt Spalten in dieser Reihenfolge aus,
    # es koennen auch Spalten weggelassen werden -> dann werden diese in der .csv auch weggelassen!
    df = pd.DataFrame(dict_in_list, columns=header)
    df.to_csv('../csv/' + zeit + '.csv', sep=',', index=False)#, index_label = header_real)   
    return None


def Message(title, text):
    tk.Tk().withdraw()  # hide the root window

    messagebox.showinfo(title, text)  # show the messagebox


if __name__ == "__main__":
    sql_object = SQLConnector()
    sql_results = sql_object.select_all('messwerte_30s', 'id ASC')

    """ 180515 wieder rausgenommen!
    # V3.00: Wert[i-1] = Wert[i] -> Wert[i] = None (NULL) -> update fuer TOC und N_ges
    sql_results_update = update_dict_in_list(sql_results)
    """
   

    # header als list in richtiger Reihenfolge schreiben
    # richtige Reihenfolge mittels pandas (siehe import), in fcn write_csv_file
    header = ['zeit', 'MID', 'pH1', 'LF', 'TOC', 'N_ges', 'Redox', 'Truebung', 
    'pH2', 'Vega1', 'Vega1_l', 'c_TOC_Vorlage', 
    'pH3', 'Vega2', 'Temp', 'Gas', 'P1_EIN', 'P2_EIN','Temp_Re']    

    """ 180515 wieder rausgenommen!
    # V3.00
    write_csv_file(sql_results_update, header)
    """

    # 180515: V3.00 wieder rausgenommen!
    write_csv_file(sql_results, header)

    # alle in messwerte_30s loeschen
    sql_object.truncate('messwerte_30s')

    Message('CSV', 'csv am %s um %s erstellt' % (
    datetime.datetime.now().strftime("%d.%m.%Y"), datetime.datetime.now().strftime("%H:%M:%S")))


'''
V3.00: Anmerkung
Mit mysql probiert -> unsere mysql Version kann nicht mehrere Tabellen UPDATEN:
 bei http://sqlfiddle.com/#!9/dfeae4/1 funktioniert es...

-- create table
CREATE TABLE employees (
    emp_id INT(11) NOT NULL AUTO_INCREMENT,
    emp_name VARCHAR(255) NOT NULL,
    salary FLOAT DEFAULT NULL,
    PRIMARY KEY (emp_id)
);

-- insert data for employees table
INSERT INTO employees(emp_name,salary)      
VALUES('Mary Doe', 1.2),
      ('Cindy Smith', 1.2),
      ('Sue Greenspan', 1.2),
      ('Grace Dell', 4.52342424123),
      ('Nancy Johnson', 4.52342424123),
      ('John Doe', 4.5),
      ('Lily Bush', 4.5);

UPDATE employees t1
        INNER JOIN
    # t2 um eine Zeile versetzt (t1.2 = t2.1)
    employees t2 ON t1.emp_id-1 = t2.emp_id 
SET 
    t1.salary = null
where
    t1.salary - t2.salary = 0;

select * from employees;
'''