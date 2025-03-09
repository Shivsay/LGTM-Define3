import os
import sys
import django
from faker import Faker
import random
import datetime

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

def create_flights(n):
    aircrafts = list(Aircraft.objects.all())
    all_flights = []  # Store created flights to create onward relationships later
    
    for aircraft in aircrafts:
        previous_arrival_station = None
        flight_sequence = []  # Store flights for this aircraft to create trip sequences
        
        for _ in range(n // len(aircrafts)):
            departure_time = fake.date_time_between_dates(
                datetime_start=datetime.datetime(2025, 3, 9),
                datetime_end=datetime.datetime(2025, 3, 15),
                tzinfo=django.utils.timezone.get_current_timezone()
            )
            arrival_time = departure_time + datetime.timedelta(hours=random.randint(4, 24))
            
            aircraft_type = aircraft.aircraft_type
            max_seating_capacity = aircraft.seating_capacity
            
            if previous_arrival_station:
                departure_station = previous_arrival_station
            else:
                departure_station = fake.random_element(elements=('LHR', 'JFK', 'CDG', 'FRA'))
            
            arrival_station = fake.random_element(elements=('LHR', 'JFK', 'CDG', 'FRA'))
            
            # Ensure departure and arrival stations are different
            while arrival_station == departure_station:
                arrival_station = fake.random_element(elements=('LHR', 'JFK', 'CDG', 'FRA'))
            
            flight = Flight.objects.create(
                flight_identifier=fake.unique.bothify(text='XX###'),
                flight_date=departure_time.date(),
                departure_station=departure_station,
                scheduled_time_of_departure=departure_time,
                arrival_station=arrival_station,
                scheduled_time_of_arrival=arrival_time,
                aircraft_type=aircraft_type,
                physical_seating_capacity=random.randint(100, max_seating_capacity),
                minimum_ground_time=random.randint(30, 120),
                onward_flight=None  # Will update this later
            )
            
            flight_sequence.append(flight)
            all_flights.append(flight)
            previous_arrival_station = arrival_station
        
        # Create onward flight relationships within the sequence
        for i in range(len(flight_sequence) - 1):
            flight_sequence[i].onward_flight = flight_sequence[i + 1]
            flight_sequence[i].save()

def create_preassignments(n):
    aircrafts = list(Aircraft.objects.all())
    for _ in range(n):
        if random.random() > 0.5:  # 50% chance to create a preassignment
            start_time = fake.date_time_between_dates(
                datetime_start=datetime.datetime(2025, 3, 9),
                datetime_end=datetime.datetime(2025, 3, 15),
                tzinfo=django.utils.timezone.get_current_timezone()
            )
            end_time = start_time + datetime.timedelta(hours=random.randint(1, 48))  # Longer preassignments for maintenance
            
            activity_type = random.choice(['Maintenance', 'Cleaning', 'Inspection', 'Training'])
            
            PreAssignment.objects.create(
                aircraft=random.choice(aircrafts),
                start_time=start_time,
                end_time=end_time,
                description=activity_type
            )

if __name__ == '__main__':
    # Clear existing data (optional)
    print("Clearing existing data...")
    Aircraft.objects.all().delete()
    Flight.objects.all().delete()
    PreAssignment.objects.all().delete()
    
    print("Creating aircraft...")
    create_aircraft(20)
    print("Creating flights...")
    create_flights(50)
    print("Creating preassignments...")
    create_preassignments(10)
    print("Data generation complete!")