# -*- coding: utf-8 -*-
# utf-8: für Umlaute+ß -> böse = u'böse'
import MySQLdb, datetime, csv, os, time
import re

import sys
import send_Email


class SQLConnector():
    def __init__(self):

        self.db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                                  user="root",  # your username
                                  passwd="admin",  # your password
                                  db="test")  # name of the data base
        self.cur = self.db.cursor()


    def drop(self, tabelle):
        """
        drop = Tabelle KOMPLETT aus Database loeschen 
        :param tabelle: 
        :return: 
        """
        self.cur.execute("DROP TABLE IF EXISTS %s" % tabelle)
        return None

    def truncate(self, tabelle):
        """
        drop = ALLE Daten der Tabelle (schnell) loeschen 
        :param tabelle: 
        :return: 
        """
        self.cur.execute("TRUNCATE TABLE %s;" % tabelle)
        return None

    def get_nth_rows(self, tabelle, n_te_zeile=2, spalte='*', order_by='id DESC'):
        '''
        z.B: bekomme jede 5te Zeile -> n_te_zeile = 5
        '''
        self.cur = self.db.cursor()
        self.cur.execute(
            "select %s from %s where %s.id mod %u = 0 order by %s;" % (
                spalte, tabelle, tabelle, n_te_zeile, order_by))
        results = self.cur.fetchall()
        return results

    def loesche_Zeilen_unterhalb(self, tabelle, behalte_bis_Zeile):
        '''
        z.B: behalte_bis_Zeile=2 -> alle Zeilen ab Zeile 3 werden PERMANENT geloescht!
        '''
        self.cur.execute(
            # "DELETE p FROM %s p LEFT JOIN (SELECT id FROM %s ORDER BY id DESC LIMIT %s) p2 USING(id) WHERE p2.id IS NULL;" % (
            # tabelle, tabelle, behalte_bis_Zeile)) #ist das Gleiche
            "DELETE FROM %s WHERE id <= (SELECT id FROM ( SELECT id FROM %s ORDER BY id DESC LIMIT 1 OFFSET %s ) foo);" % (
                tabelle, tabelle, behalte_bis_Zeile))
        # an MySQL uebergeben
        self.db.commit()
        return None

    def create_table(self, query):
        query = "CREATE TABLE stoermeldungen( Zeit TIMESTAMP NOT NULL, Name VARCHAR(25), Stand VARCHAR(25) )"
        self.cur.execute(query)
        return None

    def query(self, sql_query):
        """
        eine beliebige MySQL query
        :param sql_query: 
        :return: 
        """
        self.cur = self.db.cursor()
        self.cur.execute(sql_query)
        results = self.cur.fetchall()
        return results

    def select_columns(self, tabelle, spalte, order_by='id DESC'):
        """
        eine Spalte auswaehlen, kann auch fuer andere queries genutzt werden
        :param tabelle: 
        :param spalte: 
        :param order_by: 
        :return: 
        """
        self.cur = self.db.cursor()
        self.cur.execute("SELECT %s FROM %s ORDER BY %s;" % (spalte, tabelle, order_by))
        results = self.cur.fetchall()
        return results

    def select_newest_row(self, tabelle):
        """
        neuste Zeile ausgeben
        :param tabelle: 
        :return: 
        """
        self.cur = self.db.cursor()
        # Headernamen entnehmen
        self.cur.execute("SHOW columns from %s ;" % tabelle)
        info = self.cur.fetchall()
        header = []
        results = []
        all = []
        for row in info:
            header.append(row[0])

        # Werte entnehmen
        self.cur.execute("SELECT * FROM %s ORDER BY id DESC LIMIT 1" % (tabelle))
        results = self.cur.fetchall()

        # Dict mit Headernamen als keys
        res2 = []
        i = 0
        # nur erste Zeile -> results[0]
        for value in results[0]:
            if res2 == []:
                # dict-Eintrag in list
                res2.append({header[i]: value})
            else:
                # dict-Eintrag erweitern (nicht list)
                res2[0].update({header[i]: value})
            i += 1
        # Zeitformat anpassen
        try:
            zeit = res2[0]['zeit']
            res2[0]['zeit'] = zeit.strftime('%Y-%m-%d %H:%M:%S')
        except:
            try:
                zeit = res2[0]['Zeit']
                res2[0]['Zeit'] = zeit.strftime('%Y-%m-%d %H:%M:%S')
            except:
                try:
                    zeit = res2[0]['ts']
                    res2[0]['ts'] = zeit.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    print("Der Zeit-Header muss zeit, Zeit oder ts sein")

        # nur erste Zeile -> letzte Zeile in MySQL
        res3 = res2[0]
        return res3

    def select_lastvalueof(self, tabelle, spalte):
        """
        nimmt den letzten Wert der ausgewaehlte(n) Spalte(n) -> mit 2 Sekunden Verzoegerung!
        :param tabelle: 
        :param spalte: hier koennen mehrerer Spalten ausgewaehlt werden (z.B: 'id, zeit')
        :return: 
        """
        self.cur = self.db.cursor()
        self.cur.execute("SELECT SLEEP(2)")
        self.cur.execute("SELECT %s FROM %s ORDER BY id DESC LIMIT 1" % (spalte, tabelle))
        results = self.cur.fetchall()
        # nur Wert
        results2 = results[0][0]
        return results2

    def select_all(self, tabelle, order_by='id DESC', where=''):
        """
        alle Werte in ein list of dicts schreiben, damit kann besser gearbeitet werden
        where MUSS mit "Where " begonnen werden!
        :param tabelle:
        :param order_by:
        :param where: Where clause
        :return:
        """
        self.cur = self.db.cursor()
        # Headernamen entnehmen
        self.cur.execute("SHOW columns from %s ;" % tabelle)
        info = self.cur.fetchall()
        header = []
        for row in info:
            header.append(row[0])
        # print header

        # Werte entnehmen
        self.cur.execute("SELECT * FROM %s %s ORDER BY %s;" % (tabelle, where, order_by))
        results = self.cur.fetchall()

        # Dict mit Headernamen als keys
        res2 = []
        i_value = 0
        i_row = 0
        zeit_name = ''

        for row in results:
            # neue Zeile
            res2.append({})
            # restliche Zeile fuellen
            for value in row:
                res2[i_row].update({header[i_value]: value})
                i_value += 1

            # Zeitformat in Zeile anpassen (nach dem ersten Mal ueber zeit_name)
            try:
                zeit = res2[i_row][zeit_name]
                res2[i_row][zeit_name] = zeit.strftime('%Y-%m-%d %H:%M:%S')
            except:
                try:
                    zeit = res2[i_row]['zeit']
                    res2[i_row]['zeit'] = zeit.strftime('%Y-%m-%d %H:%M:%S')
                    zeit_name = 'zeit'
                except:
                    try:
                        zeit = res2[i_row]['Zeit']
                        res2[i_row]['Zeit'] = zeit.strftime('%Y-%m-%d %H:%M:%S')
                        zeit_name = 'Zeit'
                    except:
                        try:
                            zeit = res2[i_row]['ts']
                            res2[i_row]['ts'] = zeit.strftime('%Y-%m-%d %H:%M:%S')
                            zeit_name = 'ts'
                        except:
                            print("Der Zeit-Header muss zeit, Zeit oder ts sein")

            i_value = 0
            i_row += 1
        # print res2
        return res2

    def select_alerts(self, sql_results):
        """
        Stoermeldungen anzeigen, letzte zuerst
        """
        sql_res_ordered = []
        stoermeld_rev = []
        stoermeld = []
        row_old_vals = []
        # i muss mit genutzt werden
        i_row = 0
        i_row_val = 0
        try:
            sql_results[1]
        except:
            return 'Zu wenig Meldungen stehen zur Verfügung -> 2 müssen min. vorhanden sein'

        # Zeit-Name herausfinden
        try:
            dummy = sql_results[i_row]['zeit']
            zeit_name = 'zeit'
        except:
            try:
                dummy = sql_results[i_row]['Zeit']
                zeit_name = 'Zeit'
            except:
                try:
                    dummy = sql_results[i_row]['ts']
                    zeit_name = 'ts'
                except:
                    print("Der Zeit-Header muss zeit, Zeit oder ts sein")

        # id-Name herausfinden und id0 mit id1 vergleichen
        try:
            id0 = sql_results[i_row]['id']
            id_name = 'id'
        except:
            try:
                id0 = sql_results[i_row]['Id']
                id_name = 'Id'
            except:
                try:
                    id0 = sql_results[i_row]['ID']
                    id_name = 'ID'
                except:
                    print("Der ID-Header muss id, Id oder ID sein")

        id1 = sql_results[i_row + 1][id_name]

        # sql_results ordnen:
        # sql_results: neuste Meldung zuerst (DESC wurde genutzt)
        if (id0 > id1):
            # len beginnt mit 1, i_row beginnt mit 0 -> i=len-1
            i_row = len(sql_results) - 1
            # sql_res_ordered: neuste Meldung zum Schluss
            sql_res_ordered = reversed(sql_results)
        # sql_results: neuste Zeile zum Schluss (ASC wurde genutzt)
        elif (id0 < id1):
            i_row = 0
            # sql_res_ordered: neuste Meldung bleibt so
            sql_res_ordered = sql_results

        for row in sql_res_ordered:
            # zeit und id herausfiltern, damit sie spaeter nicht verglichen werden
            zeit = sql_results[i_row][zeit_name]
            # loesche zeit aus sql_results[i_row]
            sql_results[i_row].pop(zeit_name)
            # id
            id = sql_results[i_row][id_name]
            # loesche id aus sql_results[i_row]
            sql_results[i_row].pop(id_name)

            # list aus (bool) Werten von dict machen, row.values()=sql_results[i_row].values()
            row_vals = row.values()

            # nur die Elemente anzeigen, die einen geaenderten Stand haben,
            # der Erste Eintrag (= letzter Event) faellt weg weil row_old_vals noch leer ist
            if ((row_vals != row_old_vals) & (row_old_vals != [])):
                # row_anzeige = row_vals
                # row_old_anzeige = row_old_vals
                for row_val in row_vals:
                    # genauen Wert raussuchen
                    old_row_val = row_old_vals[i_row_val]
                    if row_val != old_row_val:
                        # # name = key -> wird nicht genutzt; Spalte i -> key davon -> auf Platz ii
                        # name = sql_results[i_row].keys()[i_row_val]

                        # GeKommen oder GeGangen zuordnen
                        if row_val == 1:
                            # key: Zeile i_meld, Spalte i_meld+anfang_Meldungen
                            row_val = 'K: %s' % (sql_results[i_row].keys()[i_row_val])
                        elif row_val == 0:
                            row_val = 'G: %s' % (sql_results[i_row].keys()[i_row_val])

                        stoermeld_rev.append(
                            {'zeit': zeit, 'st': row_val, 'id': id})
                    i_row_val += 1
            # zuruecksetzen auf anfang
            i_row_val = 0
            # bei i_row kommt es an ob sql_results
            if (id0 > id1):
                i_row -= 1
            elif (id0 < id1):
                i_row += 1
            # list in alte list schreiben, fuer Vergleich
            row_old_vals = row_vals

        # Zeilen umdrehen, damit neuste Meldungen zuerst
        for row in reversed(stoermeld_rev):
            stoermeld.append(row)
        # print stoermeld
        # print  stoermeld_rev
        return stoermeld

    def get_rownumber(self, tabelle):
        self.cur = self.db.cursor()
        self.cur.execute("SELECT COUNT(*) FROM %s" % tabelle)
        rownumber_list = self.cur.fetchall()
        rownumber = rownumber_list[0][0]
        return rownumber

    def write_to_csv(self, tabelle, location_and_name='file.csv'):
        """
        z.B: location_and_name = 'csv/myfile.csv'
        :param tabelle: 
        :param location_and_name: 
        :return: 
        """

        with open('%s' % (location_and_name), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=tabelle[0].keys())
            writer.writeheader()
            writer.writerows(tabelle)
        return None


    def write_to_csv(self, tabelle, location_and_name='file.csv'):
        """
        z.B: location_and_name = 'csv/myfile.csv'
        :param tabelle: 
        :param location_and_name: 
        :return: 
        """

        with open('%s' % (location_and_name), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=tabelle[0].keys())
            writer.writeheader()
            writer.writerows(tabelle)
        return None

