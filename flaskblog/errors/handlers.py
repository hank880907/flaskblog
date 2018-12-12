from flask import Blueprint, render_template


errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)  # tthere is another function named errorhandler instead of app_errorhandler. but it would only catch the 404 error.
def error_404(error):
    return render_template('errors/404.html'), 404 #the second is the error static code. the default is 200, we don't need to spcifiy this in other handler.


@errors.app_errorhandler(403)
def error_404(error):
    return render_template('errors/403.html'), 403 #the second is the error static code. the default is 200, we don't need to spcifiy this in other handler.

@errors.app_errorhandler(500)
def error_404(error):
    return render_template('errors/500.html'), 500 #the second is the error static code. the default is 200, we don't need to spcifiy this in other handler.
