#!/bin/python

import tornado.ioloop
import tornado.web

from os import curdir, sep, system, path
import urllib

PORT = 8000

class MainHandler(tornado.web.RequestHandler):
    tmp_file  = curdir + sep + 'tmp' + sep + 'tmp_file'
    tmp_sound = curdir + sep + 'tmp' + sep + 'tmp_sound'
    tmp_btext = curdir + sep + 'tmp' + sep + 'tmp_btext'
    
    def get(self):
        """Main index page
        """
        # display form
        url = "" # self.request.arguments.url
        sound_file = ''
        # read index template speak.html
        self.render("speak.html", url=url, sound_file=sound_file)
        # display it         

    def post(self):
        """Fetch uri, extract bodytext, tts it
           and redirect to streaming page
        """
        # fetch post data
        url = self.request.arguments['url'][0]
        # version = '.' + self.request.arguments['remote_ip'][0]
        import hashlib
        m = hashlib.md5()
        m.update(url)
        version = '.' + m.hexdigest()

        # return cached file
        if not path.exists(self.tmp_file + version):
           
            # retrieve target url
            tmp_page = urllib.urlretrieve(url, self.tmp_file + version)
        
            # extract body text
            import BodyTextExtractor
            p = BodyTextExtractor.HtmlBodyTextExtractor()
            p.feed(open(self.tmp_file + version).read())
            p.close()
            f_btext = open(self.tmp_btext + version,'w')
            f_btext.write(p.body_text())
            f_btext.close()
        
            # text2wave it
            try:
                system('text2wave ' + self.tmp_btext + version + ' -o ' + self.tmp_sound + version )
            except OSError, e:
                print >>sys.stderr, "Execution failed:", e
        
        # return streaming page
        self.render("speak.html", url        = url,
                                  sound_file = self.tmp_sound + version,
                                  body_text  = open(self.tmp_btext + version).read(),
                    )
        # @see self.redirect OR RedirectHandler
        # self.redirect('/')
        


application = tornado.web.Application([
    # routes
    (r"/", MainHandler),
    (r"/tmp/(.*)", tornado.web.StaticFileHandler,{"path": curdir+sep+'tmp'}),
    ])

if __name__ == "__main__":
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
