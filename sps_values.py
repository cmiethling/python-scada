import snap7
import datetime
import time

plc = snap7.client.Client()
plc.connect('192.168.3.222', 0, 1)

# while plc.get_connected() == 0:
#     try:
#         plc.connect('192.168.3.222', 0, 1) #('IP-address', rack, slot)
#         print('not connected')
#         time.sleep(1)
#     except snap7.common.Snap7Exception as e:
#         pass
# print 'connected!'



def set_bool(DB, offset_Byte, offset_Bit, Wert):
    wert_b = int(Wert)
    reading = plc.db_read(DB, offset_Byte, 1)  #   db_read(self, db_number, start, size):
    snap7.util.set_bool(reading, 0, offset_Bit, wert_b)  #  (_bytearray, byte_index, bool_index, value):
    plc.db_write(DB, offset_Byte, reading)  #  db_number, start, data):
    return None

def set_int(DB, offset_Byte, Wert):
    reading = plc.db_read(DB, offset_Byte, 2)  # db_read(self, db_number, start, size):
    snap7.util.set_int(reading, 0, Wert)  # (_bytearray, byte_index, _int)
    plc.db_write(DB, offset_Byte, reading)  # db_number, start, data):
    return 'success'

def set_real(DB, offset_Byte, Wert):
    reading = plc.db_read(DB, offset_Byte, 4)  # db_read(self, db_number, start, size):
    snap7.util.set_real(reading, 0, Wert)  # (_bytearray, byte_index, real)
    plc.db_write(DB, offset_Byte, reading)  # db_number, start, data):
    return 'success'


def set_dint(DB, offset_Byte, Wert):# 0...2147483647
    reading = plc.db_read(DB, offset_Byte, 4)  # db_read(self, db_number, start, size):
    snap7.util.set_dword(reading, 0, Wert)  # (_bytearray, byte_index, dword)
    plc.db_write(DB, offset_Byte, reading)  # db_number, start, data):
    return 'success'

def set_time(DB, offset_Byte, zeit):
    """
    Zeitformat 'HH:MM:SS' zB. 3 Minuten: 00:03 -> ohne Sekunden
    """
    # sec = 3600*t[0]+60*t[1]+1*t[2]
    sec = sum(x * int(t) for x, t in zip([3600, 60, 1], zeit.split(":")))
    reading = plc.db_read(DB, offset_Byte, 4)  # db_read(self, db_number, start, size):
    snap7.util.set_dword(reading, 0, sec*1000)  # (_bytearray, byte_index, dword in ms)
    plc.db_write(DB, offset_Byte, reading)  # db_number, start, data):
    return None

def set_string(DB, offset_Byte, Wert):
    reading = plc.db_read(DB, offset_Byte, 256)  # db_read(self, db_number, start, size):
    snap7.util.set_string(reading, 0, Wert, 256)  # (_bytearray, byte_index, value, max_size)
    plc.db_write(DB, offset_Byte, reading)  # db_number, start, data):
    return None



"""
alle getter
"""
def get_bool(DB, offset_Byte, offset_Bit):
    reading = plc.db_read(DB, offset_Byte, 1)  #   db_read(self, db_number, start, size):
    out = snap7.util.get_bool(reading, 0, offset_Bit)  #  (_bytearray, byte_index, bool_index):
    out2 = int(out) # mach 0 oder 1 draus (ist auch bei sps bzw. MySQL so)
    return out2

def get_int(DB, offset_Byte):
    reading = plc.db_read(DB, offset_Byte, 2)  # db_read(self, db_number, start, size):
    out = snap7.util.get_int(reading, 0)  # (_bytearray, byte_index)
    return out

def get_real(DB, offset_Byte):
    reading = plc.db_read(DB, offset_Byte, 4)  # db_read(self, db_number, start, size):
    out = snap7.util.get_real(reading, 0)  # (_bytearray, byte_index, real)
    return out


