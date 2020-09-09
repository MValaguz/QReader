# -*- coding: utf-8 -*-

"""
  ____                     _           
 / __ \                   | |          
| |  | |_ __ ___  __ _  __| | ___ _ __ 
| |  | | '__/ _ \/ _` |/ _` |/ _ \ '__|
| |__| | | |  __/ (_| | (_| |  __/ |   
 \___\_\_|  \___|\__,_|\__,_|\___|_|   
                                       
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con OpenCv e pyzbar
 Data prima ver: 22/10/2018
 Descrizione...: Il programma svolge la lettura dei codice a barra (deve essere presente una webcam) 
                 Come parametro d'ingresso (riga di comando) va passato l'indirizzo IP del server a cui collegarsi (es. qreader 10.0.4.11)

 Alcune note per la creazione dell'eseguibile che poi si può distribuire 
   - deve essere installato il pkg pyinstaller
   - per il funzionamento del programma sono ovviamente necessarie le librerie dei codici a barre, della gestione immagini, ecc. (v. sezione import)
   - eseguire il file QReader_Compile.bat che esegue tutto il lavoro (fare riferimento a questo file per i commenti e le particolarità del caso)
   - accertarsi che nella dir del sorgente di questo programma NON siano presenti directory dist e build    
"""

# Libreria per connessione webcam ed elaborazione immagini
import cv2
#import numpy as np
# Libreria per ricerca barcode nelle immagini
import pyzbar.pyzbar as pyzbar
# Libreria per collegamento a Oracle
import cx_Oracle
# Libreria per leggere informazioni di sistema (es. nome utente)
import getpass
# Libreria di collegamento alle API di windows (tramite le API posso agire per tenere la window sempre al top di tutte le altre)
import win32gui
import win32con
# Libreria di sistema
import sys

def decode(im): 
    """
       Cerca un codice a barre o qrcode nell'immagine contenuta nel parametro d'ingresso img
    """
    decodedObjects = pyzbar.decode(im)

    # Analizza i codici trovati e ne restituisce il primo
    for obj in decodedObjects:
        v_data = str(obj.data)
        v_data = v_data.replace("b'","")
        v_data = v_data.replace("'","")        
        return v_data

    # Se non trovato alcun codice restituisce none
    return None

def scrivi_in_ut_qreader(p_data):
    """
       Scrive quanto contenuto in p_data nella tabella oracle UT_QREADER
    """
    # Collegamento a Oracle
    try:
        # Stringa di connessione (l'indirizzo IP viene ricavato dal parametro d'ingresso e se non presente si collega al server di backup)
        if len(sys.argv) > 1:
            v_indirizzo_ip = sys.argv[1]
        else:
            v_indirizzo_ip = '10.0.4.11'            
        v_connect_string = 'SMILE/SMILE@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(COMMUNITY=TCP)(PROTOCOL=TCP)(Host=' + v_indirizzo_ip + ')(Port=1521)))(CONNECT_DATA=(SID=SMIG)))'        
        v_oracle_db = cx_Oracle.connect(v_connect_string)                
    except:
        return 'ko'
    
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
        
