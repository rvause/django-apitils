from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.db.models.query import QuerySet
from django.db.models.fields.files import FileField


class SerializingQuerySet(QuerySet):
    """
    Provides a queryset method to serialize the QuerySet
    """
    def serialize(self):
        return [o.serialize() for o in self]


class SerializingManager(models.Manager):
    """
    Applies the SerializingQuerySet
    """
    def get_query_set(self):
        return SerializingQuerySet(self.model, using=self._db)


class SerializeMixin(models.Model):
    objects = SerializingManager()

    class Meta:
        abstract = True

    def serialize(self, recursive=True):
        data = {}
        for field in self.__class__._meta.get_all_field_names():
            try:
                _field = self.__class__._meta.get_field(field)
                if isinstance(_field, FileField):
                    try:
                        data[field] = getattr(self, field).url
                    except ValueError:
                        data[field] = ''
                else:
                    data[field] = self.serializable_value(field)
            except FieldDoesNotExist:
                if recursive:
                    try:
                        related = getattr(self, field)
                        data[field] = []
                        for obj in related.all():
                            data[field].append(obj.serialize())
                    except AttributeError:
                        pass
        return data
