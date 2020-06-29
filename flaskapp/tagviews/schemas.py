from ..core import ma
from .models import TagView
from marshmallow import fields

# http://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html

__all__ = ['TagViewSchema']


class TagViewSchema(ma.ModelSchema):
    class Meta:
        model = TagView
        exclude = ('parent_tag', )
    tagserial = fields.String()
    user_id = fields.Integer()
