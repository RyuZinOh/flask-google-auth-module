from flask import Flask, redirect, url_for, session, request, render_template
from authlib.integrations.flask_client import OAuth
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MONGO_URI'] = os.getenv("MONGO_URI")
mail = Mail(app)
mongo = PyMongo(app)

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://openidconnect.googleapis.com/v1/',
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs'
)

def generate_otp():
    return random.randint(100000, 999999)

def send_otp_email(user_email, otp):
    msg = Message("Your OTP Code", recipients=[user_email], sender=os.getenv("MAIL_USERNAME"))
    msg.body = f"Your OTP code is: {otp}"
    mail.send(msg)

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f'Hello, {user["name"]}! (<a href="/logout">Logout</a>)'
    return '<a href="/login">Login with Google</a>'

@app.route('/login')
def login():
    return google.authorize_redirect(url_for('authorize', _external=True))

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo', token=token)
    user_info = resp.json()
    session['user_info'] = user_info
    session['user_email'] = user_info['email']
    otp = generate_otp()
    send_otp_email(user_info['email'], otp)
    session['otp'] = otp
    return redirect(url_for('verify_otp'))

@app.route('/verify', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        if entered_otp == str(session.get('otp')):
            user_info = session.get('user_info')
            mongo.db.users.insert_one({
                'google_id': user_info['sub'],
                'name': user_info['name'],
                'email': user_info['email'],
                'profile_picture': user_info['picture'],
            })
            session['user'] = user_info
            session.pop('otp', None)
            return redirect('/')
        else:
            return "Incorrect OTP. Please try again."
    return render_template('verify_otp.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('otp', None)
    session.pop('user_info', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
