class CreateTableExample():

    def __init__(self):
        self.createOrder = [
            'createUsers',
            'createAddress'
        ]


    def createUsers(self):

        return '''
            CREATE TABLE IF NOT EXISTS Users(
                userid INT UNSIGNED,
                username VARCHAR(255),
                PRIMARY KEY (userid, username)
            );
        '''

    def createAddress(self):

        return '''
            CREATE TABLE IF NOT EXISTS Address(
                uid INT UNSIGNED,
                uname VARCHAR(255),
                addrid INT UNSIGNED,
                addrname VARCHAR(255),
                PRIMARY KEY (addrid),
                FOREIGN KEY (uid, uname) REFERENCES Users(userid, username) ON DELETE CASCADE ON UPDATE NO ACTION
            );
        '''