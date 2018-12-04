from flask import *
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, bcrypt, db
from flask_login import login_user, current_user






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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. please check your email and password are correct', 'danger')
    return render_template("login.html", title="login", form=form)

