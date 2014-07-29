import sys

def main():
    """Entry-point function."""
print "Starting the processing for %s folder.",sys.argv[1]    
from watchdog.utils.collector import File_Inspector
inspector = File_Inspector(False, False)
inspector.walktree(sys.argv[1], inspector.add_file_metadata)
 #   print "Starting the data files generation." 
print 'Terminated processing File_Inspector' 

if __name__ == '__main__':
    main()
