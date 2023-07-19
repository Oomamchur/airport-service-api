from rest_framework import serializers

from airport_service.models import (
    Crew,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "airport_name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.StringRelatedField(many=False, read_only=True)
    destination = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "airplane_type")


class AirplaneSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Airplane
        fields = ("id", "airplane_name", "type", "capacity")


class FlightSerializer(serializers.ModelSerializer):
    airplane = serializers.StringRelatedField(many=False, read_only=True)
    route = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
        )


class FlightListSerializer(serializers.ModelSerializer):
    airplane = AirplaneSerializer(many=False)
    route = RouteSerializer(many=False)
    crew = CrewSerializer(many=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        )
