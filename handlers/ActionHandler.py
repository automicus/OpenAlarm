import urllib2


class ActionHandler(object):

    def __init__(self, alarmsConfig, authHandler):
        # store arguments
        self.authHandler = authHandler
        self.alarms = dict()
        for alarm in alarmsConfig:
            self.alarms[alarm['name']] = alarm

    def __getitem__(self, key):
        # retrieve actions for alarm
        if key in self.keys():
            alarm = self.alarms[key]
            out = dict()
            # create predefined functions for each action
            out['action'] = lambda: self.execUrl(alarm['action'])
            if alarm['snooze'] is not None:
                out['snooze'] = lambda: self.execUrl(alarm['snooze'])
            if alarm['off'] is not None:
                out['off'] = lambda: self.execUrl(alarm['off'])
            return out
        else:
            raise KeyError()

    def __iter__(self):
        for key in self.keys():
            yield (key, self[key])

    def keys(self):
        return self.alarms.keys()

    def execUrl(self, url):
        # authorize and open, watch for error codes
        self.authHandler.authorize()
        try:
            urllib2.urlopen(url)
            # conn.getcode()
        except urllib2.HTTPError, e:
            raise HTTPError(url, e.getcode())


# custom exceptions
class HTTPError(object):

    def __init__(self, url, code):
        super(HTTPError, self).__init__()
        self.url = url
        self.code = code

    def __str__(self):
        return "Request for URL: " + str(self.url) + "\n" + \
            "Returned Code: " + str(self.code)
