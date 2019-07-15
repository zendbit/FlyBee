import os

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

        from bottle import static_file
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
        