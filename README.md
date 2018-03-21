# FlyBee
Python microservice framework based on bottle framework, fully compatible with bottle framework.

```
Tested on Windows and Unix Systems
```

#### Requirement:
- [Python 3.x](https://python.org)
- [Gevent](http://gevent.org)
- [Bottle](https://bottlepy.org)

This microframework will automatic resolve the depedencies using the configuration file with pip tools and make easy for deployment and development.

#### The framework only have:
- app.py
- base folder

#### app.py is for managing the application:
- creating new app
- start the server
- stop the server

#### How to create new project using flybee?

```
python app.py --setup myApplication
```

the command above will create new folder called application and your myApplication will be inside the application folder. in other word the applicatin folder will hold your application collection.

#### if you run again the command:

```
python app.py --setup myApplication2
```

you will have two application myApplication and myApplication2 under application folder.

#### after creating application what should I do? you just need to run command below to test application template is running:

```
python app.py --start myApplication
```

#### if can directly start and stop the application without application name parameter if we already set the default app

```
python app.py --default myApplication2
```

#### after set the default application can directly start and stop the application using --startdefault and --stopdefault

```
python app.py --startdefault
python app.py --stopdefault
```

#### to show the default application, we can use this command

```
python app.py --showdefault
```

#### to show available application, we can use this command

```
python app.py --showapps
```

the application will run on default port 8080, you can also change the configuration but we will talk deeper in other section.

#### now after application running you just need to point the browser to [http://localhost:8080](http://localhost:8080)

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-03-21%20at%2015.39.06.png "running the apps")

how to stop the application?

```
python app.py --stop myApplication
```

You can start more than one application but must with different port.

#### Application folder structure:

let we use the myApplication and myApplication2 as example, the apps that already created will placed under application folder. Look like this:

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-02-15%20at%2006.48.13.jpg "app struct")

Ok, let look inside the myApplication folder:

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-03-21%20at%2016.13.22.png "struct")

#### The main folder:
- plugins : this folder contain our library that not direct control to UI, like encryption, Oauth to thirdparty login, database access library, etc.
- sources : this folder contain main control for user response and request. Modify header, status code and return template view. This will interact with the client UI and will related with routes of the webapps.
- templates : this folder contain templating sistem, we use templating system from bottle framework.

The structure is not strict you can add more folder or file depend on your needs :-)

#### Take a look at the plugins folder:

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-02-15%20at%2007.21.37.jpg "plugins")

plugins folder contain some tools for managing the application like session, simple ecryption, http status code constant and system cleaner.

of course you can create custom plugin, and we can import it using import tag:

```
from plugins.session import Session
```

above example is for import Session class from plugins.session module.

#### Take a look at the sources folder:

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-02-15%20at%2007.29.42.jpg "source")

inside sources folder it just like ordinary python script, contain handler webapplication request and response, the sample is home.py that contain class Home and function index. But it's not restricted you can add functional paradigm rather than class paradigm.

sources/home.py

```
from bottle import template
from shared import Shared
from plugins.session import Session

class Home():

    def index(self):

        ################################################
        # example using session from -> from plugins.session import Session
        session = Session()

        #print(dir(bottle.ext))
        # set max session age, default is 30 days
        # parameter in seconds
        # session.setMaxAge(1)

        session.add('cd', '3')
        session.add('dvd', 3)

        sessionData = session.get()
        print(sessionData)

        session.remove('cd')
        sessionData = session.get()
        print(sessionData)

        #print(session.getExpired())

        # if you want to clear session use this method
        # session.clear()
        ###############################################

        # example using shared data for from -> from shared import Shared
        data = Shared().data()
        data['top_menu'] = {
            'start_flybee':'Start FlyBee',
            'about':'About',
            'get_started':'Get Started'
        }


        return template('templates/html/reactjs_sample/home.html', data=data)
```

from the code above we can see, there are some sample code how to use the session and shared data passing to the template reactjs_sample then return response as normal html page.

#### Take a look at the templates folder:

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-03-21%20at%2015.52.06.png "templates")

The template is contain html folder and contents folder, the sample is using reactjs_sample theme to make it. the html folder contain list of themes in this case example we have reactjs_sample themes and contents folder is contains the resource of the reactjs_sample (ie: js, css, image etc)

The template is fully compatible and same with bottle SimpleTemplate, if you use bottle framework i'ts like eating burger :D.

---

