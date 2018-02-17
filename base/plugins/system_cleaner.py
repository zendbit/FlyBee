import os
from threading import Thread
import threading
from appconfig import AppConfig


class SystemCleaner():
    '''
    this startCleaner will execute each 2 hour to clean unused resource
    you can add the function to call when this cleaning session work by adding in
    AppConfig.py
    systemCleaner(self):
        return [
            functionToCall,
            functionToCall
        ]
    '''

    def __init__(self):

        self.__systemToClean = AppConfig().systemCleaner()


    def startCleaner(self):
        
        if not len([thread for thread in threading.enumerate() if thread.getName() == 'SystemCleanerThread']):

            def systemCleaner():
                while (True):
                    try:
                        for cleanSystem in self.__systemToClean:
                            cleanSystem()

                    except:
                        pass

                    threading.Event().wait(7200)

            systemCleanerThread = Thread(target=systemCleaner, name='SystemCleanerThread')
            systemCleanerThread.setDaemon(True)
            systemCleanerThread.start()