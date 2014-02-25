from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from urlparse import urlparse
import Errors
import Pages
import sys

_defaultIP = 'localhost'
_defaultPort = 5555
_alarms = dict()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # parse request, get page function
        print "Recieved Request"
        request = ArgList(urlparse(self.path).path.split('/'))
        request.Next()  # remove first entry
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
