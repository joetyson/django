from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.core import validators
from django.db import backend, connection
from django.db.models.loading import *
from django.db.models.query import Q
from django.db.models.manager import Manager
from django.db.models.base import Model, AdminOptions
from django.db.models.fields import *
from django.db.models.fields.related import *
from django.db.models.exceptions import FieldDoesNotExist, BadKeywordArguments
from django.db.models import signals
from django.utils.functional import curry
from django.utils.text import capfirst

# Admin stages.
ADD, CHANGE, BOTH = 1, 2, 3

class LazyDate:
    """
    Use in limit_choices_to to compare the field to dates calculated at run time
    instead of when the model is loaded.  For example::

        ... limit_choices_to = {'date__gt' : meta.LazyDate(days=-3)} ...

    which will limit the choices to dates greater than three days ago.
    """
    def __init__(self, **kwargs):
        self.delta = datetime.timedelta(**kwargs)

    def __str__(self):
        return str(self.__get_value__())

    def __repr__(self):
        return "<LazyDate: %s>" % self.delta

    def __get_value__(self):
        return datetime.datetime.now() + self.delta
