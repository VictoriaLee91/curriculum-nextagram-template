from instagram_web.blueprints.images.helpers import *
from config import S3_BUCKET
from flask import Flask, Blueprint, request, redirect, render_template, flash
from flask_login import login_required
from models.user import User
from werkzeug import secure_filename

images_blueprint = Blueprint('images',
                             __name__,
                             template_folder='templates')


@images_blueprint.route('/uploadfile', methods=["GET"])
@login_required
def new():
    return render_template('upload_pictures.html')


@images_blueprint.route("/", methods=["POST"])
def upload_file():
    if "user_file" not in request.files:
        return "No user_file key in request.files"

    file = request.files["user_file"]

    if file.filename == "":
        return "Please select a file"

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, S3_BUCKET)
        flash(f'Photo successfully uploaded')
        return render_template('upload_pictures.html')
        # try to return it to the database

    else:
        return redirect(url_for('home'))
