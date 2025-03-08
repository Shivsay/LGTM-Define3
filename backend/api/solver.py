from ortools.linear_solver import pywraplp
from .models import Aircraft, Flight, PreAssignment
import datetime
import logging

def solve_tail_assignment():
    try:
        print("Creating the solver...")
        # Create the solver
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            print("Solver not created.")
            return None

        print("Fetching data from the database...")
        # Fetch data from the database
        aircrafts = list(Aircraft.objects.all())
        flights = list(Flight.objects.all())
        preassignments = list(PreAssignment.objects.all())

        print("Creating variables...")
        # Create variables
        x = {}
        for flight in flights:
            for aircraft in aircrafts:
                x[(flight.flight_identifier, aircraft.aircraft_registration)] = solver.BoolVar(f'x_{flight.flight_identifier}_{aircraft.aircraft_registration}')

        print("Creating constraints for flights...")
        # Create constraints
        for flight in flights:
            solver.Add(sum(x[(flight.flight_identifier, aircraft.aircraft_registration)] for aircraft in aircrafts) == 1)

        print("Creating constraints for aircrafts...")
        for aircraft in aircrafts:
            for flight in flights:
                if flight.aircraft_type != aircraft.aircraft_type or flight.physical_seating_capacity > aircraft.seating_capacity:
                    solver.Add(x[(flight.flight_identifier, aircraft.aircraft_registration)] == 0)

        print("Creating constraints for preassignments...")
        for preassignment in preassignments:
            for flight in flights:
                if flight.scheduled_time_of_departure < preassignment.end_time and flight.scheduled_time_of_arrival > preassignment.start_time:
                    solver.Add(x[(flight.flight_identifier, preassignment.aircraft.aircraft_registration)] == 0)

        print("Setting the objective function...")
        # Objective function
        solver.Minimize(solver.Sum(x[(flight.flight_identifier, aircraft.aircraft_registration)] for flight in flights for aircraft in aircrafts))

        print("Solving the problem...")
        # Solve the problem
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            print("Optimal solution found.")
            assignments = {}
            for aircraft in aircrafts:
                assignments[aircraft.aircraft_registration] = []
                for flight in flights:
                    if x[(flight.flight_identifier, aircraft.aircraft_registration)].solution_value() == 1:
                        assignments[aircraft.aircraft_registration].append({
                            'type': 'flight',
                            'flight_identifier': flight.flight_identifier,
                            'start_time': flight.scheduled_time_of_departure,
                            'end_time': flight.scheduled_time_of_arrival,
                            'departure_station': flight.departure_station,
                            'arrival_station': flight.arrival_station
                        })
                for preassignment in preassignments:
                    if preassignment.aircraft == aircraft:
                        assignments[aircraft.aircraft_registration].append({
                            'type': 'preassignment',
                            'description': preassignment.description,
                            'start_time': preassignment.start_time,
                            'end_time': preassignment.end_time
                        })
                assignments[aircraft.aircraft_registration].sort(key=lambda x: x['start_time'])
            return assignments
        else:
            print("No optimal solution found.")
            logging.warning("Solver status: %s", status)
            logging.warning("Number of variables: %d", solver.NumVariables())
            logging.warning("Number of constraints: %d", solver.NumConstraints())
            return None
    except Exception as e:
        logging.error("An error occurred in solve_tail_assignment: %s", e)
        return None