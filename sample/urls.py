from rest_framework.routers import DefaultRouter

from sample.views import EventViewSet, EventResponseViewset

router = DefaultRouter()
router.register('event', EventViewSet)
router.register('eventresponse', EventResponseViewsetViewSet)

urlpatterns = router.urls
