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


def missingDependency(appname):
    '''
    get missing dependency and return list of missing dependency
    '''

    appconfig = getattr(__import__('application.{}.appconfig'.format(appname), fromlist=('AppConfig',)), 'AppConfig')

    # default dependency + appconfig dependency
    deps = ['gevent', 'bottle', 'pip', 'transcrypt'] + appconfig().appDependency()
    for dep in deps.copy():
        spec = find_spec(dep)
        if spec is not None:
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
        calloutput = subprocess.run('pushd {} && START /B CMD /C CALL {} appserver.py -s start {}'.format(appDir, sys.executable, ' '.join(param)), shell=True)

    else:
        calloutput = subprocess.run('cd {} && {} appserver.py -s start {} &'.format(appDir, sys.executable, ' '.join(param)), shell=True)

    print(calloutput)


def stopServer(args):
    '''
    stop server
    '''
    print('stop the server')
    appDir = os.path.sep.join((os.getcwd(), 'application', args.stop))

    if sys.platform.find('win') == 0:
        subprocess.run('pushd {} && {} appserver.py -s stop'.format(appDir, sys.executable), shell=True)

    else:
        subprocess.run('cd {} && {} appserver.py -s stop'.format(appDir, sys.executable), shell=True)


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
            calloutput = subprocess.run('{} get-pip.py'.format(sys.executable), shell=True)
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

            # updating all depedency
            pip.main(main['install', 'update'])

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


# starting point
def main():
    if sys.version_info.major < 3:
        print('#')
        print('-> only work on python version 3.x')
        print('#')
        sys.exit(1)

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

    # project creation management
    parser.add_argument('--setup', help='setup application (crate new application), --setup appname')
    args = parser.parse_args()

    # check setup command
    if args.setup:
        setupNewApp(args.setup)
        setupCheck(args.setup)

    # server start command
    elif args.start:
        setupCheck(args.start)
        startServer(args)

    # server stop command
    elif args.stop:
        stopServer(args)

    else:
        print('''
        usage:
            to setup project
            python3 app.py --setup appname

            to start
            python3 app.py --start appname [--host --port --reloader --debug --server --interval]

            to stop
            python3 app.py --stop appname
        ''')

# run the main
if __name__ == "__main__":
    main()
