from flask import Blueprint
from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)



@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int) #we can alse see this in the login route. request.args is a dictionary.
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template("home.html", posts=posts)

"""note:
posts = Post.query.all() can get all of the posts in a array. instead, posts = Post.query.paginate(page=1, per_page=5) would
return a paginate instance of paginate object on page one and 5 per page.
posts.iter_pages will return the page number of the page. 
"""



@main.route("/about")
def about():
    return render_template("about.html",title="about")