import config
import logging
import time

from time import strftime

class CSVData():

    def __init__(self):
        
        # Load configuration values & initialize class variables
        self.disableLogging = config.general['disableLogging']
        self.csvFile = config.general['csvFile']
        self.logging_formatter = config.general['logging_formatter']

        # Set up logging       
        self.logger = logging.getLogger('Database')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(self.logging_formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.disabled = self.disableLogging
      
    def getData(self):
    #gibt aktuell nur den letzten Datensatz als Array zurueck und muss noch erweitert werden
       try:
          f = open(self.csvFile,"r")
          lines = f.readlines()
          f.close()          
          for line in lines:
             line = line.strip("\n") 
             line = line.split(",")                
             return line
                    
       except ValueError:
          self.logger.error( 'Could not read file: '+self.csvFile)

    
    def setData(self, temparatur, bodenfeuchtigkeit, luftfeuchtigkeit, fuellStand):
    #schreibt datensatz in erste zeile der datei
      
        try:
            f = open(self.csvFile,"r")
            lines = f.readlines()
            f.close()
            
            newData = str(strftime("%Y-%m-%d %H:%M:%S"))+','+str(temparatur)+','+str(bodenfeuchtigkeit)+','+str(luftfeuchtigkeit)+','+str(fuellStand)+'\n'
            
            f = open(self.csvFile,"w")
            f.write(newData)
            for line in lines:
                line = line.split(",")
                if line[0] != id:
                    line = ','.join(line)
                    f.write(line)          
            f.close()
            
        except ValueError:
            self.logger.error( 'Could not read file: '+self.actionDataSource)