'''
    OpenAlarm - AlarmsParser Module
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
    This Python module reads the alarms.conf file associated with OpenAlarm.
    
    WRITTEN:     5/2013
'''

from HTMLParser import HTMLParser
import os

class AlarmsParser(HTMLParser):
    def __init_var__(self):
        # create status variables
        self._inAlarms = False
        self._inAlarm = None
        self._inKey = None
        self.alarms = []

    def read(self, fname):
        self.__init_var__()
        cache = open(fname).read()
        self.feed(cache)
        out = self.alarms
        self.__init_var__()
        return out

    # Default Syntax Handlers
    def handle_starttag(self, tag, attrs):
        #print 'START: ' + str(tag)
        if tag == 'alarms':
            self.alarms_start()
        elif tag == 'alarm':
            self.alarm_start()
        elif tag == 'name':
            self.name_start()
        elif tag == 'action':
            self.act_start()
        elif tag == 'snooze':
            self.snooze_start()
        elif tag == 'off':
            self.off_start()
        else:
            raise FormatError(self.getpos())
    def handle_endtag(self, tag):
        #print 'END: ' + str(tag)
        if tag == 'alarms':
            self.alarms_end()
        elif tag == 'alarm':
            self.alarm_end()
        elif tag == 'name':
            self.name_end()
        elif tag == 'action':
            self.act_end()
        elif tag == 'snooze':
            self.snooze_end()
        elif tag == 'off':
            self.off_end()
        else:
            raise FormatError(self.getpos())
    def handle_data(self, data):
        data = data.strip()
        if len(data) > 0:
            #print 'DATA: ' + str(data)
            if self._inAlarms:
                if self._inAlarm is not None:
                    self.alarm_data(data)
                else:
                    self.alarms_data(data)
            else:
                raise FormatError(self.getpos())

    # ALARMS tag handlers
    def alarms_start(self):
        if not self._inAlarms:
            self._inAlarms = True
        else:
            raise FormatError(self.getpos())
    def alarms_end(self):
        if self._inAlarms and self._inAlarm is None:
            self._inAlarms = False
        else:
            raise FormatError(self.getpos())
    def alarms_data(self, data):
        raise FormatError(self.getpos())

    # ALARM tag handlers
    def alarm_start(self):
        if self._inAlarms and self._inAlarm is None:
            self._inAlarm = {'name': None, 'action': None, 'snooze': None, 'off': None}
        else:
            raise FormatError(self.getpos())
    def alarm_end(self):
        if self._inAlarm is not None and self._inKey is None:
            if self._inAlarm['name'] is not None and self._inAlarm['action'] is not None:
                self.alarms.append(self._inAlarm)
                self._inAlarm = None
            else:
                raise FormatError(self.getpos())
        else:
            raise FormatError(self.getpos())
    def alarm_data(self, data):
        if self._inKey is not None:
            self._inAlarm[self._inKey] = data
        else:
            raise FormatError(self.getpos())

    # NAME tag handlers
    def name_start(self):
        if self._inAlarm is not None and self._inKey is None:
            self._inKey = 'name'
        else:
            raise FormatError(self.getpos())
    def name_end(self):
        if self._inKey == 'name' and self._inAlarm['name'] is not None:
            self._inKey = None
        else:
            raise FormatError(self.getpos())

    # ACTION tag handlers
    def act_start(self):
        if self._inAlarm is not None and self._inKey is None:
            self._inKey = 'action'
        else:
            raise FormatError(self.getpos())
    def act_end(self):
        if self._inKey == 'action' and self._inAlarm['action'] is not None:
            self._inKey = None
        else:
            raise FormatError(self.getpos())

    # SNOOZE tag handlers
    def snooze_start(self):
        if self._inAlarm is not None and self._inKey is None:
            self._inKey = 'snooze'
        else:
            raise FormatError(self.getpos())
    def snooze_end(self):
        if self._inKey == 'snooze':
            self._inKey = None
        else:
            raise FormatError(self.getpos())

    # OFF tag handlers
    def off_start(self):
        if self._inAlarm is not None and self._inKey is None:
            self._inKey = 'off'
        else:
            raise FormatError(self.getpos())
    def off_end(self):
        if self._inKey == 'off':
            self._inKey = None
        else:
            raise FormatError(self.getpos())


class FormatError(Exception):
    def __init__(self, pos):
        super(FormatError, self).__init__()
        self.pos = pos
    def __str__(self):
        return "Formatting error at: " + str(self.pos)

def readAlarms(fname):
    parser = AlarmsParser()
    return parser.read(fname)


if __name__=="__main__":
    print readAlarms(os.getenv('HOME') + '/.openAlarm/alarms.conf')
    
