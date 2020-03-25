# -*- coding: utf-8 -*-
# utf-8: für Umlaute+ß -> böse = u'böse'
from flask import Flask, render_template, jsonify, url_for, request
import json, datetime
# import time
# V3.00 Email-Benachrichtigung bei Sammelstoerung
import send_Email_V3_00

import sps_values, snap7
from  sql_connector import SQLConnector

app = Flask(__name__)


@app.route('/')
def anlage():
    sql_object = SQLConnector()
    sql_res1 = sql_object.select_newest_row('meldungen')
    sql_res2 = sql_object.select_newest_row('messwerte_1s')
    sql_results = sql_object.select_newest_row('stoermeldungen')
    # print sql_res1
    sql_results.update(sql_res1)
    sql_results.update(sql_res2)
    # Drehzahlen aus Tabelle sollwerte entnehmen
    n = sql_object.select_columns('sollwerte', 'n_R1, n_P2, n_P3', 'id DESC LIMIT 1')
    n_R1 = n[0][0]
    n_P2 = n[0][1]
    n_P3 = n[0][2]
    sql_results.update({'n_R1': n_R1, 'n_P2': n_P2, 'n_P3': n_P3})
    # print sql_results

    return render_template("anlage.html", sql_results=sql_results)


#Stoermeldungen
@app.route('/meldung')
def meldung():
    sql_object = SQLConnector()
    sql_results = sql_object.select_all('stoermeldungen')
    # print sql_results
    sql_alerts = sql_object.select_alerts(sql_results)
    # print sql_alerts
    return render_template("meldung.html", sql_results=sql_alerts)

# Diagramm Archiv
@app.route('/diagramm')
def diagramm():
    return render_template("diagramm.html")

# Daten werden extra von ajax gerufen (nicht ueber render_template, weil es nicht ueber html geht,
# sondern ueber jQuery bzw. Javascript)
@app.route('/diagramm_data')
def diagramm_data():
    sql_object = SQLConnector()
    """
    #mit Limit
    # 2880 *30s = 1d  /  480*3min = 1d  -> 2880+480 = 3360 = 1d
    rows = 2900 # 4000
    all_rows = sql_object.get_rownumber('messwerte_30s')
    # nur LIMIT machen wenn MySQL mehr als 3360 Datensaetze hat
    if (all_rows > rows):
        limit = all_rows - rows
    else:
        limit = 0
    # mit "limit OFFSET, limit" arbeiten weil amcharts "id ASC" (alte Werte zuerst) fuer Zeiten braucht
    sql_res2 = sql_object.select_all('messwerte_30s', 'id ASC LIMIT %s, %s' % (limit, rows))
    """
    #ohne Limit
    #nur alle zweiten Werte mit Where clause abfragen
    sql_res2 = sql_object.select_all('messwerte_30s', 'id ASC','WHERE id mod 2=0')

    #print sql_res2
    return jsonify(sql_res2)


# Echtzeit Diagramm
@app.route('/diagramm_echtzeit')
def diagramm_echtzeit():
    return render_template("diagramm_echtzeit.html")

@app.route('/diagramm_data_1s')
def diagramm_data_1s():
    """
    gibt Diagramm Daten zurueck fuer Echtzeit Diagramm
    Limit = 1h
    :return:
    """
    sql_object = SQLConnector()
    # 3600s = 1h
    rows = 3600
    all_rows = sql_object.get_rownumber('messwerte_1s')
    # NUR Limit machen wenn MySQL mehr als rows Datensaetze hat
    if (all_rows > rows):
        limit = all_rows - rows
    else:
        limit = 0
    #LIMIT mit zwei Zahlen (Offset, Limit) muss sein, weil ASC
    sql_res2 = sql_object.select_all('messwerte_1s', 'id ASC LIMIT %s, %s' %(limit, rows))
    # print sql_res2
    return jsonify(sql_res2)

@app.route('/new_diagramm_data')
def new_diagramm_data():
    """
    Aktualierte Daten fuer Echtzeit Diagramm
    :return:
    """
    sql_object = SQLConnector()
    sql_res2 = sql_object.select_newest_row('messwerte_1s')
    # print sql_res2
    return jsonify(sql_res2)

