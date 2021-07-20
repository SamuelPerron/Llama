# Local
from .models import BaseDBModel
from .views import base_blueprint

LONG = 'long'
SHORT = 'short'
SIDES = (
    (LONG, 'Long'),
    (SHORT, 'Short'),
)
