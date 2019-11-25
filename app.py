from flask import Flask, render_template, flash, redirect, url_for, jsonify,current_app, request, _request_ctx_stack
from flask_jwt import JWT
from security import authenticate, identity
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
Bootstrap(app)
db = SQLAlchemy(app)
app.jinja_env.filters['file_type'] = file_type
app.jinja_env.filters['datetimeformat'] = datetimeformat
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

@jwt.payload_handler
def request_handler():
    auth_header_value = request.headers.get('Authorization', None)
    auth_header_prefix = current_app.config['JWT_AUTH_HEADER_PREFIX']
    if not auth_header_value:
        # check if flask_login is configured
        if isinstance(current_app.login_manager, LoginManager):
            # load user
            current_app.login_manager._load_user()
            # if successful, this will set user variable at request context
            if hasattr(_request_ctx_stack.top, 'user'):
                # generate token
                access_token = _jwt.jwt_encode_callback(_request_ctx_stack.top.user)
                return access_token
    parts = auth_header_value.split()
    if parts[0].lower() != auth_header_prefix.lower():
        raise JWTError('Invalid JWT header', 'Unsupported authorization type')
    elif len(parts) == 1:
        raise JWTError('Invalid JWT header', 'Token missing')
    elif len(parts) > 2:
        raise JWTError('Invalid JWT header', 'Token contains spaces')
    return parts[1]
'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login')
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

    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
'''
@app.route('/bucket')
def files():
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries = my_bucket.objects.all()
    return render_template('bucket.html', my_bucket=my_bucket, files=summaries)


@app.route('/upload', methods=['POST', 'GET'])
@jwt_required()
def upload():
    if request.method == 'POST':
        file = request.files['file']

        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(S3_BUCKET)
        my_bucket.Object(file.filename).put(Body=file)
        flash('File Uploaded Successfully!')
        return redirect(url_for('files'))
    elif request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    app.run()
