from django.urls import path, include
from rest_framework import routers

from user.views import (
    AirportViewSet,
    CrewViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    FlightViewSet,
)

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("crew", CrewViewSet)
router.register("routes", RouteViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("flights", FlightViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
