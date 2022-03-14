from django import forms


class EventForm(forms.Form):
    def __init__(self, *args, **kwargs):
        event_fields = kwargs.pop('event_fields', None)
        super().__init__(*args, **kwargs)
        for field in event_fields:
            if field.field_type == 'NAME':
                self.fields[field.name] = forms.CharField(
                    label=field.display_name,
                    required=field.required,
                    max_length=100
                )
            elif field.field_type == 'ZIP_CODE':
                self.fields[field.name] = forms.CharField(
                    label=field.display_name,
                    required=field.required,
                    max_length=5
                )
            elif field.field_type == 'EMAIL':
                self.fields[field.name] = forms.EmailField(
                    label=field.display_name,
                    required=field.required,
                    max_length=255
                )
            elif field.field_type == 'CHECKBOX':
                self.fields[field.name] = forms.BooleanField(
                    label=field.display_name,
                    required=field.required
                )
