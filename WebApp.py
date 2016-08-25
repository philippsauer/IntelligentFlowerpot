import time
import config
import logging
import threading

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

def index(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'My Title'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    output = render_template('head.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)     
    output = output+'</div></body></html>'
    return output
