#! /usr/bin/python

from AlarmClock import AlarmClock
from Clock import Clock
from HTTPServer import Server
from daemon import runner
from handlers import AuthHandler, ActionHandler
import config
import os
import sys


class OpenAlarm(object):

    def __init__(self, workingDir, dataDir):
        # initialize daemon settings
        self.stdin_path = '/dev/null'
        #self.stdout_path = workingDir + os.sep + 'OpenAlarm.out'
        #self.stderr_path = workingDir + os.sep + 'OpenAlarm.err'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path = '/tmp/OpenAlarm.pid'
        self.pidfile_timeout = 5
        self.data_dir = dataDir + os.sep
        self.source_dir = workingDir + os.sep

    def run(self):
        # try to read config files
        [authConfig, alarmsConfig, httpdConfig] = \
            config.readConfig(self.data_dir, self.source_dir)
        # create the page handler
        self.authHandler = AuthHandler(authConfig)
        # create action handler
        self.actionHandler = ActionHandler(alarmsConfig, self.authHandler)
        # create the alarms
        self.alarms = {'now': Clock()}
        for (name, alarm) in self.actionHandler:
            self.alarms[name] = AlarmClock(**alarm)
        # create the server
        Server._alarms = self.alarms
        self.server = Server.startServer(**httpdConfig)
        # run the server
        self.server.serve_forever()


# main function to execute
def main():
    # get directory paths
    (source_dir, data_dir) = config.getDirectories()
    # create the application
    app = OpenAlarm(source_dir, data_dir)
    # run the daemon
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()


# function to test code
def test():
    try:
        (source_dir, data_dir) = config.getDirectories()
        app = OpenAlarm(source_dir, data_dir)
        app.run()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'Usage: OpenAlarm run|start|stop|restart'
        print ' '
        print '    run:     Start server in the foreground'
        print '    start:   Launch the server as a daemon'
        print '    stop:    Stop a running server daemon'
        print '    restart: Restart a running server daemon'
        print ' '
    else:
        if sys.argv[1] == 'run':
            test()
        else:
            main()
