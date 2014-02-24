'''
    OpenAlarm - ActionHandler Module
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
    This Python module handles API action executions for OpenAlarm.
    
    WRITTEN:     5/2013
'''

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
            conn = urllib2.urlopen(url)
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
