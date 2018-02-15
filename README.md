# FlyBee
Python microservice framework based on bottle framework, fully compatible with bottle framework.

```
Tested on Windows and Unix Systems
```

#### Requirement:
- [Python 3.x](https://python.org)
- [Gevent](http://gevent.org)
- [Bottle](https://bottlepy.org)

This microframework will automatic resolve the depedency in the configuration file using pip tools and make easy for deployment and development.

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

the command above will run your application on default port 8080, you can also change the configuration but we will talk deeper in other section.

#### now after application running you just need to point the browser to [http://localhost:8080](http://localhost:8080)

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-02-15%20at%2006.29.40.jpg "running the apps")

how to stop the application?

```
python app.py --stop myApplication
```

You can start more than one application but must with different port.

#### Application folder structure:

let we use the myApplication and myApplication2 as example, the app that we create will placed under application folder. Look like this:

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-02-15%20at%2006.48.13.jpg "app struct")

Ok, let look inside the myApplication folder:

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-02-15%20at%2006.55.06.jpg "struct")

#### The main folder:
- contents : will serving for static file like css, image, javascript, etc. We can add more static serving, but we will discuss later.
- plugins : this folder contain our library that not direct control to UI, like encryption, Oaut to thidrparty login, database access library, etc.
- sources : this folder contain main control for user response and request. Modify header, status code and return template view. This will interact with the client UI and will related with routes of the webapps.
- templates : this folder contain templating sistem, we use templating system from bottle framework.

The structure is not strict you can add more folder or file depend on your need :-)

#### Take a look at the contents folder:

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-02-15%20at%2007.14.22.jpg "contents")

as we can see, the folder content contain themes called grayscale and inside the theme contain the asset for the grayscale them. the main purpose is we can add more theme and keep it separated between them.

#### Take a look at the plugins folder:

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-02-15%20at%2007.21.37.jpg "plugins")

plugins folder contain some tools for managing the application like session, simple ecryption, http status code constant and system cleaner.

of course you can create custom plugin, and we can import it accross the application using import tag:

```
from plugins.session import Session
```

above example is for import Session class from plugins.session module.

#### Take a look at the sources folder:

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-02-15%20at%2007.29.42.jpg "source")

inside source folder is just like ordinary python script, contain handler webapplication request and response, the sample is home.py that contain class Home and function index. But it's not restricted you can add functional paradigm not class paradigm.

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


        return template('templates/grayscale/home.html', data=data)
```

from the code above we can see, than there is some sample code of using the session and shared data passing to the template grayscale then return response as normal html page.

#### Take a look at the templates folder:

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-02-15%20at%2007.39.44.jpg "templates")

The template is contain the html text, the sample is using them grayscale to make it consistent with the content/grayscale. So if we need to create new them we can create in separate folder :-).

The template is fully compatible and same with bottle SimpleTemplate, if you use bottle framework i'ts like eating burger :D.

---

Ok then we will continue with application cofiguration, the application configuration contain:
- appconfig.py : contain application configuration like, session configuration, database connection, port, server address, ssl, etc. You can customize like what you want to do.
- appserver.py : this is contain application server starting point state, contain start stop the server, call cleaner system at start up, etc.
- shared.py : this is contain shared application variable that will be used or always used on accross the application so we don't need to re define it just call from the shared data.

- shared.py
