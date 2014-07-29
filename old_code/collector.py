import grp
import pwd
import os, sys, time
from stat import *
from multiprocessing.pool import ThreadPool
from threading import Thread
from db_manager import *
import datetime
import log 
#self.pool_predictors.apply_async()

import numpy as np
import pylab as pl


PATH_LOG_FILE = './metadata_collector.log'
log.init(PATH_LOG_FILE)
logger = log.create_logger('Metatada_Collector')

access_list = []
privacy_list = []
crea_mod_list = []
modification_list = []
size_list = []
group_files = {}
user_files = {}

class File_Inspector:

 def __init__(self):
    
    self.db_handler = DB_Manager(logger, database='file_metadata_db', user='postgres', host="localhost", password='404300', port='5432')
    self.pool_manager = ThreadPool(processes=5)


 def walktree(self,top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''
    
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname).st_mode
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            self.walktree(pathname, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            logger.info( 'Skipping %s' % pathname)


 def write_summary(self, array_1, array_2, out_file_name):
     out_file = open(out_file_name, 'w')
     for it in range(0, array_1.__len__()):
         out_file.write(str(array_1[it]) + ' ' + str(array_2[it])+ '\n')
         
     out_file.close()
 
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
     pl.show()
     
 def write_summary_dict(self, dict, out_file_name):
     out_file = open(out_file_name, 'w')
     for key in dict.iterkeys():
         out_file.write(str(key) + ' ')
     out_file.write('\n')
     
     for key, value in dict.items():
         out_file.write(str(value) + ' ')
     out_file.write('\n')
         
     out_file.close()
     
  
 def visitfile(self,file):
     
                     
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
            birthtime = os.stat(file).st_birthtime
            
            privacy_level = oct(mode)[-3:]
            
            user = pwd.getpwuid(uid)[0]
            group = grp.getgrgid(gid)[0]
            print "-------------------------------------------------------"
            print "Filename: %s" % file
            print "Privacy level: %s" % privacy_level
            print "last access: %s" % time.ctime(atime)
            print "last modified: %s" % time.ctime(mtime)
            print "last status change: %s" % time.ctime(ctime)
            print "Creation time: %s" % time.ctime(birthtime)
            
            date_today = datetime.datetime.now()
            
            d1 = datetime.datetime.fromtimestamp(atime)
            d2 = datetime.datetime.fromtimestamp(birthtime)
            
            d1_ts = time.mktime(d1.timetuple())            
            d2_ts = time.mktime(d2.timetuple())

            today_ts = time.mktime(date_today.timetuple())
            
            print "Elapsed time today - access: %s" % abs(date_today - d1) 
            elapsed_ts = abs((int(today_ts-d1_ts) / 60)) 
            print "Elapsed time today - access (min): %d" % elapsed_ts

            # they are now in seconds, subtract and then divide by 60 to get minutes.
            elapsed_ac = datetime.datetime.fromtimestamp(atime) - datetime.datetime.fromtimestamp(birthtime)
            print "Elapsed time access - creation: %s" % elapsed_ac
            elapsed_ac = abs((int(d2_ts-d1_ts) / 60))
            print "Elapsed time access - creation (min): %d" % elapsed_ac
            
            d1 = datetime.datetime.fromtimestamp(mtime)
            d2 = datetime.datetime.fromtimestamp(birthtime)
            
            d1_ts = time.mktime(d1.timetuple())
            d2_ts = time.mktime(d2.timetuple())
            elapsed_cm = datetime.datetime.fromtimestamp(mtime) - datetime.datetime.fromtimestamp(birthtime)
            
            print "Elapsed time today - modification: %s" % abs(date_today - d1) 
            elapsed_tm = abs((int(today_ts-d1_ts) / 60)) 
            print "Elapsed time today - modification (min): %d" % elapsed_tm            
            
            print "Elapsed time creation - modification: %s" % elapsed_cm
            elapsed_cm = abs((int(d2_ts-d1_ts) / 60))
            print "Elapsed time creation - modification (min): %d" % elapsed_cm
            print "Size in bytes: %d" % size
            print "Group: %s" %  group
            print "User: %s" %  user
            print "-------------------------------------------------------"
            print '\n'
            
            
            privacy_list.append(privacy_level)
            #### Time in hours ####
            access_list.append((elapsed_ts/60))
            modification_list.append((elapsed_tm/60))
            crea_mod_list.append((elapsed_cm/60))
            
            num_acc = 0
            num_mods = 0
            
            #### Size of the file in Megabytes ####
            size_list.append(float(size/1024)/1024)
            try:
                if group_files[group]:
                    group_files[group] = group_files[group] + 1
            except:
                group_files[group] = 1
            
            try:  
                if user_files[user]:
                    user_files[user] = user_files[user] + 1
            except:
                user_files[user] = 1
            
            self.pool_manager.apply_async(self.db_handler.insert_metadata, (self.db_handler.con, file, atime, mtime, ctime, birthtime, size, privacy_level, group, user, elapsed_ac, elapsed_cm, elapsed_ts, elapsed_tm, num_acc, num_mods))
            #self.db_handler.select_metadata()

            
     
if __name__ == '__main__':
    print "Starting the processing."
    inspector = File_Inspector()
    
    '''walktree(sys.argv[1], visitfile) '''
    '''
    inspector.walktree("/Users/asturias/Downloads", inspector.visitfile)
    
    inspector.write_summary(privacy_list, access_list, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/privacy_access_summary.dat')
    inspector.write_summary(size_list, access_list, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/size_access_summary.dat')
    inspector.write_summary(size_list, privacy_list, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/size_privacy_summary.dat')
    inspector.write_summary(size_list, modification_list, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/size_modification_summary.dat')
    inspector.write_summary(size_list, crea_mod_list, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/size_crea_mod_summary.dat')
    inspector.write_summary_dict(user_files, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/user_files_summary.dat')
    inspector.write_summary_dict(group_files, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/group_files_summary.dat')
   '''
    inspector.plot_results('/Users/hector/Dropbox/file_metadata_collector/dat/privacy_access_summary.dat', "Privacy VS Time since last access", "Privacy (octal)", "Time since last access (hrs)")
    
    inspector.plot_results('/Users/hector/Dropbox/file_metadata_collector/dat/size_access_summary.dat', "Size VS Time since last access", "Size (mb)", "Time since last access (hrs)")
   
    print "Terminated processing of %d files ... without errors.\n" % size_list.__len__()


    

    
    