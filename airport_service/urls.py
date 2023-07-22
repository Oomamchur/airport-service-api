from django.urls import path, include
from rest_framework import routers

from airport_service.views import (
    AirportViewSet,
    CrewViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    FlightViewSet,
    OrderViewSet,
)

router = routers.DefaultRouter()
router.register("crew", CrewViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
