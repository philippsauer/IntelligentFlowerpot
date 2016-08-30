#!/usr/bin/python
import config
import subprocess
import logging

class TempHumiditySensor():

   def __init__(self):
   
      # Load configuration values & initialize class variables
      self.disableLogging = config.general['disableLogging']
      self.pin = config.sensors['tempAndHumidityGPIOPort']
      self.sensorVersion = config.sensors['tempAndHumiditySensorVersion']

      # Set up logging       
      self.logger = logging.getLogger('TempHumiditySensor')
      self.logger.setLevel(logging.DEBUG)
      ch = logging.StreamHandler()
      ch.setLevel(logging.DEBUG)
      formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      ch.setFormatter(formatter)
      self.logger.addHandler(ch)
      self.logger.disabled = self.disableLogging
   
   def getTemparature(self):
      proc = subprocess.Popen(["sudo Adafruit_DHT 11 4"], stdout=subprocess.PIPE, shell=True)
      (out, err) = proc.communicate()    
      outSplitted = out.split(" ")     
      temp = outSplitted[0][5:-3]  
      self.logger.debug('Current Temparature: '+ temp)      
      return temp

   def getHumidity(self):
      proc = subprocess.Popen(["sudo Adafruit_DHT 11 4"], stdout=subprocess.PIPE, shell=True)
      (out, err) = proc.communicate()    
      outSplitted = out.split(" ")     
      humidity = outSplitted[2][9:-4]  
      self.logger.debug('Current Humidity: '+ humidity)      
      return humidity