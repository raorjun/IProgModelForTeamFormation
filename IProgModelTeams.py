from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Define the number of developers and teams
num_developers = 15
num_teams = 5

# Productivity ratings of developers
productivity = [85, 75, 90, 70, 80, 65, 88, 72, 95, 68, 85, 78, 82, 70, 88]

# Developer attributes (1 if true, 0 otherwise)
frontend = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
backend = [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
full_stack = [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
senior = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
junior = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
international = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0]

# Calculate the average productivity
average_productivity = sum(productivity) / num_developers

# Decision variables
X = {}
for i in range(num_developers):
    for j in range(num_teams):
        X[i, j] = solver.IntVar(0, 1, f'X[{i},{j}]')

delta = solver.NumVar(0, solver.infinity(), 'delta')

# Objective: Minimize delta
solver.Minimize(delta)

# Constraint: Each developer is assigned to exactly one team
for i in range(num_developers):
    solver.Add(sum(X[i, j] for j in range(num_teams)) == 1)

# Constraint: No team has more than two frontend developers
for j in range(num_teams):
    solver.Add(sum(X[i, j] * frontend[i] for i in range(num_developers)) <= 2)

# Constraint: No team has more than two backend developers
for j in range(num_teams):
    solver.Add(sum(X[i, j] * backend[i] for i in range(num_developers)) <= 2)

# Constraint: Each team includes at least one full-stack developer
for j in range(num_teams):
    solver.Add(sum(X[i, j] * full_stack[i] for i in range(num_developers)) >= 1)

# Constraint: Each team includes at least one senior developer
for j in range(num_teams):
    solver.Add(sum(X[i, j] * senior[i] for i in range(num_developers)) >= 1)

# Constraint: Each team includes at least one junior developer
for j in range(num_teams):
    solver.Add(sum(X[i, j] * junior[i] for i in range(num_developers)) >= 1)

# Constraint: Each team includes at least one international developer
for j in range(num_teams):
    solver.Add(sum(X[i, j] * international[i] for i in range(num_developers)) >= 1)

# Constraints: The productivity of each team should not deviate from the average by more than delta
for j in range(num_teams):
    solver.Add(sum(X[i, j] * productivity[i] for i in range(num_developers)) <= average_productivity + delta)
    solver.Add(sum(X[i, j] * productivity[i] for i in range(num_developers)) >= average_productivity - delta)

# Solve the problem
status = solver.Solve()

# Output the solution
if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Minimum delta:', delta.solution_value())
    for j in range(num_teams):
        print(f'Team {j+1}:')
        for i in range(num_developers):
            if X[i, j].solution_value() > 0.5:
                print(f'  Developer {i+1}')
else:
    print('The problem does not have an optimal solution.')
