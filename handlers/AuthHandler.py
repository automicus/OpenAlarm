'''
    OpenAlarm - AuthHandler Module
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
    This Python module handles realm authentification for OpenAlarm.
    
    WRITTEN:     5/2013
'''

import urllib, urllib2

class AuthHandler(object):
    def __init__(self, auth_data):
        self._auth = auth_data

    def authorize(self):
        for entry in self._auth:
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, entry['url'], entry['user'], entry['pass'])
            authhandler = urllib2.HTTPBasicAuthHandler(passman)
            opener = urllib2.build_opener(authhandler)
            urllib2.install_opener(opener)
