import pickle
import numpy as np
import plot_utils
import os

inf = 200


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
min_time_mat = inf * np.ones((n_problems, n_planners))
min_length_mat = inf * np.ones((n_problems, n_planners), dtype=int)

mean_time_mat = np.zeros((n_problems, n_planners))
mean_length_mat = np.zeros((n_problems, n_planners))


for k in range(4):
    for i, k1 in enumerate(problem_file_names):
        for j, k2 in enumerate(planner_strings):
            if reports_all[k][k1][k2][-1]:
                n_solved_mat[i, j] += 1
                min_time_mat[i, j] = np.min([min_time_mat[i, j], round(reports_all[k][k1][k2][0], 2)])
                min_length_mat[i, j] = np.min([min_length_mat[i, j], reports_all[k][k1][k2][1]])
                
                mean_time_mat[i, j] += reports_all[k][k1][k2][0]
                mean_length_mat[i, j] += reports_all[k][k1][k2][1]
                
                
eps = 1e-7
mean_time_mat = mean_time_mat / (n_solved_mat + eps)
mean_length_mat = mean_length_mat / (n_solved_mat + eps)
      
mean_time_mat[mean_time_mat < eps] = inf
mean_length_mat[mean_length_mat < eps] = inf

#mean_length_mat = np.round(mean_length_mat).astype(int)

output_path = 'Reports/plots/'
if not os.path.exists(output_path):
    os.makedirs(output_path)
    
cols = planner_strings
rows = [row[:-4] for row in problem_file_names]

plot_utils.plot_heatmap(n_solved_mat, rows, cols, 'number of solved problems', output_path)

plot_utils.plot_heatmap(min_time_mat, rows, cols, 'minimum elapsed time', output_path)
plot_utils.plot_heatmap(min_length_mat, rows, cols, 'minimum plan length', output_path)

plot_utils.plot_heatmap(mean_time_mat, rows, cols, 'average elapsed time', output_path)
plot_utils.plot_heatmap(mean_length_mat, rows, cols, 'average plan length', output_path)
