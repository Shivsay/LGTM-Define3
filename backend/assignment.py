from django.db import models
from .aircraft import Aircraft
from .flight import Flight

class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    flight = models.ForeignKey(
        Flight, 
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    aircraft = models.ForeignKey(
        Aircraft, 
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['flight', 'aircraft'], 
                name='unique_flight_aircraft_assignment'
            )
        ]

    def __str__(self):
        return f"Assignment {self.assignment_id}: {self.flight} assigned to {self.aircraft}"
