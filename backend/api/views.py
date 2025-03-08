from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Aircraft
from .solver import solve_tail_assignment
from .utils import get_db_last_modified_time
import json
import os

from django.views.decorators.csrf import csrf_exempt

DB_PATH = 'backend/db.sqlite3'
SCHEDULE_PATH = 'backend/api/schedule.json'
TIMESTAMP_PATH = 'backend/api/db_timestamp.txt'

def example_view(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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

@csrf_exempt
def aircraft_post_view(request):
    if request.method == 'POST':
        try:
            # Load the JSON data from the request body
            data = json.loads(request.body)

            # Validate required fields
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

            # Return a success response
            return JsonResponse({'message': 'Data received', 'data': {
                'aircraft_registration': aircraft_registration,
                'aircraft_type': aircraft_type,
                'seating_capacity': seating_capacity
            }}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            # Log the exception (optional)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
