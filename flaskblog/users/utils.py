#the email sender is broken. it print the message in the cmd alternatively.
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    """this function is for saving the image with a random file name"""
    random_hex = secrets.token_hex(8) # we don't want to use the origin file name. it is very likely to repeat.
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext# concat the random_hex and the file extension together
    picture_path = os.path.join(current_app.root_path, 'static\profile_pic', picture_fn)
    #proccess the image to a smaller thumbnail 
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) # save the pic to the path.
    return picture_fn





def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@yiniu.com', recipients=[user.email])
    msg.body = '''To reset your password, visit the follow link:
{}'''.format(url_for('users.reset_token', token=token, _external=True))
    #mail.send(msg)
    print msg.body

