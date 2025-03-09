from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Aircraft, Flight
from .solver import solve_tail_assignment
from .utils import get_db_last_modified_time
import json
import os
from django.db import connection

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import AircraftSerializer, FlightSerializer

from django.views.decorators.csrf import csrf_exempt

DB_PATH = './db.sqlite3'
SCHEDULE_PATH = './api/schedule.json'
TIMESTAMP_PATH = './api/db_timestamp.txt'

# Update the solve_assignment function to include parameters from the request

@csrf_exempt
def solve_assignment(request):
    # Parse parameters from the request
    data = json.loads(request.body) if request.body else {}
    
    # Extract parameters with defaults
    aircraft_subtype = data.get('aircraft_subtype')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    respect_preassignments = data.get('respect_preassignments', True)
    excluded_aircraft = data.get('excluded_aircraft', [])
    maintain_trips = data.get('maintain_trips', True)
    
    # Convert date strings to date objects if provided
    start_date = None
    end_date = None
    if start_date_str:
        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid start_date format'}, status=400)
    
    if end_date_str:
        try:
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid end_date format'}, status=400)
    
    # Call the solver with the parameters
    assignments = solve_tail_assignment(
        aircraft_subtype=aircraft_subtype,
        start_date=start_date,
        end_date=end_date,
        respect_preassignments=respect_preassignments,
        excluded_aircraft=excluded_aircraft,
        maintain_trips=maintain_trips
    )
    
    if assignments is None:
        return JsonResponse({'status': 'error', 'message': 'No solution found'}, status=400)
    
    result = [{'aircraft': aircraft, 'schedule': schedule} for aircraft, schedule in assignments.items()]
    
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
    #print(serializer.data)
    return JsonResponse(serializer.data, safe=False)



def flight_list(request):
    flights = Flight.objects.all()
    serializer = FlightSerializer(flights, many=True)
    print(serializer.data)
    return JsonResponse(serializer.data, safe=False)


def del_all_aircraft():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM api_aircraft")
    

def del_all_flight():
    Flight.objects.all().delete()
    
def del_all(request):
    Aircraft.objects.all().delete()
    #del_all_aircraft()
