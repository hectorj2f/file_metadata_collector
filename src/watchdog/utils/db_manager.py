'''
:synopsis: Database manager module to store all the file metadata
:author: Hector Fernandez
'''

import psycopg2
import sys, time
import datetime
import log 

con = None  

class DB_Manager:
     
    def __init__(self, logger, reset_db, database, user, host, password, port):
        
        try:
            self.logger = logger
            self.con = None
            self.con = psycopg2.connect(database='file_metadata_db_pro', user='postgres', host="127.0.0.1", password='404300', port='5432') 
            
            if reset_db:
                cur = self.con.cursor()
                cur.execute("DROP TABLE IF EXISTS file_metadata")
                cur.execute("CREATE table file_metadata ( file_id bigserial primary key, filename varchar(1500) NOT NULL, owner_name varchar(50) NOT NULL, owner_grp varchar(50) NOT NULL, size bigint NOT NULL, privacy integer NOT NULL, date_modified timestamp default NULL, date_creation timestamp default NULL, date_access timestamp default NULL, date_status_change timestamp default NULL, elapsed_ac integer NOT NULL, elapsed_cm integer NOT NULL, elapsed_ts integer NOT NULL, elapsed_tm integer NOT NULL, num_acc integer NOT NULL, num_mods integer NOT NULL);")
            
            self.con.commit()
            
        except psycopg2.DatabaseError, e:
            if self.con:
                self.con.close();
            self.logger.error( 'Error DB_Manager() %s' % e)    
            sys.exit(1)
        except Exception as e:
            self.logger.error( 'Exception DB_Manager %s' % e)
     
    def get_connection(self):
        return self.con   
    
    def select_fields(self, field1, field2, field3=None ):
       try:
            cur = self.con.cursor()
            if field3 is None:
                query = "SELECT "+ str(field1) + ", "+ str(field2) + " FROM file_metadata"
            else:
                query = "SELECT "+ str(field1) + ", "+ str(field2) + ", "+ str(field3) +" FROM file_metadata"

            cur.execute(query)          
            rows = cur.fetchall()
          
          #  self.logger.info('SQL results select_metadata_num_mods() %s' % rows)   
           
            return rows
       except psycopg2.DatabaseError, e:
            self.logger.error('Error select_fields() %s' % e)      


    
    def close_connection(self):
        if self.con:
                self.con.close();
         
    def insert_metadata(self, file,atime,mtime,ctime,birthtime,size, privacy, group,user, elapsed_ac, elapsed_cm, elapsed_ts, elapsed_tm, num_acc, num_mods):
       try:

           cur = self.con.cursor()

           query = "INSERT INTO file_metadata (filename, owner_name, owner_grp, size, privacy, date_modified, date_creation, date_access, date_status_change, elapsed_ac, elapsed_cm, elapsed_ts, elapsed_tm, num_acc, num_mods) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
         #  self.logger.info("SQL query insert_metadata() %s "% query)
           
           cur.execute(query, (file, user, group, str(size), privacy, datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S'),  datetime.datetime.fromtimestamp(birthtime).strftime('%Y-%m-%d %H:%M:%S'),  datetime.datetime.fromtimestamp(atime).strftime('%Y-%m-%d %H:%M:%S'),  datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S'), str(elapsed_ac), str(elapsed_cm), str(elapsed_ts), str(elapsed_tm), str(num_acc), str(num_mods) ) )           
           #cur.executemany(query, (file, user, group, str(size) ) )
        
           self.con.commit()
    
       except psycopg2.DatabaseError, e:
           if self.con:
               self.con.rollback()
               self.logger.error('Error insert_metadata() %s' % e)    
    
    def delete_metadata_filename(self, filename):
         try:
            cur = self.con.cursor()
            cur.execute('DELETE file_metadata WHERE filename=%s' % filename)          
            self.con.commit()    

         except psycopg2.DatabaseError, e:
            self.logger.error('Error delete_metadata_filename() %s' % e)
            
    
    def select_metadata(self):
         try:
            cur = self.con.cursor()
            cur.execute('SELECT  filename, owner_name, owner_grp, size, privacy, date_modified, date_creation, date_access, date_status_change, elapsed_ac, elapsed_cm, elapsed_ts, elapsed_tm, num_acc, num_mods FROM file_metadata order by file_id')          
            ver = cur.fetchone()
          #  self.logger.info('SQL results select_metadata() %s' % ver)    

         except psycopg2.DatabaseError, e:
            self.logger.error('Error select_metadata() %s' % e)    

    def select_metadata_filename(self, filename):
         try:
            cur = self.con.cursor()
            cur.execute("SELECT filename, owner_name, owner_grp, size, privacy, date_modified, date_creation, date_access, date_status_change, elapsed_ac, elapsed_cm, elapsed_ts, elapsed_tm, num_acc, num_mods FROM file_metadata WHERE filename='%s'" % filename)          
            ver = cur.fetchone()
           # self.logger.info('SQL results select_metadata_filename() %s' % ver)    

         except psycopg2.DatabaseError, e:
            self.logger.error('Error select_metadata_filename() %s' % e)
            
        
    def is_metadata_filename(self, filename):
         try:
            cur = self.con.cursor()
            cur.execute("SELECT filename, owner_name, owner_grp, size, privacy, date_modified, date_creation, date_access, date_status_change, elapsed_ac, elapsed_cm, elapsed_ts, elapsed_tm, num_acc, num_mods FROM file_metadata WHERE filename='%s'" % filename)          
            ver = cur.fetchone()
           # self.logger.info('SQL results select_metadata_filename() %s' % ver)
   
            return cur.fetchone().len()
         except psycopg2.DatabaseError, e:
            self.logger.error('Error get_metadata_filename() %s' % e)
            
    def select_metadata_num_acc(self, filename):
         try:
            cur = self.con.cursor()
            cur.execute("SELECT num_acc FROM file_metadata WHERE filename='%s'" % filename)          
            ver = cur.fetchone()[0]
                    
            #self.logger.info('SQL results select_metadata_num_acc() %s' % ver)   
           
            return ver
         except psycopg2.DatabaseError, e:
            self.logger.error('Error select_metadata_num_acc() %s' % e)   
            
    def select_metadata_num_mods(self, filename):
         try:
            cur = self.con.cursor()
            cur.execute("SELECT num_mods FROM file_metadata WHERE filename='%s'" % filename)          
            ver = cur.fetchone()[0]
          
           # self.logger.info('SQL results select_metadata_num_mods() %s' % ver)   
           
            return ver
         except psycopg2.DatabaseError, e:
            self.logger.error('Error select_metadata_num_mods() %s' % e)  
            
    
                
    def update_metadata_all(self, filename,atime,mtime,ctime,birthtime,size, privacy, group,user, elapsed_ac, elapsed_cm, elapsed_ts, elapsed_tm, num_acc, num_mods):
         try:
            cur = self.con.cursor()
           
            query = "UPDATE file_metadata SET date_access=%s, date_modified=%s, date_status_change=%s, date_creation=%s, size=%s, privacy=%s, owner_grp=%s, owner_name=%s, elapsed_ac=%s, elapsed_cm=%s, elapsed_ts=%s, elapsed_tm=%s, num_acc=%s, num_mods=%s WHERE filename=%s"        
           # self.logger.info("SQL query update_metadata_all() %s "% query)
            cur.execute(query, (datetime.datetime.fromtimestamp(atime).strftime('%Y-%m-%d %H:%M:%S'), datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S'),  datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S'),  datetime.datetime.fromtimestamp(birthtime).strftime('%Y-%m-%d %H:%M:%S'), 
                                str(size), privacy, group, user, str(elapsed_ac), str(elapsed_cm), str(elapsed_ts), str(elapsed_tm), str(num_acc), str(num_mods), filename ) )
            self.con.commit()            
            self.logger.info('Number of rows updated: %d' % cur.rowcount)    

         except psycopg2.DatabaseError, e:
            self.logger.error('Error update_metadata_num_acc() %s' % e)    
    
    def update_metadata_num_mods(self, filename):
         try:
            cur = self.con.cursor()
            cur.execute("SELECT num_mods FROM file_metadata WHERE filename='%s'" % filename)          
            ver = cur.fetchone()
          
            cur.execute("UPDATE file_metadata SET num_mods=%s WHERE filename='%s'", ((int(ver)+1), filename))        
            
            self.con.commit()
            self.logger.info('Number of rows updated: %d' % cur.rowcount)    

         except psycopg2.DatabaseError, e:
            self.logger.error('Error update_metadata_num_mods() %s' % e)   
'''                    
if __name__ == '__main__':
   PATH_LOG_FILE = '/tmp/plot_metadata.log'
   import watchdog.utils.log  as log  
   log.init(PATH_LOG_FILE)
   logger = log.create_logger('Metatada_Collector')

   db = DB_Manager(logger, False, database='file_metadata_db', user='postgres', host="localhost", password='404300', port='5432')
   db.select_fields("filename", "privacy", "size")
'''