from datetime import datetime

from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from sample.models import Event, EventResponse
from sample.serializers import EventSerializer, EventResponseSerializer


class EventViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Get data for an event
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'event_key'

    def retrieve(self, request, *args, **kwargs):
        current_datetime = pytz.UTC.localize(datetime.utcnow())
        event = self.get_object()
        if event.start_date <= current_datetime <= event.end_date:
            data = {}
            frontend_fields = [
                'banner_image',
                'headline',
                'body',
                'legal',
                'field_data'
            ]
            for field in frontend_fields:
                value = getattr(event, field)
                if value:
                    data[field] = value
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

class EventResponseViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Submit a response to an event
    """
    queryset = EventResponse.objects.all()
    serializer_class = EventResponseSerializer

    event_key = serializer.data['event']

    try:
        current_datetime = pytz.UTC.localize(datetime.utcnow())
        event = Event.objects.get(
            event_key=event_key,
            start_date__lte=current_datetime,
            end_date__gte=current_datetime
        )
        request.data['event'] = event.pk
    except Event.DoesNotExist:
        return Response(data={"error": "Event Not Found"}, status=status.HTTP_404_NOT_FOUND)

    super(EventResponseViewset, self).create(request, *args, **kwargs)
    return Response(status=status.HTTP_201_CREATED)
