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
