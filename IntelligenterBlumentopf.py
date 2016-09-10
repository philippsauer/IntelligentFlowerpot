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
    remotePowerSupplyController = RemotePowerSupplyController()
    groundHumiditySensor = GroundHumiditySensor()
    lightSensor = LightSensor()
    sun = sun(lat=ib.coordsLat,long=ib.coordsLong)  
    csvData = CSVData()
    
    ib.logger.debug('IntelligenterBlumentopf is up and running...')  
    
    while True:
    
        #check sensors
        ib.humidity = groundHumiditySensor.getGroundHumidity()
        ib.temp = tempHumiditySensor.getTemparature()
        ib.level = 999 #tbd (Tim)
        ib.brightness = lightSensor.getBrightness()
        
        #take care of invalid sensor responses
        if(not isinstance(ib.humidity, int)):
            ib.humidity = 0 
        if(not isinstance(ib.temp, int)):
            ib.temp = 0 
        if(not isinstance(ib.level, int)):
            ib.level = 0 
        if(not isinstance(ib.brightness, int)):
            ib.brightness = 0 
                
        #write data to file
        csvData.setData(ib.temp, ib.brightness, ib.humidity, ib.level)
        
        #if necessary run pump
        if(int(ib.humidity) < ib.criticalHumidity):
            remotePowerSupplyController.runPump()
        
        # get sunset & sunrise 
        sunset = sun.sunset(when=datetime.datetime.now())
        sunrise = sun.sunrise(when=datetime.datetime.now())
        sunsetHourToTimeZone = int(sunset.hour) + 2
        sunset = sunset.replace(hour = sunsetHourToTimeZone)
        sunrise = sunrise.replace(hour = sunsetHourToTimeZone)
        now = datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second)
        
        if (now < sunrise):
            remotePowerSupplyController.lightOff() 
            
        if (now > sunrise and now < sunset):
        
            # enable lamp if its too dark
            if(int(ib.brightness) < ib.criticalBrightness):
                remotePowerSupplyController.lightOn()
            else:
                remotePowerSupplyController.lightOff() 
        
        # is it after sunset?
        if (now > sunset):
        
            now_sec = now.hour*60*60 + now.minute*60 + now.second
            sunset_sec = sunset.hour*60*60 + sunset.minute*60 + sunset.second
        
            # should the light shine?
            if( now_sec-sunset_sec < ib.additionalLightingDuration):
            
                # enable lamp if its too dark
                if(int(ib.brightness) < ib.criticalBrightness):
                    remotePowerSupplyController.lightOn()
                else:
                    remotePowerSupplyController.lightOff() 
           
            else:
                remotePowerSupplyController.lightOff()                          
            
        #wait some Time        
        time.sleep(ib.checkSensorsInterval)
        
        
