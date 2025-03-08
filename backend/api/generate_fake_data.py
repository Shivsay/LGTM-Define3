import os
import sys
import django
from faker import Faker
import random
import datetime
import json

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'definebackend.settings')
django.setup()

from api.models import Aircraft, Flight, PreAssignment

fake = Faker()

def create_aircraft(n):
    for _ in range(n):
        aircraft_type = fake.random_element(elements=('A320', 'B737', 'A380', 'B777'))
        seating_capacity = {
            'A320': random.randint(150, 180),
            'B737': random.randint(130, 160),
            'A380': random.randint(400, 500),
            'B777': random.randint(300, 400)
        }[aircraft_type]
        
        Aircraft.objects.create(
            aircraft_registration=fake.unique.bothify(text='??###'),
            aircraft_type=aircraft_type,
            seating_capacity=seating_capacity
        )

def create_flights_and_preassignments(n_flights, n_preassignments):
    aircrafts = list(Aircraft.objects.all())
    data = []
    
    for aircraft in aircrafts:
        current_time = datetime.datetime(2025, 3, 9, tzinfo=django.utils.timezone.get_current_timezone())
        schedule = []
        
        for _ in range(n_flights):
            departure_time = current_time
            arrival_time = departure_time + datetime.timedelta(hours=random.randint(4, 24))
            
            flight = Flight.objects.create(
                flight_identifier=fake.unique.bothify(text='FL###'),
                flight_date=departure_time.date(),
                departure_station=fake.random_element(elements=('LHR', 'JFK', 'CDG', 'FRA')),
                scheduled_time_of_departure=departure_time,
                arrival_station=fake.random_element(elements=('LHR', 'JFK', 'CDG', 'FRA')),
                scheduled_time_of_arrival=arrival_time,
                aircraft_type=aircraft.aircraft_type,
                physical_seating_capacity=aircraft.seating_capacity,
                minimum_ground_time=random.randint(30, 120)
            )
            
            schedule.append({
                "type": "flight",
                "flight_identifier": flight.flight_identifier,
                "start_time": departure_time.isoformat(),
                "end_time": arrival_time.isoformat(),
                "departure_station": flight.departure_station,
                "arrival_station": flight.arrival_station
            })
            
            current_time = arrival_time + datetime.timedelta(minutes=random.randint(30, 120))
        
        for _ in range(n_preassignments):
            if random.random() > 0.5:  # 50% chance to create a preassignment
                start_time = current_time
                end_time = start_time + datetime.timedelta(hours=random.randint(1, 2))
                
                preassignment = PreAssignment.objects.create(
                    aircraft=aircraft,
                    start_time=start_time,
                    end_time=end_time,
                    description=fake.sentence()
                )
                
                schedule.append({
                    "type": "preassignment",
                    "description": preassignment.description,
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat()
                })
                
                current_time = end_time + datetime.timedelta(minutes=random.randint(30, 120))
        
        data.append({
            "aircraft": aircraft.aircraft_registration,
            "schedule": schedule
        })
    
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    create_aircraft(10)
    create_flights_and_preassignments(5, 3)