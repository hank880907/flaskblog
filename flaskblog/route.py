from flask import *
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdateForm
from flaskblog import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required






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


@app.route('/account')
@login_required             #a decorator for login required.
def account():
    form=UpdateForm()
    image_file = url_for('static', filename='profile_pic/'+current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)
    
    