Ok then we will continue with application cofiguration, the application configuration contain:
- appconfig.py : contain application configuration, like session configuration, database connection, port, server address, ssl, etc. You can customize like what you want to do.
- appserver.py : this is contain application server starting point state, contain start stop the server, call cleaner system at start up, etc.
- shared.py : this is contain shared application variable that will be used accross the application so we don't need to re define it just call from the shared data.

```
class Shared():

    # return shared data used by template
    def data(self):

        data = {
            'page_title':'FlyBee Reactjs Sample',
            }

        return data


    # return client script used by template
    # css and script resource
    def clientScripts(self):

        scripts = {
            'reactjs_sample':{
                'link':[
                    #'href="/contents/grayscale/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet"',
                    #'href="/contents/grayscale/vendor/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css"',
                ],
                'script':[
                    'src="/templates/reactjs_sample/js/react/react.production.min.js"',
                    'src="/templates/reactjs_sample/js/react/react-dom.production.min.js"',
                    'src="/templates/reactjs_sample/js/react/babel.min.js"'
                ],
                'meta':[
                    #'charset="utf-8"',
                    #'name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"',
                ]
            }
        }

        return scripts
```

shared.py contain resource to shared accorss application, in the code above contain data() and clientScripts() shared resource.

the data() as you can see it called from the sources/home.py that will be pass to the template data.
the clientScripts() is contain definition of meta, link and javascript will be used for the templates, we can see that reactjs_sample containt the link, meta and script definition. This clientScripts() is called from templates/html/reactjs_sample/header.html

```
% from shared import Shared
<html>
    <head>
        <title>{{data.get('page_title')}}</title>

        <!-- add meta -->
        % scripts = Shared().clientScripts().get('reactjs_sample')
        % for meta in scripts.get('meta'):
        <meta {{!meta}}>
        % end

        <!-- add client link -->
        % for link in scripts.get('link'):
        <link {{!link}}>
        % end

        <!-- add client script -->
        % for script in scripts.get('script'):
        <script {{!script}}></script>
        % end
    </head>
    <body>
```

from this case we can create separate resource that useable from accross the aplication context. But the structure is not restricted you can modify like what you want to do :-D.

