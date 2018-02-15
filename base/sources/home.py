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
    