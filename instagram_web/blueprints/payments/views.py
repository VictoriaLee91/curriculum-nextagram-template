from flask import Blueprint, render_template, redirect, request, flash, url_for
from models.images import Images
from models.payments import Payments
from instagram_web.util.braintree import complete_transaction, generate_client_token
from instagram_web.util.sendgrid import *

payments_blueprint = Blueprint(
    'payments', __name__, template_folder='templates')


# @payments_blueprint.route('/', methods=["GET"])
# def index():
#     return render_template('payments/new.html')


@payments_blueprint.route('/new', methods=["GET"])
def new():
    # image = Images.get_or_none(Images.id == image_id)
    client_token = generate_client_token()
    return render_template('payments/new.html', client_token=client_token)


@payments_blueprint.route('/payment', methods=["POST"])
def create():
    payment_nonce = request.form.get('')
    amount = request.form.get('payment_amount')
    # image = Images.get_or_none(Images.id == image_id)

    # if not image:
    #     flash('no image found', 'warning')
    #     return redirect(url_for('home'))

    if not amount:
        flash('no amount specified', 'warning')
        return redirect(url_for('payments.new', image_id=image.id))

    if not payment_nonce:
        flash('Error with payment, please try again.', 'warning')
        return redirect(url_for('users.show', username=Images.user.username))

    if result != complete_transaction(payment_nonce, amount):
        flash('oops', 'warning')
        return redirect(url_for('payments.new', image_id == image.id))

    new_payment = Payments(
        user_id=current_user.id,
        amount=amount,
        # image_id=image.id
    )

    if not new_payment.save():
        flash('Unable to complete payment', 'warning')
        return redirect(url_for('payments.new'))
        #  image_id == image.id

    flash('payment successful')
    return redirect(url_for('show'))


@payments_blueprint.route('/<transaction_id>', methods=['GET'])
def show(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        return email()
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        return email()
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('payments/show.html', transaction=transaction, result=result)
