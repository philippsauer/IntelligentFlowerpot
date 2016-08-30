import time
import sys
import RPi.GPIO as GPIO
import config
import logging

class RemotePowerSupplyController():

    def __init__(self):
   
        # Load configuration values & initialize class variables
        self.disableLogging = config.general['disableLogging']
        self.pumpDuration = config.general['pumpDuration']
        self.rfidAttempts = config.general['rfidAttempts']
        self.transmitterGPIOPort = config.sensors['transmitterGPIOPort']

		# Set up logging       
        self.logger = logging.getLogger('RemotePowerSupplyController')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.disabled = self.disableLogging
        
        self.no1_pump_on = '01011001011010100101011001011010010101010101101001101001010101010'
        self.no1_pump_off ='01011001011010100101011001011010010101010101101001101010010101010'
        self.no2_light_on = '01011001011010100101011001011010010101010101101001101001010101100'
        self.no2_light_off ='01011001011010100101011001011010010101010101101001101010010101100'
         
        self.short_pause = 0.00020
        self.short_delay = 0.00020
        self.long_pause = 0.00120
        self.repeat_delay = 0.00240
        self.repeat_pause = 0.01000

    def runPump(self):
        self.logger.debug('Running runPump()') 
        self.transmit_code(self.no1_pump_on);
        time.sleep(self.pumpDuration)
        self.transmit_code(self.no1_pump_off);
        
    def lightOn(self):
        self.transmit_code(self.no2_light_on);
        
    def lightOff(self):    
        self.transmit_code(self.no2_light_off);
    
    def transmit_code(self, code):

        '''Transmit a chosen code string using the GPIO transmitter'''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.transmitterGPIOPort, GPIO.OUT)
        for t in range(self.rfidAttempts):
            for i in code:
                if i == '1':
                    GPIO.output(self.transmitterGPIOPort, 1)
                    time.sleep(self.short_delay)
                    GPIO.output(self.transmitterGPIOPort, 0)
                    time.sleep(self.short_pause)
                elif i == '0':
                    GPIO.output(self.transmitterGPIOPort, 1)
                    time.sleep(self.short_delay)
                    GPIO.output(self.transmitterGPIOPort, 0)
                    time.sleep(self.long_pause)
                else:
                    continue
            
            #repeat pattern
            GPIO.output(self.transmitterGPIOPort, 0)
            time.sleep(self.repeat_pause)
            GPIO.output(self.transmitterGPIOPort, 1)
            time.sleep(self.short_delay)
            GPIO.output(self.transmitterGPIOPort, 0)
            time.sleep(self.repeat_delay)        
            
        GPIO.cleanup()
    