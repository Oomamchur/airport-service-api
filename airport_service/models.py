from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Crew(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural = "crew"
        ordering = ["last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Airport(models.Model):
    airport_name = models.CharField(max_length=60, unique=True)
    closest_big_city = models.CharField(max_length=60)

    class Meta:
        ordering = ["airport_name"]

    def __str__(self):
        return self.airport_name


class Route(models.Model):
    source = models.ForeignKey(
        Airport, related_name="source_routs", on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        Airport, related_name="destination_routs", on_delete=models.CASCADE
    )
    distance = models.IntegerField()

    class Meta:
        ordering = ["source"]
        unique_together = ("source", "destination")

    def clean(self):
        if self.source == self.destination:
            raise ValidationError("Source and destination cannot be the same.")
        if self.distance <= 0:
            raise ValidationError("Distance should be greater than 0.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.source} to {self.destination}"


class AirplaneType(models.Model):
    airplane_type = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ["airplane_type"]

    def __str__(self):
        return self.airplane_type


class Airplane(models.Model):
    airplane_name = models.CharField(max_length=60)
    type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    class Meta:
        ordering = ["airplane_name"]

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.airplane_name


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    crew = models.ManyToManyField(Crew)

    class Meta:
        ordering = ["departure_time"]

    def __str__(self):
        return f"{self.route.source} to {self.route.destination}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    def clean(self) -> None:
        if not (1 <= self.row <= self.flight.airplane.rows):
            raise ValidationError(
                f"row should be in range:" f" [1, {self.flight.airplane.rows}]"
            )
        if not (1 <= self.seat <= self.flight.airplane.seats_in_row):
            raise ValidationError(
                f"seat should be in range:"
                f" [1, {self.flight.airplane.seats_in_row}]"
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("flight", "row", "seat")

    def __str__(self) -> str:
        return f"{str(self.flight)} (row: {self.row}, seat: {self.seat})"
