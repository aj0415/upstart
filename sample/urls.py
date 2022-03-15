from django.urls import path
from rest_framework.routers import DefaultRouter

from sample.views import EventView, EventViewSet, EventResponseViewset

router = DefaultRouter()
router.register('event', EventViewSet)
router.register('eventresponse', EventResponseViewset)

urlpatterns = [
    path('eventform', EventView.as_view()),
]
urlpatterns += router.urls
