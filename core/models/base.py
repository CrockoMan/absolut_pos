from django.db import models, DataError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


# UNSAVED = object()
# DEFERRED = object()

class BaseModelException(Exception):
    pass


def sane_repr(*attrs):
    if 'id' not in attrs and 'pk' not in attrs:
        attrs = ('id',) + attrs

    def _repr(self):
        cls = type(self).__name__

        pairs = ('{}={}'.format(a, repr(getattr(self, a, None))) for a in attrs)

        return '<%s at 0x%x: %s>' % (cls, id(self), ', '.join(pairs))

    return _repr


class BaseModel(models.Model):
    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('дата изменения', auto_now=True)

    # objects = BaseManager()

    class Meta:
        abstract = True

    # __repr__ = sane_repr('id')
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    # def __getstate__(self):
    #     d = self.__dict__.copy()
    #     d.pop('_Model__data', None)
    #     return d
    #
    # def __reduce__(self):
    #     (model_unpickle, stuff, _) = super(BaseModel, self).__reduce__()
    #     return (model_unpickle, stuff, self.__getstate__())
    #
    # def __setstate__(self, state):
    #     self.__dict__.update(state)

    def save(self, **kwargs):
        try:
            update_fields = kwargs.get('update_fields')
            if update_fields is not None and 'updated_at' not in update_fields:
                kwargs.update({'update_fields': update_fields + ['updated_at']})
            result = super().save(**kwargs)
        except DataError as e:
            if 'character varying' in str(e):
                raise BaseModelException(e)
            else:
                raise
        else:
            return result
