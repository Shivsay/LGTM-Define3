from rest_framework import serializers
from .models import Aircraft
from .models import Flight

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'  # or specify the fields you want to include

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'  # or specify the fields you want to include

