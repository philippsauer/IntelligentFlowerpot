general = dict(
    disableLogging = False,
    csvFile = 'data.csv',
    logging_formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    pumpDuration = 3, #sekunden
    additionalLightingDuration = 30800, #sekunden
    rfidAttempts = 10, 
    coordsLat = 50.56,
    coordsLong = 11.35,
)

app = dict(
    host = '0.0.0.0',
    port = 80,
    debug = False,
)

sensors = dict(
    checkSensorsInterval = 1, #sekunden
    test = 1,
    transmitterGPIOPort = 18,
    brightnessGPIOPort = 17,
    tempAndHumidityGPIOPort = 4,
    tempAndHumiditySensorVersion = 11,
    LevelSensorGPIOPort = 27,
    LevelSensorBPS = 2000,
    criticalHumidity = 30, #welcher Wert macht hier Sinn?
    criticalBrightness = 50, #welcher Wert macht hier Sinn?
)
