# Intelligenter Blumentopf
University Project for Home Automation

## Steuerung der Funksteckdosen

Das An- bzw. Ausschalten der Funksteckdose A erfolgt über die Befehle

    sudo python transmit.py a_off
    sudo python transmit.py a_on

### Auslesen der Schaltcodes

Um die Funksteckdosen über das Transmitter-Modul steuern zu können mussten zuerst die Schaltcodes ermittelt werden. Dies geschah mit Hilfe des Receiver-Moduls und einer Anleitung von
http://www.instructables.com/id/Super-Simple-Raspberry-Pi-433MHz-Home-Automation/step2/Sniffing-the-handset-codes/

Je nach Anschluss des Moduls muss im Script `receive.py` der jeweilige GPIO-Pin angegeben werden, welcher die Daten empfängt:

    RECEIVE_PIN = 17

Um das Script `receive.py` ausführbar zu machen muss das Modul `matplotlib` installiert sein. Die Ausführung erfolgt über:

    sudo python receive.py

Anschließend lauscht das Script für 5 Sekunden auf eingehende Signale am angegebenen Pin. Die Signale werden über einen Plot ausgegeben:

![Schaltcodes](images/schaltCodes_4.PNG?raw=true "Schaltcodes")

Anschließend konnten die konkreten Schaltcodes vom Plot abgelesen werden. Im Fall unseres Projektes wird die Funksteckdose A durch wiederholtes Senden der folgenden Bitstrings an- bzw. ausgeschaltet:

    An:  '10010110101010101010101001100110010101010101100101101001010101011'
    Aus: '10010110101010101010101001100110010101010101100101101010010101011'

### Konfiguration des Transmitters
