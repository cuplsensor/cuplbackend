from .core import db, ma

class BaseSchema(ma.ModelSchema):
    class Meta:
        sqla_session = db.session
