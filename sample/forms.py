from django import forms

from sample.models import Event


class EventForm(forms.Form):
    def __init__(self, *args, **kwargs):
        event_key = kwargs.pop('event_key', None)
        super(EventForm, self).__init__(*args, **kwargs)
        event = Event.objects.get(event_key=event_key)
        for field in event.event_fields.all():
            if field.field_type.name == 'NAME':
                self.fields[field.name] = forms.CharField(
                    label=field.display_name,
                    required=field.required,
                    max_length=100
                )
            elif field.field_type.name == 'ZIP_CODE':
                self.fields[field.name] = forms.CharField(
                    label=field.display_name,
                    required=field.required,
                    max_length=5
                )
            elif field.field_type.name == 'EMAIL':
                self.fields[field.name] = forms.EmailField(
                    label=field.display_name,
                    required=field.required,
                    max_length=255
                )
            elif field.field_type.name == 'CHECKBOX':
                self.fields[field.name] = forms.BooleanField(
                    label=field.display_name,
                    required=field.required
                )
