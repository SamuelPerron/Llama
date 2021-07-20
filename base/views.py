from flask import Blueprint, jsonify
from flask_swagger import swagger

# Local
from .. import create_app

base_blueprint = Blueprint('base', __name__)


@base_blueprint.route('/')
def spec():
    app = create_app()
    swag = swagger(app)
    swag['info']['title'] = 'Llama'

    return jsonify(swag)