def main():        
    global v_data
    global v_exit   
    global v_found
    global v_x
    global v_y
    global v_oracle_problems
    
    # variabile globale che indica se si deve uscire dal programma 
    # (in realtà è possibile uscire dal programma anche tramite il tasto q)    
    v_exit  = False
    # variabile globale che indica se è stato trovato un codice a barre
    v_found = False    
    # variabile che riporta la posizione x per il disegno dei pittogrammi
    v_x = 1
    
    def controllo_eventi_del_mouse(event, x, y, flags, param):
        """
           Controllo eventi del mouse (da notare le variabili globali)
        """
        global v_data
        global v_exit
        global v_found
        global v_x
        global v_y
        global v_oracle_problems
        
        # è stato premuto il pulsante del mouse in rilascio..controllo dove...
        if event == cv2.EVENT_LBUTTONUP:                
            # è stato premuto il tasto No--> quindi vuol dire che la lettura non va considerata
            # e il programma ritorna a mettersi in scansione
            if x > v_x and x < (v_x + 70) and y > v_y and y < (v_y + 70):                  
                v_found = False            
            # è stato premuto il tasto Si--> quindi vuol dire che la lettura va considerata
            # valida e si deve uscire dal programma
            if x > v_x and x < (v_x + 70) and y > (v_y +80) and y < (v_y + 150):                  
                # Se è stato trovato un codice a barre, lo salvo nel DB
                if v_data is not None:                                
                    # Scrive il dato trovato nel DB di SMILE
                    if scrivi_in_ut_qreader(v_data)=='ko':
                        v_oracle_problems = True                        
                    # se il dato è stato scritto --> passo alla prossima lettura
                    else:
                        v_found = False            

    """
      Ciclo principale di apertura e lettura del flusso dati proveniente dalla webcam
    """        
    # Definizione di un font per la scrittura a video e relativo colore testo
    font = cv2.FONT_HERSHEY_SIMPLEX
    v_text_color = (0,0,0)
        
    # Attiva le webcam per la cattura del video        
    capture = cv2.VideoCapture(0)        
            
    # Se la webcam non è presente o non è riconosciuta...
    if not capture.isOpened():
        v_webcam = False
        #img = np.zeros((512,512,3), np.uint8)   questa istruzione crea un'immagine nera
        # Carico un'immagine di sfondo che riporta attenzione sul fatto che la webcam non è stata trovata
        img = cv2.imread('qreader.png')
    else:        
        v_webcam = True
        
    # Inizia il ciclo di lettura del flusso video proveniente dalla webcam o dall'immagine fissa            
    v_1a_volta = True
    v_oracle_problems = False
    v_pos_text_riga1 = (10, 10)            
    v_pos_text_riga2 = (10, 20)                            
    while True:       
        # Se premuto il tasto q oppure richiesto da apposito flag, esco dal form
        if (cv2.waitKey(1) & 0xFF in (ord('q'),ord('Q'))) or (v_exit):
            break   
        # Se premuta la X sulla window, esco dal form
        if cv2.getWindowProperty('QReader 1.0a', 0) < 0 and not v_1a_volta:
            break
                               
        # Se webcam è presente, leggo il prossimo frame che mi sta passando        
        if v_webcam:
            ret, img = capture.read()        
            v_win_size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                          int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))                        
            # Posizione del testo dei messaggi in fondo alla window
            v_pos_text_riga1 = (10, v_win_size[1]-50)            
            v_pos_text_riga2 = (10, v_win_size[1]-20)                        
            # definisco il rettagolo che contiene il mirino e quindi il crop dell'immagine che viene effettivamente scansionata
            v_larghezza_mirino = 300 
            v_altezza_mirino = 200
            v_mirino_top_left = ( int((v_win_size[0]-v_larghezza_mirino)/2), int((v_win_size[1]-v_altezza_mirino)/2) )                        
            #print(v_mirino_top_left[1])
            # taglio l'immagine della sola zona dove compare il mirino (la prima coppia è coordinate y mentre la seconda la x)            
            #print(str(v_mirino_top_left[1]) + ' ' + str(v_altezza_mirino) + ' ' + str(v_mirino_top_left[0]) + ' ' + str(v_larghezza_mirino))            
            # la ricerca dei codici a barre viene svolta se non trovato alcun codice dalla scansione precedente
            if not v_found:
                v_crop_img = img[v_mirino_top_left[1]:v_mirino_top_left[1]+v_altezza_mirino, v_mirino_top_left[0]:v_mirino_top_left[0]+v_larghezza_mirino]        
                # scrivo immagina ritagliata
                #cv2.imwrite('prova.png',v_crop_img)
                # converto il frame in bianco e nero per aumentarne il contrasto
                v_bianco_e_nero = cv2.cvtColor(v_crop_img, cv2.COLOR_BGR2GRAY)                    
                # eseguo l'analisi dell'immagine per cercare eventuali codice a barre, qrcode ecc
                # Tale procedura al momento restituisce solo il primo codice trovato ma in realtà
                # legge tutti i codici presenti
                v_data = decode(v_bianco_e_nero)
                # Se è stato trovato un codice a barre imposto l'apposita variabile che farà diventare il mirino verde
                # e visualizzerà i "pulsanti" per conferma
                if v_data is not None:                                                
                    v_found = True
                                                                                                                              
            # Disegna il mirino (rosso se non ha letto nulla)            
            if v_found:
                v_colore = (0,255,0)                
                cv2.putText(img,'Code trovato! ' + v_data, v_pos_text_riga2, font, 1, v_text_color, 1, cv2.LINE_AA)                       
                # Disegno i pittogrammi-pulsanti
                v_x = int(v_win_size[0]-75)            
                v_y = int((v_win_size[1]-150)/2)            
                cv2.rectangle(img, (v_x,v_y),    (v_x+70,v_y+70) , (0,0,255),2)                                  
                cv2.rectangle(img, (v_x,v_y+80), (v_x+70,v_y+150) ,(0,255,0),2)                      
                cv2.putText(img,'No', (v_x + 17,  v_y+43),  font, 1, (0,0,255), 2,cv2.LINE_AA)                                
                cv2.putText(img,'Si', (v_x + 17,  v_y+123), font, 1, (0,255,0), 2,cv2.LINE_AA)                                                            
            else:
                v_colore = (0,0,255)
                cv2.putText(img,'Scansione in corso....',v_pos_text_riga2, font, 1, v_text_color, 1,cv2.LINE_AA)                                
                
            cv2.rectangle(img,(v_mirino_top_left[0], v_mirino_top_left[1]), (v_mirino_top_left[0]+v_larghezza_mirino, v_mirino_top_left[1]+v_altezza_mirino),v_colore,2)      
            cv2.line(img, ( v_mirino_top_left[0] + int(v_larghezza_mirino/2), v_mirino_top_left[1] + int(v_altezza_mirino/2) - 20) , 
                          ( v_mirino_top_left[0] + int(v_larghezza_mirino/2), v_mirino_top_left[1] + int(v_altezza_mirino/2) + 20) ,
                          v_colore,
                          2)
            cv2.line(img, ( v_mirino_top_left[0] + int(v_larghezza_mirino/2) - 20, v_mirino_top_left[1] + int(v_altezza_mirino/2) ) , 
                          ( v_mirino_top_left[0] + int(v_larghezza_mirino/2) + 20, v_mirino_top_left[1] + int(v_altezza_mirino/2) ) ,
                          v_colore,
                          2)     
                                                                   
        # Emette la scritta se ci sono problemi di connessione a Oracle
        if v_oracle_problems:
            cv2.putText(img,'Problema connessione a SMILE!', v_pos_text_riga1, font, 1, (0,0,255), 1, cv2.LINE_AA)                          
        
        # Aggiorna lo schermo        
        cv2.imshow('QReader 1.0a', img)            
        cv2.moveWindow('QReader 1.0a', 620,110)                
        
        # Ricerco il puntatore della finestra 
        v_win_handle = win32gui.FindWindow(None, 'QReader 1.0a')
        # Se finestra trovata --> ne forzo la visualizzazione davanti a tutte le window aperte in questo momento 
        # in questo modo l'applicazione rimane sempre in primo piano
        if v_win_handle is not None:            
            win32gui.SetWindowPos(v_win_handle, win32con.HWND_TOPMOST, 0, 0, 0, 0,win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)            
        
        # associo la funzione che controlla gli eventi del mouse
        cv2.setMouseCallback('QReader 1.0a', controllo_eventi_del_mouse)    
        
        v_1a_volta = False
                                    
    # Chiudo la webcam e la window
    capture.release()
    cv2.destroyAllWindows()		
    
if __name__ == "__main__":    
    main()