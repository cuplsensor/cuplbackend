from ..core import ma
from ..baseschema import BaseSchema
from .models import User

# http://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html

__all__ = ['UserSchema']

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
