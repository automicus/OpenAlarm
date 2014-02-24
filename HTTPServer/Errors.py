'''
    OpenAlarm - HTTPServer - Errors Module
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
    This Python module contains the error prototypes that are raised
    inside of OpenAlarm's HTTP server.
    
    WRITTEN:     5/2013
'''

class HTTP404(Exception):
    def __init__(self):
        super(HTTP404, self).__init__()
        self.code = 404
    def __str__(self):
        return "404: Page Not Found"
    def __repr__(self):
        return self.__str__()
