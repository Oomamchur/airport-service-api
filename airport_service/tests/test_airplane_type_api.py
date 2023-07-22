from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from airport_service.models import AirplaneType
from airport_service.serializers import AirplaneTypeSerializer

AIRPLANE_TYPE_URL = reverse("airport:airplanetype-list")


def detail_url(airplane_type_id: int):
    return reverse_lazy("airport:airplanetype-detail", args=[airplane_type_id])


def test_airplane_type(**params) -> AirplaneType:
    defaults = {
        "airplane_type": "test type"
    }
    defaults.update(**params)
    return AirplaneType.objects.create(**defaults)


class UnauthenticatedAirplaneTypeApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(AIRPLANE_TYPE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneTypeApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test123@test.com",
            "Test1234",
        )
        self.client.force_authenticate(self.user)

    def test_auth_required(self) -> None:
        response = self.client.get(AIRPLANE_TYPE_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTypeApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin123@admin.com",
            "test1234",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane_type(self) -> None:
        test_airplane_type()
        airplane_type = AirplaneType.objects.all()

        serializer = AirplaneTypeSerializer(airplane_type, many=True)

        response = self.client.get(AIRPLANE_TYPE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_airplane_type(self) -> None:
        airplane_type = test_airplane_type()
        url = detail_url(airplane_type.id)
        serializer = AirplaneTypeSerializer(airplane_type)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_airplane_type(self) -> None:
        airplane_type = test_airplane_type()
        url = detail_url(airplane_type.id)
        payload = {
            "airplane_type": "changed",
        }

        response1 = self.client.patch(url, payload)
        response2 = self.client.get(url)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["airplane_type"], payload["airplane_type"])

    def test_delete_airplane_type(self) -> None:
        airplane_type = test_airplane_type()
        url = detail_url(airplane_type.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
