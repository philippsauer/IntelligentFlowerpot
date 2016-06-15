general = dict(
    disableLogging = False,
    logging_formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

app = dict(
    host = '0.0.0.0',
    port = 80,
    debug = False,
)

sensors = dict(
    transmitterGPIOPort = 18,
    brightnessGPIOPort = 17
)
