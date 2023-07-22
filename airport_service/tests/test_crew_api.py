from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from airport_service.models import Crew
from airport_service.serializers import CrewSerializer

CREW_URL = reverse("airport:crew-list")


def detail_url(crew_id: int):
    return reverse_lazy("airport:crew-detail", args=[crew_id])


def test_crew(**params) -> Crew:
    defaults = {
        "first_name": "Name",
        "last_name": "Surname",
    }
    defaults.update(**params)
    return Crew.objects.create(**defaults)


class UnauthenticatedCrewApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(CREW_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test123@test.com",
            "Test1234",
        )
        self.client.force_authenticate(self.user)

    def test_auth_required(self) -> None:
        response = self.client.get(CREW_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin123@admin.com",
            "test1234",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_crew(self) -> None:
        test_crew()
        crew = Crew.objects.all()

        serializer = CrewSerializer(crew, many=True)

        response = self.client.get(CREW_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_crew(self) -> None:
        crew = test_crew()
        url = detail_url(crew.id)
        serializer = CrewSerializer(crew)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_crew(self) -> None:
        crew = test_crew()
        url = detail_url(crew.id)
        payload = {
            "first_name": "changed name",
        }

        response1 = self.client.patch(url, payload)
        response2 = self.client.get(url)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["first_name"], payload["first_name"])

    def test_delete_crew(self) -> None:
        crew = test_crew()
        url = detail_url(crew.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
