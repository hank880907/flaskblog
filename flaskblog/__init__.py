#__init__ is a file that tell the python shell that this is a package.
# it will load it when import anything in the package.
#It is used to prevent circular import.


from flask import Flask
from flask_sqlalchemy import SQLAlchemy #data base
from flask_bcrypt import Bcrypt #use to create password and varify password
from flask_login import LoginManager #login module




app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # the defalt local testing data base path.
db = SQLAlchemy(app) #use cmd to import flaskblog project and call the db.create_all() to create a empty database
bcrypt = Bcrypt(app) # create a instance of bcrypt.
login_manager = LoginManager(app)
login_manager.login_message_category = 'info'  # in this case, 'info' is a category in bootstrap.



# this is for redirct the user to the login page if the user want to go to a page that needs to login to acccess.
login_manager.login_view = 'login'  #login is function name of the route




# the import route needs to be at the end of the file
# to avoid circular import.
import route