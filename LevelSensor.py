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
		self.logger = logging.getLogger('LevelSensor')
		self.logger.setLevel(logging.DEBUG)
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		ch.setFormatter(formatter)
		self.logger.addHandler(ch)
		self.logger.disabled = self.disableLogging
        

	
    def getLevel(self):
    
        pi = pigpio.pi()
		self.rx = vw.rx(pi, self.pin, self.bps)
		while True:
		    if not self.rx.ready():
		        time.sleep(0.1)
		    else:
		        msg = "".join(chr (c) for c in self.rx.get())
		        #self.logger.debug("Received msg: " + msg  #Complete Message
		        self.logger.debug("Received distance: " + msg[10:len(msg)-1]  #only level
		        if msg[len(msg)-1] == '$':
		            break
		data = {}
		data['level']          = msg[10:len(msg)-1]
			
		level   = msg[10:len(msg)-1]
		self.rx.cancel()
		self.pi.stop()
		
		return level
