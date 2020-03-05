from ..core import ma
from .models import BoxView
from marshmallow import fields

# http://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html

__all__ = ['BoxViewSchema']


class BoxViewSchema(ma.ModelSchema):
    class Meta:
        model = BoxView
        exclude = ('parent_box', 'parent_user')
    boxserial = fields.String()