from django.db import DataError
from django.db import models


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

    class Meta:
        abstract = True

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
