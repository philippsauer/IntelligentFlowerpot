#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import threading
import time
import logging

from WebApp import WebApp
from TempHumiditySensor import TempHumiditySensor 
from CSVData import CSVData

class IntelligenterBlumentopf(threading.Thread):

    # Constructor
    def __init__(self):
        
        # Get configuration
        self.disableLogging = config.general['disableLogging']
        self.checkSensorsInterval = config.sensors['checkSensorsInterval']
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
        
        
if __name__ == '__main__':
    
    ib = IntelligenterBlumentopf()
    tempHumiditySensor = TempHumiditySensor()
    csvData = CSVData()
    ib.logger.debug('IntelligenterBlumentopf is up and running...')  
    
    while True:
    
        #check sensors
        humidity = tempHumiditySensor.getTemparature()
        temp = tempHumiditySensor.getHumidity()
        
        #write data to file
        csvData.setData(temp, '(bodenfeuchtigkeit)', humidity, '(fuellstand)')
        
        #wait some Time        
        time.sleep(ib.checkSensorsInterval)
