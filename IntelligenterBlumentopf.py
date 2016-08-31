#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import threading
import time
import logging

from WebApp import WebApp
from TempHumiditySensor import TempHumiditySensor 
from RemotePowerSupplyController import RemotePowerSupplyController
from CSVData import CSVData

class IntelligenterBlumentopf(threading.Thread):

    # Constructor
    def __init__(self):
        
        # Get configuration
        self.disableLogging = config.general['disableLogging']
        self.checkSensorsInterval = config.sensors['checkSensorsInterval']
        self.criticalHumidity = config.sensors['criticalHumidity']
        self.criticalBrightness = config.sensors['criticalBrightness']
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
          
        self.humidity = 999
        self.temp = 999
        self.level = 999  
        self.brightness = 999  
        
if __name__ == '__main__':
    
    ib = IntelligenterBlumentopf()
    tempHumiditySensor = TempHumiditySensor()
    remotePowerSupplyController = RemotePowerSupplyController()
    csvData = CSVData()
    ib.logger.debug('IntelligenterBlumentopf is up and running...')  
    
    while True:
    
        #check sensors
        ib.humidity = tempHumiditySensor.getHumidity()
        ib.temp = tempHumiditySensor.getTemparature()
        ib.level = 999 #tbd 
        ib.brightness = 999 #tbd 
        
        #write data to file
        csvData.setData(ib.temp, ib.brightness, ib.humidity, ib.level)
        
        #do something
        if(int(ib.humidity) < ib.criticalHumidity):
            remotePowerSupplyController.runPump()
            
        if(int(ib.brightness) < ib.criticalBrightness):
            remotePowerSupplyController.lightOn()
                   
        #wait some Time        
        time.sleep(ib.checkSensorsInterval)
        
        