if __name__ == "__main__":
    sql_object = SQLConnector()
    # sm_dict =  sql_object.query('SELECT P1_St FROM stoermeldungen')
    # print sm_dict
    tup_tup = sql_object.query('SELECT c_TOC_Vorlage FROM messwerte_30s ORDER BY id asc LIMIT 10;')
    list_tup1 = list(tup_tup)
    list_tup2 = list_tup1[1:]

    # ersten Wert in neuer Tabelle schreiben, weil dieser nicht geschrieben werden kann 
    # (differenz = list2[0]-list1[0] -> list2[0] ~ list1[-1] = NAN) 
    list3 = [list_tup1[0][0]]

    # laenge von l2 muss genommen werden, weil len(l2) < len(l1) -> ansonsten Error: index out of range
    for index in range(0, len(list_tup2)):
        dif = list_tup2[index][0] - list_tup1[index][0]
        if dif == 0:
            xl3_val = None
        else:
            xl3_val = list_tup2[index][0]
        list3.append(xl3_val)
    print list3
    print list_tup1



'''
# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

cur.execute("USE test") # select the database

print cur.execute("SHOW TABLES")    # execute 'SHOW TABLES' (but data is not returned)

#cur.execute("DROP TABLE IF EXISTS stoermeldungen")

#cur.execute("CREATE TABLE stoermeldungen( Zeit TIMESTAMP NOT NULL, Name VARCHAR(25), Stand VARCHAR(25) )")

cur.execute("INSERT INTO stoermeldungen(Zeit, Name, Stand ) VALUES(CURRENT_TIMESTAMP,'Pump1', 'gekomme')")

cur.execute("SELECT * FROM stoermeldungen")
results = cur.fetchall()
print results
for row in results:
    zeit = row[0]
    name= row[1]
    stand = row[2]

    # Now print fetched result
    print "zeit=%s,name=%s,stand=%s" % (zeit.strftime('%Y-%m-%d %H:%M:%S'), name, stand)

db.close()
'''
