#!/usr/bin/python
import config
import subprocess
import logging
import spidev
import os
import time


class LightSensor():

   def __init__(self):
   
      # Load configuration values & initialize class variables
      self.disableLogging = config.general['disableLogging']

      # Set up logging       
      self.logger = logging.getLogger('LightSensor')
      self.logger.setLevel(logging.DEBUG)
      ch = logging.StreamHandler()
      ch.setLevel(logging.DEBUG)
      formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      ch.setFormatter(formatter)
      self.logger.addHandler(ch)
      self.logger.disabled = self.disableLogging
      self.spi = spidev.SpiDev()

   def getBrightness(self):
   
      delay = 1.0
      self.spi.open(0,1)
      val = self.readChannel(0)
      self.logger.debug('Current Brightness: '+ str(100*(1023-val)/1023))
      if (val != 0):
         return 100*(1023-val)/1023
    
   def readChannel(self, channel):
      val = self.spi.xfer2([1,(8+channel)<<4,0])
      data = ((val[1]&3) << 8) + val[2]
      return data     
      
   def is_number(self, s):
      try:
         float(s)
         return True
      except ValueError:
         return False
