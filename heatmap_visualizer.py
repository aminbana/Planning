import pickle
import numpy as np
import plot_utils
import os

    


reports_all = []

for i in range(4):
    reports_all.append(pickle.load(file=open( "Reports/report" + str(i + 1), "rb" )))


#planner_strings = list (reports_all[0][list (reports_all[0].keys())[0]].keys())
#black_list = ['ff_naive_greedy']
#for b in black_list:
#    planner_strings.remove(b)
    
planner_strings = ["backward", "forward", "ff_naive_bestchild",
                   "ff_enforced", "ff_modified_enforced", "ff_probabilistic_modified_enforced"]

problem_file_names = reports_all[0].keys()


n_problems = len(problem_file_names)
n_planners = len(planner_strings)

n_solved_mat = np.zeros((n_problems, n_planners), dtype=int)
time_mat = 200 * np.ones((n_problems, n_planners))
length_mat = 200 * np.ones((n_problems, n_planners), dtype=int)


for k in range(4):
    for i, k1 in enumerate(problem_file_names):
        for j, k2 in enumerate(planner_strings):
            if reports_all[k][k1][k2][-1]:
                n_solved_mat[i, j] += 1
                time_mat[i, j] = np.min([time_mat[i, j], round(reports_all[k][k1][k2][0], 2)])
                length_mat[i, j] = np.min([length_mat[i, j], reports_all[k][k1][k2][1]])
                
                
output_path = 'Reports/plots/'
if not os.path.exists(output_path):
    os.makedirs(output_path)
    
plot_utils.plot_heatmap(n_solved_mat, problem_file_names, planner_strings, 'number of solved problems', output_path)
plot_utils.plot_heatmap(time_mat, problem_file_names, planner_strings, 'minimum elapsed time', output_path)
plot_utils.plot_heatmap(length_mat, problem_file_names, planner_strings, 'minimum plan length', output_path)
