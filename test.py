#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import threading
import time
import logging
import datetime

from sunrise import sun 
from WebApp import WebApp
from TempHumiditySensor import TempHumiditySensor 
from RemotePowerSupplyController import RemotePowerSupplyController
from CSVData import CSVData
from GroundHumiditySensor import GroundHumiditySensor
from LightSensor import LightSensor

class IntelligenterBlumentopf(threading.Thread):

    # Constructor
    def __init__(self):
        
        # Get configuration
        self.disableLogging = config.general['disableLogging']
        self.checkSensorsInterval = config.sensors['checkSensorsInterval']
        self.criticalHumidity = config.sensors['criticalHumidity']
        self.criticalBrightness = config.sensors['criticalBrightness']
        self.coordsLong = config.general['coordsLong']
        self.coordsLat = config.general['coordsLat']
        self.additionalLightingDuration = config.general['additionalLightingDuration']
        self.initializeWifi = False

        
        # Start logging       
        self.logger = logging.getLogger('IntelligenterBlumentopf')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.disabled = self.disableLogging
      
        # Initialize WebApp
        self.webApp = WebApp(self) 
          
        self.humidity = 100
        self.temp = 100
        self.level = 100  
        self.brightness = 100  
        

        
if __name__ == '__main__':
    
    ib = IntelligenterBlumentopf()
    tempHumiditySensor = TempHumiditySensor()
    
    ib.logger.debug('IntelligenterBlumentopf is up and running...')  
    
    while True:

        ib.temp = int(tempHumiditySensor.getTemparature())


        
        
