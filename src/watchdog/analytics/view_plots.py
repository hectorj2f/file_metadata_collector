import cherrypy
from plot_data import Plot_Data 
from plot_db import Plot_Db
from plot_file import Plot_File
import StringIO
import urllib, base64

class View_Plots(object):
    
    def read_dat_plot(self, plot_manager, path_file, title, x_label, y_label, filename):
        fig = None
        imgdata = None
        plot_manager = Plot_Data()
        uri = plot_manager.get_plot_results(path_file, title, x_label, y_label, filename)

    #    fig = plt.gcf()
        
     #   imgdata = StringIO.StringIO()
     #   fig.savefig(imgdata, format='png')
     #   imgdata.seek(0)  # rewind the data

        #html = "Content-type: image/png\n"
      #  uri = 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))
        html = '<img src = "%s" witdh="300px" height="300px" /> <br />' % uri
        
        return html
    
    
    def get_db_plot(self, plot_manager, title, x_label, y_label, field1, field2, filename):
        fig = None
        imgdata = None
        plot_manager = Plot_Data()
        uri = plot_manager.get_plot_db_results( title, x_label, y_label, field1, field2, filename)
        html = '<img src = "%s" witdh="300px" height="300px" /> <br />' % uri
        
        return html
    
    def index(self):
      #  test8 = Plot_Db("Filename extension occurrences", "Extension", "Occurrences", "filename", "size", "occurrences" )
        test8 = Plot_Db("Size VS Num. modifications", "Size (mb)", "Num. modifications", "size", "num_mods" )
        test9 = Plot_Db("Size VS Num. access", "Size (mb)", "Num. access", "size", "num_acc" )
        
        test1 = Plot_Db("Num. modifications VS Permissions (octal)", "Num. modifications", "Permissions (octal)", "num_mods", "privacy")
        test2 = Plot_Db("Num. access VS Elapsed time today - modification (min)", "Num. access", "Size (mb)", "num_acc", "elapsed_tm")
        test6 = Plot_Db("Num. access VS Num. modifications", "Num. access", "Num. modifications", "num_acc", "num_mods")
        
        test3 = Plot_Db("Permissions (octal) VS Time since last access (hrs)", "Privacy (octal)", "Time since last access (min)", "privacy", "elapsed_ts")
        test5 = Plot_Db("Size VS Permissions (octal)", "Size (mb)", "Permissions (octal)", "size","privacy")
        test4 = Plot_Db("Size VS Time since last access", "Size (mb)", "Time since last access (min)", "size", "elapsed_ts" )
        
        test7 = Plot_Db("Size VS Time since last access", "Size (mb)", "Time since last modification (min)", "size", "elapsed_tm" )
       
        
        #test3 = Plot_File('/Users/hector/Dropbox/file_metadata_collector/dat/privacy_access_summary.dat', "Permissions (octal) VS Time since last access (hrs)", "Privacy (octal)", "Time since last access (hrs)", "plot_file_a")
        #test5 = Plot_File('/Users/hector/Dropbox/file_metadata_collector/dat/size_privacy_summary.dat', "Size VS Permissions (octal)", "Size (mb)", "Permissions (octal)", "plot_file_c")
        #test4 = Plot_File('/Users/hector/Dropbox/file_metadata_collector/dat/size_access_summary.dat', "Size VS Time since last access", "Size (mb)", "Time since last access (hrs)", "plot_file_b")
        
         
        
        html = '<html><body>'
        html += '<h1 align="center"> PC Data Scanner -- Charts </h1>'
        html += '<div align="center"><table>'
        html += '<tr>'
        html += '<td><img src = "%s" witdh="300px" height="300px" /> <br /></td>' % test1.uri
        html += '<td><img src = "%s" witdh="300px" height="300px" /> <br /></td>' % test2.uri
        html += '<td><img src = "%s" witdh="300px" height="300px" /> <br /></td>' % test3.uri
        html += '</tr>'
        html += '<tr>'
        html += '<td><img src = "%s" witdh="300px" height="300px" /> <br /></td>' % test4.uri
        html += '<td><img src = "%s" witdh="300px" height="300px" /> <br /></td>' % test5.uri
        html += '<td><img src = "%s" witdh="300px" height="300px" /> <br /></td>' % test6.uri
        html += '</tr>'
        html += '<tr>'
        html += '<td><img src = "%s" witdh="300px" height="300px" /> <br /></td>' % test7.uri
        html += '<td><img src = "%s" witdh="700px" height="300px" /> <br /></td>' % test8.uri
        html += '<td><img src = "%s" witdh="700px" height="300px" /> <br /></td>' % test9.uri
        html += '</tr>'
        html += '</table></div></body></html>'
        return html
    index.exposed = True
    
cherrypy.quickstart(View_Plots())
