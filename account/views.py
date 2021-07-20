from flask import Blueprint, abort

# Local
from ..base.responses import DetailsHttpResponse
from ..base.utils import get_current_account
from .serializers import AccountSerializer

accounts_blueprint = Blueprint('account', __name__)


@accounts_blueprint.route('/')
def account():
    """
    Get account details
    ---
    tags:
        - users
    definitions:
        - schema:
            id: Group
            properties:
            name:
                type: string
                description: the group's name
    parameters:
        - in: body
        name: body
        schema:
            id: User
            required:
            - email
            - name
            properties:
            email:
                type: string
                description: email for user
            name:
                type: string
                description: name for user
            address:
                description: address for user
                schema:
                id: Address
                properties:
                    street:
                    type: string
                    state:
                    type: string
                    country:
                    type: string
                    postalcode:
                    type: string
            groups:
                type: array
                description: list of groups
                items:
                $ref: "#/definitions/Group"
    responses:
        201:
        description: User created
    """
    account = get_current_account()
    if account:
        return DetailsHttpResponse(account, AccountSerializer).json()

    return abort(404)


@accounts_blueprint.route('/reset_account')
def reset_account():
    account = get_current_account()
    if account:
        account.reset()

        new_account = get_current_account()
        return DetailsHttpResponse(new_account, AccountSerializer).json()

    return abort(404)
