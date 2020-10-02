# PY-BUCKET
This web app provide AWS S3 based file managing features including UPLOAD, *DELETE*, DOWNLOAD along with login features.

![alt](https://i.ibb.co/myrY9Zb/output-onlinepngtools.png)

### Project Overview
> To Develop an application that provides a list of items in a AWS S3 bucket as well as provide a user registration and authentication system. Registered users will have the ability to UPLOAD, DOWNLOAD and DELETE their own items in the BUCKET. The project also uses throttling for  various API's call rate.

### Why This Project?
> Modern web applications perform a variety of functions and provide amazing features and utilities to their users; but deep down, it’s really all just creating, reading, updating and deleting data. In this project, I combined my knowledge of building dynamic websites with persistent data storage to create a web application that provides a compelling service to your users.

### What Did I Learn?
  * Develop a RESTful web application using the Python framework Flask
  * Implementing Flask-login and Flask-jwt-extended for security.
  * Implementing UPLOAD, DOWNLOAD and DELETE in a S3 bucket.
  * Throttling for API call rate
  * Responsive UI
  
  #### Important **pip** packages used in this app
  * [boto3](https://pypi.org/project/boto3/)
  * [Flask-JWT-Extended](https://pypi.org/project/Flask-JWT-Extended/)
  * [Flask-Limiter](https://pypi.org/project/Flask-Limiter/)
  * [Flask-Login](https://pypi.org/project/Flask-Login/)
  * [Flask-SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/)

### How to Run?

#### PreRequisites
  * [Python ~3.7](https://www.python.org/)
  
#### Setup Project:
#####  1. Clone or Download the project and `cd` into the `PyBucket/` folder.

#####  2. Upgrade pip
   ```
   $ python3 -m pip install --user --upgrade pip
   ```

#####  3. Install virtualenv
  - On macOS and Linux:
  ```
  $ python3 -m pip install --user virtualenv
  ```

  - On Windows:
  ```
  py -m pip install --user virtualenv
  ```
  
  
##### 4. Creating a virtual environment
 - On macOS and Linux:
 
 ```
 python3 -m venv env
 ```
 
 -On Windows:
 ```
 py -m venv env
 ```
#####  5. Commands to activate virtual env:

  - On macOS and Linux:
  ```
  $ source env/bin/activate
  ```

  - On Windows:
  ```
  .\env\Scripts\activate
  ```

#####  6. Install dependencies:
  ```
  $ pip install -r requirements.txt
  ```

#####  7. Change AWS *S3_KEY*, *S3_SECRET* and *S3_BUCKET* with your own values in `.env` file.
  ```
  source env/bin/actvate
  export FLASK_APP=app.py
  export FLASK_DEBUG=1

  export S3_BUCKET='YOUR_BUCKET_NAME' 
  export S3_KEY='YOUR_KEY' 
  export S3_SECRET='YOUR_SECRET_NOT_MINE' 
  ```

#### Launch Project
#####  1. run the app using command:
  ```
  $ flask run
  ```
  
#####  2. Access and test your application by visiting [http://localhost:5000](http://localhost:5000).


### If you're running into issues:
contact me on [twitter](https://www.twitter.com/harshsahu97/)
