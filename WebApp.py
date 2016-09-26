import time
import config
import logging
import threading
import csv
import os
from configparser import ConfigParser
from flask import Flask, url_for, render_template, request, jsonify #, Response
from flask.ext.classy import FlaskView, route

app = Flask(__name__)

class WebApp(FlaskView, threading.Thread):

    def __init__(self, ib):
        
        # Load configuration
        self.disableLogging = config.general['disableLogging']

        # Set up logging       
        self.logger = logging.getLogger('WebApp')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.disabled = self.disableLogging
        
        # run WebApp thread
        self.webAppThread = threading.Thread(target=self.runApp, args=())
        self.webAppThread.daemon = True
        self.webAppThread.start()
        
        # put object references into Flask config
        app.config['INTELLIGENTER_BLUMENTOPF'] = ib

    def runApp(self):
        host =  config.app['host']
        port =  config.app['port']
        app.debug = config.app['debug']  
        app.run(host=host, port=port)

def get_csv():
    csv_path = 'data.csv'
    csv_file = open(csv_path, 'rb')
    csv_obj = csv.reader(csv_file)
    csv_list = list(csv_obj)
    return csv_list

@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    template = 'head.html'
    object_list = get_csv()
    return render_template(template, object_list=object_list)

@app.route('/save')
def save():
    output = ""
    output = output+ render_template('header.html')
    #output = output+ '<div id="content">'
    output = output+"<h1>Saving new configuration...</h1>"  
    
    additionalLightingDuration = request.args.get('additionalLightingDuration')
    checkSensorsInterval = request.args.get('checkSensorsInterval')
    criticalHumidity = request.args.get('criticalHumidity')
    criticalBrightness = request.args.get('criticalBrightness')
        
    if additionalLightingDuration and checkSensorsInterval and criticalHumidity and criticalBrightness: 

        config = ConfigParser()
        config.read('userproperties.ini')
        config.set('IntelligenterBlumentopf', 'additionalLightingDuration', additionalLightingDuration)
        config.set('IntelligenterBlumentopf', 'checkSensorsInterval', checkSensorsInterval)
        config.set('IntelligenterBlumentopf', 'criticalHumidity', criticalHumidity)
        config.set('IntelligenterBlumentopf', 'criticalBrightness', criticalBrightness)
        with open('userproperties.ini', 'w') as configfile:
            config.write(configfile)
        
        output = output+"<p>Successful. Please reboot</p>"
        output = output+'<br><form method="get" action="/reboot"><button type="submit">Reboot!</button></form>'

    else:
        output = output+"<p>Failed: Configuration values are invalid.</p>"                 
    output = output+'</div></body></html>'
    return output 
    
@app.route('/reboot')
def reboot():
    os.system('reboot') 
    return
    
@app.route('/config')
def configure():
    output = ""
    output = output+render_template('header.html')
    output = output+render_template('settings.html')
    return output      