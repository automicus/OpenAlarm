'''
    OpenAlarm - Config Module
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
    This module handles the configuration files for the OpenAlarm program.
    
    WRITTEN:     5/2013
'''

import os, platform
from shutil import copyfile
from AuthParser import readAuth
from AlarmsParser import readAlarms
from HttpdParser import readHttpd

# find source director
def getDirectories():
    # find source code dir
    source_dir = os.path.abspath(os.path.dirname(__file__) + os.sep + '..') + os.sep
    # find data directory
    if platform.system() in ['Linux', 'Darwin']:
        data_dir = os.getenv('HOME') + os.sep + '.openAlarm' + os.sep
    elif platform.system() is 'Windows':
        data_dir = os.getenv('APPDATA') + os.sep + 'openAlarm' + os.sep
    else:
        raise UnrecognizedOperatingSystem()
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    # return results    
    return (source_dir, data_dir)

# read configuration files
def readConfig(data_dir, source_dir):
    config_msg = ''
    try:
        authConfig = readAuth(data_dir + 'auth.conf')
    except IOError:
        copyfile(source_dir + 'template' + os.sep + 'auth.conf', data_dir + 'auth.conf')
        config_msg += '\n\nAn auth.conf template has been placed into the data directory.\nPlease configure it before use. '
    try:
        alarmsConfig = readAlarms(data_dir + 'alarms.conf')
    except IOError:
        copyfile(source_dir + 'template' + os.sep + 'alarms.conf', data_dir + 'alarms.conf')
        config_msg += '\n\nAn alarms.conf template has been placed into the data directory.\nPlease configure if before use. '
    try:
        httpdConfig = readHttpd(data_dir + 'httpd.conf')
    except IOError:
        copyfile(source_dir + 'template' + os.sep + 'httpd.conf', data_dir + 'httpd.conf')
        config_msg += '\n\nAn httpd.conf template has been placed into the data directory.\nPlease review this configuration before use. '
    if len(config_msg) > 0:
        config_msg += '\n\nThe data directory is: ' + data_dir
        raise ConfigurationNeeded(config_msg)
    return [authConfig, alarmsConfig, httpdConfig]


# custom exception
class UnrecognizedOperatingSystem(Exception):
    def __str__(self):
        return 'Your operating system (' + platform.system() + ') is not recognized by openAlarm.'
class ConfigurationNeeded(Exception):
    def __init__(self, msg):
        super(ConfigurationNeeded, self).__init__(self)
        self.msg = msg
    def __str__(self):
        return self.msg
