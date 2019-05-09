from flask import Blueprint, render_template, redirect, request, flash, url_for
from models.images import Images
from instagram_web.util.braintree import complete_transaction, client_token, payment_nonce


donations_blueprint = Blueprint(
    'payments', __name__, template_folder='templates')


@payments_blueprint.route('/<image_id>/new', methods=["GET"])
def new(image_id):
    image = image.get_or_none(Image.id == image_id)
    client_token = generate_client_token()
    if not image:
        flash('unable to find image')
        return redirect(url_for('home'))
    return render_template('payments/new.html', image=image)


@payments_blueprint.route('/<image_id>/checkout', methods=["POST"])
def create(image_id):
    payment_nonce = request.form.get('')
    amount = request.form.get('payment_amount')
    image = Image.get_or_none(Image.id == image_id)

    if not image:
        flash('no image found')
        return redirect(url_for('home'))

    if not amount:
        flash('no amount specified')
        return redirect(url_for('payments.new', image_id=image.id))

    if not payment_nonce:
        flash('Error with payment, please try again.')
        return redirect(url_for('users.show', username=Images.user.username))

    result = complete_transaction(payment_nonce, amount)
