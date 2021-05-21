from flask import Blueprint, abort

from ..base.responses import DetailsHttpResponse
from ..base.utils import get_current_account
from .serializers import AccountSerializer

accounts_blueprint = Blueprint("account", __name__)


@accounts_blueprint.route("/")
def account():
    account = get_current_account()
    if account:
        return DetailsHttpResponse(account, AccountSerializer).json()

    return abort(404)


@accounts_blueprint.route("/reset_account")
def reset_account():
    account = get_current_account()
    if account:
        account.reset()

        new_account = get_current_account()
        return DetailsHttpResponse(new_account, AccountSerializer).json()

    return abort(404)
