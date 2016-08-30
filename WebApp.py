import time
import config
import logging
import threading
#import csv

from flask import Flask, url_for, render_template, request, jsonify
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

        
@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    template = 'head.html'
    return render_template(template)

@app.route("/data.csv")
def data():
    output = "data.csv"
#    csv_path = './static/data.csv'
#    csv_file = open(csv_path, 'rb')
#    csv_obj = csv.DictReader(csv_file)
#    output = csv_obj
    return output