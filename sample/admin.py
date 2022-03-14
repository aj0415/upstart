from django.contrib import admin

from project.utils import ExportJsonMixin
from sample.models import (
    Event,
    EventField,
    EventFieldType,
    EventResponse,
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'start_date',
        'end_date',
        'url',
        'event_key',
        'updated_at',
        'created_at'
    )
    search_fields = ['name', 'event_key']
    case_insensitive_search_fields = ['name', 'event_key']

@admin.register(EventField)
class EventFieldAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'field_type',
        'display_name',
        'required'
    )
    search_fields = ['name', 'field_type__name']
    case_insensitive_search_fields = ['name', 'field_type__name']

@admin.register(EventFieldType)
class EventFieldTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description'
    )
    search_fields = ['name']
    case_insensitive_search_fields = ['name']

@admin.register(EventResponse)
class EventResponseAdmin(admin.ModelAdmin, ExportJsonMixin):
    list_display = (
        'data',
        'event',
        'created_at'
    )
    search_fields = ['event__name', 'event__event_key']
    case_insensitive_search_fields = ['event__name', 'event__event_key']
    actions = ["export_json_as_csv"]
