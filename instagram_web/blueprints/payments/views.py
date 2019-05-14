from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import current_user
from models.images import Images
from models.payments import Payments
from instagram_web.util.braintree import complete_transaction, generate_client_token, transact
from instagram_web.util.sendgrid import *
import braintree

payments_blueprint = Blueprint(
    'payments', __name__, template_folder='templates')

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement,

]


@payments_blueprint.route('/<id>/new', methods=["GET"])
def index(id):
    image = Images.get_by_id(id)
    client_token = generate_client_token()
    return render_template('payments/new.html', image=image, client_token=client_token)


@payments_blueprint.route('/<id>/payment', methods=["POST"])
def create(id):
    image = Images.get_by_id(id)
    payment_amount = request.form.get('amount')
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:

        new_payment = Payments(
            image_id=image.id,
            donor=current_user.id,
            payment_amount=payment_amount
        ).save()
        return redirect(url_for('payments.show_checkout', transaction_id=result.transaction.id, id=image))

    else:
        for x in result.errors.deep_errors:
            flash('Error')
        return redirect(url_for('payments.index', id=id))


@payments_blueprint.route('/<id>/<transaction_id>', methods=["GET"])
def show_checkout(id, transaction_id):
    image = Images.get_by_id(id)
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    email()

    result = {
        'header': 'Transaction Failed',
        'icon': 'fail',
        'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
    }
    email()
    return render_template('payments/show.html', transaction=transaction, result=result, id=id)
