# using gevent service
from gevent import monkey; monkey.patch_all()
from bottle import route, run, template, request, Bottle, static_file
from shared import Shared
from appconfig import AppConfig
from argparse import ArgumentParser
from plugins.system_cleaner import SystemCleaner
from plugins.session import Session

import os
import subprocess
import sys
import socket
import bottle
import builtins


appserverPIDFile = 'appserver.id'


def writePID(appPID):
    result = False

    try:
        f = open(appserverPIDFile, mode='w')
        f.write('{}'.format(appPID))
        f.close()
        result = True

    except Exception as ex:
        print(ex)

    return result


def readPID():
    pid = None

    try:
        f = open(appserverPIDFile, mode='r')
        pid = f.readline().strip()
        f.close()

    except Exception as ex:
        print(ex)

    return pid


# override the builtins function
# don't print if debug is False
def overrideBuiltinPrint():
    _print = print

    def debugPrint(*args, **kwargs):
        if AppConfig().serverOptions().get('debug'):
            _print(*args, **kwargs)
            
    builtins.print = debugPrint


def serverStart(kwargs={}):
    app = Bottle()
    appConfig = AppConfig()
    bottle.TEMPLATES.clear()

    # register routes
    for appRoute in appConfig.registerRoutes():
        app.route(appRoute[0], appRoute[1], appRoute[2])

    # start system cleaner
    SystemCleaner().startCleaner()

    # init the session
    Session()

    serverOptions = appConfig.serverOptions()
    host = serverOptions.get('host') if not kwargs.get('host') else kwargs.get('host')
    port = serverOptions.get('port') if not kwargs.get('port') else kwargs.get('port')
    reloader = serverOptions.get('reloader') if not kwargs.get('reloader') else kwargs.get('reloader')
    debug = serverOptions.get('debug') if not kwargs.get('debug') else kwargs.get('debug')
    server = serverOptions.get('server') if not kwargs.get('server') else kwargs.get('server')
    interval = serverOptions.get('interval') if not kwargs.get('interval') else kwargs.get('interval')
    certfile = serverOptions.get('ssl').get('certfile') if not kwargs.get('certfile') else kwargs.get('certfile')
    keyfile = serverOptions.get('ssl').get('keyfile') if not kwargs.get('keyfile') else kwargs.get('keyfile')
    
    if os.access(os.getcwd(), os.W_OK) or (os.is_file(appserverPIDFile) and os.access(appserverPIDFile, os.W_OK)):
        # try to check the address already bind or not
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        alreadyRun = False
        try:
            s.bind((host, port))
            writePID(str(os.getpid()))

        except Exception as ex:
            alreadyRun = True
            print('server already running or address already in used {}:{} -> {}'.format(host, port, ex))

            # if in debug mode try kill the server and force alradyRun to false
            if reloader and debug:
                if serverStop(kwargs) == 0:
                    alreadyRun = False

        finally:
            s.close()

        if not alreadyRun:
            overrideBuiltinPrint()

            if certfile is None or keyfile is None:
                run(app=app, host=host, port=port, reloader=reloader, debug=debug, server=server, interval=interval)

            else:
                run(app=app, host=host, port=port, reloader=reloader, debug=debug, server=server, interval=interval, certfile=certfile, keyfile=keyfile)

        else:
            print('----------')
            print('| server already running or address already in used {}:{} |'.format(host, port))
            print('----------')


    else:
        print('''You don't have write access to {}, need read write access!'''.format(os.getcwd()))


def serverStop(kwargs={}):
    returnCode = 0
    pids = readPID()

    if pids and pids.strip() != '':
        calloutput = None

        if sys.platform.find('win') == 0:
            calloutput = subprocess.run('''taskkill /F /PID {}'''.format(pids), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={'LANG':'C'})
        else:
            calloutput = subprocess.run('''kill -9 {}'''.format(pids), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={'LANG':'C'})
            
        print(calloutput)
        returnCode = calloutput.returncode

        if calloutput and calloutput.returncode == 0:
            try:
                os.remove('appserver.id')   
            except Exception as ex:
                print(ex)

    return returnCode


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', help='send signal to server (start|stop)')
    parser.add_argument('--host', help='set host of server')
    parser.add_argument('--port', help='set port of server', type=int)
    parser.add_argument('--reloader', help='set reloader of server for auto reload on development mode', type=bool)
    parser.add_argument('--debug', help='set debuging mode', type=bool)
    parser.add_argument('--server', help='set server for serving the application')
    parser.add_argument('--interval', help='reload interval for auto reload')
    parser.add_argument('--certfile', help='ssl cert file')
    parser.add_argument('--keyfile', help='ssl key file')

    args = parser.parse_args()

    kwargs = {
        'host':args.host,
        'port':args.port,
        'reloader':args.reloader,
        'debug':args.debug,
        'server':args.server,
        'intervel':args.interval,
        'certfile':args.certfile,
        'keyfile':args.keyfile
    }

    if args.s == 'start':
        serverStart(kwargs)

    elif args.s == 'stop':
        serverStop(kwargs)

    else:
        print('''
        usage:

            to start
            python3 appserver.py -s start [--host --port --reloader --debug --server --interval --certfile --keyfile] &

            to stop
            python3 appserver.py -s stop
        ''')
