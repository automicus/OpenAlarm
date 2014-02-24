'''
    OpenAlarm - HTTPServer - Pages Module
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
    This Python module renders the "web pages" returned for API requests
    that are made to OpenAlarm's HTTP Server.
    
    WRITTEN:     5/2013
'''

import Server, Errors

def root(args=[]):
    out = ""
    for (name, alarm) in Server._alarms.iteritems():
        out += name + ': ' + str(alarm) + "\n"
    return out

def known_alarm(name, args=[]):
    alarm = Server._alarms[name]
    loop = True
    fun = alarm.http
    try:
        while loop:
            # get next command
            cmd = args.next()
            if cmd is None or cmd is '': cmd='get'; loop=False
            # find function set
            fun = fun[cmd]
            if type(fun) is not dict: loop=False

    except KeyError:
        raise Errors.HTTP404()

    else:
        return fun(alarm, args.next())

def unknown_alarm(name, args):
    raise Errors.HTTP404() 

def getPage(name):
    if name == '' or name is None:
        return root
    else:
        if name in Server._alarms.keys():
            return lambda args: known_alarm(name, args)
        else:
            return lambda args: unknown_alarm(name, args)
