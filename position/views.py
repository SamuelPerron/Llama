from flask import Blueprint, abort, request

# Local
from ..base.responses import ListHttpResponse, SuccessResponse
from ..base.utils import get_current_account
from .serializers import PositionSerializer

positions_blueprint = Blueprint('positions', __name__)


@positions_blueprint.route('/')
def positions():
    account = get_current_account()

    return ListHttpResponse(account.positions, PositionSerializer).json()


@positions_blueprint.route('/close', methods=('POST',))
def close():
    # Local
    from . import Position

    position_ids = request.get_json().get('ids', [])
    positions = [
        Position.query.filter_by(id=id).first() for id in position_ids
    ]

    if None in positions:
        abort(404)

    for position in positions:
        position.close()

    return SuccessResponse().json()