@app.route('/vorlage')
def vorlage():
    sql_object = SQLConnector()
    sql_results = sql_object.select_newest_row('sollwerte')
    #print sql_results

    Notfallvar_aktiv = sql_object.select_lastvalueof('befehle', 'Notfallvar_aktiv')
    # Beschickungsvar nicht in sql Datenbank
    Beschickungsvar = sps_values.get_int(104, 126)
    # Notfallvar_aktiv = sps_values.get_bool(101, 0, 3)

    # V2.00 Nachtrag: Truebung als 2. Vorlagebeschickungs-Ausloesung
    c_TOC_Trueb = sql_object.select_lastvalueof('befehle', 'c_TOC_Trueb')
    sql_results.update({'c_TOC_Trueb': c_TOC_Trueb})
    # print "Notfallvar_aktiv: ", Notfallvar_aktiv, "Beschickungsvar: ", Beschickungsvar, "c_TOC_Trueb: ", c_TOC_Trueb

    sql_results.update({'Notfallvar_aktiv': Notfallvar_aktiv})
    sql_results.update({'Beschickungsvar': Beschickungsvar})
    # print sql_results
    return render_template("vorlage.html", sql_results=sql_results)


@app.route('/ruhrwerk')
def ruhrwerk():
    sql_object = SQLConnector()
    sql_results = sql_object.select_newest_row('sollwerte')
    return render_template("ruhrwerk.html", sql_results=sql_results)


@app.route('/reaktor')
def reaktor():
    sql_object = SQLConnector()
    sql_results = sql_object.select_newest_row('sollwerte')
    # Radio button KV1_auto_aktiv initialisieren
    kv1_auto_aktiv = sql_object.select_lastvalueof('befehle', 'KV1_auto_aktiv')
    sql_results.update({'KV1_auto_aktiv': kv1_auto_aktiv})

    return render_template("reaktor.html", sql_results=sql_results)


@app.route('/not_abschaltung')
def not_abschaltung():
    sql_object = SQLConnector()
    sql_results = sql_object.select_newest_row('sollwerte')
    return render_template("not_abschaltung.html", sql_results=sql_results)

@app.route('/mysql')
def mysql():
    sql_object = SQLConnector()
    # aenderbare Werte in sql_results schreiben
    bf = sql_object.get_rownumber('befehle')
    meld = sql_object.get_rownumber('meldungen')
    st = sql_object.get_rownumber('stoermeldungen')

    sw = sql_object.get_rownumber('sollwerte')
    mw_1s = sql_object.get_rownumber('messwerte_1s')
    mw_30s = sql_object.get_rownumber('messwerte_30s')
    sql_results = {'tab-sollwerte': sw, 'tab-befehle': bf, 'tab-meldungen': meld, 'tab-messwerte_1s': mw_1s,
                   'tab-messwerte_30s': mw_30s, 'tab-stoermeldungen': st}
    return render_template("mysql.html", sql_results=sql_results)




"""
Werte Manipulatoren (siehe change_values.js und costant_request.js)
"""
@app.route('/sollwert')
def sollwert():
    value = request.args.get('value')
    id = request.args.get('id')
    # data = (DB, offset_byte, type)
    data = sps_values.get_Sollwerte_DB(id)
    # print data, id, value
    if data[2] == 'real':
        sps_values.set_real(data[0], data[1], value)
    elif data[2] == 'int':
        sps_values.set_int(data[0], data[1], value)
    elif data[2] == 'time':
        sps_values.set_time(data[0], data[1], value)
    elif data[2] == 'dint':
        sps_values.set_dint(data[0], data[1], value)

    # Aenderung ins WebUI laden
    sql_object = SQLConnector()
    try:
        received_value = sql_object.select_lastvalueof('sollwerte', id)
    except:
        # fuer Gas im Anlagebild (Zusatz)-> ist nicht in Tabelle 'sollwerte'
        received_value = sql_object.select_lastvalueof('messwerte_1s', id)
    # bei time im Zeitformat 'H:MM:SS' wiedergeben
    if data[2] == 'time':
        sec = received_value.seconds
        delta = datetime.timedelta(seconds=sec)
        received_value = str(delta)[-8:]  # z.B: " 1:01:01"
    sql_results = {id: received_value}
    print 'sollwert: ', sql_results
    return jsonify(sql_results)


@app.route('/input_table_rows')
def input_table_rows():
    value = request.args.get('value')
    id = request.args.get('id')
    name = sps_values.get_Tables(id)
    sql_object = SQLConnector()
    # value: aus unicode int machen
    # print type(value)
    sql_object.loesche_Zeilen_unterhalb(name, int(value))
    # Anzahl der Zeilen wieder zurueckgeben
    rownumber = sql_object.get_rownumber(name)
    print name, '-> neue Tabellenlänge: ', rownumber
    sql_results = {id: rownumber}
    return jsonify(sql_results)


