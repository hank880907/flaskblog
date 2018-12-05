from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

'''
keep in mind that:

the baseclass for all your models is called db.Model.
It's stored on the SQLAlchemy instance you have to creat.
see Quickstart for more details.

some parts that are required in SQLAlchemy are optional
in Flask-SQLAlchemy. For instance the table name is automatically
set for you unless overridden.
It's derived form the class name converted to lowercase and with "CamelCase"
converted to "camel_case". to override the table name, set the __tablename__
class attribute.s
'''



@login_manager.user_loader
def load_user(user_id):
    '''for login the user'''
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    '''
    create the data base structure of the user name
    backref is a function that can use the post to find the user.
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # i don't clearly know what does the backref works. is "author" a commend ??
    posts = db.relationship('Post', backref='author', lazy=True) # the string 'Post' refer to the class post
    
    def __repr__(self):
        return "user:{}, email:{}, image:{}".format(self.username, self.email, self.image_file)






class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100) , nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # what does the foreign Key dose?
    
    def __repr__(self):
        return "post:{}, date:{}".format(self.title, self.date_posted)