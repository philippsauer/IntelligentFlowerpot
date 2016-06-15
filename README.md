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

## Steuerung der Funksteckdosen

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
