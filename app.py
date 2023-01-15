from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps

# instantiate the flask class
app = Flask(__name__)

# secret key 
app.config['SECRET_KEY'] = 'a6f997b90008489793044d418cf8b10f'


def token_required(func):
    # decorator factory which invokes update_wrapper() method 
    # passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        # You can use the JWT errors in exception
        # except jwt.InvalidTokenError:
        #     return 'Invalid token'
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated

# the home route
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently!' 

# the auth route

# authenticate only if you copy your token and paste it after /auth?token=your_token
# Hit enter and you will get the message below.
@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard!'  

# the login route
@app.route('/login', methods=['POST'])
def login():
    # this can be done using try except block for precise functionalities
    if request.form['username'] and request.form['password'] == '1234':
        session['logged_in'] = True
        token = jwt.encode(
            {
            'user' : request.form['username'],
            'expiration' : str(datetime.utcnow() + timedelta(seconds=120))
            },
            app.config['SECRET_KEY']
        ) 
        return jsonify({'token' : token.decode('utf-8')})
    else:
        # WWW-Authenticate - response header that defines the HTTP authentication method
        return make_response('Unable to verify', 403, {'WWW-Authenticate' : 'Basic realm:Authentication Failed!'})


if __name__ == "__main__":
    app.run(debug=True)