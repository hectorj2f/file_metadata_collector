
import numpy as np
import matplotlib.pyplot as pl
from  watchdog.utils.db_manager import *
import watchdog.utils.log
import StringIO
import urllib, base64
import os
import json

PATH_LOG_FILE = '/tmp/plot_metadata.log'
log.init(PATH_LOG_FILE)
logger = log.create_logger('Metatada_Collector')


class Plot_Data:
    
 def __init__(self):
     from  watchdog.utils.db_manager import DB_Manager
     self.db_handler = DB_Manager(logger, False, database='file_metadata_db_pro', user='postgres', host="localhost", password='404300', port='5432')
     #self.plot_db_results("title", "x_label", "y_label", "num_mods", "privacy")
     
 
 def plot_db_results(self, title, x_label, y_label, field1, field2):
     rows = self.db_handler.select_fields(field1, field2)
     
     array_1 = []
     array_2 = []
     for field in rows:
         array_1.append( field[0] )
         array_2.append( field[1] )
     
     # use pylab to plot x and y
     pl.plot(array_1, array_2, 'ro')
     # give plot a title
     pl.title(title)
     # make axis labels
     pl.xlabel(x_label)
     pl.ylabel(y_label)

     # set axis limits
  #   pl.xlim(0, 1090)
   #  pl.ylim(0, 8)
     # show the plot on the screen
     pl.figure()
     pl.draw()
 

 def print_flare_pdf_results(self, out_file_name, field1, field2):
     rows = self.db_handler.select_fields(field1, field2)
     print 'Printing flare pdf results in json format.'
     json_data = []
     
     out_file = open(out_file_name, 'w')
     for field in rows:
         filename=os.path.basename(str(field[0]))
         if filename.__len__() < 30 and ".pdf" in filename:
             json_data.append({'name':filename,'size':str(field[1])})
        # out_file.write("{\"name\": \""+os.path.basename(str(field[0]))+"\", \"size\":"+ str(field[1])+ '},\n')
     
     out_file.write(json.dumps({'name':"flare",'children':json_data}))
     out_file.close()
     print 'Terminated json pdf file generation.'
     
 def print_flare_results(self, out_file_name, field1, field2):
     rows = self.db_handler.select_fields(field1, field2)
     print 'Printing flare results in json format.'
     json_data = []
     
     out_file = open(out_file_name, 'w')
     for field in rows:
         filename=os.path.basename(str(field[0]))
         #if filename.__len__() < 20 and ".pdf" in filename:
         if field[1] > 0:
             json_data.append({'name':filename,'size':str(field[1])})
        # out_file.write("{\"name\": \""+os.path.basename(str(field[0]))+"\", \"size\":"+ str(field[1])+ '},\n')
     
     out_file.write(json.dumps({'name':"flare",'children':json_data}))
     out_file.close()
     print 'Terminated json file generation.'
     
 def print_flare_extensions_results(self, out_file_name, field1, field2):
     rows = self.db_handler.select_fields(field1, field2)
     print 'Printing flare extensions results in json format.'
     json_dic = {}
     json_data = []
     
     out_file = open(out_file_name, 'w')
     for field in rows:
         filename=os.path.basename(str(field[0]))
         extension = ""
         if len(os.path.splitext(filename)) > 1 and os.path.splitext(filename)[1].__len__() > 0 and field[1] > 1000:
             extension = os.path.splitext(filename)[1]
             print 'File with extension %s' % extension
             
             try:
                 if json_dic[extension] and field[1] > 0:
                     json_dic[extension].append({'name':filename,'size':str(field[1])})
             except Exception as e:
                 if field[1] > 0:
                     json_data_aux = []
                     json_data_aux.append({'name':filename,'size':str(field[1])})
                     json_dic[extension]=json_data_aux
         else:
              print 'Filename without extension %s' % filename
              '''
              try:
                 if json_dic['other'] and field[1] > 0:
                     json_dic['other'].append({'name':filename,'size':str(field[1])})
              except Exception as e:
                 if field[1] > 0:
                     json_data_aux = []
                     json_data_aux.append({'name':filename,'size':str(field[1])})
                     json_dic['other']=json_data_aux
        '''
     for key, value in json_dic.iteritems():
         json_data.append({'name':key,'children':value})
     
     out_file.write(json.dumps({'name':"flare",'children':json_data}))
     out_file.close()
     print 'Terminated json extensions file generation.'
 
 def print_extensions_accORmod(self, out_file_name, field1, field2, filtered=False):
     rows = self.db_handler.select_fields(field1, field2)
     print 'Printing flare extensions results in json format.'
     json_dic = {}
     json_data = []
     extensions_system = ['.dbx','.plist', '.db', '.localstorage','.sqlite', '.localstorage-journal','.log', '.db-wal', '.db-shm', '.lockN']
     
     out_file = open(out_file_name, 'w')
     for field in rows:
         filename=os.path.basename(str(field[0]))
         extension = ""
         if len(os.path.splitext(filename)) > 1 and os.path.splitext(filename)[1].__len__() > 0:
             extension = os.path.splitext(filename)[1]
             if not filtered:
                 try:
                     if json_dic[extension] and field[1] > 0:
                         json_dic[extension] = json_dic[extension] + field[1]
                 except Exception as e:
                     if field[1] > 0:
                         json_dic[extension]=field[1]
                     
             else:
                
                try:
                 if json_dic[extension] and field[1] > 0 and (extension not in extensions_system):
                     json_dic[extension] = json_dic[extension] + field[1]
                except Exception as e:
                 if field[1] > 0 and (extension not in extensions_system):
                     json_dic[extension]=field[1]

     from collections import OrderedDict
     json_dic = OrderedDict(sorted(json_dic.items(), reverse=True, key=lambda x: x[1]))

     for key, value in json_dic.iteritems():
         #print 'File with extension %s quantity: %s ' % (key, value)
            
         json_data.append({'name':key,'size':value})
     
     out_file.write(json.dumps({'name':"flare",'children':json_data}))
     out_file.close()

     print 'Terminated json extensions file generation.'
     
     
 def print_flare_extensions_occurrences(self, out_file_name, field1, field2):
     rows = self.db_handler.select_fields(field1, field2)
     print 'Printing flare extensions occurrences in json format.'
     json_dic = {}
     json_data = []
     out_file = open(out_file_name, 'w')
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

     from collections import OrderedDict
     json_dic = OrderedDict(sorted(json_dic.items(), reverse=True, key=lambda x: x[1]))

     for key, value in json_dic.iteritems():
         #print 'File with extension %s quantity: %s ' % (key, value)
            
         json_data.append({'name':key,'size':value})
     
     out_file.write(json.dumps({'name':"flare",'children':json_data}))
     out_file.close()
     print 'Terminated json occurrences file generation.'

     
 def print_flare_3c_results(self, out_file_name, field1, field2, field3):
     rows = self.db_handler.select_fields(field1, field2, field3)
     print 'Printing flare 3combo results in json format.'
     json_dic = {}
     json_data = []
     out_file = open(out_file_name, 'w')
     for field in rows:
         filename=os.path.basename(str(field[0]))
         try:
             if json_dic[str(field[2])] and field[1] > 0:
                 json_dic[str(field[2])].append({'name':filename,'size':str(field[1])})
         except Exception as e:
             if field[1] > 0:
                 json_data_aux = []
                 json_data_aux.append({'name':filename,'size':str(field[1])})
                 json_dic[str(field[2])]=json_data_aux
             
        
     for key, value in json_dic.iteritems():
         json_data.append({'name':key,'children':value})
     
     out_file.write(json.dumps({'name':"flare",'children':json_data}))
     out_file.close()
     print 'Terminated json 3combo file generation.'
     
 def print_codeFlower_folders(self, out_file_name, field1, field2, field3):
     rows = self.db_handler.select_fields(field1, field2, field3)
     print 'Printing print_codeFlower_folders results in json format.'
     json_num_files = {}
     json_data = []
     json_data_size_files = {}
     out_file = open(out_file_name, 'w')
     for field in rows:
         filename=str(field[0])
         home_path = filename.replace("/Users/hector/","")        
         home_path = home_path.split("/")[0]
         filename = os.path.basename(str(field[0]))
        
         try:
             if json_num_files[home_path] and field[1] > 0:
                 json_data_size_files[home_path] = json_data_size_files[home_path] + int(field[1]/1024)
                 json_num_files[home_path] = json_num_files[home_path] + 1
         except Exception as e:
             if field[1] > 0:
                 json_data_size_files[home_path] = int(field[1]/1024)
                 json_num_files[home_path]=1
             
        
     for key, value in json_num_files.iteritems():
         array = []
         iterator = 0
         num_files_reduced = (value*0.05)/100
         if num_files_reduced >= 1: 
           while (iterator < num_files_reduced):
             array.append({'name':key+str(iterator),'size':json_data_size_files[key], 'files':value})
             iterator+=1
         json_data.append({'name':key,'children':array})
     
     out_file.write(json.dumps({'name':"root",'children':json_data}))
     out_file.close()
     
     print 'Terminated print_codeFlower_folders file generation.'

     
 def plot_results(self, filename_path, title, x_label, y_label ):
     file = open( filename_path, "r" )
     array_1 = []
     array_2 = []
     for line in file:
         parts = line.split(" ")
         array_1.append( parts[0] )
         array_2.append( parts[1].replace("\n","") )
         
     file.close()
     
     # use pylab to plot x and y
     pl.plot(array_1, array_2, 'ro')
     # give plot a title
     pl.title(title)
     # make axis labels
     pl.xlabel(x_label)
     pl.ylabel(y_label)
     
     # set axis limits
  #   pl.xlim(0, 1090)
   #  pl.ylim(0, 8)
     # show the plot on the screen
     pl.figure()
     pl.draw()


