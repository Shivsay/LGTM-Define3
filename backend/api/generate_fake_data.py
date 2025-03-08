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
    for _ in range(n):
        departure_time = fake.date_time_between_dates(
            datetime_start=datetime.datetime(2025, 3, 9),
            datetime_end=datetime.datetime(2025, 3, 10),
            tzinfo=django.utils.timezone.get_current_timezone()
        )
        arrival_time = departure_time + datetime.timedelta(hours=random.randint(4, 24))
        
        Flight.objects.create(
            flight_identifier=fake.unique.bothify(text='XX###'),
            flight_date=departure_time.date(),
            departure_station=fake.random_element(elements=('LHR', 'JFK', 'CDG', 'FRA')),
            scheduled_time_of_departure=departure_time,
            arrival_station=fake.random_element(elements=('LHR', 'JFK', 'CDG', 'FRA')),
            scheduled_time_of_arrival=arrival_time,
            aircraft_type=fake.random_element(elements=('A320', 'B737', 'A380', 'B777')),
            physical_seating_capacity=random.randint(100, 300),
            minimum_ground_time=random.randint(30, 120)
        )

def create_preassignments(n):
    aircrafts = list(Aircraft.objects.all())
    for _ in range(n):
        if random.random() > 0.5:  # 50% chance to create a preassignment
            start_time = fake.date_time_between_dates(
                datetime_start=datetime.datetime(2025, 3, 9),
                datetime_end=datetime.datetime(2025, 3, 10),
                tzinfo=django.utils.timezone.get_current_timezone()
            )
            end_time = start_time + datetime.timedelta(hours=random.randint(1, 2))
            
            PreAssignment.objects.create(
                aircraft=random.choice(aircrafts),
                start_time=start_time,
                end_time=end_time,
                description=fake.sentence()
            )
# def create_assignments(n):
#     flights = list(Flight.objects.all())
#     aircrafts = list(Aircraft.objects.all())
#     for _ in range(n):
#         Assignment.objects.create(
#             flight=random.choice(flights),
#             aircraft=random.choice(aircrafts)
#         )

if __name__ == '__main__':
    create_aircraft(10)
    create_flights(50)
    create_preassignments(10)
    # create_assignments(50)