from django.db import models


class Crew(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)

    class Meta:
        ordering = ["last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Airport(models.Model):
    airport_name = models.CharField(max_length=60)
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

    def __str__(self):
        return f"{self.source} to {self.destination}"


class AirplaneType(models.Model):
    airplane_type = models.CharField(max_length=60)

    class Meta:
        ordering = ["airplane_type"]

    def __str__(self):
        return self.airplane_type


class Airplane(models.Model):
    airplane_name = models.CharField(max_length=60)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)

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

    crew = models.ManyToManyField(Crew, blank=True)

    class Meta:
        ordering = ["departure_time"]

    def __str__(self):
        return f"{self.route.source} to {self.route.destination}"
