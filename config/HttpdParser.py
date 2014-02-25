from HTMLParser import HTMLParser


class HttpdParser(HTMLParser):

    def __init_var__(self):
        # create status variables
        self._inHttpd = None
        self._inKey = None
        self.httpd = None

    def read(self, fname):
        self.__init_var__()
        cache = open(fname).read()
        self.feed(cache)
        out = self.httpd
        self.__init_var__()
        return out

    # Default Syntax Handlers
    def handle_starttag(self, tag, attrs):
        #print 'START: ' + str(tag)
        if tag == 'httpd':
            self.httpd_start()
        elif tag == 'ip':
            self.ip_start()
        elif tag == 'port':
            self.port_start()
        else:
            raise FormatError(self.getpos())

    def handle_endtag(self, tag):
        #print 'END: ' + str(tag)
        if tag == 'httpd':
            self.httpd_end()
        elif tag == 'ip':
            self.ip_end()
        elif tag == 'port':
            self.port_end()
        else:
            raise FormatError(self.getpos())

    def handle_data(self, data):
        data = data.strip()
        if len(data) > 0:
            #print 'DATA: ' + str(data)
            if self._inHttpd:
                self.httpd_data(data)
            else:
                raise FormatError(self.getpos())

    # HTTPD tag handlers
    def httpd_start(self):
        if self._inHttpd is None:
            self._inHttpd = {'ip': None, 'port': None}
        else:
            raise FormatError(self.getpos())

    def httpd_end(self):
        if self._inHttpd is not None and self._inKey is None:
            if self._inHttpd['ip'] is not None \
                    and self._inHttpd['port'] is not None:
                self.httpd = self._inHttpd
                self._inHttpd = None
            else:
                raise FormatError(self.getpos())
        else:
            raise FormatError(self.getpos())

    def httpd_data(self, data):
        if self._inKey is not None:
            self._inHttpd[self._inKey] = data
        else:
            raise FormatError(self.getpos())

    # IP tag handlers
    def ip_start(self):
        if self._inHttpd is not None and self._inKey is None:
            self._inKey = 'ip'
        else:
            raise FormatError(self.getpos())

    def ip_end(self):
        if self._inKey == 'ip' and self._inHttpd['ip'] is not None:
            self._inKey = None
        else:
            raise FormatError(self.getpos())

    # PORT tag handlers
    def port_start(self):
        if self._inHttpd is not None and self._inKey is None:
            self._inKey = 'port'
        else:
            raise FormatError(self.getpos())

    def port_end(self):
        if self._inKey == 'port' and self._inHttpd['port'] is not None:
            self._inKey = None
        else:
            raise FormatError(self.getpos())


class FormatError(Exception):
    def __init__(self, pos):
        super(FormatError, self).__init__()
        self.pos = pos

    def __str__(self):
        return "Formatting error at: " + str(self.pos)


def readHttpd(fname):
    parser = HttpdParser()
    return parser.read(fname)


if __name__ == "__main__":
    print readHttpd('../httpd.conf')
