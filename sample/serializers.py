from rest_framework import serializers

from sample.models import Event, EventResponse


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'name',
            'start_date',
            'end_date',
            'banner_image',
            'headline',
            'body',
            'legal',
            'event_fields',
            'url',
            'event_key'
            'created_at',
            'updated_at'
        )

class EventResponseSerializer(serializers.ModelSerializer):
    event = serializers.CharField(source='event.event_key')

    class Meta:
        model = EventResponse
        fields = (
            'event',
            'data',
            'created_at'
        )

    def create(self, validated_data):
        event_key = validated_data['event']['event_key']
        event = Event.objects.get(id=int(event_key))
        validated_data['event'] = event

        valid_event_fields = set(event.event_fields.all().values_list('name', flat=True))
        data_fields = validated_data['data'].keys()
        if len(data_fields) != len(valid_event_fields):
            raise serializers.ValidationError('Invalid data provided')
        for data_field in data_fields:
            if data_field not in valid_event_fields:
                raise serializers.ValidationError('Invalid data provided')

        event_response = EventResponse(**validated_data)
        event_response.save()

        return event_response

class EventPageSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        event_fields = kwargs.pop('event_fields', None)
        super(EventPageSerializer, self).__init__(*args, **kwargs)
        for field in event_fields:
            if field.field_type == 'NAME':
                self.fields[field.name] = serializers.CharField(
                    label=field.display_name,
                    required=field.required,
                    max_length=100
                )
            elif field.field_type == 'ZIP_CODE':
                self.fields[field.name] = serializers.CharField(
                    label=field.display_name,
                    required=field.required,
                    max_length=5
                )
            elif field.field_type == 'EMAIL':
                self.fields[field.name] = serializers.EmailField(
                    label=field.display_name,
                    required=field.required,
                    max_length=255
                )
            elif field.field_type == 'CHECKBOX':
                self.fields[field.name] = serializers.BooleanField(
                    label=field.display_name,
                    required=field.required
                )
