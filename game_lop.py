import csv
from ortools.linear_solver import pywraplp
#import parse_test as parse_vars

def main():
    T = 1000
    P = 10
    # opening the CSV file
    with open('bgg.csv', mode='r', encoding="utf8") as file:

        # reading the CSV file
        csvFile = csv.reader(file)
        # displaying the contents of the CSV file

        csv_array = []

        for i, lines in enumerate(csvFile):
            newList = []
            for line in lines:
                newList.append(line)
            csv_array.append(newList)

        num_lines = len(csv_array)

        indexDict = {}
        for i, category in enumerate(csv_array[0]):
            indexDict[category] = i

        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            return

        infinity = solver.infinity()
        x = {}
        x[0] = solver.IntVar(0, infinity, 'number of players')
        for j in range(1, num_lines):
            x[j] = solver.IntVar(0, 1, '{}'.format(
                csv_array[j][indexDict['objectname']]))
        print('number of variables =', solver.NumVariables())

        baverage_index = indexDict['baverage']
        min_players_index = indexDict['minplayers']
        max_players_index = indexDict['maxplayers']
        playing_time_index = indexDict['playingtime']

        for i in range(1, num_lines):
            solver.Add(x[0] - float(csv_array[i]
                       [min_players_index]) * x[i] >= 0)
            solver.Add(x[0] <= float(
                csv_array[i][max_players_index]) + P - P * x[i])

        time_list = []
        for i in range(1, num_lines):
            time_list.append(float(csv_array[i][playing_time_index]))
        time_list.insert(0, 0)

        constraint_expr = \
            [time_list[j] * x[j] for j in range(num_lines)]
        solver.Add(sum(constraint_expr) <= T)
        
        constraint_expr = \
            [x[j] for j in range(num_lines)]
        solver.Add(sum(constraint_expr) <= P)

        objective_list = []
        for i in range(1, num_lines):
            objective_list.append(float(csv_array[i][baverage_index]))
        objective_list.insert(0, 0)

        objective = solver.Objective()
        objective.SetCoefficient(x[0], 0)
        for j in range(num_lines):
            objective.SetCoefficient(x[j], objective_list[j])
        objective.SetMaximization()

        status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('time constraint =', T)
        print('game constraint =', P)
        print('objective value =', solver.Objective().Value())
        print('# of players:',x[0].solution_value())
        print('games played:')
        time_sum = 0
        game_sum = 0
        for j in range(1, num_lines):
            if x[j].solution_value() == 1:
                time_sum += float(csv_array[j][playing_time_index])
                game_sum += 1
                print(x[j].name())
        print('total # of games played:', game_sum)
        print('total time played:', time_sum)
        print('problem solved in %f milliseconds' % solver.wall_time())
        print('problem solved in %d iterations' % solver.iterations())
        print('problem solved in %d branch-and-bound nodes' % solver.nodes())
    else:
        print('the problem does not have an optimal solution.')


if __name__ == '__main__':
    main()
