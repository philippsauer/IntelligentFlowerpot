general = dict(
    disableLogging = False,
    csvFile = 'data.csv',
    logging_formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    pumpDuration = 5,
    rfidAttempts = 10,  
)

app = dict(
    host = '0.0.0.0',
    port = 80,
    debug = False,
)

sensors = dict(
    checkSensorsInterval = 6, #sollte groesser sein als pumpDuration
    transmitterGPIOPort = 18,
    brightnessGPIOPort = 17,
    tempAndHumidityGPIOPort = 4,
    tempAndHumiditySensorVersion = 11,
    LevelSensorGPIOPort = 27,
    LevelSensorBPS = 2000,
    criticalHumidity = 30, #welcher Wert macht hier Sinn?
    criticalBrightness = 10, #welcher Wert macht hier Sinn?
)
