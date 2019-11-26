from flask import Flask, Response, render_template, flash, redirect, url_for, jsonify,current_app, request, _request_ctx_stack
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, current_user,login_user, logout_user, login_required
import boto3
from werkzeug.security import generate_password_hash, check_password_hash
from config import S3_BUCKET, S3_KEY, S3_SECRET
from filters import datetimeformat, file_type


s3 = boto3.client('s3', aws_access_key_id=S3_KEY,
                  aws_secret_access_key=S3_SECRET)
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['JWT_SECRET_KEY'] = 'super-secretxyyxyyy'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
Bootstrap(app)
db = SQLAlchemy(app)
app.jinja_env.filters['file_type'] = file_type
app.jinja_env.filters['datetimeformat'] = datetimeformat
login_manager = LoginManager()
login_manager.init_app(app)
jwt = JWTManager(app)
blacklist = set()
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist
'''
@jwt_required
def logoutx():
    return 'xxxx'
    jti = get_raw_jwt()['jti']
    return jti
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200
'''

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login')
@limiter.exempt
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
       
    if user and check_password_hash(user.password,password):
        login_user(user, remember=remember)
        return redirect(url_for('files'))
    else:
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))



@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    flash('You can login now!')
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/files')
def files():
    if current_user.is_authenticated:
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(S3_BUCKET)
        summaries = my_bucket.objects.all()
        return render_template('bucket.html', my_bucket=my_bucket, files=summaries)
    else:
        return render_template('login.html')

@app.route('/upload', methods=['POST', 'GET'])
@limiter.limit("4 per minute")
def upload():
    if request.method == 'POST':
        file = request.files['file']
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(S3_BUCKET)
        my_bucket.Object(file.filename).put(Body=file)
        flash('File Uploaded Successfully!')
        return redirect(url_for('files'))
    elif request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('upload.html')
        else:
            return render_template('login.html')

@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']
    s3_resource = boto3.resource('s3')
    my_bucket= s3_resource.Bucket(S3_BUCKET)
    file_obj = my_bucket.Object(key).get()
    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition":"attachment;filename={}".format(key)}
    )

@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']
    s3_resource = boto3.resource('s3')
    my_bucket= s3_resource.Bucket(S3_BUCKET)
    my_bucket.Object(key).delete()

    flash('The file has been deleted')
    return redirect(url_for('files'))

if __name__ == '__main__':
    app.run()
