

import grp
import pwd
import os, sys, time
from stat import *


dict_dirs_files= {}

def count_files(top, level, counter):
    '''recursively descend the directory tree rooted at top,
       counting the amount of regular files'''
    
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        try:
          mode = os.stat(pathname).st_mode
          if S_ISDIR(mode):
            # It's a directory, recurse into it
             counter =  count_files(pathname,(level+1),counter)
          else:
             #print 'Counter %d Filename %s' % (counter, pathname)
            # It's a file, call the callback function
             counter = counter + 1
          
        except Exception as e:
            print('Error in file or directory: %s %s' % (pathname, e))
    return counter

def count_files_dir(top, level, counter):
    '''recursively descend the directory tree rooted at top,
       counting the amount of regular files'''
    
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        try:
          mode = os.stat(pathname).st_mode
          if S_ISDIR(mode):
            # It's a directory, recurse into it
             counter =  count_files(pathname,(level+1),0)
             if level < 1:
                 print 'Counter %d Filename %s Num. Files %d' % (counter, pathname, counter) 
                 dict_dirs_files[pathname]=counter
          else:
             #print 'Counter %d Filename %s' % (counter, pathname)
            # It's a file, call the callback function
             counter = counter + 1
          
        except Exception as e:
            print('Error in file or directory: %s %s' % (pathname, e))
        
    return counter 
    
print 'Starting ...'
path = '/Users/hector'
print count_files_dir(path,0, 0)
print 'Terminated !'   