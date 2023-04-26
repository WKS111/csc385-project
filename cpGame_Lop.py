# have to turn all coefficients, including in objective function, into integers -- multiplying by a scalar doesn't change solution space

from ortools.sat.python import cp_model # import libraries

model = cp_model.CpModel() # create the model
var_upper_bound = max(50, 45, 37) # maximum of three b-values
x = model.NewIntVar(0, var_upper_bound, 'x') # sets an integer variable x that ranges between values 0 and 50
y = model.NewIntVar(0, var_upper_bound, 'y') # not really sure about the upper bound though...what if a variable was being subtracted and was unbounded...
z = model.NewIntVar(0, var_upper_bound, 'z')

# add constraints
model.Add(2 * x + 7 * y + 3 * z <= 50) # adds constraint 2x + 7y + 3z <= 50; constraint has been multiplied by 2
model.Add(3 * x - 5 * y + 7 * z <= 45)
model.Add(5 * x + 2 * y - 6 * z <= 37)

# define objective function
model.Maximize(2 * x + 2 * y + 3 * z) # sets z = 2x + 2y + 3z as maximization function

# call the solver
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 10 # sets atime limit of 10 seconds
status = solver.Solve(model)

# display results
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f'Maximum of objective function: {solver.ObjectiveValue()}\n')
    print(f'x = {solver.Value(x)}')
    print(f'y = {solver.Value(y)}')
    print(f'z = {solver.Value(z)}')
else:
    print('No solution found.')

# Statistics.
print('\nStatistics')
print(f'  status   : {solver.StatusName(status)}')
print(f'  conflicts: {solver.NumConflicts()}')
print(f'  branches : {solver.NumBranches()}')
print(f'  wall time: {solver.WallTime()} s')


