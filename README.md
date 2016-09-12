# Intelligenter Blumentopf
University Project for Home Automation

## Ordnerstruktur

    /static/    <--- Enthält sämtliche statische Dateien (Images, CSS, Javascript etc.)
    /templates/ <--- Hier liegen sämltiche HTML-Dateien, welche von der Flask-Webapp verwendet werden
    .           <--- Python- und sonstige Programmfiles liegen direkt im Projektverzeichnis

## Die Web-Applikation
### Vorbereitung

Um den Webserver zu starten und die Web-App laufen zu lassen, muss zuerst das Micro-Framework "Flask" mit der Erweiterung "flask-classy" auf dem Raspberry installiert sein. Die installation kann mit folgenden Kommandos erfolgen:

    sudo pip install Flask
    sudo pip install flask_classy

### Start des Servers

Der Start des Servers erfolgt automatisch beim Start der Haupt-Anwendung:

    sudo python IntelligenterBlumentopf.py
    
Der Server ist nun über http://localhost/ (direkt von RaspberryPi), bzw. von anderen Netzwerkgeräten über folgende Adresse erreichbar: http://192.168.*.*/

### Lichtsteuerung

Programm zur Berechnung des Sonnenuntergangs als sunrise.py:

    http://michelanders.blogspot.de/2010/12/calulating-sunrise-and-sunset-in-python.html
    
### Steuerung der Funksteckdosen

Das An- bzw. Ausschalten der Funksteckdose A erfolgt über die Befehle

    sudo python transmit.py a_off
    sudo python transmit.py a_on

### Auslesen der Schaltcodes

Um die Funksteckdosen über das Transmitter-Modul steuern zu können mussten zuerst die Schaltcodes ermittelt werden. Dies geschah mit Hilfe des mitgelieferten Receiver-Moduls und auf Basis einer Anleitung auf Instructables.com: [Link](http://www.instructables.com/id/Super-Simple-Raspberry-Pi-433MHz-Home-Automation) 

Je nach Anschluss des Moduls muss im Script `receive.py` der jeweilige GPIO-Pin angegeben werden, welcher die Daten empfängt:

    RECEIVE_PIN = 17

Um das Script `receive.py` ausführbar zu machen muss das Modul `matplotlib` installiert sein. Die Ausführung erfolgt über:

    sudo python receive.py

Anschließend lauscht das Script für 5 Sekunden auf eingehende Signale am angegebenen Pin. Die Signale werden über einen Plot ausgegeben:

![Schaltcodes](static/schaltCodes_4.PNG?raw=true "Schaltcodes")

Anschließend konnten die konkreten Schaltcodes vom Plot abgelesen werden. Im Fall unseres Projektes wird die Funksteckdose A durch wiederholtes Senden der folgenden Bitstrings an- bzw. ausgeschaltet:

    An:  '10010110101010101010101001100110010101010101100101101001010101011'
    Aus: '10010110101010101010101001100110010101010101100101101010010101011'

### Konfiguration des Transmitters

Um die Funksteckdose erfolgreich anzusteuern, muss das Transmitter-Modul einen der oben genannten Bitstrings senden. Wichtig ist hierbei die korrekte Länge der Pausen. Aus den Plot des vorherigen Kapitels wurden daher folgende Zeiten abgelesen:

    short_pause = 0.00020
    short_delay = 0.00020
    long_pause = 0.00120
    repeat_delay = 0.00240
    repeat_pause = 0.01000
    
Weiterhin wichtig ist die Einstellung des korrekten Pins, an welchem das Datenkabel des Moduls angeschlossen wird:

    TRANSMIT_PIN = 18
    
Auf Basis dieser Zeiten und des vordefinierten Bitstrings wird das Signal der Funktfernbedienung imitiert. Da es im Programmverlauf zu Verzögerungen im Millisekundenbereich kommen kann (z.B. auf Grund hoher CPU Auslastung), besteht die Möglichkeit das der imitierte Schaltcode nicht korrekt erkannt wird. Die folgende Einstellung regelt deshalb wie oft die jeweilige Anweisung (on/off) abgesendet werden soll. Um sicher zu gehen wird ein Wert von 10 eingestellt:

    NUM_ATTEMPTS = 10

### Anschluss der 433MHz-Module

![Anschluss](static/schaltCodes_pins.jpg?raw=true "Anschluss")

### Helligkeitssensor

Ausführung erfolgt über folgenden Befehl:

    sudo python light.py
    
Ausgegeben wird entweder 0 (kein Licht), oder 1 (Licht) in einer Dauerschleife.

### Temparatur + Luftfeuchtigkeit (Modul DHT11)

Installation und einrichtung erfolgte in Anlehnung an:
https://jankarres.de/2015/02/raspberry-pi-mit-sensoren-und-gpio-arbeiten/

Adafruit (wird vorausgesetzt) gibt's hier: https://pypi.python.org/pypi/Adafruit_Python_DHT/1.1.2

Test Command (usage: sudo Adafruit_DHT [11|22|2302] GPIOpin#):
    example: sudo Adafruit_DHT 11 4

### Kommunikation zwischen Arduino (Sender) und Raspberry Pi (Empfänger)

#### Arduino Nano

- DHT22 Temperatur/Feuchtigkeitssensor
- HC-SR04 Ultraschallsensor
- 433 Mhz Sender

#### Verkabelung

- Data Temperatur D2
- Data Sender D7
- Pin Echo D11
- Pin Trigger D12

#### Libraries

- DHT
- VirtualWire
- NewPing

#### Raspberry

Zum empfangen der Sensordaten via 433 Mhz Pigpio installieren (http://abyz.co.uk/rpi/pigpio/index.html)

    wget abyz.co.uk/rpi/pigpio/pigpio.zip
    unzip pigpio.zip
    cd PIGPIO
    make -j4
    sudo make install
    
Pigpio daemon starten

    sudo pigpiod
    
Piscope zur Überprüfung des für den Empfänger gewählten GPIO zur Hilfe nehmen (http://abyz.co.uk/rpi/pigpio/piscope.html)

    wget abyz.co.uk/rpi/pigpio/piscope.tar
    tar xvf piscope.tar
    cd PISCOPE
    make hf
    make install

Piscope starten

    cd PISCOPE
    piscope
    
VirtualWire Klasse für Python importieren (http://abyz.co.uk/rpi/pigpio/code/vw.zip)

    
## Autostart des Raspberry Pi anpassen

### Rechte für Scripte setzen

Rechte für IntelligenterBlumentopf.py so setzen, dass das Script ausführbar ist

    sudo chmod +x /home/pi/pfad/IntelligenterBlumentopf.py

### Autostart anpassen

Pigpio Daemon und danach das Python Script automatisch nach dem Hochfahren starten lassen

Dafür die rc.local wie folgt öffnen

    sudo nano /etc/rc.local

und folgende Zeilen eintragen

    sudo pigpiod
    python /home/pi/pfad/IntelligenterBlumentopf.py &
    exit 0   

mit STRG+O & ENTER speichern und STRG+X schließen
