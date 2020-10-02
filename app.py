from flask_cors import CORS
from flask import Flask, request, Response, jsonify
import logging
import database as db
import hashlib

logging.basicConfig(filename='server.log', format='[%(levelname)-7s] : %(asctime)s : %(name)-8s : %(message)s',
                    level=logging.DEBUG, datefmt='%b %d, %g | %H:%M:%S')
log = logging.getLogger(__name__)

db.connect_DB()

#####   Flask App   #####
app = Flask(__name__)
CORS(app)
# app.config.from_pyfile('config.py')

#####   App Routes  #####


@app.route('/app/user', methods=['POST'])
def addUser():
    content = request.json
    # print(content)
    if all(keys in content for keys in ('username', 'password')) and len(content) == 2:
        _p = hashlib.md5(content['password'].encode())
        content['password'] = _p.hexdigest()
        if db.createUser(content):
            return jsonify({'status': 'account created'})
    # jsonify({'status': 'unable to create account'}),
    return Response(status=400)


@app.route('/app/user/auth', methods=['POST'])
def authenticate():
    content = request.json
    if all(keys in content for keys in ('username', 'password')) and len(content) == 2:
        auth = db.validateUser(content)
        return jsonify({'status': 'success' if auth['found'] and auth['auth'] else 'failure', 'userId': auth['userID']})
    # jsonify({'status': 'unable to create account'}),
    return Response(status=400)


@app.route('/app/sites/list/')
def fetchAllWebsites():
    userID = request.args.get('user')
    res = db.getAllWebsites(userID)
    websites = []
    for _r in res:
        websites.append(
            {'website': _r[0], 'username': _r[1], 'password': _r[2]})
    return jsonify(websites)


@app.route('/app/sites', methods=['POST'])
def addCredential():
    content = request.json
    userID = request.args.get('user')
    print(userID, userID is not None, all(keys in content for keys in (
        'website', 'username', 'password')) and len(content) == 3, db.userExists(int(userID)))
    if userID is not None and all(keys in content for keys in ('website', 'username', 'password')) and len(content) == 3 and db.userExists(userID):
        content['userID'] = userID
        print(content)
        if db.addWebsitePass(content):
            return jsonify({'status': 'success'})
    return Response(status=400)


if __name__ == "__main__":
    # log.info('Starting Flask Sever.')
    log.debug('Starting Flask Sever.')
    app.run(host='0.0.0.0', port=5000, debug=True)
