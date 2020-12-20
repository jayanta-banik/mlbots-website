# imports
from flask_cors import CORS, cross_origin
from flask import Flask, redirect, render_template, jsonify, request, send_from_directory
import json
# local imports


# global variables
app = Flask(__name__)
cors = CORS(app)

# routes


@app.route('/helloworld')
def hello_world():
    return "Hello World!"


@app.route('/')
def landing_page():
    return redirect('/home', code=302)


@app.route('/home')
def welcome():
    with open('static/welcome.html') as file:
        page = file.read()
    return page


@app.route('/authentication-gateway', methods=['GET'])
def auth_gateway():
    fwdid = request.args.get('fwdid', default='none', type=str)
    trytimes = request.args.get('trytimes', default='1', type=int)
    with open('static/auth.html') as file:
        page = file.read()
    data = {'fwdid': fwdid,'trytimes': trytimes}
    
    for k,v in data.items():
        page = page.replace('{%s}'%k, str(v))

    if int(trytimes) > 1:
    	page = page.replace('''<!-- <div class="card-title text-danger">
                        Invalid credentials. Try agian.
                    </div> -->''',
                    '''<div class="card-title text-danger">
                        Invalid credentials. Try agian.
                    </div>''')
    return page


@app.route('/auth_redirect', methods=['POST'])
def validation():
    fwdid = request.form.get('fwdid')
    trytimes = request.form.get('trytimes')
    username = request.form.get('username')
    password = request.form.get('password')
    
    with open('res/password.txt') as file:
        profiles = eval(file.read())
        
    if username in profiles:
        if profiles[username] == password:
            return fwdid
    return redirect('/authentication-gateway?fwdid=%s&trytimes=%s'%(fwdid,int(trytimes)+1))


# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     with open('page request catch.txt', 'a+') as file:
#         file.write('request: %s\n' % path)
#     return render_template('static/RequestPageNotFound.html')

if __name__ == '__main__':
    app.run(debug=True)
