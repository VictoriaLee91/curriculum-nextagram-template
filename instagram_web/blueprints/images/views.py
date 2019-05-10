from instagram_web.util.helpers import *
from config import S3_BUCKET
from flask import Flask, Blueprint, request, redirect, render_template, flash, url_for
from flask_login import login_required, current_user
from models.user import User
from models.images import Images
from werkzeug import secure_filename

images_blueprint = Blueprint('images',
                             __name__,
                             template_folder='templates')


@images_blueprint.route('/uploadfile', methods=["GET"])
@login_required
def new():
    return render_template('upload_pictures.html')


@images_blueprint.route("/new_uploadfile", methods=["POST"])
def upload_file():
    if 'user_image' not in request.files:
        flash(f"No user image key in request.files")
        return redirect(url_for('home'))

    file = request.files['user_image']

    if file.filename == "":
        return "Please select a file"

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, S3_BUCKET)
        upload_image = Images(user_image=file.filename,
                              user_id=current_user.id)

        if upload_image.save():
            flash(f'Photo successfully uploaded.')
            return render_template('upload_pictures.html')
        else:
            flash(f'Unable to upload picture. Please try again.')
            return render_template('upload_pictures.html')

    else:
        return redirect(url_for('home'))

# @images_blueprint.route("/", methods=["POST"])
# def display_images():
