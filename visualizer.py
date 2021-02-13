import pickle
reports = pickle.load(file=open( "Reports/report", "rb" ))
reports_random = pickle.load(file=open( "Reports/report_random", "rb" ))

planner_strings = ["ff", "backward", "forward"]

# import numpy as np
# import matplotlib.pyplot as plt
# for i, planner_string in enumerate (planner_strings): 
#     values = [reports[max_length][planner_string][0][0] for max_length in range(5, 100, 10)]
#     print (values)
#     plt.plot (values, label = planner_string)
# plt.legend()
# plt.show ()

import numpy as np
import matplotlib.pyplot as plt

# data to plot

problem_file_names = reports.keys()

n_groups = len (problem_file_names)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.2
opacity = 0.8

for i, planner_string in enumerate (planner_strings):
    values = []
    for problem_file_name in problem_file_names:
        if reports[problem_file_name][planner_string][2]:
            values.append(reports[problem_file_name][planner_string][0])
        else:
            values.append(0)

    plt.bar(index + bar_width * i, values, bar_width,alpha=opacity,label=planner_string)

plt.xlabel('Problem')
plt.ylabel('Running time')
plt.title('Runtime comparisan for different planners')

plt.xticks(index + bar_width - 0.05, [s.split (".txt")[0] for s in problem_file_names])
plt.legend()

plt.tight_layout()
plt.show()

for i, planner_string in enumerate (planner_strings):
    values = []
    for problem_file_name in problem_file_names:
        if reports[problem_file_name][planner_string][2]:
            values.append(reports[problem_file_name][planner_string][1])
        else:
            values.append(0)
            
    plt.bar(index + bar_width * i, values, bar_width,alpha=opacity,label=planner_string)

plt.xlabel('Problem')
plt.ylabel('plan length')
plt.title('Plan length comparisan for different planners')
plt.xticks(index + bar_width - 0.05, [s.split (".txt")[0] for s in problem_file_names])
plt.legend()

plt.tight_layout()
plt.show()


for i, planner_string in enumerate (planner_strings):
    time_values = []
    length_values = []
    total = 0
    unsolved = 0
    for max_length in reports_random.keys():
        for rep in reports_random[max_length][planner_string]:
            total += 1
            if rep[2]:
                time_values.append (reports_random[max_length][planner_string][0][0])
                length_values.append (reports_random[max_length][planner_string][0][1])
            else:
                unsolved += 1

            
    print ("planner" , planner_string, "with mean time:" , np.mean(time_values) , "with mean length:", np.mean(length_values), "num unsolved:", unsolved )