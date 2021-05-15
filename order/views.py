from flask import Blueprint, abort, request
from .models import Order
from .serializers import OrderSerializer
from ..base.responses import ListHttpResponse, ErrorHttpResponse, DetailsHttpResponse
from ..base.serializers import ValidationError

orders_blueprint = Blueprint('orders', __name__)

@orders_blueprint.route('/', methods=('GET', 'POST',))
def orders():
    if request.method == 'GET':
        orders = Order.query.all()
        response = ListHttpResponse(orders, OrderSerializer, request)
        return response.json()

    try:
        # TODO: Inject account into data
        # TODO: Handle new error logic
        serializer = OrderSerializer(request.json, True)
        return DetailsHttpResponse(serializer.instance, OrderSerializer, request).json()
    except ValidationError as e:
        return ErrorHttpResponse(e.errors).json()
    