def get_dint(DB, offset_Byte):# 0...2147483647
    reading = plc.db_read(DB, offset_Byte, 4)  # db_read(self, db_number, start, size):
    out = snap7.util.get_dword(reading, 0)  # (_bytearray, byte_index)
    return out

def get_time(DB, offset_Byte):
    """
    Zeitformat 'H:MM:SS'
    """
    # sec = 3600*t[0]+60*t[1]+1*t[2]
    #sec = sum(x * int(t) for x, t in zip([3600, 60, 1], zeit.split(":")))
    reading = plc.db_read(DB, offset_Byte, 4)  # db_read(self, db_number, start, size):
    millisec = snap7.util.get_dword(reading, 0)  # (_bytearray, byte_index)

    delta = datetime.timedelta(seconds = millisec/1000)
    delta_str = str(delta)[-8:]  # z.B: " 1:01:01"
    # hours, minutes, seconds = [int(val) for val in delta_str.split(":", 3)]
    # weeks = delta.days // 7
    # days = delta.days % 7
    return delta_str

def get_string(DB, offset_Byte):
    reading = plc.db_read(DB, offset_Byte, 256)  # db_read(self, db_number, start, size):
    out = snap7.util.get_string(reading, 0, 256)  # (_bytearray, byte_index, value, max_size)
    return out


def get_Sollwerte_DB(x):
    """
    return: List: (DB, offset_byte, type (real, int, time or dint))
    """
    return {
        # Parameter Vorlage
        'c_TOC_krit':       (104, 72, 'real'),
        'c_TOC_max':        (104, 76, 'real'),
        'c_TOC_Vorlage':    (104, 80, 'real'),
        'c_TOC_Vorlage_max':(104, 84, 'real'),
        'F_abm':            (104, 88, 'real'),
        'T_F_abm':          (104, 92, 'int'),
        'Delta_T_Weiche':   (104, 94, 'int'),
        'T_P1_max':         (104, 96, 'int'),
        'T_P2_max':         (104, 98, 'int'),
        'T_P3_max':         (104, 100, 'int'),
        'VN_min':           (104, 102,'real'),
        'VN_max':           (104, 106, 'real'),
        'Delta_VN_1':       (104, 110, 'real'),
        'Delta_VN_2':       (104, 114, 'real'),
        'Delta_VN_3':       (104, 118, 'real'),
        'Delta_VN_4':       (104, 122, 'real'),
        # nicht in Tabelle Sollwerte
        # 'Beschickungsvar':  (104, 126, 'int'),

        # Parameter Ruehrwerk
        'T_R1_an':          (104, 128, 'int'),
        'T_R1_aus':         (104, 130, 'int'),
        'n_R1':             (104, 132, 'real'),

        # Parameter Reaktor
        'V2_krit':          (104, 158, 'real'),
        'T_P2_max1':        (104, 136, 'int'),
        'n_P2':             (104, 138, 'real'),
        'theta_MH_min':     (104, 142, 'real'),
        'theta_MH_max':     (104, 146, 'real'),
        'T_P3_an':          (104, 150, 'int'),
        'T_P3_aus':         (104, 152, 'int'),
        'n_P3':             (104, 154, 'real'),
        'V_RBes1':          (104, 202, 'real'),
        'V_RBes2':          (104, 206, 'real'),
        'V_RBes3':          (104, 210, 'real'),
        'V_RBes4':          (104, 214, 'real'),
        'V_RBes5':          (104, 218, 'real'),
        'V_RBes6':          (104, 222, 'real'),
        'V_RBes7':          (104, 226, 'real'),
        'V_RBes8':          (104, 230, 'real'),
        'V_RBes9':          (104, 234, 'real'),
        'V_RBes10':         (104, 238, 'real'),

        'Startzeit1':       (104, 162, 'time'),
        'Startzeit2':       (104, 166, 'time'),
        'Startzeit3':       (104, 170, 'time'),
        'Startzeit4':       (104, 174, 'time'),
        'Startzeit5':       (104, 178, 'time'),
        'Startzeit6':       (104, 182, 'time'),
        'Startzeit7':       (104, 186, 'time'),
        'Startzeit8':       (104, 190, 'time'),
        'Startzeit9':       (104, 194, 'time'),
        'Startzeit10':      (104, 198, 'time'),

        # Notabschaltung
        'V2_Not':           (104, 242, 'real'),

        # V1.20 Nachtrag: einstellbare Zeit bevor P2 angeht (fuer P3)
        'T_P2_bevor_ein':   (104, 246, 'int'),

        #Gas fuer Anlage Bild
        'Gas':              (105, 0, 'dint'),

        # V2.00 Nachtrag: Truebung als 2. Vorlagebeschickungs-Ausloesung
        'Trueb_krit':       (104, 248, 'real'),
        'Trueb_max':        (104, 252, 'real'),
    }.get(x, 'Sollwert nicht geschrieben')


