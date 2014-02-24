'''
     OpenAlarm - Clock Module
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
     This Python module contains the an interface to the current time
     for OpenAlarm.

     WRITTEN:     5/2013
'''


#import time, datetime
from time import sleep
from datetime import timedelta, datetime

class Clock(object):

    # standard API functions
    def __init__(self, *args):
        pass
    def __repr__(self, *args):
        return 'Current Time: ' + self.now()
    def __str__(self, *args):
        return self.__repr__()
        
    # Functions that manipulate the current time
    def now(self, *args):
        return datetime.now().strftime('%I:%M %p')
    def nowHour(self, *args):
        return datetime.now().strftime('%I')
    def nowMinute(self, *args):
        return datetime.now().strftime('%M')
    def nowAmPm(self, *args):
        return datetime.now().strftime('%p')
    def nowPlus(self, delta=None, hours=0, minutes=0, *args):
        if delta is None:
            delta = timedelta(hours=hours, minutes=minutes)
        plustime = datetime.now() + delta
        return plustime

    # http interface to this class
    http = {'hour': {'get': nowHour},
            'minute': {'get': nowMinute},
            'ampm': {'get': nowAmPm},
            'get': now}
