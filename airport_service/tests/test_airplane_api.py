from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from airport_service.models import Airplane, AirplaneType
from airport_service.serializers import AirplaneSerializer, AirplaneListSerializer

AIRPLANE_URL = reverse("airport:airplane-list")


def detail_url(airplane_id: int):
    return reverse_lazy("airport:airplane-detail", args=[airplane_id])


def test_airplane_type(**params) -> AirplaneType:
    defaults = {
        "airplane_type": "test type",
    }
    defaults.update(**params)
    return AirplaneType.objects.create(**defaults)


def test_airplane(**params) -> Airplane:
    defaults = {
        "airplane_name": "test",
        "rows": 1,
        "seats_in_row": 6
    }
    defaults.update(**params)
    return Airplane.objects.create(**defaults)


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(AIRPLANE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "Test1234",
        )
        self.client.force_authenticate(self.user)

    def test_auth_required(self) -> None:
        response = self.client.get(AIRPLANE_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "test1234",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane(self) -> None:
        airplane_type = test_airplane_type()
        test_airplane(type=airplane_type)
        test_airplane(airplane_name="test", type=airplane_type)
        airplane = Airplane.objects.all()

        serializer = AirplaneListSerializer(airplane, many=True)

        response = self.client.get(AIRPLANE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_airplane(self) -> None:
        airplane_type = test_airplane_type()
        airplane = test_airplane(type=airplane_type)
        url = detail_url(airplane.id)
        serializer = AirplaneSerializer(airplane)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_airplane_type(self) -> None:
        airplane_type = test_airplane_type()
        airplane = test_airplane(type=airplane_type)
        url = detail_url(airplane.id)
        payload = {
            "airplane_name": "changed",
        }

        response1 = self.client.patch(url, payload)
        response2 = self.client.get(url)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["airplane_name"], payload["airplane_name"])

    def test_delete_airplane(self) -> None:
        airplane_type = test_airplane_type()
        airplane = test_airplane(type=airplane_type)
        url = detail_url(airplane.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