def get_Messwerte_DB(x):
    """
    return: List: (DB, offset_byte, type (real, int, time or dint))
    """
    return {
        'MID':              (103, 0, 'real'),
        'pH1':              (103, 4, 'real'),
        'LF':               (103, 8, 'real'),
        'TOC':              (103, 12, 'real'),
        'N_ges':            (103, 16, 'real'),
        'Truebung':         (103, 20, 'real'),
        'Redox':            (103, 24, 'real'),
        'Vega1':            (103, 28, 'real'),
        'pH2':              (103, 32, 'real'),
        'Temp':             (103, 36, 'real'),
        'pH3':              (103, 40, 'real'),
        'Vega2':            (103, 44, 'real'),
        'c_TOC_Vorlage':    (103, 48, 'real'),

        'Gas':              (105, 0, 'dint'),
        'P1_EIN':           (102, 2, 5),
        'P2_EIN':           (102, 2, 6),

        #V1.20 Nachtrag: Vega1_l
        'Vega1_l':          (103, 56, 'real'),

        # V2.01 Nachtrag: Temperatur Rechen
        'Temp_Re':          (103, 60, 'real'),
    }.get(x, 'Messwert nicht geschrieben')



def get_Befehle_DB(x):
    """
    return: List: (DB, offset_byte, bit)
    """
    return {
        'KV1_auto_aktiv':       (101, 0, 0),
        'Auto_Hand':            (101, 0, 1),
        'Quittierung':          (101, 0, 2),
        'Notfallvar_aktiv':     (101, 0, 3),
        'H_P1':                 (101, 0, 4),
        'H_P2':                 (101, 0, 5),
        'H_P3':                 (101, 0, 6),
        'H_KV1':                (101, 0, 7),
        'H_R1':                 (101, 1, 0),
        'H_Heiz':               (101, 1, 1),
        'P3_end_man_interrupt': (101, 1, 2),

        # V2.00 Nachtrag: Truebung als 2. Vorlagebeschickungs-Ausloesung
        'c_TOC_Trueb':          (101, 1, 3),   #0=c_TOC, 1=Truebung
    }.get(x, 'Befehl nicht geschrieben')


def get_Meldungen_DB(x):
    """
    return: List: (DB, offset_byte, bit)
    """
    return {
        'P1_EIN':           (102, 2, 5),
        'P2_EIN':           (102, 2, 6),
        'P3_EIN':           (102, 2, 7),
        'KV1_offen':        (102, 4, 1),
        'R1_EIN':           (102, 3, 1),
        'Heiz_EIN':         (102, 3, 0),
    }.get(x, 'Meldung nicht geschrieben')

def get_Tables(x):
    return {
        'tab-befehle':          ('befehle'),
        'tab-meldungen':        ('meldungen'),
        'tab-stoermeldungen':   ('stoermeldungen'),
        'tab-messwerte_1s':     ('messwerte_1s'),
        'tab-messwerte_30s':    ('messwerte_30s'),
        'tab-sollwerte':        ('sollwerte'),
    }.get(x, 'Tabelle nicht vorhanden')
