rmdir dist\QReader /S /Q
rem COMPILAZIONE del programma qreader (il parametro --windowed non fa comparire la window console quando viene mandato in esecuzione
pyinstaller --windowed --icon=QReader.ico QReader.py
rem pyinstaller --icon=QReader.ico QReader.py
rem copia della libreria della lettura barcode (non la riconosce e non la copia automaticamente dalle liberie installate)
xcopy pyzbar dist\QReader\pyzbar /S /H /I
rem copia della libreria di connessione Oracle (essa è stata ricavata prendendola dal package di installazione oracle "instant client"
rem attenzione perché sul client di destinazione dovrà essere settata la variabile NLS_LANG
xcopy oraociei11.dll dist\QReader
rem copia dell'immagine di qreader (verrà utilizzata come sfondo nel caso non venga trovata una telecamera collegata)
xcopy QReader.png dist\QReader 
rmdir build /S /Q
pause
