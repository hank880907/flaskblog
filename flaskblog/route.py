import os
from flask import *
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdateForm
from flaskblog import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from PIL import Image






posts = [
    {
        'author':'hank wu',
        'title':'blog post1',
        'content':'i am the hamsomest guy on the world',
        'date_posted':'december 1, 2018'
    },
    
    {
        'author':'jeff meng',
        'title':'blog post2',
        'content':'i am the stupidest guy on the world',
        'date_posted':'nomember 1, 2018'
    }    
]





@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)





@app.route("/about")
def about():
    return render_template("about.html",title="about")








@app.route("/register", methods=['GET', 'POST'])
def register():
    '''this is the background program for register page.'''
    # if the user is authenticated, return to home.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # load form
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username= form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created successfuly, you are now able to login", 'success')
        return redirect(url_for('login'))    
    return render_template("register.html", title="Register", form=form)







@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user is authenticated. return to home.
    if current_user.is_authenticated:
        return redirect(url_for('home'))    
    # if user is not authenticated, load login form
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # check if the account exit.
        if user and bcrypt.check_password_hash(user.password, form.password.data): # check for password.
            login_user(user, remember=form.remember.data)
            #next is a query argument. if the user is comming from a login required page, than the 'next' argument will exist
            #next is the page where the user is comming from. use get function. if next doesn't exit, it will return null.
            next_page = request.args.get('next')  #args is a dictionary. but we don't use [] to find the data.
            flash('Login successfully', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. please check your email and password are correct', 'danger')
    return render_template("login.html", title="login", form=form)







@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))








@app.route('/account', methods=['GET', 'POST'])
@login_required             #a decorator for login required.
def account():
    form=UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated!', 'success')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pic/'+current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)









def save_picture(form_picture):
    """this function is for saving the image with a random file name"""
    random_hex = secrets.token_hex(8) # we don't want to use the origin file name. it is very likely to repeat.
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext# concat the random_hex and the file extension together
    picture_path = os.path.join(app.root_path, 'static\profile_pic', picture_fn)
    #proccess the image to a smaller thumbnail 
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) # save the pic to the path.
    return picture_fn
    