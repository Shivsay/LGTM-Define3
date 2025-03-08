from django.db import models

class Flight(models.Model):
    flight_identifier = models.CharField(max_length=20, primary_key=True)
    flight_date = models.DateField()
    departure_station = models.CharField(max_length=10)
    scheduled_time_of_departure = models.DateTimeField()
    arrival_station = models.CharField(max_length=10)
    scheduled_time_of_arrival = models.DateTimeField()
    aircraft_type = models.CharField(max_length=50)
    physical_seating_capacity = models.PositiveIntegerField()
    minimum_ground_time = models.PositiveIntegerField(help_text="Ground time in minutes")
    onward_flight = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='previous_flights'
    )

    class Meta:
        # Although flight_identifier is set as primary key, we might need to consider
        # a composite key of flight_identifier and flight_date in a real-world scenario
        constraints = [
            models.UniqueConstraint(
                fields=['flight_identifier', 'flight_date'], 
                name='unique_flight_per_day'
            )
        ]

    def __str__(self):
        return f"{self.flight_identifier} ({self.flight_date}): {self.departure_station} to {self.arrival_station}"
