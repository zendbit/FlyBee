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


    def smtpOptions(self):
        '''
        you can add multiple email configuration (smtp)
        {
            'config1':{
                'server':'smtp.gmail.com',
                'port':0,
                'user':'',
                'password':'',
                'ssl':{
                    'certfile':None,
                    'keyfile':None
                }
            },
            'config2':{
                'server':'smtp.server1.com',
                'port':0,
                'user':'',
                'password':'',
                'ssl':{
                    'certfile':None,
                    'keyfile':None
                }
            }
        }
        '''

        return {
            'mailer_1':{
                'server':'',
                'port':0,
                'user':'',
                'password':'',
                'ssl':{
                    'certfile':None,
                    'keyfile':None
                }
            }
        }


    def sessionOptions(self):
        '''
        control session
        '''
        
        return {
            'default_max_age':604800,
            'data_dir':os.path.sep.join([os.getcwd(), 'plugins', 'session_data'])
        }


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
            # serving static file
            ['/contents/<filename:path>', 'GET', lambda filename: static_file(filename, root=os.path.sep.join([os.getcwd(), 'contents']))],

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
        