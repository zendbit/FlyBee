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