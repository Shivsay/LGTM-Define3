from ortools.linear_solver import pywraplp
from .models import Aircraft, Flight, PreAssignment

def solve_tail_assignment():
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

    # Fetch data from the database
    aircrafts = list(Aircraft.objects.all())
    flights = list(Flight.objects.all())
    preassignments = list(PreAssignment.objects.all())

    # Create variables
    x = {}
    for flight in flights:
        for aircraft in aircrafts:
            x[(flight.id, aircraft.id)] = solver.BoolVar(f'x_{flight.id}_{aircraft.id}')

    # Create constraints
    for flight in flights:
        solver.Add(sum(x[(flight.id, aircraft.id)] for aircraft in aircrafts) == 1)

    for aircraft in aircrafts:
        for flight in flights:
            if flight.aircraft_type != aircraft.aircraft_type or flight.physical_seating_capacity > aircraft.seating_capacity:
                solver.Add(x[(flight.id, aircraft.id)] == 0)

    for preassignment in preassignments:
        for flight in flights:
            if flight.scheduled_time_of_departure < preassignment.end_time and flight.scheduled_time_of_arrival > preassignment.start_time:
                solver.Add(x[(flight.id, preassignment.aircraft.id)] == 0)

    # Objective function
    solver.Minimize(solver.Sum(x[(flight.id, aircraft.id)] for flight in flights for aircraft in aircrafts))

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        assignments = []
        for flight in flights:
            for aircraft in aircrafts:
                if x[(flight.id, aircraft.id)].solution_value() == 1:
                    assignments.append((flight, aircraft))
        return assignments
    else:
        return None