from argparse import ArgumentParser
from importlib.util import find_spec

import os
import subprocess
import sys
import datetime
import sys
import urllib.request
import subprocess
import shutil
import socket
import glob


def missingDependency(appname):
    '''
    get missing dependency and return list of missing dependency
    '''

    import pip

    appconfig = getattr(__import__('application.{}.appconfig'.format(appname), fromlist=('AppConfig',)), 'AppConfig')

    # default dependency + appconfig dependency
    deps = ['gevent', 'bottle', 'pip', 'transcrypt', 'pymysql', 'psycopg2-binary', 'pymongo', 'anpylar'] + appconfig().appDependency()
    installedDeps = [pkg.key for pkg in pip.get_installed_distributions()]
    for dep in deps.copy():
        if dep in installedDeps:
            deps.remove(dep)

    return deps


def buildParameter(args):
    '''
    build parameter using given parameter
    '''
    param = []

    if args.host is not None:
        param.append('--host')
        param.append(args.host)

    if args.port is not None:
        param.append('--port')
        param.append(args.port)

    if args.reloader is not None:
        param.append('--reloader')
        param.append(args.reloader)

    if args.debug is not None:
        param.append('--debug')
        param.append(args.debug)

    if args.server is not None: 
        param.append('--server')
        param.append(args.server)

    if args.interval is not None: 
        param.append('--interval')
        param.append(args.interval)

    if args.certfile is not None: 
        param.append('--certfile')
        param.append(args.certfile)

    if args.keyfile is not None: 
        param.append('--keyfile')
        param.append(args.keyfile)

    return param


def startServer(args):
    '''
    start the server with givern parameter
    '''

    callouput = None
    param = buildParameter(args)

    print('emit the server...')

    appDir = os.path.sep.join((os.getcwd(), 'application', args.start))

    if sys.platform.find('win') == 0:
        calloutput = subprocess.run('pushd {} && START /B CMD /C CALL {} appserver.py -s start {}'.format(appDir, sys.executable, ' '.join(param)), shell=True, env={'LANG':'C'})

    else:
        calloutput = subprocess.run('cd {} && {} appserver.py -s start {} &'.format(appDir, sys.executable, ' '.join(param)), shell=True, env={'LANG':'C'})

    print(calloutput)


def stopServer(args):
    '''
    stop server
    '''
    print('stop the server')
    appDir = os.path.sep.join((os.getcwd(), 'application', args.stop))

    if sys.platform.find('win') == 0:
        subprocess.run('pushd {} && {} appserver.py -s stop'.format(appDir, sys.executable), shell=True, env={'LANG':'C'})

    else:
        subprocess.run('cd {} && {} appserver.py -s stop'.format(appDir, sys.executable), shell=True, env={'LANG':'C'})


def setupCheck(appname):
    '''
    check dependency when starting the application
    '''
    missDeps = missingDependency(appname)
    if len(missDeps) == 0:
        print('#')
        print('-> all depedency is complete')
        print('#')

    else:
        print('#')
        print('-> missing depedencies!')
        print('-> '.format(missDeps))
        # check if python pip is installeds
        try:
            missDeps.index('pip')
            print('=> installing pip from {}...'.format('https://bootstrap.pypa.io/get-pip.py'))
            urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')
            calloutput = subprocess.run('{} get-pip.py'.format(sys.executable), shell=True, env={'LANG':'C'})
            os.remove('get-pip.py')

        except ValueError:
            pass

        finally:
            # install the depedency if python pip is not missing
            import pip
            for dep in missDeps:
                print('=> installing {}...'.format(dep))
                if dep.find('transcrypt') != -1:
                    pip.main(['install', 'transcrypt'])

                else:
                    pip.main(['install', dep])

            try:
                # updating all depedency
                pip.main(main['install', 'update'])

            except Exception as ex:
                print(ex)

        print('#')


def setupNewApp(appname):
    '''
    crate application template for new project
    '''
    appDir = os.path.sep.join((os.getcwd(), 'application', appname))
    baseDir = os.path.sep.join((os.getcwd(), 'base'))
    print('# create new application {}'.format(appDir))
    if not os.path.isdir(appDir):
        try:
            shutil.copytree(baseDir, appDir)
            print('-------------------------')
            def printStructureApp(prefix, appDirStruct):
                for fileInDir in os.listdir(appDirStruct):
                    print('{}  {}'.format(prefix, fileInDir))
                    fileInDiPath = os.path.sep.join((appDirStruct, fileInDir))
                    if os.path.isdir(fileInDiPath):
                        printStructureApp(((' '*len(prefix)) + '  +----'), fileInDiPath)

            printStructureApp('----', appDir)

        except Exception as ex:
            print(ex)

    else:
        print('x directory already used, make sure application is not confict with other application {}'.format(appDir))
        print('#')
        sys.exit(1)


