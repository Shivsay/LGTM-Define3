from ortools.linear_solver import pywraplp

def solve_tail_assignment(flights, aircraft):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables: Assign each flight to exactly one aircraft
    x = {}
    for f in flights:
        for a in aircraft:
            x[f, a] = solver.BoolVar(f'flight_{f}_aircraft_{a}')

    # Constraint: Each flight must be assigned to one aircraft
    for f in flights:
        solver.Add(sum(x[f, a] for a in aircraft) == 1)

    # Constraint: An aircraft cannot be overloaded
    for a in aircraft:
        solver.Add(sum(x[f, a] * flights[f]["passengers"] for f in flights) <= aircraft[a]["capacity"])

    # Objective: Minimize total cost (or maximize efficiency)
    objective = solver.Objective()
    for f in flights:
        for a in aircraft:
            objective.SetCoefficient(x[f, a], flights[f]["cost"][a])
    objective.SetMinimization()

    # Solve the optimization problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        assignment = {f: a for f in flights for a in aircraft if x[f, a].solution_value() == 1}
        return assignment
    else:
        return None
