'''
    OpenAlarm - HTTPServer - Server Module
    Copyright (C) 2013 Ryan M. Kraus (Humble.Robot.Development@gmail.com)
  
    LICENSE:
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.
           
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
       
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
          
    DESCRIPTION:
    This Python module contains the base HTTP Server used by OpenAlarm.
    
    WRITTEN:     5/2013
'''

from threading import Thread
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import urlparse
import Pages, Errors
import sys

_defaultIP = 'localhost'
_defaultPort = 5555
_alarms = dict()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # parse request, get page function
        print "Recieved Request"
        request = ArgList(urlparse(self.path).path.split('/'))
        request.Next() # remove first entry
        page = Pages.getPage(request.Next())
        # make response
        try:
            # try to execute the page
            response = page(request)
            # send page results
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(response)
            #self.wfile.write(request)
        except Errors.HTTP404, e:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(e)
        except:
            # send error
            e = sys.exc_info()[0]
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(e)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def startServer(ip=_defaultIP, port=_defaultPort, handler=Handler):
    port = int(float(port))
    return ThreadedHTTPServer((ip, port), handler)


class ArgList(list):
    def Next(self):
        try:
            return self.pop(0).strip()
        except IndexError:
            return None
    def next(self):
        try:
            return self.pop(0).lower().strip()
        except IndexError:
            return None

# functions that test basic server functionality
def test():
    try:
        print "Server Running"
        server = startServer()
        server.serve_forever()
    except KeyboardInterrupt:
        print "Server Terminated"
if __name__ == "__main__":
    test()
