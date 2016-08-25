general = dict(
    disableLogging = False,
    csvFile = 'data.csv',
    logging_formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   
)

app = dict(
    host = '0.0.0.0',
    port = 80,
    debug = False,
)

sensors = dict(
    checkSensorsInterval = 1,
    transmitterGPIOPort = 18,
    brightnessGPIOPort = 17,
    tempAndHumidityGPIOPort = 4,
    tempAndHumiditySensorVersion = 11,
)
