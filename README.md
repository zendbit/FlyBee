# FlyBee
Python microservice framework based on bottle framework, fully compatible with bottle framework.

```
Tested on Windows and Unix Systems
```

Requirement:
- [Python 3.x](https://python.org)
- [Gevent](http://gevent.org)
- [Bottle](https://bottlepy.org)

This microframework will automatic resolve the depedency in the configuration file using pip tools and make easy for deployment and development.

The framework only have:
- app.py
- base folder

app.py is for managing the application:
- creating new app
- start the server
- stop the server

How to create new project using flybee?

```
python app.py --setup myApplication
```

the command above will create new folder called application and your myApplication will be inside the application folder. in other word the applicatin folder will hold your application collection.

if you run again the command:

```
python app.py --setup myApplication2
```

you will have two application myApplication and myApplication2 under application folder.

after creating application what should I do? you just need to run command below to test application template is running:

```
python app.py --start myApplication
```

the command above will run your application on default port 8080, you can also change the configuration but we will talk deeper in other section.

now after application running you just need to point the browser to [http://localhost:8080](http://localhost:8080)

![alt text](https://raw.githubusercontent.com/zenvarlab/image-asset/master/Screen%20Shot%202018-02-15%20at%2006.29.40.jpg "running the apps")
