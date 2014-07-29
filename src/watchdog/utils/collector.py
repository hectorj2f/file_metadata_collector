
'''
:synopsis: Database manager module to store all the file metadata
:author: Hector Fernandez
'''

import grp
import pwd
import os, sys, time
from stat import *
from multiprocessing.pool import ThreadPool
from threading import Thread
from db_manager import *
import datetime
import log 

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


database_handler = DB_Manager(logger, False, database='file_metadata_db', user='postgres', host='127.0.0.1', password='404300', port='5432')

class File_Inspector:

 def __init__(self, reset_db, threading=False, db_handler=None):
    try:
        if not db_handler:
            self.db_handler = DB_Manager(logger, reset_db, database='file_metadata_db', user='postgres', host='127.0.0.1', password='404300', port='5432')
        else:
            self.db_handler = db_handler
        
    except Exception as e:
        print 'Error in File)inspector'
        print e
    self.pool_manager = None
    if threading:
        self.pool_manager = ThreadPool(processes=5)
    

 def walktree(self,top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''
    
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        try:
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
        except Exception as e:
            logger.error('collector.py walktree error in file or directory: %s %s' % (pathname, e))

 
 def write_summary(self, array_1, array_2, out_file_name):
     out_file = open(out_file_name, 'w')
     for it in range(0, array_1.__len__()):
         out_file.write(str(array_1[it]) + ' ' + str(array_2[it])+ '\n')
         
     out_file.close()
      
 def generate_data_files(self):
     
    self.write_summary(privacy_list, access_list, '/Users/hector/file_metadata_collector/dat/privacy_access_summary.dat')
    self.write_summary(size_list, access_list, '/Users/hector/file_metadata_collector/dat/size_access_summary.dat')
    self.write_summary(size_list, privacy_list, '/Users/hector/file_metadata_collector/dat/size_privacy_summary.dat')
    self.write_summary(size_list, modification_list, '/Users/hector/file_metadata_collector/dat/size_modification_summary.dat')
    self.write_summary(size_list, crea_mod_list, '/Users/hector/file_metadata_collector/dat/size_crea_mod_summary.dat')
    self.write_summary_dict(user_files, '/Users/hector/file_metadata_collector/dat/user_files_summary.dat')
    self.write_summary_dict(group_files, '/Users/hector/file_metadata_collector/dat/group_files_summary.dat')
 
 
 def write_summary_dict(self, dict, out_file_name):
     out_file = open(out_file_name, 'w')
     for key in dict.iterkeys():
         out_file.write(str(key) + ' ')
     out_file.write('\n')
     
     for key, value in dict.items():
         out_file.write(str(value) + ' ')
     out_file.write('\n')
         
     out_file.close()
    
 
 def add_file_metadata(self,file):
     
                     
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
            birthtime = os.stat(file).st_birthtime
            
            privacy_level = oct(mode)[-3:]
            
            user = pwd.getpwuid(uid)[0]
            group = grp.getgrgid(gid)[0]
            logger.info( "-------------------------------------------------------")
            logger.info( "Filename: %s" % file)
            logger.info("Privacy level: %s" % privacy_level)
            logger.info( "last access: %s" % time.ctime(atime))
            logger.info( "last modified: %s" % time.ctime(mtime))
            logger.info( "last status change: %s" % time.ctime(ctime))
            logger.info( "Creation time: %s" % time.ctime(birthtime))
            
            date_today = datetime.datetime.now()
            
            d1 = datetime.datetime.fromtimestamp(atime)
            d2 = datetime.datetime.fromtimestamp(birthtime)
            
            d1_ts = time.mktime(d1.timetuple())            
            d2_ts = time.mktime(d2.timetuple())

            today_ts = time.mktime(date_today.timetuple())
            
            logger.info( "Elapsed time today - access: %s" % abs(date_today - d1)) 
            elapsed_ts = abs((int(today_ts-d1_ts) / 60)) 
            logger.info( "Elapsed time today - access (min): %d" % elapsed_ts)

            # they are now in seconds, subtract and then divide by 60 to get minutes.
            elapsed_ac = datetime.datetime.fromtimestamp(atime) - datetime.datetime.fromtimestamp(birthtime)
            logger.info( "Elapsed time access - creation: %s" % elapsed_ac)
            elapsed_ac = abs((int(d2_ts-d1_ts) / 60))
            logger.info( "Elapsed time access - creation (min): %d" % elapsed_ac)
            
            d1 = datetime.datetime.fromtimestamp(mtime)
            d2 = datetime.datetime.fromtimestamp(birthtime)
            
            d1_ts = time.mktime(d1.timetuple())
            d2_ts = time.mktime(d2.timetuple())
            elapsed_cm = datetime.datetime.fromtimestamp(mtime) - datetime.datetime.fromtimestamp(birthtime)
            
            logger.info( "Elapsed time today - modification: %s" % abs(date_today - d1)) 
            elapsed_tm = abs((int(today_ts-d1_ts) / 60)) 
            logger.info( "Elapsed time today - modification (min): %d" % elapsed_tm)            
            
            logger.info( "Elapsed time creation - modification: %s" % elapsed_cm)
            elapsed_cm = abs((int(d2_ts-d1_ts) / 60))
            logger.info( "Elapsed time creation - modification (min): %d" % elapsed_cm)
            logger.info( "Size in bytes: %d" % size)
            logger.info( "Group: %s" %  group)
            logger.info( "User: %s" %  user)
            logger.info( "-------------------------------------------------------")
            logger.info( '\n')
            
            
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
            
          #  self.pool_manager.apply_async(
            if self.pool_manager:
                self.pool_manager.apply_async(self.db_handler.insert_metadata, ( file, atime, mtime, ctime, birthtime, size, privacy_level, group, user, elapsed_ac, elapsed_cm, elapsed_ts, elapsed_tm, num_acc, num_mods))
            else:    
                self.db_handler.insert_metadata( file, atime, mtime, ctime, birthtime, size, privacy_level, group, user, elapsed_ac, elapsed_cm, elapsed_ts, elapsed_tm, num_acc, num_mods)
            #self.db_handler.select_metadata()

 def delete_file_metadata(self,file):
      
            self.db_handler.delete_metadata_filename(file)

 def close_db_connecion(self):
            self.db_handler.close_connection()
  
 def is_file_metadata(self, filename):
     return  (self.db_handler.is_metadata_filename(filename) > 0)
 
 def update_file_metadata(self,file):
            num_acc = 0
            num_mods = 0
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
            birthtime = os.stat(file).st_birthtime
            
            privacy_level = oct(mode)[-3:]
            
            user = pwd.getpwuid(uid)[0]
            group = grp.getgrgid(gid)[0]
            logger.info( "-------------------------------------------------------")
            logger.info("Filename: %s" % file)
            logger.info("Privacy level: %s" % privacy_level)
            logger.info("last access: %s" % time.ctime(atime))
            logger.info("last modified: %s" % time.ctime(mtime))
            logger.info("last status change: %s" % time.ctime(ctime))
            logger.info("Creation time: %s" % time.ctime(birthtime))
            
            date_today = datetime.datetime.now()
            
            d1 = datetime.datetime.fromtimestamp(atime)
            d2 = datetime.datetime.fromtimestamp(birthtime)
            
            d1_ts = time.mktime(d1.timetuple())            
            d2_ts = time.mktime(d2.timetuple())

            today_ts = time.mktime(date_today.timetuple())
            
            logger.info("Elapsed time today - access: %s" % abs(date_today - d1) )
            elapsed_ts = abs((int(today_ts-d1_ts) / 60)) 
            logger.info("Elapsed time today - access (min): %d" % elapsed_ts)

            # they are now in seconds, subtract and then divide by 60 to get minutes.
            elapsed_ac = datetime.datetime.fromtimestamp(atime) - datetime.datetime.fromtimestamp(birthtime)
            logger.info("Elapsed time access - creation: %s" % elapsed_ac)
            elapsed_ac = abs((int(d2_ts-d1_ts) / 60))
            logger.info("Elapsed time access - creation (min): %d" % elapsed_ac)
            
            d1 = datetime.datetime.fromtimestamp(mtime)
            d2 = datetime.datetime.fromtimestamp(birthtime)
            
            d1_ts = time.mktime(d1.timetuple())
            d2_ts = time.mktime(d2.timetuple())
            elapsed_cm = datetime.datetime.fromtimestamp(mtime) - datetime.datetime.fromtimestamp(birthtime)
            
            logger.info("Elapsed time today - modification: %s" % abs(date_today - d1) )
            elapsed_tm = abs((int(today_ts-d1_ts) / 60)) 
            logger.info("Elapsed time today - modification (min): %d" % elapsed_tm      )      
            
            logger.info("Elapsed time creation - modification: %s" % elapsed_cm)
            elapsed_cm = abs((int(d2_ts-d1_ts) / 60))
            logger.info("Elapsed time creation - modification (min): %d" % elapsed_cm)
            logger.info("Size in bytes: %d" % size)
            logger.info("Group: %s" %  group)
            logger.info("User: %s" %  user)
            logger.info("-------------------------------------------------------")
            logger.info('\n')
            
            num_acc = self.db_handler.select_metadata_num_acc(file)
            num_mods = self.db_handler.select_metadata_num_mods(file) 
            
            logger.info('Num access: %d' % num_acc)
            logger.info('Num modifications: %d' % num_mods)
            
            self.db_handler.update_metadata_all(file, atime, mtime, ctime, birthtime, size, privacy_level, group, user, elapsed_ac, elapsed_cm, elapsed_ts, elapsed_tm, num_acc, num_mods)
            #self.db_handler.select_metadata()

 def update_file_metadata_counters(self, file, only_access):
            num_acc = 0
            num_mods = 0
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
            birthtime = os.stat(file).st_birthtime
            
            privacy_level = oct(mode)[-3:]
            
            user = pwd.getpwuid(uid)[0]
            group = grp.getgrgid(gid)[0]
            logger.info("-------------------------------------------------------")
            logger.info("Filename: %s" % file)
            logger.info("Privacy level: %s" % privacy_level)
            logger.info("last access: %s" % time.ctime(atime))
            logger.info("last modified: %s" % time.ctime(mtime))
            logger.info("last status change: %s" % time.ctime(ctime))
            logger.info("Creation time: %s" % time.ctime(birthtime))
            
            date_today = datetime.datetime.now()
            
            d1 = datetime.datetime.fromtimestamp(atime)
            d2 = datetime.datetime.fromtimestamp(birthtime)
            
            d1_ts = time.mktime(d1.timetuple())            
            d2_ts = time.mktime(d2.timetuple())

            today_ts = time.mktime(date_today.timetuple())
            
            logger.info("Elapsed time today - access: %s" % abs(date_today - d1)) 
            elapsed_ts = abs((int(today_ts-d1_ts) / 60)) 
            logger.info("Elapsed time today - access (min): %d" % elapsed_ts)

            # they are now in seconds, subtract and then divide by 60 to get minutes.
            elapsed_ac = datetime.datetime.fromtimestamp(atime) - datetime.datetime.fromtimestamp(birthtime)
            logger.info("Elapsed time access - creation: %s" % elapsed_ac)
            elapsed_ac = abs((int(d2_ts-d1_ts) / 60))
            logger.info("Elapsed time access - creation (min): %d" % elapsed_ac)
            
            d1 = datetime.datetime.fromtimestamp(mtime)
            d2 = datetime.datetime.fromtimestamp(birthtime)
            
            d1_ts = time.mktime(d1.timetuple())
            d2_ts = time.mktime(d2.timetuple())
            elapsed_cm = datetime.datetime.fromtimestamp(mtime) - datetime.datetime.fromtimestamp(birthtime)
            
            logger.info("Elapsed time today - modification: %s" % abs(date_today - d1)) 
            elapsed_tm = abs((int(today_ts-d1_ts) / 60)) 
            logger.info("Elapsed time today - modification (min): %d" % elapsed_tm)            
            
            logger.info("Elapsed time creation - modification: %s" % elapsed_cm)
            elapsed_cm = abs((int(d2_ts-d1_ts) / 60))
            logger.info("Elapsed time creation - modification (min): %d" % elapsed_cm)
            logger.info("Size in bytes: %d" % size)
            logger.info("Group: %s" %  group)
            logger.info("User: %s" %  user)
            logger.info("-------------------------------------------------------")
            logger.info('\n')
            
            if only_access:
                num_acc = self.db_handler.select_metadata_num_acc(file) + 1
                num_mods = self.db_handler.select_metadata_num_mods(file)
            else:
                num_acc = self.db_handler.select_metadata_num_acc(file) 
                num_mods = self.db_handler.select_metadata_num_mods(file) + 1
            
            logger.info('Num access: %d' % num_acc)
            logger.info('Num modifications: %d' % num_mods)
            
            self.db_handler.update_metadata_all(file, atime, mtime, ctime, birthtime, size, privacy_level, group, user, elapsed_ac, elapsed_cm, elapsed_ts, elapsed_tm, num_acc, num_mods)
            #self.db_handler.select_metadata()

 '''    
if __name__ == '__main__':
    print "Starting the processing."
    inspector = File_Inspector()
    
    walktree(sys.argv[1], add_file_metadata) 
    
    inspector.walktree("/Users/asturias/Downloads", inspector.visitfile)
    
    inspector.write_summary(privacy_list, access_list, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/privacy_access_summary.dat')
    inspector.write_summary(size_list, access_list, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/size_access_summary.dat')
    inspector.write_summary(size_list, privacy_list, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/size_privacy_summary.dat')
    inspector.write_summary(size_list, modification_list, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/size_modification_summary.dat')
    inspector.write_summary(size_list, crea_mod_list, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/size_crea_mod_summary.dat')
    inspector.write_summary_dict(user_files, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/user_files_summary.dat')
    inspector.write_summary_dict(group_files, '/Users/asturias/Development/Dropbox/file_metadata_collector/dat/group_files_summary.dat')
   
    inspector.plot_results('/Users/hector/Dropbox/file_metadata_collector/dat/privacy_access_summary.dat', "Privacy VS Time since last access", "Privacy (octal)", "Time since last access (hrs)")
    
    inspector.plot_results('/Users/hector/Dropbox/file_metadata_collector/dat/size_access_summary.dat', "Size VS Time since last access", "Size (mb)", "Time since last access (hrs)")
   
    print "Terminated processing of %d files ... without errors.\n" % size_list.__len__()
    
    '''