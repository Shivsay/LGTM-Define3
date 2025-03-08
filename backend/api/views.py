from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Aircraft
from .models import Flight
from .solver import solve_tail_assignment
from .utils import get_db_last_modified_time
import json
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AircraftSerializer, FlightSerializer

from django.views.decorators.csrf import csrf_exempt

DB_PATH = 'backend/db.sqlite3'
SCHEDULE_PATH = 'backend/api/schedule.json'
TIMESTAMP_PATH = 'backend/api/db_timestamp.txt'



def solve_assignment(request):
    current_timestamp = get_db_last_modified_time(DB_PATH)

    # Check if the timestamp file exists
    if os.path.exists(TIMESTAMP_PATH):
        with open(TIMESTAMP_PATH, 'r') as timestamp_file:
            previous_timestamp = float(timestamp_file.read().strip())
    else:
        previous_timestamp = None

    # Check if the database has changed
    if previous_timestamp == current_timestamp:
        # Check if the schedule file exists
        if os.path.exists(SCHEDULE_PATH):
            with open(SCHEDULE_PATH, 'r') as schedule_file:
                schedule = json.load(schedule_file)
            return JsonResponse({'status': 'success', 'assignments': schedule})

    # Run the solver
    assignments = solve_tail_assignment()
    if assignments is None:
        return JsonResponse({'status': 'error', 'message': 'No solution found'}, status=400)
    
    result = [{'aircraft': aircraft, 'schedule': schedule} for aircraft, schedule in assignments.items()]

    # Save the new timestamp and schedule
    with open(TIMESTAMP_PATH, 'w') as timestamp_file:
        timestamp_file.write(str(current_timestamp))
    with open(SCHEDULE_PATH, 'w') as schedule_file:
        json.dump(result, schedule_file)

    return JsonResponse({'status': 'success', 'assignments': result})

def example_view(request):
    return HttpResponse("Hello, world. You're at the index.")


@csrf_exempt
def aircraft_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            aircraft_registration = data.get('aircraft_registration')
            aircraft_type = data.get('aircraft_type')
            seating_capacity = data.get('seating_capacity')

            if not aircraft_registration or not aircraft_type or seating_capacity is None:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

                
            aircraft = Aircraft(
                aircraft_registration=aircraft_registration,
                aircraft_type=aircraft_type,
                seating_capacity=seating_capacity
            )
            aircraft.save()  

            return JsonResponse({'message': 'Data received', 'data': {
                'aircraft_registration': aircraft_registration,
                'aircraft_type': aircraft_type,
                'seating_capacity': seating_capacity
            }}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def flight_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            flight_identifier = data.get('flight_identifier')
            flight_date = data.get('flight_date')
            departure_station = data.get('departure_station')
            scheduled_time_of_departure = data.get('scheduled_time_of_departure')
            arrival_station = data.get('arrival_station')
            scheduled_time_of_arrival = data.get('scheduled_time_of_arrival')
            aircraft_type = data.get('aircraft_type')
            physical_seating_capacity = data.get('physical_seating_capacity')
            minimum_ground_time = data.get('minimum_ground_time')
            onward_flight = data.get('onward_flight')

            if not flight_identifier or not flight_date or not departure_station or not scheduled_time_of_departure or not arrival_station or not scheduled_time_of_arrival or not aircraft_type or physical_seating_capacity is None or minimum_ground_time is None:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            flight = Flight(
                flight_identifier=flight_identifier,
                flight_date=flight_date,
                departure_station=departure_station,
                scheduled_time_of_departure=scheduled_time_of_departure,
                arrival_station=arrival_station,
                scheduled_time_of_arrival=scheduled_time_of_arrival,
                aircraft_type=aircraft_type,
                physical_seating_capacity=physical_seating_capacity,
                minimum_ground_time=minimum_ground_time,
                onward_flight=onward_flight  #can be null/should be null
            )
            flight.save()

            return JsonResponse({'message': 'Flight created successfully', 'data': {
                'flight_identifier': flight_identifier,
                'flight_date': flight_date,
                'departure_station': departure_station,
                'scheduled_time_of_departure': scheduled_time_of_departure,
                'arrival_station': arrival_station,
                'scheduled_time_of_arrival': scheduled_time_of_arrival,
                'aircraft_type': aircraft_type,
                'physical_seating_capacity': physical_seating_capacity,
                'minimum_ground_time': minimum_ground_time,
                'onward_flight': onward_flight
            }}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def aircraft_list(request):
    aircrafts = Aircraft.objects.all()
    serializer = AircraftSerializer(aircrafts, many=True)
    print(serializer.data)
    #return Response(serializer.data)

def flight_list(request):
    flights = Flight.objects.all()
    serializer = FlightSerializer(flights, many=True)
    print(serializer.data)
    #return Response(serializer.data) 

