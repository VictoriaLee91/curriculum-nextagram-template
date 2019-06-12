import os
from flask import Flask, Blueprint, request, redirect, url_for, render_template, flash
from flask_login import current_user
from models.user import User
from instagram_web.util.helpers import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug import secure_filename

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)

    if not User.validate_password(password):
        flash(f'Password invalid')
        return render_template('users/new.html')

    newuser = User(username=username, email=email, password=hashed_password)

    if newuser.save():
        flash("New user successfully registered!")
        return redirect(url_for('users.new'))

    else:
        flash("User registration unsuccessful")
        return render_template('users/new.html', errors=newuser.errors)


# @users_blueprint.route('/<username>', methods=["GET"])
# def show(username):
#     pass


@users_blueprint.route('/index', methods=["GET"])
def index():
    return render_template('index.html', users=User.select())


@users_blueprint.route("/<username>/profilepage", methods=["GET"])
def profilepage(username):
    user = User.get_or_none(User.username == username)
    if not user:
        flash('Nope.')
    else:
        return render_template('profile_page.html', User=User)


@users_blueprint.route("/uploadprofile", methods=["GET"])
def change_picture():
    # profile_image = User.get_or_none(User.profile_image == profile_image)
    return render_template('update_profile.html')


@users_blueprint.route("/new_uploadprofile", methods=["POST"])
def upload_profile():
    if 'profile_image' not in request.files:
        flash(f"No user image key in request.files")
        return redirect(url_for('home'))

    file = request.files['profile_image']

    if file.filename == "":
        return "Please select a file"

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, S3_BUCKET)

        update_profile_image = User.update(
            profile_image=file.filename).where(User.id == current_user.id)

        if update_profile_image.execute():
            flash(f'Photo successfully uploaded.')
            return render_template('update_profile.html')
        else:
            flash(f'Unable to upload picture. Please try again.')
            return render_template('update_profile.html')

    else:
        return redirect(url_for('home'))


@users_blueprint.route('/<id>/edit', methods=["GET"])
def edit(id):
    user = User.get_by_id(id)
    if current_user == user:
        return render_template('edit_details.html', user=user)
    else:
        flash('You cannot do this action.')
        return redirect(url_for('home'))


@users_blueprint.route('/<id>', methods=["POST"])
def update(id):
    user = User.get_by_id(id)

    if not current_user == user:
        flash('Unauthorised')
        return render_template('edit_details.html', user=user)

    else:
        new_user_name = request.form.get('new_user_name')
        new_email = request.form.get('new_email')
        new_password = request.form.get('new_password')
        hashed_password = generate_password_hash
        (new_password)

        update_user = User.update(
            username=new_user_name,
            email=new_email,
            password=hashed_password
        ).where(User.id == id)

    if not update_user.execute():
        flash(f"Unable to update, please try again")
        return render_template('edit_details.html', user=user)

    flash('Successfully updated')
    return redirect(url_for('home'))