#  Hier werden Daten von Javascript nur gesendet
@app.route('/radio_choice', methods=['POST'])
def radio_choice():
    json_dict = json.loads(request.form['json_dict'])
    name = json_dict['name']
    value = json_dict['value']
    if name == 'Auto':
        sps_values.set_bool(101, 0, 1, value)
    elif name == 'Beschickungsvar':
        sps_values.set_int(104, 126, value)
    elif name == 'Notfallvar_aktiv':
        sps_values.set_bool(101, 0, 3, value)
    elif name == 'KV1_auto_aktiv':
        sps_values.set_bool(101, 0, 0, value)
    # V2.00 Nachtrag: Truebung als 2. Vorlagebeschickungs-Ausloesung
    elif name == 'c_TOC_Trueb':
        sps_values.set_bool(101, 1, 3, value)
    print name, value
    return 'None'


@app.route('/change_bool')
def change_bool():
    value = request.args.get('value')
    id = request.args.get('id')
    data = sps_values.get_Befehle_DB(id)
    print id, value
    if value == 'change':
        old_val = sps_values.get_bool(data[0], data[1], data[2])
        new_val = not old_val
        sps_values.set_bool(data[0], data[1], data[2], new_val)
    #     fuer Testbit
    elif value == '1':
        try:
            sps_values.set_bool(data[0], data[1], data[2], 1)
            snap = 1
        except snap7.common.Snap7Exception as e:
            print "snap7 Fehler"
            snap = 0
            pass
    elif value == "0":
        sps_values.set_bool(data[0], data[1], data[2], 0)
    # Ausgabe an WebUI
    # fuer Testbit
    if id == 'Quittierung':
        sql_object = SQLConnector()
        test = sql_object.select_lastvalueof('befehle', 'Quittierung')
        #test = sps_values.get_bool(101, 0, 1) #-> Auto, nur fuer Testzwecke
        sql_res = {'Testbit': test, 'Snap7':snap}
        # print sql_res
        return jsonify(sql_res)
    else:
        return 'None' # alle ausser Testbit


# Hand-Auto Radio Button initialisieren
@app.route('/page_load')
def page_load():
    # bei jeder Seitenladung wird SQLConnector() erstellt -> zu langsam
    sql_object = SQLConnector()
    auto1 = sql_object.select_columns('befehle', 'Auto_Hand', 'id DESC LIMIT 1')
    auto = auto1[0][0]
    # auto = sps_values.get_bool(101, 0, 1) #ueber snap7
    sql_res = {'Auto_Hand':auto}
    """
    test = sql_object.select_columns('befehle', 'Quittierung', 'id DESC LIMIT 1')
    testbit = test[0][0]
    # testbit = sps_values.get_bool(101, 0, 1) #-> Auto, nur fuer Testzwecke
    sql_res = {'Testbit': testbit, 'Auto_Hand':auto}
    """
    # print sql_res
    return jsonify(sql_res)


@app.route('/anlage_const_req')
def anlage_const_req():
    sql_object = SQLConnector()
    # Messwerte
    sql_res1 = sql_object.select_newest_row('messwerte_1s')
    # Stoermeldungen
    sql_res2 = sql_object.select_newest_row('stoermeldungen')
    # Betriebsmeldungen
    sql_res3 = sql_object.select_newest_row('meldungen')
    return jsonify(sql_res1, sql_res2, sql_res3)

# V3.00 Email-Benachrichtigung bei Sammelstoerung
# 180417 Von six_hour zu one_hour_interval_req
@app.route('/one_hour_interval_req')
def one_hour_interval_req():
    last_value = request.args.get('last_value')

    sql_object = SQLConnector()
    sm_dict =  sql_object.select_newest_row('stoermeldungen')
    # Id und Zeit loeschen
    sm_dict.pop('Id')
    sm_dict.pop('zeit')
    sm_list = sm_dict.values()
    #Sammelstoerung, wenn nur eine Stoerung=1 dann SS = True
    SS = 1 in sm_list
    # print "last_value: ", last_value

    # last_value ist String!
    if SS & (last_value == "false"):        
        send_Email_V3_00.send_mail("Mindestens eine Stoerung in der Biogas Versuchsanlage in Baruth steht an!")
    else:
        pass
    # last_value aktualisieren
    last_value = SS

    return jsonify(last_value)
    

"""
@app.route('/testbit')
def testbit():
    sql_object = SQLConnector()
    # Testbit -> sehen ob PROGRAMM laeuft oder nicht (v.a. MySQL Verbindung)
    test = sql_object.select_columns('befehle', 'Quittierung', 'id DESC LIMIT 1')
    testbit = test[0][0]
    #testbit = sps_values.get_bool(101, 0, 1) #-> Auto, nur fuer Testzwecke
    sql_res = {'Testbit': testbit}
    # print sql_res
    return jsonify(sql_res)
"""
if __name__ == '__main__':
    app.run(debug=True)
    