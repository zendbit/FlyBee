from appconfig import AppConfig
import sqlite3
import os
import pymysql
import pymysql.cursors
import psycopg2
import psycopg2.extras
import pymongo


####################################
# MongoDb connection
####################################
class MongoDbConn():

    def __init__(self, config):
        self.__config = AppConfig().databaseOptions().get('mongodb').get(config)
        self.__host = self.__config.get('host')
        self.__user = self.__config.get('user')
        self.__port = self.__config.get('port')
        self.__password = self.__config.get('password')
        self.__sslCertFile = self.__config.get('ssl_certfile')
        self.__sslKeyFile = self.__config.get('ssl_keyfile')
        self.__sslPassphrase = self.__config.get('ssl_pem_passphrase')
        self.__useSsl = False

        if self.__sslCertFile and self.__sslKeyFile:
            self.__useSsl = True

        self.__conn = None


    def connect(self):
        try:
            if self.__user != '' and self.__password:
                self.__conn = pymongo.MongoClient(host=self.__host, port=self.__port, username=self.__user, password=self.__password, ssl=self.__useSsl, ssl_certfile=self.__sslCertFile, ssl_keyfile=self.__sslKeyFile, ssl_pem_passphrase=self.__sslPassphrase)

            else:
                self.__conn = pymongo.MongoClient(host=self.__host, port=self.__port, ssl=self.__useSsl, ssl_certfile=self.__sslCertFile, ssl_keyfile=self.__sslKeyFile, ssl_pem_passphrase=self.__sslPassphrase)

        except Exception as ex:
            print(ex)

        return self.__conn


    def close(self):
        if self.__conn:
            self.__conn.close()


####################################
# postgres connection
####################################
class PostgreConn():

    CODE_OK = 'ok'
    CODE_FAIL = 'fail'

    def __init__(self, config):
        self.__config = AppConfig().databaseOptions().get('postgre').get(config)
        self.__host = self.__config.get('host')
        self.__user = self.__config.get('user')
        self.__port = self.__config.get('port')
        self.__password = self.__config.get('password')
        self.__db = self.__config.get('db')
        self.__conn = None


    def __connect(self):
        self.__conn = psycopg2.connect(host=self.__host, user=self.__user, password=self.__password, dbname=self.__db, port=self.__port, cursor_factory=psycopg2.extras.DictCursor)
        return self.__conn.cursor()


    def __close(self):
        if self.__conn:
            self.__conn.close()

    def execute(self, query):
        '''
        execute non return data query, like insert, update, delete data
        return value:
        {
            'code':'ok'|'fail',
            'message':'success message'|'error message'
        }
        '''

        outputMessage = {
            'code':PostgreConn.CODE_FAIL,
            'message':None
        }

        try:
            cur = self.__connect()
            cur.execute(query)
            self.__conn.commit()
            outputMessage['code'] = PostgreConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self.__close()

        return outputMessage


    def fetchAll(self, query):
        '''
        fetch all query data as list of row sqlite object
        {
            'code':'ok'|'fail',
            'message':'success message'|'error message',
            'data':None|[list of sqlite row object]
        }
        '''

        outputMessage = {
            'code':PostgreConn.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            cur = self.__connect()
            cur.execute(query)
            data = cur.fetchall()
            outputMessage['code'] = PostgreConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'
            outputMessage['data'] = data

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self.__close()

        return outputMessage


    def fetchOne(self, query):
        '''
        fetch one query data as single row sqlite object
        {
            'code':'ok'|'fail',
            'message':'success message'|'error message',
            'data':None|sqlite row object
        }
        '''

        outputMessage = {
            'code':PostgreConn.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            cur = self.__connect()
            cur.execute(query)
            data = cur.fetchone()
            outputMessage['code'] = PostgreConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'
            outputMessage['data'] = data

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self.__close()

        return outputMessage

    
    def createTable(self, models):
        """
        create table that will receive parameter as models of object creation of table

        for example we have the current class of creation table definition:

        the self.createOrder should be ordering of creation table

        class CreateTableExample():

            def __init__(self):
                self.createOrder = [
                    'createUsers',
                    'createAddress'
                ]


            def createUsers(self):

                return '''
                    CREATE TABLE IF NOT EXISTS Users(
                        userid INTEGER,
                        username VARCHAR(255),
                        PRIMARY KEY (userid, username)
                    );
                '''

            def createAddress(self):

                return '''
                    CREATE TABLE IF NOT EXISTS Address(
                        uid INTEGER,
                        uname VARCHAR(255),
                        addrid INTEGER,
                        addrname VARCHAR(255),
                        PRIMARY KEY (addrid),
                        FOREIGN KEY (uid, uname) REFERENCES Users(userid, username) ON DELETE CASCADE ON UPDATE NO ACTION
                    );
                '''

        {
            'code':'ok'|'fail',
            'message':'success message'|'error message',
            'data':None|[list of sqlite row object]
        }

        with class creation table above we can use as:
        
        from plugins.dbconn import PostgreConn
        conn = PostgreConn('conn1')
        conn.createTable(CreateTableExample())
        """

        outputMessage = {
            'code':PostgreConn.CODE_FAIL,
            'message':None
        }

        try:
            createOrder = getattr(models, 'createOrder')
            for create in createOrder:
                exeCreate = getattr(models, create)
                outputMessage = self.execute(exeCreate())

        except Exception as ex:
            outputMessage['message'] = 'fail executed create table command {}'.format(ex)

        return outputMessage


####################################
# mariadb and mysql connection
####################################
class MariaDbConn():

    CODE_OK = 'ok'
    CODE_FAIL = 'fail'

    def __init__(self, config):
        self.__config = AppConfig().databaseOptions().get('mariadb').get(config)
        self.__host = self.__config.get('host')
        self.__user = self.__config.get('user')
        self.__port = self.__config.get('port')
        self.__password = self.__config.get('password')
        self.__db = self.__config.get('db')
        self.__conn = None


    def __connect(self):
        self.__conn = pymysql.connect(host=self.__host, user=self.__user, password=self.__password, db=self.__db, port=self.__port, cursorclass=pymysql.cursors.DictCursor)
        return self.__conn.cursor()


    def __close(self):
        if self.__conn:
            self.__conn.close()

    def execute(self, query):
        '''
        execute non return data query, like insert, update, delete data
        return value:
        {
            'code':'ok'|'fail',
            'message':'success message'|'error message'
        }
        '''

        outputMessage = {
            'code':MariaDbConn.CODE_FAIL,
            'message':None
        }

        try:
            cur = self.__connect()
            cur.execute(query)
            self.__conn.commit()
            outputMessage['code'] = MariaDbConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self.__close()

        return outputMessage


    def fetchAll(self, query):
        '''
        fetch all query data as list of row sqlite object
        {
            'code':'ok'|'fail',
            'message':'success message'|'error message',
            'data':None|[list of sqlite row object]
        }
        '''

        outputMessage = {
            'code':MariaDbConn.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            cur = self.__connect()
            cur.execute(query)
            data = cur.fetchall()
            outputMessage['code'] = MariaDbConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'
            outputMessage['data'] = data

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self.__close()

        return outputMessage


    def fetchOne(self, query):
        '''
        fetch one query data as single row sqlite object
        {
            'code':'ok'|'fail',
            'message':'success message'|'error message',
            'data':None|sqlite row object
        }
        '''

        outputMessage = {
            'code':MariaDbConn.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            cur = self.__connect()
            cur.execute(query)
            data = cur.fetchone()
            outputMessage['code'] = MariaDbConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'
            outputMessage['data'] = data

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self.__close()

        return outputMessage

    
    def createTable(self, models):
        """
        create table that will receive parameter as models of object creation of table

        for example we have the current class of creation table definition:

        the self.createOrder should be ordering of creation table

        class CreateTableExample():

            def __init__(self):
                self.createOrder = [
                    'createUsers',
                    'createAddress'
                ]


            def createUsers(self):

                return '''
                    CREATE TABLE IF NOT EXISTS Users(
                        userid UNSIGNED INT,
                        username VARCHAR(255),
                        PRIMARY KEY (userid, username)
                    );
                '''

            def createAddress(self):

                return '''
                    CREATE TABLE IF NOT EXISTS Address(
                        uid UNSIGNED INT,
                        uname VARCHAR(255),
                        addrid UNSIGNED INT,
                        addrname VARCHAR(255),
                        PRIMARY KEY (addrid),
                        FOREIGN KEY (uid, uname) REFERENCES Users(userid, username) ON DELETE CASCADE ON UPDATE NO ACTION
                    );
                '''

        {
            'code':'ok'|'fail',
            'message':'success message'|'error message',
            'data':None|[list of sqlite row object]
        }

        with class creation table above we can use as:
        
        from plugins.dbconn import MariaDbConn
        conn = MariaDbConn('conn1')
        conn.createTable(CreateTableExample())
        """

        outputMessage = {
            'code':MariaDbConn.CODE_FAIL,
            'message':None
        }

        try:
            createOrder = getattr(models, 'createOrder')
            for create in createOrder:
                exeCreate = getattr(models, create)
                outputMessage = self.execute(exeCreate())

        except Exception as ex:
            outputMessage['message'] = 'fail executed create table command {}'.format(ex)

        return outputMessage


####################################
# sqlite connection
####################################
class SqliteConn():
    '''
    sqlite connection
    this connection will depend on the appconfig.py databseOptions:
    'sqlite':{
        'conn1':
        {
            'pragma':[the pragma list],
            'dbfile':path to database file
        }
    }

    usage:

    from plugins.dbconn import SqliteConn
    conn = SqliteConn('conn1')

    test initialize the table create:

    from.models.sqlite_example.example_create_table import CreateTableExample
    conn.createTable(CreateTableExample())

    all return value should be in form of:
    {
        'code':'ok'|'fail',
        'message':'success message'|'error message',
        'data':return value of data
    }

    data:

    fetchAll will return list of sqlite row object
    fetchOne will return one sqlite row object
    execute will no return any data
    '''

    CODE_OK = 'ok'
    CODE_FAIL = 'fail'

    def __init__(self, config):

        self.__config = AppConfig().databaseOptions().get('sqlite').get(config)
        self.__dbfile = self.__config.get('dbfile')
        self.__pragma = self.__config.get('pragma')
        self.__conn = None

        # init data dir if not exists
        dataDir = os.path.sep.join(self.__dbfile.split(os.path.sep)[:-1])
        os.makedirs(dataDir, exist_ok=True)


    def __connect(self):
        # connect to sqlite file
        self.__conn = sqlite3.connect(self.__dbfile)
        self.__conn.row_factory = sqlite3.Row
        return self.__conn.cursor()


    def __close(self):
        if self.__conn:
            self.__conn.close()

    def __executePragma(self, cur):
        if self.__pragma and len(self.__pragma):
            cur.executescript(';'.join(['PRAGMA {}'.format(pragma) for pragma in self.__pragma]))
            self.__conn.commit()


    def execute(self, query):
        '''
        execute non return data query, like insert, update, delete data
        return value:
        {
            'code':'ok'|'fail',
            'message':'success message'|'error message'
        }
        '''

        outputMessage = {
            'code':SqliteConn.CODE_FAIL,
            'message':None
        }

        try:
            cur = self.__connect()
            self.__executePragma(cur)
            cur.execute(query)
            self.__conn.commit()
            outputMessage['code'] = SqliteConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self.__close()

        return outputMessage


    def fetchAll(self, query):
        '''
        fetch all query data as list of row sqlite object
        {
            'code':'ok'|'fail',
            'message':'success message'|'error message',
            'data':None|[list of sqlite row object]
        }
        '''

        outputMessage = {
            'code':SqliteConn.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            cur = self.__connect()
            self.__executePragma(cur)
            cur.execute(query)
            data = cur.fetchall()
            outputMessage['code'] = SqliteConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'
            outputMessage['data'] = data

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self.__close()

        return outputMessage


    def fetchOne(self, query):
        '''
        fetch one query data as single row sqlite object
        {
            'code':'ok'|'fail',
            'message':'success message'|'error message',
            'data':None|sqlite row object
        }
        '''

        outputMessage = {
            'code':SqliteConn.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            cur = self.__connect()
            self.__executePragma(cur)
            cur.execute(query)
            data = cur.fetchone()
            outputMessage['code'] = SqliteConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'
            outputMessage['data'] = data

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self.__close()

        return outputMessage


    def createTable(self, models):
        """
        create table that will receive parameter as models of object creation of table

        for example we have the current class of creation table definition:

        the self.createOrder should be ordering of creation table

        class CreateTableExample():

            def __init__(self):
                self.createOrder = [
                    'createUsers',
                    'createAddress'
                ]


            def createUsers(self):

                return '''
                    CREATE TABLE IF NOT EXISTS Users(
                        userid UNSIGNED INT,
                        username VARCHAR(255),
                        PRIMARY KEY (userid, username)
                    );
                '''

            def createAddress(self):

                return '''
                    CREATE TABLE IF NOT EXISTS Address(
                        uid UNSIGNED INT,
                        uname VARCHAR(255),
                        addrid UNSIGNED INT,
                        addrname VARCHAR(255),
                        PRIMARY KEY (addrid),
                        FOREIGN KEY (uid, uname) REFERENCES Users(userid, username) ON DELETE CASCADE ON UPDATE NO ACTION
                    );
                '''

        {
            'code':'ok'|'fail',
            'message':'success message'|'error message',
            'data':None|[list of sqlite row object]
        }

        with class creation table above we can use as:
        
        from plugins.dbconn import SqliteConn
        conn = SqliteConn('conn1')
        conn.createTable(CreateTableExample())
        """

        outputMessage = {
            'code':SqliteConn.CODE_FAIL,
            'message':None
        }

        try:
            createOrder = getattr(models, 'createOrder')
            for create in createOrder:
                exeCreate = getattr(models, create)
                outputMessage = self.execute(exeCreate())

        except Exception as ex:
            outputMessage['message'] = 'fail executed create table command {}'.format(ex)

        return outputMessage

