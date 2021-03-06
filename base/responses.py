# Standard libraries
from datetime import datetime

# Local
from .constants import DEFAULT_TIME_FORMAT


class SuccessResponse:
    def json(self):
        return {
            'success': True,
            'timestamp': datetime.now().strftime(DEFAULT_TIME_FORMAT),
        }


class HttpResponse:
    def __init__(self, data, serializer, request=None):
        self.data = data
        self.request = request
        self.serializer = serializer

    def json(self):
        return {
            'timestamp': datetime.now().strftime(DEFAULT_TIME_FORMAT),
        }


class DetailsHttpResponse(HttpResponse):
    def json(self):
        return {
            'data': self.serializer(self.data).to_representation(),
            'timestamp': datetime.now().strftime(DEFAULT_TIME_FORMAT),
        }


class ListHttpResponse(HttpResponse):
    def json(self):
        json = super().json()

        json['data'] = [
            self.serializer(obj).to_representation() for obj in self.data
        ]
        json['count'] = len(self.data)

        return json


class ErrorHttpResponse:
    def __init__(self, errors):
        self.errors = errors

    def json(self):
        return {'errors': self.errors, 'count': len(self.errors)}
