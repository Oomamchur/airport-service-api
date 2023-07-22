from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from airport_service.models import Airport, Route
from airport_service.serializers import RouteListSerializer, RouteSerializer

ROUTE_URL = reverse("airport:route-list")


def detail_url(route_id: int):
    return reverse_lazy("airport:route-detail", args=[route_id])


def test_airport(**params) -> Airport:
    defaults = {
        "name": "Test",
        "closest_big_city": "Kyiv"
    }
    defaults.update(**params)
    return Airport.objects.create(**defaults)


def test_route(**params) -> Airport:
    defaults = {
        "distance": 1000
    }
    defaults.update(**params)
    return Route.objects.create(**defaults)


class UnauthenticatedRouteApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(ROUTE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test123@test.com",
            "Test1234",
        )
        self.client.force_authenticate(self.user)

    def test_auth_required(self) -> None:
        response = self.client.get(ROUTE_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin123@admin.com",
            "test1234",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_route(self) -> None:
        airport1 = test_airport()
        airport2 = test_airport(name="Test2", closest_big_city="Test2")
        route1 = test_route(source=airport1, destination=airport2)
        route2 = test_route(source=airport2, destination=airport1)
        routes = Route.objects.all()
        serializer = RouteListSerializer(routes, many=True)

        response = self.client.get(ROUTE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_route(self) -> None:
        airport1 = test_airport()
        airport2 = test_airport(name="Test2", closest_big_city="Test2")
        route = test_route(source=airport1, destination=airport2)
        url = detail_url(route.id)
        serializer = RouteSerializer(route)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_route(self) -> None:
        airport1 = test_airport()
        airport2 = test_airport(name="Test2", closest_big_city="Test2")
        route = test_route(source=airport1, destination=airport2)
        url = detail_url(route.id)
        payload = {
            "distance": 200
        }

        response1 = self.client.patch(url, payload)
        response2 = self.client.get(url)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["distance"], payload["distance"])

    def test_delete_route(self) -> None:
        airport1 = test_airport()
        airport2 = test_airport(name="Test2", closest_big_city="Test2")
        route = test_route(source=airport1, destination=airport2)
        url = detail_url(route.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
