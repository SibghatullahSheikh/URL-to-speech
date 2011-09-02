# -*- coding: utf-8 -*-

import string,cgi,time
from os import curdir, sep, system
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import urllib
import BodyTextExtractor
import festival

PORT = 8000

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        #print parsed_path
        try:
            if self.path.endswith(".html"):
                f = open(curdir + sep + self.path) #page1.html
                self.send_response(200)
                self.send_header('Content-type',    'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                self.wfile.write("</body></html>")
                f.close()
                return
            #if self.path.endswith(def_path):   #our dynamic content
            if parsed_path.path == '/speak': # action
                # find url
                target_url = urllib.unquote(parsed_path.query.split('=',1)[1])
                # fetch given url
                tmp_file = curdir + '/tmp_file'
                filehandle = urllib.urlretrieve(target_url, tmp_file)
                
                # extract body text
                html = open(tmp_file).read()
                p = BodyTextExtractor.HtmlBodyTextExtractor()
                p.feed(html)
                p.close()

                maintext = p.body_text()
                mt = open(curdir + sep + 'tmp_maintext','w')
                mt.write(maintext)
                mt.close()
                
                # text2wave it
                tmp_sound = './tmp_sound'
                # fest = festival.Festival()
                # fest.wave(source=maintext, dest=tmp_sound)
                try:
                    system('text2wave ' + curdir+sep+'tmp_maintext' + ' -o ' + tmp_sound)
                except OSError, e:
                    print >>sys.stderr, "Excecution failed:", e
                
                # return html audio and stream
                self.send_response(200)
                self.send_header('Content-type',    'text/html')
                self.end_headers()

                # generate html page result
                f = open(curdir + sep + 'page1.html') # same pageagain
                self.wfile.write(f.read())

                self.wfile.write('<hr/>Debug info<hr/>')
                self.wfile.write('<pre>Summary:<br/>'  + p.summary()   + '</pre>')
                self.wfile.write('<pre>Bodytext:<br/>' + maintext + '</pre>')
                self.wfile.write('<pre>Fulltext:<br/>' + p.full_text() + '</pre>')

                self.wfile.write("<hr/><small>Copyright (c) 2011 by thinKING -- Generated on " + str(time.time()) + "</small>")
                self.wfile.write("</body></html>")
                f.close()
                return
                
            if parsed_path.path == '/tmp_sound':
                t1 = open(curdir + '/tmp_sound').read()
                # return stream
                self.send_response(200)
                self.send_header('Content-type',    'audio/x-wav')
                self.end_headers()
                self.wfile.write(t1)
                return
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

def main():
    try:
        server = HTTPServer(('', 8000), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

# present html form
# fetch given url
# extract body text
# text2wave it
# return html audio and stream