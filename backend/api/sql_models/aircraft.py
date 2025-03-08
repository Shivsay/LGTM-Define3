from django.db import models

class Aircraft(models.Model):
    aircraft_registration = models.CharField(max_length=10, primary_key=True)
    aircraft_type = models.CharField(max_length=50)
    seating_capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.aircraft_registration} ({self.aircraft_type})"
