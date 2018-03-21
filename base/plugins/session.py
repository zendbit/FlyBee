from bottle import response, request
import datetime
from hashlib import md5
import os
import pickle
import inspect
from appconfig import AppConfig
from pickle import Pickler, Unpickler

class Session():

    def __init__(self):

        self.__sessionOption = AppConfig().sessionOptions()

        # check if folder not exist then create the data dir
        dataDir = self.__sessionOption.get('data_dir')
        if dataDir and not os.path.isdir(dataDir):
            try:
                os.makedirs(dataDir)

            except Exception as ex:
                print(ex)

        # initialize session
        # add default session
        currentUtcTime = self.__getCurrentUtcTimeHash()

        # init session if not exist
        request.get_cookie('s', currentUtcTime.get('hexdigest'))


    def __readSessionFile(self, sessionFile):

        loadedData = dict()

        f = None
        try:
            f = open(sessionFile, mode='rb')
            loadedData = Unpickler(f).load()

        except Exception as e:
            print('Warning when read session file %s' % e)
            
        finally:
            if f:
                f.close()

        return loadedData


    def _writeSessionFile(self, sessionFile, loadedData):

        f = None
        try:
            f = open(sessionFile, mode='wb')
            Pickler(f, protocol=pickle.HIGHEST_PROTOCOL).dump(loadedData)

        except Exception as e:
            print('Warning when read session file %s' % e)
            
        finally:
            if f:
                f.close()


    def setMaxAge(self, maxAge):

        '''
        setMaxAge(value)
        set max age of the session
        '''
        try:
            currentUtcTime = self.__getCurrentUtcTimeHash()

            # get cookie from current request if not exist just add it
            cookieSessionData = request.get_cookie('s', currentUtcTime.get('hexdigest'))

            # create session file
            if os.path.isdir(self.__sessionOption.get('data_dir')):
                sessionFile = os.path.join(self.__sessionOption.get('data_dir'), cookieSessionData)

                if os.path.isfile(sessionFile):
                    loadedData = self.__readSessionFile(sessionFile)

                    # set max ages for current session
                    if isinstance(loadedData, dict):
                        loadedData['max_age'] = maxAge

                    self._writeSessionFile(sessionFile, loadedData)

            response.set_cookie('s', cookieSessionData, max_age=maxAge)

        except Exception as e:
            print (e)


    def __getCurrentUtcTimeHash(self):

        utcdt = datetime.datetime.utcnow().isoformat()
        mdsHash = md5(utcdt.encode('utf-8'))

        utcnowDiggest = {'utc_datetime':utcdt, 'hexdigest':mdsHash.hexdigest()}

        return utcnowDiggest


    def add(self, key, value):

        '''
        add(key, value)
        add value to session, if key already exist will update the last value
        '''
        try:
            currentUtcTime = self.__getCurrentUtcTimeHash()

            # get cookie from current request if not exist just add it
            cookieSessionData = request.get_cookie('s', currentUtcTime.get('hexdigest'))

            # create session file
            if os.path.isdir(self.__sessionOption.get('data_dir')):
                sessionFile = os.path.join(self.__sessionOption.get('data_dir'), cookieSessionData)

                isNotNewSession = os.path.isfile(sessionFile)

                loadedData = dict()

                if isNotNewSession:
                    loadedData = self.__readSessionFile(sessionFile)

                if isinstance(loadedData, dict):
                    loadedData[key] = value

                    # if default max_ages None set default to 30 days 2592000 seconds
                    # if max ages is not defined ye then add to session data and cookies data
                    if (loadedData.get('max_age') is None):
                        loadedData['max_age'] = self.__sessionOption.get('default_max_age')

                    # add created date if not exist in the data
                    if (loadedData.get('date_created') is None):
                        loadedData['date_created'] = currentUtcTime['utc_datetime']

                self._writeSessionFile(sessionFile, loadedData)

                # set default max age if new
                if (not isNotNewSession):
                    response.set_cookie('s', cookieSessionData, max_age=self.__sessionOption.get('default_max_age'))

                else:
                    response.set_cookie('s', cookieSessionData)

            else:
                raise Exception('Session dir is not exist %s' % self.__sessionOption.get('data_dir'))

        except Exception as e:
            print(e)


    def clear(self):

        '''
        clear()
        clear all instance of session
        '''
        try:
            currentUtcTime = self.__getCurrentUtcTimeHash()

            # get cookie from current request if not exist just add it
            cookieSessionData = request.get_cookie('s', currentUtcTime.get('hexdigest'))

            # create session file
            if os.path.isdir(self.__sessionOption.get('data_dir')):
                sessionFile = os.path.join(self.__sessionOption.get('data_dir'), cookieSessionData)

                if (os.path.isfile(sessionFile)):
                    os.remove(sessionFile)

            response.set_cookie('s', cookieSessionData, max_age=0)
            response.delete_cookie(cookieSessionData)

        except Exception as e:
            print(e)


    def get(self, key=None):

        '''
        get()
        get available current session session
        '''
        sessionData = None
        try:
            currentUtcTime = self.__getCurrentUtcTimeHash()

            # get cookie from current request if not exist just add it
            cookieSessionData = request.get_cookie('s', currentUtcTime.get('hexdigest'))

            # create session file
            if os.path.isdir(self.__sessionOption.get('data_dir')):
                sessionFile = os.path.join(self.__sessionOption.get('data_dir'), cookieSessionData)

                if os.path.isfile(sessionFile):
                    if key:
                        sessionData = self.__readSessionFile(sessionFile).get(key)

                    else:
                        sessionData = self.__readSessionFile(sessionFile)

        except Exception as e:
            print(e)

        return sessionData


    def remove(self, key):

        '''
        remove(key)
        remove session key, will return deleted session key value pair {key, value}
        '''
        removedData = {}

        try:
            currentUtcTime = self.__getCurrentUtcTimeHash()

            # get cookie from current request if not exist just add it
            cookieSessionData = request.get_cookie('s', currentUtcTime.get('hexdigest'))

            # create session file
            if os.path.isdir(self.__sessionOption.get('data_dir')):
                sessionFile = os.path.join(self.__sessionOption.get('data_dir'), cookieSessionData)

                if os.path.isfile(sessionFile):
                    loadedData = self.__readSessionFile(sessionFile)

                    if isinstance(loadedData, dict):

                        if loadedData.get(key) is not None:
                            removedData[key] = loadedData.pop(key)

                    self._writeSessionFile(sessionFile, loadedData)

        except Exception as e:
            print(e)

        return removedData


    def getExpired(self):

        '''
        getExpired()
        get expired session file, will return list of absolute path from expired session file
        '''
        expiredSession = list()

        if os.path.isdir(self.__sessionOption.get('data_dir')):

            files = os.listdir(self.__sessionOption.get('data_dir'))
            for fname in files:

                sessionFile = os.path.sep.join([self.__sessionOption.get('data_dir'), fname])
                if os.path.isfile(sessionFile):
                    sessionData = self.__readSessionFile(sessionFile)

                    if isinstance(sessionData, dict):
                        sessionDatetime = sessionData.get('date_created')
                        sessionMaxAge = sessionData.get('max_age')

                        if sessionDatetime is not None and sessionMaxAge is not None:
                            timeDelta = datetime.datetime.utcnow() - datetime.datetime.strptime(sessionDatetime, '%Y-%m-%dT%H:%M:%S.%f')

                            totalTimeDeltaInSeconds = timeDelta.days*86400 + timeDelta.seconds
                            
                            # if expired add to expiredSession
                            if totalTimeDeltaInSeconds >= sessionMaxAge:
                                expiredSession.append(sessionFile)

        return expiredSession


    def CleanExpiredSession(self):

        for expiredSession in self.getExpired():
            os.remove(expiredSession)
            