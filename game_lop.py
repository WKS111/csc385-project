import csv
from ortools.linear_solver import pywraplp
from ast import literal_eval
#import parse_test as parse_vars

def main():
    T = 1000
    P = 10
    W = 20
    # opening the CSV file
    with open('BGG Top 100.csv', mode='r', encoding="utf8") as file:

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
        for i, cat in enumerate(csv_array[0]):
            indexDict[cat] = i

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
        category_index = indexDict['category']
        aweight_index = indexDict['aweight']

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
        
        weight_list = []
        for i in range(1, num_lines):
            weight_list.append(float(csv_array[i][aweight_index]))
        weight_list.insert(0, 0)

        constraint_expr = \
            [weight_list[j] * x[j] for j in range(num_lines)]
        solver.Add(sum(constraint_expr) <= W)
        
        constraint_expr = \
            [x[j] for j in range(num_lines)]
        solver.Add(sum(constraint_expr) <= P)
        
        #Category Constraints
        category_dict = {}
        for i in range(1, num_lines):
            for cat in literal_eval(csv_array[i][category_index]):
                if cat in category_dict:
                    category_dict[cat].append(i)
                else:
                    category_dict[cat] = [i]

        for cat1 in category_dict:
            for cat2 in category_dict:
                if cat1 != cat2:
                    constraint_expr1 = \
                        [x[j] for j in category_dict[cat1]]
                    constraint_expr2 = \
                        [x[k] for k in category_dict[cat2]]
                    solver.Add(sum(constraint_expr1) <= sum(constraint_expr2) + 1)
        
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
    
    # The following exports the model as a string in LP format
    model_as_string = solver.ExportModelAsLpFormat(False)

    # Save the string in a file
    lp_file = open( 'games' + '.lp', 'w', encoding = 'utf-8')
    lp_file.write( model_as_string )
    lp_file.close()



if __name__ == '__main__':
    main()
