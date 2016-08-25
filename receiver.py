import vw
import time
import pigpio


if __name__ == "__main__":

    RX=27
    BPS=2000 
    pi = pigpio.pi()
    rx = vw.rx(pi, RX, BPS)

    c = chr
    d = chr
    
    start = time.time()

    print("Auf Daten warten")
    while (time.time()-start) < 100:      
        while rx.ready():
            #print("".join(chr (c) for c in rx.get()))
            print(rx.get())

        
    rx.cancel()
    pi.stop()
