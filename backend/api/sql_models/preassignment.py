from django.db import models
from .aircraft import Aircraft

class PreAssignment(models.Model):
    preassignment_id = models.AutoField(primary_key=True)
    aircraft = models.ForeignKey(
        Aircraft, 
        on_delete=models.CASCADE,
        related_name='preassignments'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"PreAssignment {self.preassignment_id}: {self.description} for {self.aircraft}"
