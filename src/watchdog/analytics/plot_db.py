
import numpy as np
import matplotlib.pyplot as pl
from  watchdog.utils.db_manager import *
import watchdog.utils.log
import StringIO
import urllib, base64
import os



PATH_LOG_FILE = '/tmp/plot_metadata.log'
log.init(PATH_LOG_FILE)
logger = log.create_logger('Metatada_Collector')

       
class Plot_Db():
    def __init__(self, title, x_label, y_label, field1, field2, method=""):
       if not 'occurrences' in method: 
        self.db_handler = DB_Manager(logger, False, database='file_metadata_db_pro', user='postgres', host="localhost", password='404300', port='5432')
        rows = self.db_handler.select_fields(field1, field2)
        array_1 = []
        array_2 = []
        field1_max = 0
        field1_min = 1000000000
        field2_max = 0 
        field2_min = 1000000000
        
        for field in rows:
            if field[0] > field1_max:
                field1_max = field[0]
            if field[0] < field1_min:
                field1_min = field[0]
         
            if field[1] > field2_max:
                field2_max = field[1]
            if field[1] < field2_min:
                field2_min = field[1]       
            array_1.append( field[0] )
            array_2.append( field[1] )
        
        pl.title(title)
        pl.xlabel(x_label)
        pl.ylabel(y_label) 
        pl.xlim(field1_min, field1_max)
        pl.ylim(field2_min, field2_max)
   
        pl.draw()
        fig = pl.figure(1)
        ax = fig.add_subplot(111)     
                
        ax.plot(array_1, array_2, 'D', color='red')

       # imgdata = StringIO.StringIO()
        #pl.savefig('%s.png' % filename)
        imgdata = StringIO.StringIO()
       # pl.savefig('%s.png' % filename)
        pl.savefig(imgdata, format='png')
   
        imgdata.seek(0)
        self.uri = 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))
        
       else:
          self.file_extensions_occurrences(title, x_label, y_label, field1, field2)
    
    def file_extensions_occurrences(self, title, x_label, y_label, field1, field2):
        self.db_handler = DB_Manager(logger, False, database='file_metadata_db', user='postgres', host="localhost", password='404300', port='5432')
        rows = self.db_handler.select_fields(field1, field2)
        
        json_dic = {}
        json_data = []
        for field in rows:
         filename=os.path.basename(str(field[0]))
         extension = ""
         if len(os.path.splitext(filename)) > 1 and os.path.splitext(filename)[1].__len__() > 0:
             extension = os.path.splitext(filename)[1]
             
             try:
                 if json_dic[extension] and field[1] > 0:
                     json_dic[extension] = json_dic[extension] + 1
             except Exception as e:
                 if field[1] > 0:
                     json_dic[extension]=1
        array_1 = []
        array_2 = []
        occur_max = 0
        occur_min = 1000000000
        for key, value in json_dic.iteritems():
            print 'File with extension %s quantity: %s ' % (key, value)
            if value > occur_max:
                occur_max = value
            if value < occur_min:
                occur_min = value

            array_1.append( key )
            array_2.append( value )
        
        
        ind = np.arange(len(array_1))
        width = 200
        
        fig, ax = pl.subplots()
        rects1 = ax.bar(ind+width, array_2, width, color='r' )
        
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.set_xticks(ind+width)
        
        n = len(array_1)  # New variable with the right length to calculate bar width
        width = 1. / (1 + n)
        ax.set_xticks(ind + n/2. * width)
                
        ax.set_xticklabels(array_1, rotation=90)
       
        pl.title(title)
        
        pl.ylabel(y_label) 
        pl.xlabel(x_label) 
        pl.xlim(0, len(array_1))
       # pl.ylim(field2_min, field2_max)
   
        pl.draw()

       # imgdata = StringIO.StringIO()
        #pl.savefig('%s.png' % filename)
        imgdata = StringIO.StringIO()
       # pl.savefig('%s.png' % filename)
        pl.savefig(imgdata, format='png')
   
        imgdata.seek(0)
        self.uri = 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))