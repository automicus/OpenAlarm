from HTMLParser import HTMLParser


class AuthParser(HTMLParser):

    def __init_var__(self):
        # create status variables
        self._inAuth = False
        self._inRealm = None
        self._inKey = None
        self.realms = []

    def read(self, fname):
        self.__init_var__()
        cache = open(fname).read()
        self.feed(cache)
        out = self.realms
        self.__init_var__()
        return out

    # Default Syntax Handlers
    def handle_starttag(self, tag, attrs):
        #print 'START: ' + str(tag)
        if tag == 'auth':
            self.auth_start()
        elif tag == 'realm':
            self.realm_start()
        elif tag == 'url':
            self.url_start()
        elif tag == 'username':
            self.user_start()
        elif tag == 'password':
            self.pass_start()
        else:
            raise FormatError(self.getpos())

    def handle_endtag(self, tag):
        #print 'END: ' + str(tag)
        if tag == 'auth':
            self.auth_end()
        elif tag == 'realm':
            self.realm_end()
        elif tag == 'url':
            self.url_end()
        elif tag == 'username':
            self.user_end()
        elif tag == 'password':
            self.pass_end()
        else:
            raise FormatError(self.getpos())

    def handle_data(self, data):
        data = data.strip()
        if len(data) > 0:
            #print 'DATA: ' + str(data)
            if self._inAuth:
                if self._inRealm is not None:
                    self.realm_data(data)
                else:
                    self.auth_data(data)
            else:
                raise FormatError(self.getpos())

    # AUTH tag handlers
    def auth_start(self):
        if not self._inAuth:
            self._inAuth = True
        else:
            raise FormatError(self.getpos())

    def auth_end(self):
        if self._inAuth and self._inRealm is None:
            self._inAuth = False
        else:
            raise FormatError(self.getpos())

    def auth_data(self, data):
        raise FormatError(self.getpos())

    # REALM tag handlers
    def realm_start(self):
        if self._inAuth and self._inRealm is None:
            self._inRealm = {'url': None, 'user': None, 'pass': None}
        else:
            raise FormatError(self.getpos())

    def realm_end(self):
        if self._inRealm is not None and self._inKey is None:
            if self._inRealm['url'] is not None and \
                    self._inRealm['user'] is not None and \
                    self._inRealm['pass'] is not None:
                self.realms.append(self._inRealm)
                self._inRealm = None
            else:
                raise FormatError(self.getpos())
        else:
            raise FormatError(self.getpos())

    def realm_data(self, data):
        if self._inKey is not None:
            self._inRealm[self._inKey] = data
        else:
            raise FormatError(self.getpos())

    # URL tag handlers
    def url_start(self):
        if self._inRealm is not None and self._inKey is None:
            self._inKey = 'url'
        else:
            raise FormatError(self.getpos())

    def url_end(self):
        if self._inKey == 'url' and self._inRealm['url'] is not None:
            self._inKey = None
        else:
            raise FormatError(self.getpos())

    # USERNAME tag handlers
    def user_start(self):
        if self._inRealm is not None and self._inKey is None:
            self._inKey = 'user'
        else:
            raise FormatError(self.getpos())

    def user_end(self):
        if self._inKey == 'user' and self._inRealm['user'] is not None:
            self._inKey = None
        else:
            raise FormatError(self.getpos())

    # PASSWORD tag handlers
    def pass_start(self):
        if self._inRealm is not None and self._inKey is None:
            self._inKey = 'pass'
        else:
            raise FormatError(self.getpos())

    def pass_end(self):
        if self._inKey == 'pass' and self._inRealm['pass'] is not None:
            self._inKey = None
        else:
            raise FormatError(self.getpos())


class FormatError(Exception):
    def __init__(self, pos):
        super(FormatError, self).__init__()
        self.pos = pos

    def __str__(self):
        return "Formatting error at: " + str(self.pos)


def readAuth(fname):
    parser = AuthParser()
    return parser.read(fname)


if __name__ == "__main__":
    print readAuth('../auth.conf')