if __name__ == '__main__':
    
  plotter = Plot_Data()
    
 # plotter.plot_results('/Users/hector/Dropbox/file_metadata_collector/dat/privacy_access_summary.dat', "Privacy VS Time since last access", "Privacy (octal)", "Time since last access (hrs)")
 # plotter.plot_results('/Users/hector/Dropbox/file_metadata_collector/dat/size_access_summary.dat', "Size VS Time since last access", "Size (mb)", "Time since last access (hrs)")
 # plotter.plot_results('/Users/hector/Dropbox/file_metadata_collector/dat/size_privacy_summary.dat', "Size VS Permissions ", "Size (mb)", "Permissions (octal)")
 
  #plotter.print_flare_pdf_results('./web/json_data/flare_test_pdf.json', "filename", "size")
#  plotter.print_flare_extensions_results('./web/json_data/flare_extensions.json', "filename", "size")
  #plotter.print_flare_extensions_occurrences('./web/json_data/flare_extensions_occur.json', "filename", "size")
 # plotter.print_extensions_accORmod('./web/json_data/flare_extensions_mods.json', "filename", "num_mods", True)
 # plotter.print_extensions_accORmod('./web/json_data/flare_extensions_acc.json', "filename", "num_acc", True)
 # plotter.print_codeFlower_folders('./web/json_data/file_in_home_folders.json', "filename", "size", "privacy") 
  plotter.print_codeFlower_folders('./web/json_data/data_node_tree.json', "filename", "size", "privacy") 
 
 # plotter.print_flare_results('./web/json_data/flare_test_num_mods.json', "filename", "num_mods")
  #plotter.print_flare_results('./web/json_data/flare_test_num_acc.json', "filename", "num_acc")
 # plotter.print_flare_3c_results('./web/json_data/flare_test_3c_num_acc.json', "filename", "num_acc", "privacy")
 # plotter.print_flare_3c_results('./web/json_data/flare_test_3c_num_mods.json', "filename", "num_mods", "privacy")
  #pl.show()
