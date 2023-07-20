from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from airport_service.models import Airport
from airport_service.serializers import AirportSerializer

AIRPORT_URL = reverse("airport:airport-list")


def detail_url(airport_id: int):
    return reverse_lazy("airport:airport-detail", args=[airport_id])


def test_airport(**params) -> Airport:
    defaults = {
        "name": "Boryspil",
        "closest_big_city": "Kyiv"
    }
    defaults.update(**params)
    return Airport.objects.create(**defaults)


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(AIRPORT_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "Test1234",
        )
        self.client.force_authenticate(self.user)

    def test_auth_required(self) -> None:
        response = self.client.get(AIRPORT_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "test1234",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airport(self) -> None:
        test_airport()
        test_airport(name="Boryspil-2")
        airport = Airport.objects.all()

        serializer = AirportSerializer(airport, many=True)

        response = self.client.get(AIRPORT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_airport(self) -> None:
        airport = test_airport()
        url = detail_url(airport.id)
        serializer = AirportSerializer(airport)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_airport(self) -> None:
        airport = test_airport()
        url = detail_url(airport.id)
        payload = {
            "name": "Boryspil-2"
        }

        response1 = self.client.patch(url, payload)
        response2 = self.client.get(url)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["name"], payload["name"])

    def test_delete_airport(self) -> None:
        airport = test_airport()
        url = detail_url(airport.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
