import urllib2


class AuthHandler(object):

    def __init__(self, auth_data):
        self._auth = auth_data

    def authorize(self):
        for entry in self._auth:
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, entry['url'],
                                 entry['user'], entry['pass'])
            authhandler = urllib2.HTTPBasicAuthHandler(passman)
            opener = urllib2.build_opener(authhandler)
            urllib2.install_opener(opener)
