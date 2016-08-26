import vw
import time
import pigpio
import datetime
import config
import logging

class LevelSensor():

   def __init__(self):
   
      # Load configuration values & initialize class variables
      self.disableLogging = config.general['disableLogging']
      self.pin = config.sensors['LevelSensorGPIOPort']
      self.bps = config.sensors['LevelSensorBPS']

      # Set up logging       
      self.logger = logging.getLogger('Database')
      self.logger.setLevel(logging.DEBUG)
      ch = logging.StreamHandler()
      ch.setLevel(logging.DEBUG)
      formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      ch.setFormatter(formatter)
      self.logger.addHandler(ch)
      self.logger.disabled = self.disableLogging
	  
	  # GPIO Connection
	  self.pi = pigpio.pi()
      self.rx = vw.rx(pi, self.pin, self.bps)
	  
	  #self.rx.cancel()
      #self.pi.stop()

    def getLevel(self):

        while True:
            if not self.rx.ready():
                time.sleep(0.1)
            else:
                msg = "".join(chr (c) for c in self.rx.get())
                self.logger.debug("Received distance: {dist}".format(dist=msg)
                if msg[len(msg)-1] == '$':
                    break

        data = {}
		data['level']          = msg[10:len(msg)-1]
		
        #data['humidity']      = msg[0:4]
        #data['temperature']   = msg[5:9]       
        #data['timestamp']     = str(datetime.datetime.utcnow().isoformat())

        level   = msg[10:len(msg)-1]
		#h   = float(msg[0:4]) / 100.0
        #t   = float(msg[5:9]) / 100.0
        #ts  = str(datetime.datetime.utcnow().isoformat())

        #print h
        #print t
        #print d
        #print ts
        #print(data)		
		return level

