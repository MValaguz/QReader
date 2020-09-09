# -*- coding: utf-8 -*-

# Libreria per collegamento a Oracle
import cx_Oracle
# Libreria per leggere informazioni di sistema (es. nome utente)
import getpass

def scrivi_in_ut_qreader(p_data):
    """
       Scrive quanto contenuto in p_data nella tabella oracle UT_QREADER
    """
    # Apertura del cursore e scrittura nella tabella di lavoro fatta con nome utente e il dato appena letto
    v_oracle_cursor = v_oracle_db.cursor()    
    # Controllo se record utente esiste già
    v_istruzione_sql = "select count(*) from UT_QREADER where USER_CO = '" + getpass.getuser() + "' and CODIC_CO = '" + p_data + "'"    
    v_oracle_cursor.execute(v_istruzione_sql)                        
    # Se esiste aggiorno
    if v_oracle_cursor.fetchone()[0] > 0:
        v_istruzione_sql = "update UT_QREADER set CODIC_CO = '"+p_data+"'"
    # altrimenti aggiungo    
    else:
        v_istruzione_sql = "insert into UT_QREADER values('"+getpass.getuser()+"','"+p_data+"')";    
    print(v_istruzione_sql)
    v_oracle_cursor.execute(v_istruzione_sql)                        
    # Committo
    v_oracle_db.commit()                                
    # Chiudo il cursore 
    v_oracle_cursor.close()    
            
print('Avvio test....')
print(cx_Oracle.clientversion())
connect_string = "SMILE/SMILE@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(""COMMUNITY=TCP)(PROTOCOL=TCP)(Host=10.0.4.11)(Port=1521)))(""CONNECT_DATA=(SID=SMIG)))"
print(connect_string)                         
v_oracle_db = cx_Oracle.connect(connect_string)        
scrivi_in_ut_qreader('test qreader')
print('Fine test premere invio per continuare...')
a=input()