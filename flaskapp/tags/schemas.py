from ..core import ma
from .models import Tag

__all__ = ['TagSchema', 'ConsumerTagSchema', 'ConsumerTagDescriptionSchema']


class TagSchema(ma.ModelSchema):
    class Meta:
        model = Tag
        exclude = ('captures',)


class ConsumerTagSchema(ma.ModelSchema):
    class Meta:
        model = Tag
        exclude = ('secretkey', 'captures', 'id',)


class ConsumerTagDescriptionSchema(ConsumerTagSchema):
    class Meta:
        fields = ('description',)