ok, this is the final parts. We will discuss about appconfig.py. This file is contain the applicatin configuration you can add the ssl certificate and key then your site will serve as https protocol [https://localhost:8080](https://localhost:8080). hmm easy isn't?

appconfig.py

```
import os
from bottle import static_file

class AppConfig():


    def appDependency(self):

        '''
        provide your app depedency will automatic install with pip
        ex:
        return = [
            'request',
            'gevent',
            'bottle',
        ]
        '''
        return [
        ]


    def databaseOptions(self):

        return {
            'sqlite':{
                'conn1':{
                    'pragma':['foreign_keys=1', 'case_sensitive_like=1', 'auto_vacuum=1'],
                    'dbfile':os.path.sep.join((os.getcwd(), 'cached_data', 'sqlite', 'example.db'))
                }
            },
            'mariadb':{
                'conn1':{
                    'host':'127.0.0.1',
                    'port':3306,
                    'user':'',
                    'password':'',
                    'db':'',
                    # see mysql_ssl_set() mysql documentation
                    # ssl conn
                    'ssl':{
                        'ca':None, # not require cert and key
                        'capath':None,
                        'cert':None,
                        'key':None,
                        'cipher':None
                    }
                }
            },
            'postgre':{
                'conn1':{
                    'host':'127.0.0.1',
                    'port':5432,
                    'user':'',
                    'password':'',
                    'db':'',
                    # ssl conn
                    'ssl':{
                        'sslrootcert':None, # not required sslcert and sslkey
                        'sslcert':None,
                        'sslkey':None
                    }
                }
            },
            'mongodb':{
                'conn1':{
                    'host':'127.0.0.1',
                    'port':27017,
                    'user':'',
                    'password':'',
                    # ssl conn
                    'ssl':{
                        'ssl_certfile':None,
                        'ssl_keyfile':None,
                        'ssl_pem_passphrase':None
                    }
                }
            }
        }


    def imapOptions(self):

        return {
            'imap1':{
                'server':'imap.gmail.com',
                'port':None,
                'user':'',
                'password':'',
                'ssl':{
                    'certfile':None,
                    'keyfile':None,
                    'password':None
                },
                'data_dir':os.path.sep.join((os.getcwd(), 'cached_data', 'mail'))
            }
        }


    def smtpOptions(self):
        '''
        you can add multiple email configuration (smtp)
        {
            'config1':{
                'server':'smtp.gmail.com',
                'port':None,
                'user':'',
                'password':'',
                'ssl':{
                    'certfile':None,
                    'keyfile':None,
                    'password':None
                }
            }
        }
        '''

        return {
            'smtp1':{
                'server':'',
                'port':None,
                'user':'',
                'password':'',
                'ssl':{
                    'certfile':None,
                    'keyfile':None,
                    'password':None
                }
            }
        }


    def sessionOptions(self):
        '''
        control session
        '''
        
        return {
            'default_max_age':604800,
            'data_dir':os.path.sep.join((os.getcwd(), 'cached_data', 'session_data')),
        }


    def serverOptions(self):
        '''
        default server option
        '''
        return {
            'host':'localhost',
            'port':8080,
            'reloader':True, # set to False for production
            'debug':True, # set to False for production
            'server':'gevent',
            'interval':1,
            'ssl':{
                # ssl cert file path ex: os.path.sep.join((os.getcwd(), 'ssl', 'server.crt'))
                'certfile':None,
                # ssl key file path ex: os.path.sep.join((os.getcwd(), 'ssl', 'server.key'))
                'keyfile':None
            }
        }


    def registerRoutes(self):
        '''
        routes of the application
        add custom routes with
        return [
            ['routes path', ['POST', 'GET', 'PUT', 'DELETE', ..etc], handler]
        ]
        '''

        from sources.home import Home

        return [
            # serving static file from each templates
            ['/templates/<filename:path>', 'GET', lambda filename: static_file(filename, root=os.path.sep.join([os.getcwd(), 'templates', 'contents']))],

            # home index test
            ['/', ['GET'], Home().index],
        ]

    
    def systemCleaner(self):
        '''
        System cleaner for cleaning session and other
        you can add other system cleaning here will run each 2 hour
        '''
        
        from plugins.session import Session

        return [
            Session().CleanExpiredSession
        ]
```

the appDependency(self) section is your list of dependency, will be installed using pip tool automatic and sync if target deployment is not meet the dependency.

for example if you use the pymongo for mongodb driver you can add it to the list like this:

```
def appDependency(self):

        '''
        provide your app depedency will automatic install with pip
        ex:
        return = [
            'request',
            'gevent',
            'bottle',
        ]
        '''
        return [
        'pymongo'
        ]
```

and your system will automatically sync and install the related dependency using pip tool, if target platform did not meet the dependency.

the sessionOptions(self), contain session configuration like max_age and session data folder to store the session file.

```
def sessionOptions(self):
        '''
        control session
        '''
        
        return {
            'default_max_age':604800,
            'data_dir':os.path.sep.join([os.getcwd(), 'plugins', 'session_data'])
        }
```

the default value is one week max age in seconds.

the serverOptions(self), contain configuration for server the default value is port 8080 but you can changes the value and configure to meet your need.

```
def severOptions(self):
        '''
        default server option
        '''
        return {
            'host':'localhost',
            'port':8080,
            'reloader':True, # set to False for production
            'debug':True, # set to False for production
            'server':'gevent',
            'interval':1,
            'ssl':{
                # ssl cert file path ex: os.path.sep.join((os.getcwd(), 'ssl', 'server.crt'))
                'certfile':None,
                # ssl key file path ex: os.path.sep.join((os.getcwd(), 'ssl', 'server.key'))
                'keyfile':None
            }
        }
```

for development it's okay to set the reloader and debug to True with interval value 1 seconds. It's mean the realoader will automatically reset te server to manage the code changes.

but if we want to deploy to production we need to change the value of reloader and debut to False.

the registerRoutes(self), this is contain route of our webapplication. This section will maping the the routes of our web and make it clear. For example if you want to pass request parameter routes, your function should meet the parameter of the routes definition

ex:

```
['/', ['GET'], Home().index] => this will serve the localhost:8080 to Home().index()

['/auth/login', ['GET', 'POST'], Auth().login] => this will serve the localhost:8080/auth/login to Auth().login()

['/user/<id>', ['GET', 'POST'], Employee().details] => this will serve the localhost:8080/user/1 to Employee().details(id)

['/user/<id>/<gid>', ['GET', 'POST'], Employee().details] => this will serve the localhost:8080/user/ to Employee().details(id, gid)
```

Ok, we finish the flybee framework structure then you also can pass the command option to override serverOptions

```
python app.py --start myApplication [--host --port --reloader --debug --interval --certfile --keyfile]

python app.py --start myApplication --host 192.168.1.100 --port 9090 --reloader false --debug false
```
