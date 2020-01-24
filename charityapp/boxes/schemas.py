from ..core import ma
from .models import Box

__all__ = ['BoxSchema', 'ConsumerBoxSchema']


class BoxSchema(ma.ModelSchema):
    class Meta:
        model = Box


class ConsumerBoxSchema(ma.ModelSchema):
    class Meta:
        model = Box
        exclude = ('secretkey', 'captures', 'id', 'boxviews')
