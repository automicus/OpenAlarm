'''
     OpenAlarm - AlarmClock Module
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
     This Python module contains the AlarmClock class that operates as an
     alarm clock. Actions can be set for when the alarm is activated,
     turned off, and snoozed.

     WRITTEN:     5/2013
'''


#import time, datetime
from Clock import Clock
from time import sleep
from threading import Thread
from datetime import timedelta, datetime

class AlarmClock(Clock):
    # default hardcoded option settings
    _hrInc = 1 # hours
    _minInc = 5 # minutes
    _sleepTime = 2 # seconds
    _snoozeTime = timedelta(minutes=5)
    _snoozeAvailFor = timedelta(minutes=20)

    # standard API functions
    def __init__(self, action, snooze=None, off=None, *args):
        # save arguments
        self._action = action
        self._off = off
        self._snooze = snooze
        # initialize status variables
        self._enabled = False
        self._sounding = False
        self.lastSounded = datetime(1987, 11, 30, 0, 0)
        # initialize alarm time
        self.setTime()
    def __repr__(self, *args):
        return 'Alarm Set For ' + self.getTime()
    
    # functions that manipulate the set time as a whole
    def getTime(self, *args):
        return self._setTime.strftime('%I:%M %p')
    def setTime(self, time=None, hour=0, minute=0, *args):
        if time is None:
            hour = int(float(hour))
            minute = int(float(minute))
            time = datetime(1987, 11, 30, hour, minute)
        self._setTime = time

    # functions that manipulate the set hour
    def getHour(self, *args):
        return self._setTime.strftime('%I')
    def setHour(self, val, *args):
        val = int(float(val))
        self._setTime = self._setTime.replace(hour=val)
        return self.getHour()
    def incHour(self, amount=None, *args):
        if amount is None or amount is '':
            inc_hours = self._hrInc
            off_hours = int(self.getHour()) % inc_hours
            self.incHour(amount = inc_hours-off_hours)
        else:
            amount = int(float(amount))
            self._setTime += timedelta(hours=amount) 
        return self.getHour()
    def decHour(self, amount=None, *args):
        if amount is None or amount is '':
            inc_hours = self._hrInc
            off_hours = int(self.getHour()) % inc_hours
            if off_hours == 0:
                self.decHour(amount = inc_hours)
            else:
                self.decHour(amount = off_hours)
        else:
            amount = int(float(amount))
            self._setTime -= timedelta(hours=amount) 
        return self.getHour()

    # functions that manipulate the set minute
    def getMinute(self, *args):
        return self._setTime.strftime('%M')
    def setMinute(self, val, *args):
        val = int(float(val))
        self._setTime = self._setTime.replace(minute=val)
        return self.getMinute()
    def incMinute(self, amount=None, *args):
        if amount is None or amount is '':
            inc_minutes = self._minInc
            off_minutes = int(self.getMinute()) % inc_minutes
            self.incMinute(amount = inc_minutes-off_minutes)
        else:
            amount = int(float(amount))
            self._setTime += timedelta(minutes=amount)
        return self.getMinute()
    def decMinute(self, amount=None, *args):
        if amount is None or amount is '':
            inc_minutes = self._minInc
            off_minutes = int(self.getMinute()) % inc_minutes
            if off_minutes == 0:
                self.decMinute(amount = inc_minutes)
            else:
                self.decMinute(amount = off_minutes)
        else:
            amount = int(float(amount))
            self._setTime -= timedelta(minutes=amount)
        return self.getMinute()

    # functions that manipulate AM/PM
    def getAmPm(self, *args):
        return self._setTime.strftime('%p')
    def setAmPm(self, val, *args):
        if val.upper() in ['AM', 'PM']:
            if val.upper() != self._setTime.strftime('%p'):
                self.incHour(12)
        return self.getAmPm()
    def incAmPm(self, *args):
        self.incHour(12)
        return self.getAmPm()
    def decAmPm(self, *args):
        return self.incAmPm()

    # alarm enabling and disabling
    def enable(self, *args):
        if not self._enabled:
            self._enabled = True
            Thread(target=self.__worker__).start()
    def disable(self, *args):
        self._enabled = False
    def enabled(self, *args):
        return self._enabled

    # functions that manipulate the snooze feature
    def snoozeAvailable(self, *args):
        out = self._snooze is not None
        out = out and (datetime.now() - self.lastSounded) < self._snoozeAvailFor
        return out
    def snooze(self, *args):
        if self._snooze is not None:
            if self.snoozeAvailable():
                self._snooze()
                self.setTime(self.nowPlus(self._snoozeTime))
                self.enable()
            else:
                raise SnoozeNotAvailable()
        else:
            raise SnoozeNotSetup()

    # functions that handle the alarm action itself
    def alert(self, *args):
        self._enabled = False
        self.lastSounded = datetime.now()
        self._action()
        if self._off is not None:
            self._sounding = True
    def off(self, *args):
        if self._off is not None:
            if self._sounding:
                self._off()
                self._sounding = False
            else:
                raise AlarmNotSounding()
        else:
            raise AlarmOffNotSetup()
    def sounding(self, *args):
        return self._sounding

    # private functions, not called directly
    def __worker__(self, *args):
        # wait to go off
        while self._enabled and (self.now() != self.getTime()):
            sleep(self._sleepTime)
        if self._enabled:
            # go off
            self.alert()

    # http interface to this class
    http = {'time': {'hour': {'get': getHour, 'set': setHour, 'inc': incHour, 'dec': decHour},
                     'minute': {'get': getMinute, 'set': setMinute, 'inc': incMinute, 'dec': decMinute},
                     'ampm': {'get': getAmPm, 'set': setAmPm, 'inc': incAmPm, 'dec': decAmPm},
                     'get': getTime},
            'status': {'get': enabled, 'enabled': enabled, 'sounding': sounding, 'snoozeavail': snoozeAvailable},
            'cmd': {'get': str, 'enable': enable, 'disable': disable, 'snooze': snooze, 'off': off},
            'get': getTime}

# Dummy functions for a test alarm
def __dummyAction__():
    print 'GOING OFF'
def __dummySnooze__():
    print 'SNOOZE SET'
def __dummyOff__():
    print 'ALARM TURNED OFF'
def __test__():
    a = alarm(action=__dummyAction__, 
        snooze=__dummySnooze__,
        off=__dummyOff__)
    return a

# Custom Exceptions
class SnoozeNotSetup(Exception): pass
class SnoozeNotAvailable(Exception): pass
class AlarmOffNotSetup(Exception): pass
class AlarmNotSounding(Exception): pass

