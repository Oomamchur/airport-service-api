from django.contrib.auth import get_user_model
from django.db.models import F, Count
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from airport_service.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
)
from airport_service.serializers import (
    FlightListSerializer,
    FlightDetailSerializer,
)

FLIGHT_URL = reverse("airport:flight-list")


def detail_url(flight_id: int):
    return reverse_lazy("airport:flight-detail", args=[flight_id])


def test_airplane_type(**params) -> AirplaneType:
    defaults = {
        "airplane_type": "test type",
    }
    defaults.update(**params)
    return AirplaneType.objects.create(**defaults)


def test_airplane(**params) -> Airplane:
    defaults = {"airplane_name": "Mriya", "rows": 1, "seats_in_row": 6}
    defaults.update(**params)
    return Airplane.objects.create(**defaults)


def test_airport(**params) -> Airport:
    defaults = {"name": "Boryspil", "closest_big_city": "Kyiv"}
    defaults.update(**params)
    return Airport.objects.create(**defaults)


def test_route(**params) -> Airport:
    defaults = {"distance": 1000}
    defaults.update(**params)
    return Route.objects.create(**defaults)


def test_flight(**params) -> Airport:
    defaults = {
        "departure_time": "2023-07-19T19:30:46+03:00",
        "arrival_time": "2023-07-19T21:30:00+03:00",
    }
    defaults.update(**params)
    return Flight.objects.create(**defaults)


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(FLIGHT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "Test1234",
        )
        self.client.force_authenticate(self.user)

    def test_list_flight(self) -> None:
        airplane_type = test_airplane_type()
        airplane1 = test_airplane(type=airplane_type)
        airplane2 = test_airplane(airplane_name="Cessna", type=airplane_type)
        airport1 = test_airport()
        airport2 = test_airport(name="Test", closest_big_city="Test")
        route1 = test_route(source=airport1, destination=airport2)
        route2 = test_route(source=airport2, destination=airport1)
        test_flight(airplane=airplane1, route=route1)
        test_flight(airplane=airplane2, route=route2)
        flights = Flight.objects.annotate(
            tickets_available=(
                F("airplane__rows") * F("airplane__seats_in_row")
                - Count("tickets")
            )
        )
        serializer = FlightListSerializer(flights, many=True)

        response = self.client.get(FLIGHT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_flight_by_source(self) -> None:
        airplane_type = test_airplane_type()
        airplane1 = test_airplane(type=airplane_type)
        airplane2 = test_airplane(airplane_name="Cessna", type=airplane_type)
        airport1 = test_airport()
        airport2 = test_airport(name="Test", closest_big_city="Test")
        route1 = test_route(source=airport1, destination=airport2)
        route2 = test_route(source=airport2, destination=airport1)
        test_flight(airplane=airplane1, route=route1)
        test_flight(airplane=airplane2, route=route2)
        annotated_flights = Flight.objects.annotate(
            tickets_available=(
                F("airplane__rows") * F("airplane__seats_in_row")
                - Count("tickets")
            )
        )
        serializer1 = FlightListSerializer(annotated_flights[0])
        serializer2 = FlightListSerializer(annotated_flights[1])

        response = self.client.get(FLIGHT_URL, {"source": "Test"})

        self.assertIn(serializer2.data, response.data["results"])
        self.assertNotIn(serializer1.data, response.data["results"])

    def test_filter_flight_by_date(self) -> None:
        airplane_type = test_airplane_type()
        airplane1 = test_airplane(type=airplane_type)
        airplane2 = test_airplane(airplane_name="Cessna", type=airplane_type)
        airport1 = test_airport()
        airport2 = test_airport(name="Test", closest_big_city="Test")
        route1 = test_route(source=airport1, destination=airport2)
        route2 = test_route(source=airport2, destination=airport1)
        test_flight(airplane=airplane1, route=route1)
        test_flight(
            airplane=airplane2,
            route=route2,
            departure_time="2023-07-08T21:30:00+03:00",
        )
        annotated_flights = Flight.objects.annotate(
            tickets_available=(
                F("airplane__rows") * F("airplane__seats_in_row")
                - Count("tickets")
            )
        )
        serializer1 = FlightListSerializer(annotated_flights[0])
        serializer2 = FlightListSerializer(annotated_flights[1])

        response = self.client.get(FLIGHT_URL, {"date": "2023-07-08"})

        self.assertIn(serializer2.data, response.data["results"])
        self.assertNotIn(serializer1.data, response.data["results"])

    def test_retrieve_flight(self) -> None:
        airplane_type = test_airplane_type()
        airplane = test_airplane(type=airplane_type)
        airport1 = test_airport()
        airport2 = test_airport(name="Test", closest_big_city="Test")
        route = test_route(source=airport1, destination=airport2)
        flight = test_flight(airplane=airplane, route=route)
        url = detail_url(flight.id)
        serializer = FlightDetailSerializer(flight)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_flight_forbidden(self) -> None:
        airplane_type = test_airplane_type()
        airplane = test_airplane(type=airplane_type)
        airport1 = test_airport()
        airport2 = test_airport(name="Test", closest_big_city="Test")
        route = test_route(source=airport1, destination=airport2)
        payload = {
            "route": route,
            "airplane": airplane,
            "departure_time": "2023-07-19T19:30:46+03:00",
            "arrival_time": "2023-07-19T21:30:00+03:00",
        }
        response = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "test1234", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_flight(self) -> None:
        airplane_type = test_airplane_type()
        airplane = test_airplane(type=airplane_type)
        airport1 = test_airport()
        airport2 = test_airport(name="Test", closest_big_city="Test")
        route = test_route(source=airport1, destination=airport2)
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2024-07-19T19:30:46+03:00",
            "arrival_time": "2024-07-19T21:30:00+03:00",
        }
        response = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_route(self) -> None:
        airplane_type = test_airplane_type()
        airplane = test_airplane(type=airplane_type)
        airport1 = test_airport()
        airport2 = test_airport(name="Test", closest_big_city="Test")
        route = test_route(source=airport1, destination=airport2)
        flight = test_flight(airplane=airplane, route=route)
        url = detail_url(flight.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
