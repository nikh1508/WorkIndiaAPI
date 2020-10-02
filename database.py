import mysql.connector
import logging
import sys

logging.basicConfig(filename='server.log', format='[%(levelname)-7s] : %(asctime)s : %(name)-8s : %(message)s',
                    level=logging.DEBUG, datefmt='%b %d, %g | %H:%M:%S')

log = logging.getLogger(__name__)
mydb = None
cursor = None
connected = False


def connect_DB():
    global mydb, cursor, connected
    try:
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='workindia_user',
            passwd='user_password',
        )
        log.info('connected to database')
        connected = True
        cursor = mydb.cursor()
        cursor.execute('USE {}'.format('test_db'))
    except mysql.connector.Error as err:
        log.error('Could not connect to Mysql server. Error : {}'.format(err))
        sys.exit(-1)


def createUser(user):
    if not connected:
        return False
    log.info('Creating new user: {}'.format(user['username']))
    row = ('INSERT INTO users(userID, username, password) '
           'VALUES(NULL, %s, %s)')
    try:
        cursor.execute(row, (user['username'], user['password']))
        mydb.commit()
        return True
    except mysql.connector.Error as err:
        mydb.rollback()
        log.error('Could not insert into the table. Error : {}'.format(err))
    return False


def validatePass(db_row, password):
    return db_row[2] == password


def userExists(userID):
    try:
        cursor.execute(
            'SELECT userID FROM users WHERE userID={}'.format(userID))
        res = cursor.fetchall()
        return len(res) > 0
    except mysql.connector.Error as err:
        log.error('Could not fetch credentials. Error:: {}'.format(err))
    return False


def validateUser(user):
    response = {'found': False, 'auth': False, 'userID': None}
    if not connected:
        return False
    log.info('Validating user')
    try:
        cursor.execute(
            "SELECT * FROM users where username='{}'".format(user['username']))
        rows = cursor.fetchall()
        if(len(rows) == 0):
            return response
        response['found'] = True
        if validatePass(rows[0], user['password']):
            response['auth'] = True
            response['userID'] = rows[0][0]
    except mysql.connector.Error as err:
        log.error('Could not fetct users')
    return response


def addWebsitePass(data):
    log.info('Adding new website credentials')
    row = ('INSERT INTO website_directory(id, userID, website, username, password) '
           'VALUES(NULL, %s, %s, %s, %s)')

    try:
        cursor.execute(row, (data['userID'], data['website'],
                             data['username'], data['password']))
        mydb.commit()
        return True
    except mysql.connector.Error as err:
        log.error('Could not add website entry. Error:: {}'.format(err))
    return False


def getAllWebsites(userID):
    log.info('Fetching All Website Credentials')
    try:
        cursor.execute(
            'SELECT website, username, password FROM website_directory WHERE userID={}'.format(userID))
        res = cursor.fetchall()
        return res
    except mysql.connector.Error as err:
        log.error('Could not fetch credentials. Error:: {}'.format(err))


# connect_DB()
# # createUser({'username': 'test', 'password': 'testpass'})
# # print(validateUser({'username': 'test', 'password': 'testpass'}))
# # print(addWebsitePass({'userID': 100, 'website': 'www.abcxyz.com',
# #                       'username': 'test', 'password': 'testpass'}))

# print(getAllWebsites(100))
# print(userExists(102))
