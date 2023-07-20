from django.db import transaction
from rest_framework import serializers

from airport_service.models import (
    Crew,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Ticket,
    Order,
)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source = serializers.StringRelatedField(many=False, read_only=True)
    destination = serializers.StringRelatedField(many=False, read_only=True)


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "airplane_type")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "airplane_name", "type", "rows", "seats_in_row")


class AirplaneListSerializer(AirplaneSerializer):
    type = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Airplane
        fields = ("id", "airplane_name", "type", "capacity")


class FlightSerializer(serializers.ModelSerializer):
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


class FlightListSerializer(serializers.ModelSerializer):
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


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        if not (1 <= attrs["row"] <= attrs["flight"].airplane.rows):
            raise serializers.ValidationError(
                f"row should be in range:"
                f" [1, {attrs['flight'].airplane.rows}]"
            )
        if not (1 <= attrs["seat"] <= attrs["flight"].airplane.seats_in_row):
            raise serializers.ValidationError(
                f"seat should be in range:"
                f" [1, {attrs['flight'].airplane.seats_in_row}]"
            )

    class Meta:
        model = Ticket
        fields = ("id", "flight", "row", "seat")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    @transaction.atomic
    def create(self, validated_data) -> Order:
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)
        for ticket_data in tickets_data:
            Ticket.objects.create(order=order, **ticket_data)
        return order
