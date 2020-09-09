# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

def decode(im): 
    # Cerca i codici nell'immagine
    decodedObjects = pyzbar.decode(im)

    # Analizza i codici trovati e ne restituisce il primo
    for obj in decodedObjects:
        return obj.data

    # Se non trovato alcun codice restituisce none
    return None
    
def main():
    # Definizione di un font per la scrittura a video
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Attiva le webcam per la cattura del video
    capture = cv2.VideoCapture(0)    
            
    # Se la webcam non è presente o non è riconosciuta...
    if not capture.isOpened():
        v_webcam = False
        #img = np.zeros((512,512,3), np.uint8)   questa istruzione crea un'immagine nera
        # Carico un'immagine di sfondo
        img = cv2.imread('test codici a barre.png')
        # Scrivo il messaggio di errore
        cv2.putText(img,'Webcam non trovata!', (10,470), font, 1, (0,0,0), 1,cv2.LINE_AA)        
    else:        
        v_webcam = True
                            
    # Inizia il ciclo di lettura del flusso video proveniente dalla webcam o dall'immagine fissa
    y = 150
    while True:
        # Se premuto il tasto q esco dal form
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break   
        
        # Se webcam è presente, leggo il prossimo frame che mi sta passando
        if v_webcam:
            ret, img = capture.read()        
            # Emetto il testo indicante che deve essere letto un codice
            cv2.putText(img,'Read QRcode',(10,450), font, 1,(255,255,255),1,cv2.LINE_AA)                    
            # converto il frame in bianco e nero per aumentarne il contrasto
            v_bianco_e_nero = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)        
            # taglio l'immagine della sola zona dove compare il mirino (la prima coppia è coordinate y mentre la seconda la x)            
            v_crop_img = img[150:300, 150:350]        
            # eseguo l'analisi dell'immagine per cercare eventuali codice a barre, qrcode ecc
            # Tale procedura al momento restituisce solo il primo codice trovato ma in realtà
            # legge tutti i codici presenti
            v_data = decode(v_crop_img)
            # Se è stato trovato un codice a barre, lo visualizzo
            if v_data is not None:                
                cv2.putText(img,'Data found! ' + str(v_data), (10,470), font, 1,(255,255,255),1,cv2.LINE_AA)      
                              
        # Disegna il mirino (rosso se non ha letto nulla)
        cv2.rectangle(img,(150-1,150-1),(350+1,300+1),(0,0,255),1)      
        cv2.line(img,(150,y-1),(350,y-1),(0,0,0),1)
        cv2.line(img,(150,y),(350,y),(0,0,255),1)
        
        y += 1
        
        if y > 300:
            y = 150
            
        # Test per taglio dell'immagine
        #v_crop_img = img[150:300, 150:350]        
        #cv2.imwrite('prova.png',v_crop_img)
        #break            
                            
        # Aggiorna lo schermo        
        cv2.imshow('Barcode reader v1.1', img)         

    # Chiudo la webcam e la window
    capture.release()
    cv2.destroyAllWindows()		
    
if __name__ == "__main__":
    main()