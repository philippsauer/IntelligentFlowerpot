import vw
import time
import pigpio
import datetime

class LevelSensor

    if __name__ == "__main__":

        RX=27
        BPS=2000 
        pi = pigpio.pi()
        rx = vw.rx(pi, RX, BPS)

        start = time.time()

        print "Waiting for data on pin #{rx} at {bps} bps".format(rx=RX, bps=BPS)

        while True:
            if not rx.ready():
                time.sleep(0.1)
            else:
                msg = "".join(chr (c) for c in rx.get())

                print "Received distance: {dist}".format(dist=msg)
                if msg[len(msg)-1] == '$':
                    break

        rx.cancel()
        pi.stop()

        data = {}
        data['humidity']       = msg[0:4]
        data['temperature']    = msg[5:9]
        data['level']          = msg[10:len(msg)-1]
        data['timestamp']      = str(datetime.datetime.utcnow().isoformat())

        h   = float(msg[0:4]) / 100.0
        t   = float(msg[5:9]) / 100.0
        l   = msg[10:len(msg)-1]
        ts  = str(datetime.datetime.utcnow().isoformat())

        print h
        print t
        print d
        print ts

        print(data)

    def getLevel(self)
        return l

