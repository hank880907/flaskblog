#__init__ is a file that tell the python shell that this is a package.
# it will load it when import anything in the package.
#It is used to prevent circular import.
# Email is not working


# todo: change the per_page to costumeizeable
# todo: make the reset password can only use once


import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy #data base
from flask_bcrypt import Bcrypt #use to create password and varify password
from flask_login import LoginManager #login module
from flask_mail import Mail
from flaskblog.config import Config





db = SQLAlchemy() #use cmd to import flaskblog project and call the db.create_all() to create a empty database
bcrypt = Bcrypt() # create a instance of bcrypt.
login_manager = LoginManager()
login_manager.login_message_category = 'info'  # in this case, 'info' is a category in bootstrap.


mail = Mail()


# this is for redirct the user to the login page if the user want to go to a page that needs to login to acccess.
login_manager.login_view = 'users.login'  #login is function name of the route



# the import route needs to be at the end of the file
# to avoid circular import.





def create_app(config_class=Config):
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app) #use cmd to import flaskblog project and call the db.create_all() to create a empty database
    bcrypt.init_app(app) # create a instance of bcrypt.
    login_manager.init_app(app)    
    mail.init_app(app)
    
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    return app