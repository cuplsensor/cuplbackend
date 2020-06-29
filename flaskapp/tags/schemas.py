from ..core import ma
from .models import Tag

__all__ = ['TagSchema', 'ConsumerTagSchema']


class TagSchema(ma.ModelSchema):
    class Meta:
        model = Tag
        exclude = ('captures', 'tagviews')


class ConsumerTagSchema(ma.ModelSchema):
    class Meta:
        model = Tag
        exclude = ('secretkey', 'captures', 'id', 'tagviews')
