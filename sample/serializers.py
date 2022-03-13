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
