from django.db import models

from apitils.models import SerializeMixin


class Person(SerializeMixin, models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.first_name
