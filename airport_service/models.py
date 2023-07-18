from django.db import models


class Crew(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Airport(models.Model):
    airport_name = models.CharField(max_length=60)
    closest_big_city = models.CharField(max_length=60)

    def __str__(self):
        return self.airport_name


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE)
    distance = models.IntegerField()


class AirplaneType(models.Model):
    airplane_type = models.CharField(max_length=60)

    def __str__(self):
        return self.airplane_type


class Airplane(models.Model):
    airplane_name = models.CharField(max_length=60)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)

    def __str__(self):
        return self.airplane_name


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
