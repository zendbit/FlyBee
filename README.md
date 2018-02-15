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
- source : this folder contain main control for user response and request. Modify header, status code and return template view. This will interact with the client UI and will related with routes of the webapps.
- template : this folder contain templating sistem, we use templating system from bottle framework.

The structure is not strict you can add more folder or file depend on your need :-)

#### Take look at the contents folder:
