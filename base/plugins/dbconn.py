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
        self._config = AppConfig().databaseOptions().get('mongodb').get(config)
        self._host = self._config.get('host')
        self._user = self._config.get('user')
        self._port = self._config.get('port')
        self._password = self._config.get('password')
        self._sslCertFile = self._config.get('ssl_certfile')
        self._sslKeyFile = self._config.get('ssl_keyfile')
        self._sslPassphrase = self._config.get('ssl_pem_passphrase')
        self._useSsl = False

        if self._sslCertFile and self._sslKeyFile:
            self._useSsl = True

        self._conn = None


    def connect(self):
        try:
            if self._user != '' and self._password:
                self._conn = pymongo.MongoClient(host=self._host, port=self._port, username=self._user, password=self._password, ssl=self._useSsl, ssl_certfile=self._sslCertFile, ssl_keyfile=self._sslKeyFile, ssl_pem_passphrase=self._sslPassphrase)

            else:
                self._conn = pymongo.MongoClient(host=self._host, port=self._port, ssl=self._useSsl, ssl_certfile=self._sslCertFile, ssl_keyfile=self._sslKeyFile, ssl_pem_passphrase=self._sslPassphrase)

        except Exception as ex:
            print(ex)

        return self._conn


    def close(self):
        if self._conn:
            self._conn.close()


####################################
# postgres connection
####################################
class PostgreConn():

    CODE_OK = 'ok'
    CODE_FAIL = 'fail'

    def __init__(self, config):
        self._config = AppConfig().databaseOptions().get('postgre').get(config)
        self._host = self._config.get('host')
        self._user = self._config.get('user')
        self._port = self._config.get('port')
        self._password = self._config.get('password')
        self._db = self._config.get('db')
        self._sslMode = 'disable'
        self._sslrootcert = None
        self._sslcert = None
        self._sslkey = None

        ssl = self._config.get('ssl')
        if ssl:
            self._sslrootcert = ssl.get('sslrootcert')
            self._sslcert = ssl.get('sslcert')
            self._sslkey = ssl.get('sslkey')

            if self._sslrootcert or self._sslcert or self._sslkey:
                self._sslMode = 'verify-full'

        self._conn = None


    def _connect(self):
        self._conn = psycopg2.connect(host=self._host, user=self._user, password=self._password, dbname=self._db, port=self._port, cursor_factory=psycopg2.extras.DictCursor, sslmode=self._sslMode, sslrootcert=self._sslrootcert, sslcert=self._sslcert, sslkey=self._sslkey)
        return self._conn.cursor()


    def _close(self):
        if self._conn:
            self._conn.close()

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
            cur = self._connect()
            cur.execute(query)
            self._conn.commit()
            outputMessage['code'] = PostgreConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self._close()

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
            cur = self._connect()
            cur.execute(query)
            data = cur.fetchall()
            outputMessage['code'] = PostgreConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'
            outputMessage['data'] = data

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self._close()

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
            cur = self._connect()
            cur.execute(query)
            data = cur.fetchone()
            outputMessage['code'] = PostgreConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'
            outputMessage['data'] = data

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self._close()

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
        self._config = AppConfig().databaseOptions().get('mariadb').get(config)
        self._host = self._config.get('host')
        self._user = self._config.get('user')
        self._port = self._config.get('port')
        self._password = self._config.get('password')
        self._db = self._config.get('db')
        self._ssl = {}

        ssl = self._config.get('ssl')
        if ssl:
            for sslcert in ssl:
                if ssl.get(sslcert):
                    self._ssl[sslcert] = ssl.ge(sslcert)

        self._conn = None


    def _connect(self):
        self._conn = pymysql.connect(host=self._host, user=self._user, password=self._password, db=self._db, port=self._port, cursorclass=pymysql.cursors.DictCursor, ssl=self._ssl)
        return self._conn.cursor()


    def _close(self):
        if self._conn:
            self._conn.close()

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
            cur = self._connect()
            cur.execute(query)
            self._conn.commit()
            outputMessage['code'] = MariaDbConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self._close()

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
            cur = self._connect()
            cur.execute(query)
            data = cur.fetchall()
            outputMessage['code'] = MariaDbConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'
            outputMessage['data'] = data

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self._close()

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
            cur = self._connect()
            cur.execute(query)
            data = cur.fetchone()
            outputMessage['code'] = MariaDbConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'
            outputMessage['data'] = data

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self._close()

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

        self._config = AppConfig().databaseOptions().get('sqlite').get(config)
        self._dbfile = self._config.get('dbfile')
        self._pragma = self._config.get('pragma')
        self._conn = None

        # init data dir if not exists
        dataDir = os.path.sep.join(self._dbfile.split(os.path.sep)[:-1])
        os.makedirs(dataDir, exist_ok=True)


    def _connect(self):
        # connect to sqlite file
        self._conn = sqlite3.connect(self._dbfile)
        self._conn.row_factory = sqlite3.Row
        return self._conn.cursor()


    def _close(self):
        if self._conn:
            self._conn.close()

    def _executePragma(self, cur):
        if self._pragma and len(self._pragma):
            cur.executescript(';'.join(['PRAGMA {}'.format(pragma) for pragma in self._pragma]))
            self._conn.commit()


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
            cur = self._connect()
            self._executePragma(cur)
            cur.execute(query)
            self._conn.commit()
            outputMessage['code'] = SqliteConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self._close()

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
            cur = self._connect()
            self._executePragma(cur)
            cur.execute(query)
            data = cur.fetchall()
            outputMessage['code'] = SqliteConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'
            outputMessage['data'] = data

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self._close()

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
            cur = self._connect()
            self._executePragma(cur)
            cur.execute(query)
            data = cur.fetchone()
            outputMessage['code'] = SqliteConn.CODE_OK
            outputMessage['message'] = 'Success executed sql command'
            outputMessage['data'] = data

        except Exception as ex:
            outputMessage['message'] = 'fail executed sql command {}'.format(ex)

        finally:
            self._close()

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

