import Errors
import Server


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
            if cmd is None or cmd is '':
                cmd = 'get'
                loop = False
            # find function set
            fun = fun[cmd]
            if type(fun) is not dict:
                loop = False

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
