from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    '''this class is for manage the registration form'''
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=15)])
    
    email = StringField("Email", validators=[DataRequired(), Email()])
    
    password = PasswordField("password", validators=[DataRequired()])
    
    confirm_password = PasswordField("confirm password", validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField("sign up")
    
    def validate_username(self, username):
        '''
        custum validators. formate:
        
        def validate_field(self, field):
            if (condition)
                raise ValidationError('message')
        '''
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('The username is already exist. Please choose another one')
        
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('The email is taken. Please use a different one')
    
    
class LoginForm(FlaskForm):
    
    email = StringField("Email", validators=[DataRequired(), Email()])
    
    password = PasswordField("password", validators=[DataRequired()])
    remember = BooleanField("remember me")
    submit = SubmitField("login")
    
    
    
    
class UpdateForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=15)])    
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")
    picture = FileField("Update profile picture", validators=[FileAllowed(['jpg','png'])])
    
    def validate_username(self, username):
        if (current_user.username!=username.data):
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('The username is taken. please choose another one.')
            
    def validate_email(self, email):
        if (current_user.email!=email.data):
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('The email is taken. please choose another one.')    