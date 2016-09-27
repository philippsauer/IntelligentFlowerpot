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
from LevelSensor import LevelSensor 
from configparser import ConfigParser

class IntelligenterBlumentopf(threading.Thread):

    # Constructor
    def __init__(self):
        
        # Get configuration
        self.disableLogging = config.general['disableLogging']
        self.coordsLong = config.general['coordsLong']
        self.coordsLat = config.general['coordsLat']
        self.initializeWifi = False
        
        # Get user configuration
        self.userConfiguration = ConfigParser()
        self.userConfiguration.read('userproperties.ini')
        
        self.criticalHumidity = self.userConfiguration.getint('IntelligenterBlumentopf', 'criticalHumidity')       
        if(not isinstance(self.criticalHumidity, int)):
            self.criticalHumidity = config.sensors['criticalHumidity']
            
        self.criticalBrightness = self.userConfiguration.getint('IntelligenterBlumentopf', 'criticalBrightness')       
        if(not isinstance(self.criticalBrightness, int)):
            self.criticalBrightness = config.sensors['criticalBrightness']
        
        self.checkSensorsInterval = self.userConfiguration.getint('IntelligenterBlumentopf', 'checkSensorsInterval')       
        if(not isinstance(self.checkSensorsInterval, int)):
            self.checkSensorsInterval = config.sensors['checkSensorsInterval']
            
        self.additionalLightingDuration = self.userConfiguration.getint('IntelligenterBlumentopf', 'additionalLightingDuration')       
        if(not isinstance(self.additionalLightingDuration, int)):
            self.additionalLightingDuration = config.general['additionalLightingDuration']            
                
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
    levelSensor = LevelSensor()
    sun = sun(lat=ib.coordsLat,long=ib.coordsLong)  
    csvData = CSVData()
    
    ib.logger.debug('IntelligenterBlumentopf is up and running...') 
    ib.logger.debug('self.criticalHumidity:'+str(ib.criticalHumidity))  
    ib.logger.debug('self.criticalBrightness:'+str(ib.criticalBrightness)) 
    ib.logger.debug('self.checkSensorsInterval:'+str(ib.checkSensorsInterval)) 
    ib.logger.debug('self.additionalLightingDuration:'+str(ib.additionalLightingDuration)) 
  
    
    
    
    
    while True:
    
        #check sensors
        ib.humidity = groundHumiditySensor.getGroundHumidity()
        ib.temp = int(tempHumiditySensor.getTemparature())
        ib.level = levelSensor.getLevel()   
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
        sunriseHourToTimeZone = int(sunrise.hour) + 2
        sunset = sunset.replace(hour = sunsetHourToTimeZone)
        sunrise = sunrise.replace(hour = sunriseHourToTimeZone)
        now = datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second)
        
        ib.logger.debug('Now: '+ unicode(now))  
        ib.logger.debug('Sunrise: '+ unicode(sunrise))  
        ib.logger.debug('Sunset: '+ unicode(sunset))  
        
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
        
        