# set default app
def setDefaultApp(appname):
    appDir = os.path.sep.join((os.getcwd(), 'application', appname))
    defaultapp = os.path.sep.join((os.getcwd(), 'default.app'))
    if os.path.isdir(appDir):
        try:
            f = open(defaultapp, 'w+')
            f.write('{}'.format(appname))
            f.close()

        except Exception as ex:
            print('Failed set default app. {}'.format(ex))

    else:
        print('Failed set default app. No such application with name {}'.format(appname))


def getDefaultApp():
    appname = None
    defaultapp = os.path.sep.join((os.getcwd(), 'default.app'))
    if os.path.isfile(defaultapp):
        try:
            f = open(defaultapp, 'r')
            appname = f.readline().strip()
            f.close()

        except Exception as ex:
            print('Failed get default app. {}'.format(ex))

    else:
        print('Failed get default app. Default app not set yet.')

    return appname

def showApplicationList():
    appDir = glob.glob(os.path.sep.join((os.getcwd(), 'application', '*')))
    print('#')
    filteredApp = [fapp.split(os.path.sep)[-1] for fapp in appDir if os.path.isdir(fapp)]
    if len(filteredApp) != 0:
        for app in filteredApp:
            print('-> {}'.format(app))

    else:
        print('-> {}'.format('no available application'))
    print('#')

# starting point
def main():
    if sys.version_info.major < 3:
        print('#')
        print('-> only work on python version 3.x')
        print('#')
        sys.exit(1)

    defaultapp = getDefaultApp()

    parser = ArgumentParser()

    # server management
    parser.add_argument('--start', help='start the application, --start appname')
    parser.add_argument('--stop', help='stop the application, --stop appname')
    parser.add_argument('--host', help='set host of server')
    parser.add_argument('--port', help='set port of server', type=int)
    parser.add_argument('--reloader', help='set reloader of server for auto reload on development mode', type=bool)
    parser.add_argument('--debug', help='set debuging mode', type=bool)
    parser.add_argument('--server', help='set server for serving the application')
    parser.add_argument('--interval', help='reload interval for auto reload')
    parser.add_argument('--certfile', help='ssl cert file')
    parser.add_argument('--keyfile', help='ssl key file')
    parser.add_argument('--default', help='set default app, so we can only call app.py with param --startdefault and --stopdefault param. --default appname')
    parser.add_argument('--showdefault', help='show the default application, --showdefault', action='store_true')
    parser.add_argument('--showapps', help='show available application list, --showapps', action='store_true')
    parser.add_argument('--stopdefault', help='stop the default application, --stopdefault', action='store_true')
    parser.add_argument('--startdefault', help='start the default application, --startdefault', action='store_true')

    # project creation management
    parser.add_argument('--setup', help='setup application (crate new application), --setup appname')

    #defaultapp = getDefaultApp()
    #if defaultapp:
    #    parser.set_defaults(start=defaultapp, stop=defaultapp)

    #print(parser.get_default('start'))

    args = parser.parse_args()

    defaultapp = getDefaultApp()

    # check setup command
    if args.setup:
        setupNewApp(args.setup)
        setupCheck(args.setup)

    # server start command
    elif args.start:
        setupCheck(args.start)
        startServer(args)

    elif args.startdefault:
        if defaultapp:
            args.start = defaultapp
            setupCheck(args.start)
            startServer(args)

    # set default app
    elif args.default:
        setDefaultApp(args.default)

    # server stop command
    elif args.stop:
        stopServer(args)

    elif args.stopdefault:
        if defaultapp:
            args.stop = defaultapp
            stopServer(args)

    elif args.showdefault:
        print('#')
        print('-> {}'.format(getDefaultApp()))
        print('#')

    elif args.showapps:
        showApplicationList()

    else:
        print('''
        usage:
            to setup project
            python3 app.py --setup appname

            to start
            python3 app.py --start appname [--host --port --reloader --debug --server --interval]

            to stop
            python3 app.py --stop appname

            set default app
            python3 app.py --default appname

            start default app
            python3 app.py --startdefault [--host --port --reloader --debug --server --interval]

            stop default app
            python3 app.py --stopdefault

            show available application
            python3 app.py --showapps
        ''')

# run the main
if __name__ == "__main__":
    main()
