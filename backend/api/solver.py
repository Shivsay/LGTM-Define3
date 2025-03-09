from ortools.linear_solver import pywraplp
from .models import Aircraft, Flight, PreAssignment
import logging
import datetime

def solve_tail_assignment(
    aircraft_subtype=None,  # Filter by aircraft type/subtype
    start_date=None,        # Start of the assignment period
    end_date=None,          # End of the assignment period
    respect_preassignments=True,  # Whether to respect preassignments
    excluded_aircraft=None,  # List of aircraft registrations to exclude
    maintain_trips=True     # Whether to maintain trips on the same aircraft
):
    try:
        print("Creating the solver...")
        # Create the solver
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            logging.error("Failed to create solver")
            return None

        print("Fetching data from the database...")
        # Fetch data from the database with filters
        aircraft_query = Aircraft.objects.all()
        flight_query = Flight.objects.all()
        preassignment_query = PreAssignment.objects.all() if respect_preassignments else PreAssignment.objects.none()
        
        # Apply filters based on parameters
        if aircraft_subtype:
            aircraft_query = aircraft_query.filter(aircraft_type=aircraft_subtype)
        
        if excluded_aircraft:
            aircraft_query = aircraft_query.exclude(aircraft_registration__in=excluded_aircraft)
        
        if start_date:
            flight_query = flight_query.filter(flight_date__gte=start_date)
            if respect_preassignments:
                preassignment_query = preassignment_query.filter(end_time__gte=start_date)
        
        if end_date:
            flight_query = flight_query.filter(flight_date__lte=end_date)
            if respect_preassignments:
                preassignment_query = preassignment_query.filter(start_time__lte=end_date)
        
        aircrafts = list(aircraft_query)
        flights = list(flight_query)
        preassignments = list(preassignment_query)
        
        if not aircrafts:
            logging.warning("No aircraft available after filtering")
            # Return empty but valid assignment structure instead of None
            return {}
        if not flights:
            logging.warning("No flights available after filtering")
            # Return empty assignments for each aircraft
            return {aircraft.aircraft_registration: [] for aircraft in aircrafts}

        print("Creating variables...")
        # Create variables
        x = {}
        for flight in flights:
            for aircraft in aircrafts:
                x[(flight.flight_identifier, aircraft.aircraft_registration)] = solver.BoolVar(f'x_{flight.flight_identifier}_{aircraft.aircraft_registration}')

        # Create relaxation variables for each flight (allows for unassigned flights in worst case)
        relaxation_vars = {}
        for flight in flights:
            relaxation_vars[flight.flight_identifier] = solver.BoolVar(f'relax_{flight.flight_identifier}')
        
        print("Creating constraints for flights...")
        # Each flight must be assigned to exactly one aircraft OR relaxed
        flight_constraints = {}
        for flight in flights:
            constraint = solver.Add(
                sum(x[(flight.flight_identifier, aircraft.aircraft_registration)] for aircraft in aircrafts) + 
                relaxation_vars[flight.flight_identifier] == 1
            )
            flight_constraints[flight.flight_identifier] = constraint

        print("Creating constraints for aircrafts...")
        # Aircraft type and seating capacity constraints
        aircraft_constraints = []
        for aircraft in aircrafts:
            for flight in flights:
                if flight.aircraft_type != aircraft.aircraft_type or flight.physical_seating_capacity > aircraft.seating_capacity:
                    constraint = solver.Add(x[(flight.flight_identifier, aircraft.aircraft_registration)] == 0)
                    aircraft_constraints.append((flight.flight_identifier, aircraft.aircraft_registration, constraint))

        preassignment_constraints = []
        if respect_preassignments:
            print("Creating constraints for preassignments...")
            # Preassignments constraints
            for preassignment in preassignments:
                for flight in flights:
                    if flight.scheduled_time_of_departure < preassignment.end_time and flight.scheduled_time_of_arrival > preassignment.start_time:
                        constraint = solver.Add(x[(flight.flight_identifier, preassignment.aircraft.aircraft_registration)] == 0)
                        preassignment_constraints.append((flight.flight_identifier, preassignment.aircraft.aircraft_registration, constraint))

        print("Creating constraints to prevent overlapping flights for the same aircraft...")
        # Prevent overlapping flights for the same aircraft
        overlap_constraints = []
        for aircraft in aircrafts:
            for i in range(len(flights)):
                for j in range(i + 1, len(flights)):
                    flight_i = flights[i]
                    flight_j = flights[j]
                    if flight_i.scheduled_time_of_arrival + datetime.timedelta(minutes=flight_i.minimum_ground_time) > flight_j.scheduled_time_of_departure:
                        constraint = solver.Add(x[(flight_i.flight_identifier, aircraft.aircraft_registration)] + 
                                              x[(flight_j.flight_identifier, aircraft.aircraft_registration)] <= 1)
                        overlap_constraints.append((flight_i.flight_identifier, flight_j.flight_identifier, aircraft.aircraft_registration, constraint))

        trip_constraints = []
        if maintain_trips:
            print("Creating constraints to maintain trips on the same aircraft...")
            # Enforce onward flight assignments to the same aircraft if maintain_trips is True
            for flight in flights:
                if flight.onward_flight and flight.onward_flight in flights:
                    for aircraft in aircrafts:
                        # If a flight is assigned to an aircraft, its onward flight must be assigned to the same aircraft
                        constraint = solver.Add(x[(flight.flight_identifier, aircraft.aircraft_registration)] <=
                                  x[(flight.onward_flight.flight_identifier, aircraft.aircraft_registration)])
                        trip_constraints.append((flight.flight_identifier, flight.onward_flight.flight_identifier, aircraft.aircraft_registration, constraint))

        print("Setting the objective function...")
        # Objective function - prioritize minimizing relaxation variables (unassigned flights)
        # with a high penalty, then minimize total assignment costs
        high_penalty = 1000  # Large penalty for unassigned flights
        solver.Minimize(
            high_penalty * solver.Sum(relaxation_vars[flight.flight_identifier] for flight in flights) +
            solver.Sum(x[(flight.flight_identifier, aircraft.aircraft_registration)] for flight in flights for aircraft in aircrafts)
        )

        print("Solving the problem...")
        # Set a time limit for the solver
        solver.set_time_limit(300000)  # 300 seconds (5 minutes)

        # Solve the problem
        status = solver.Solve()

        # Always return assignments, even if not optimal
        assignments = {}
        for aircraft in aircrafts:
            assignments[aircraft.aircraft_registration] = []
            # Check if any flights are assigned to this aircraft
            for flight in flights:
                var = x.get((flight.flight_identifier, aircraft.aircraft_registration))
                if var and var.solution_value() > 0.5:  # Check if variable exists and is set to 1
                    assignments[aircraft.aircraft_registration].append({
                        'type': 'flight',
                        'flight_identifier': flight.flight_identifier,
                        'start_time': flight.scheduled_time_of_departure,
                        'end_time': flight.scheduled_time_of_arrival,
                        'departure_station': flight.departure_station,
                        'arrival_station': flight.arrival_station
                    })
            
            # Add preassignments to this aircraft
            if respect_preassignments:
                for preassignment in preassignments:
                    if preassignment.aircraft == aircraft:
                        assignments[aircraft.aircraft_registration].append({
                            'type': 'preassignment',
                            'description': preassignment.description,
                            'start_time': preassignment.start_time,
                            'end_time': preassignment.end_time
                        })
            
            # Sort by start time
            assignments[aircraft.aircraft_registration].sort(key=lambda x: x['start_time'])
        
        # Add unassigned flights to the output
        unassigned_flights = []
        if status != pywraplp.Solver.OPTIMAL:
            for flight in flights:
                if relaxation_vars[flight.flight_identifier].solution_value() > 0.5:
                    unassigned_flights.append({
                        'flight_identifier': flight.flight_identifier,
                        'aircraft_type': flight.aircraft_type,
                        'departure_station': flight.departure_station,
                        'arrival_station': flight.arrival_station,
                        'start_time': flight.scheduled_time_of_departure,
                        'end_time': flight.scheduled_time_of_arrival,
                    })
        
        # Add metadata about the solution
        solution_metadata = {
            'status': 'optimal' if status == pywraplp.Solver.OPTIMAL else 'feasible' if status == pywraplp.Solver.FEASIBLE else 'infeasible',
            'unassigned_flights': unassigned_flights,
            'objective_value': solver.Objective().Value() if status in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE] else None,
            'num_variables': solver.NumVariables(),
            'num_constraints': solver.NumConstraints()
        }

        if status == pywraplp.Solver.OPTIMAL:
            print("Optimal solution found.")
            logging.info("Found optimal solution with objective value: %s", solver.Objective().Value())
        elif status == pywraplp.Solver.FEASIBLE:
            print("Feasible but not optimal solution found.")
            logging.warning("Found feasible solution with objective value: %s", solver.Objective().Value())
        else:
            print("No optimal solution found. Returning best effort assignment.")
            logging.warning("Solver status: %s", status)
            logging.warning("Number of variables: %d", solver.NumVariables())
            logging.warning("Number of constraints: %d", solver.NumConstraints())
        
        # Return the assignments with metadata
        return {
            'assignments': assignments,
            'metadata': solution_metadata
        }
    except Exception as e:
        logging.error("An error occurred in solve_tail_assignment: %s", e)
        # Return empty dictionary with error information rather than None
        return {
            'assignments': {},
            'metadata': {
                'status': 'error',
                'error_message': str(e)
            }
        }
