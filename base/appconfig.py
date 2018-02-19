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
            'data_dir':os.path.sep.join((os.getcwd(), 'cached_data', 'session_data'))
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
        