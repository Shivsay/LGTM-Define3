from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from .solver import solve_tail_assignment

def optimize_tail_assignment(request):
    flights = {
        "AF514": {"passengers": 100, "cost": {"A320": 5000, "A380": 10000}},
        "BA214": {"passengers": 200, "cost": {"A320": 6000, "A380": 12000}},
        "AF112": {"passengers": 150, "cost": {"A320": 5500, "A380": 11000}},
        "BA312": {"passengers": 250, "cost": {"A320": 7000, "A380": 14000}},
    }
    aircraft = {
        "A320": {"capacity": 200},
        "A380": {"capacity": 500},
    }

    result = solve_tail_assignment(flights, aircraft)
    
    if result:
        return JsonResponse({"assignment": result})
    else:
        return JsonResponse({"error": "No feasible assignment found"}, status=400)