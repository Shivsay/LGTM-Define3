from rest_framework import serializers
from .models import Aircraft

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'  # or specify the fields you want to include
