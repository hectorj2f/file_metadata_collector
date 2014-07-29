
import numpy as np
import matplotlib.pyplot as pl
from  watchdog.utils.db_manager import *
import watchdog.utils.log
import StringIO
import urllib, base64

PATH_LOG_FILE = './plot_metadata.log'
log.init(PATH_LOG_FILE)
logger = log.create_logger('Metatada_Collector')

         
class Plot_File():
    def __init__(self, filename_path, title, x_label, y_label, filename):
        
        file = open( filename_path, "r" )
        array_1 = []
        array_2 = []
        field1_max = 0
        field1_min = 1000000000
        field2_max = 0 
        field2_min = 1000000000
        
        for line in file:
            parts = line.split(" ")
            field1 = float(parts[0])
            field2 = float(parts[1].replace("\n",""))
            if field1 > field1_max:
                field1_max = field1
            if field1 < field1_min:
                field1_min = field1
         
            if field2 > field2_max:
                field2_max = field2
            if field2 < field2_min:
                field2_min = field2
            
            array_1.append( field1 )
            array_2.append( field2 )
         
        file.close()
        
        
        pl.xlabel(x_label)
        pl.ylabel(y_label)
        pl.xlim(field1_min, field1_max)
        pl.ylim(field2_min, field2_max)
   
        pl.draw() 
        fig = pl.figure(1)
        ax = fig.add_subplot(111)     
                
        ax.plot(array_1, array_2, 'D', color='red')

        imgdata = StringIO.StringIO()
       # pl.savefig('%s.png' % filename)
        pl.savefig(imgdata, format='png')
   
        imgdata.seek(0)
        self.uri = 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))