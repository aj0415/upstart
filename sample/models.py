import random
import string

from django.contrib.postgres.fields import JSONField
from django.db import models

import sample.globals as env


class EventFieldType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(EventFieldType, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class EventField(models.Model):
    name = models.CharField(unique=True, max_length=255)
    field_type = models.ForeignKey(EventFieldType, on_delete=models.CASCADE)
    display_name = models.TextField(blank=True, null=True, help_text='Display text next to field')
    required = models.BooleanField(default=True, help_text='Require user input')

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    banner_image = models.URLField(max_length=300, null=True, blank=True)
    headline = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    legal = models.TextField(null=True, blank=True)
    event_fields = models.ManyToManyField(EventField)
    url = models.URLField(max_length=300, null=True, editable=False)
    event_key = models.CharField(max_length=255, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def field_data(self):
        """
        Return list of fields and their corresponding information
        """
        field_data = []
        for field in self.event_fields.all():
            field_data.append(
                {
                    'name': field.name,
                    'field_type': field.field_type.name,
                    'display_name': field.display_name,
                    'required': field.required
                }
            )
        return field_data

    @property
    def field_list(self):
        """
        Return event fields comma separated in a string
        """
        return ",".join([f.name for f in self.event_fields.all()])

    def save(self, *args, **kwargs):
        """
        Generate key and url for event and save
        """
        if not self.event_key:
            self.event_key = "".join(random.choices(string.ascii_leters + string.digits, k=6))
        self.url = "{}?event={}".format(env.EVENT_BASE_URL, str(self.event_key))
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.name, self.event_key)


class EventResponse(models.Model):
    data = JSONField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
