import time
import sys
import RPi.GPIO as GPIO

a_on =  '10010110101010101010101001100110010101010101100101101001010101011'
a_off = '10010110101010101010101001100110010101010101100101101010010101011'
 
short_pause = 0.00020
short_delay = 0.00020
long_pause = 0.00120
repeat_delay = 0.00240
repeat_pause = 0.01000

NUM_ATTEMPTS = 10
TRANSMIT_PIN = 18

def transmit_code(code):

    '''Transmit a chosen code string using the GPIO transmitter'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(NUM_ATTEMPTS):
        for i in code:
            if i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(short_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(short_pause)
            elif i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(short_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(long_pause)
            else:
                continue
        
        #repeat pattern
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(repeat_pause)
        GPIO.output(TRANSMIT_PIN, 1)
        time.sleep(short_delay)
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(repeat_delay)        
        
    GPIO.cleanup()

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')

