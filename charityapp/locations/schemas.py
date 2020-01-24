from ..core import ma
from ..baseschema import BaseSchema
from .models import Location

# http://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html

__all__ = ['LocationSchema']

class LocationSchema(ma.ModelSchema):
    class Meta:
        model = Location
        strict = True
