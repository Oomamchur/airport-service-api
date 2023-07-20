from django.test import TestCase

from airport_service.models import Crew, Airport, Route, AirplaneType, Airplane, Flight


class ModelsTests(TestCase):
    def test_crew_str(self) -> None:
        crew = Crew.objects.create(first_name="test", last_name="test")

        self.assertEquals(str(crew), f"{crew.first_name} {crew.last_name}")

    def test_airport_str(self) -> None:
        airport = Airport.objects.create(name="test", closest_big_city="test city")

        self.assertEquals(str(airport), airport.name)

    def test_route_str(self) -> None:
        airport1 = Airport.objects.create(name="test1", closest_big_city="test city1")
        airport2 = Airport.objects.create(name="test2", closest_big_city="test city2")
        route = Route.objects.create(
            source=airport1,
            destination=airport2,
            distance=100
        )

        self.assertEquals(str(route), f"{route.source.name} to {route.destination.name}")

    def test_airplane_type_str(self) -> None:
        airplane_type = AirplaneType.objects.create(airplane_type="big")

        self.assertEquals(str(airplane_type), airplane_type.airplane_type)

    def test_airplane_str(self) -> None:
        type = AirplaneType.objects.create(airplane_type="big")
        airplane = Airplane.objects.create(airplane_name="test", type=type, rows=3, seats_in_row=4)

        self.assertEquals(str(airplane), airplane.airplane_name)

    def test_flight_str(self) -> None:
        type = AirplaneType.objects.create(airplane_type="big")
        airplane = Airplane.objects.create(airplane_name="test", type=type, rows=3, seats_in_row=4)
        airport1 = Airport.objects.create(name="test1", closest_big_city="test city1")
        airport2 = Airport.objects.create(name="test2", closest_big_city="test city2")
        route = Route.objects.create(
            source=airport1,
            destination=airport2,
            distance=100
        )
        flight = Flight.objects.create(
            route=route,
            airplane=airplane,
            departure_time="2023-07-19 18:30:00",
            arrival_time="2023-07-20 18:30:00",
        )

        self.assertEquals(str(flight), f"{flight.route.source} to {flight.route.destination}")
