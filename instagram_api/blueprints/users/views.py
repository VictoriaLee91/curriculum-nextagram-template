from flask import Blueprint

users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"


@users_api_blueprint('/<username', methods=['POST'])
@jwt_required()  # read up on jwt in flask. install flask-jwt. follow documentation
def show(username):
    user = User.get_or_none(User.username == username)

    if not user:
        resp = {
            'message': 'No user found with this username.'
        }


'user': {
    'id': user.id,
    'username': user.username,
    'email': user.email
}
