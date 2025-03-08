from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Aircraft
from .solver import solve_tail_assignment
import json

from django.views.decorators.csrf import csrf_exempt

def example_view(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def solve_assignment(request):
    assignments = solve_tail_assignment()
    if assignments is None:
        return JsonResponse({'status': 'error', 'message': 'No solution found'}, status=400)
    
    result = [{'flight': str(flight), 'aircraft': str(aircraft)} for flight, aircraft in assignments]
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
