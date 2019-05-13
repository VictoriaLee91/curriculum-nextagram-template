import braintree
from config import MERCHANT_ID, PUBLIC_KEY, PRIVATE_KEY
import os

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=MERCHANT_ID,
        public_key=PUBLIC_KEY,
        private_key=PRIVATE_KEY
    )
)


def generate_client_token():
    return gateway.client_token.generate()


def transact(options):
    return gateway.transaction.sale(options)


def find_transaction(id):
    return gateway.transaction.find(id)


def complete_transaction(nonce, amount):
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    if not result.is_success:
        return False
    return True
