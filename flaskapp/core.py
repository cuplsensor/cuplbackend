# -*- coding: utf-8 -*-
"""
    overholt.core
    ~~~~~~~~~~~~~
    core module
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
import marshmallow_sqlalchemy as ma

from flask import current_app, abort

#: Flask-SQLAlchemy extension instance
db = SQLAlchemy(engine_options={'pool_pre_ping': True})


class OverholtError(Exception):
    """Base application error class."""

    def __init__(self, msg):
        self.msg = msg


class OverholtFormError(Exception):
    """Raise when an error processing a form occurs."""

    def __init__(self, errors=None):
        self.errors = errors


class Service(object):
    """A :class:`Service` instance encapsulates common SQLAlchemy model
    operations in the context of a :class:`Flask` application.
    """
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """Checks if the specified model instance matches the service's model.
        By default this method will raise a `ValueError` if the model is not the
        expected type.
        :param model: the model instance to check
        :param raise_error: flag to raise an error on a mismatch
        """
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    def _preprocess_params(self, kwargs):
        """Returns a preprocessed dictionary of parameters. Used by default
        before creating a new instance or updating an existing instance.
        :param kwargs: a dictionary of parameters
        """
        kwargs.pop('csrf_token', None)
        return kwargs

    def save(self, model):
        """Commits the model to the database and returns the model
        :param model: the model to save
        """
        self._isinstance(model)
        db.session.add(model)
        db.session.commit()
        return model

    def all(self):
        """Returns a generator containing all instances of the service's model.
        """
        return self.__model__.query.all()

    def get(self, id):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.
        :param id: the instance id
        """
        return self.__model__.query.get(id)

    def get_all(self, *ids):
        """Returns a list of instances of the service's model with the specified
        ids.
        :param *ids: instance ids
        """
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def find(self, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.
        :param **kwargs: filter parameters
        """
        return self.__model__.query.filter_by(**kwargs)

    def random(self, **kwargs):
        """Returns one random instance of the service's model. There is an optional filter.
        :param **kwargs: filter parameters
        """
        return self.find(**kwargs).order_by(func.random()).first()

    def first(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.
        :param **kwargs: filter parameters
        """
        return self.find(**kwargs).first()

    def first_or_404(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments or raises a 404 error if the instance does not exist.
        :param **kwargs: filter parameters
        """
        modelname = self.__class__.__model__.__name__

        # Do not use first_or_404 because we want a custom error message that says what cannot be found.
        rv = self.find(**kwargs).first()
        if rv is None:
            abort(404, 'Error 404: {modelname} not found'.format(modelname=modelname))
        return rv

    def one(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.
        :param **kwargs: filter parameters
        """
        return self.find(**kwargs).one()

    def get_or_404(self, id):
        """Returns an instance of the service's model with the specified id or
        raises an 404 error if an instance with the specified id does not exist.
        :param id: the instance id
        """
        return self.__model__.query.get_or_404(id)

    def new(self, **kwargs):
        """Returns a new, unsaved instance of the service's model class.
        :param **kwargs: instance parameters
        """
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        """Returns a new, saved instance of the service's model class.
        :param **kwargs: instance parameters
        """
        newobj = self.new(**kwargs)
        current_app.logger.info(newobj.__repr__)
        return self.save(newobj)

    def update(self, model, **kwargs):
        """Returns an updated instance of the service's model class.
        :param model: the model to update
        :param **kwargs: update parameters
        """
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        self.save(model)
        return model

    def delete(self, model):
        """Immediately deletes the specified model instance.
        :param model: the model instance to delete
        """
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()
