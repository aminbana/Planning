import pickle
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import repeat

reports = pickle.load(file=open( "Reports/report_reversal", "rb" ))
planner_strings = list (reports[list (reports.keys())[0]].keys())

problem_file_names = reports.keys()

for i, planner_string in enumerate (planner_strings):
    if planner_string == "ff_naive_greedy":
        continue
    
    values = []
    names = []
    for problem_file_name in problem_file_names:
        times = list (reports[problem_file_name][planner_string].values())
        times = [t[0] for t in times]
        mean = sum (times) / len (times)
            
        values.append(mean)
        names.append(problem_file_name)
    plt.plot (names, values, label = planner_string)
plt.legend()
plt.xlabel("problem name")
plt.ylabel("elapsed time (s)")
plt.title("runtime comparison on reversal problem")
plt.ylim([0,100])
plt.show()
    


reports = pickle.load(file=open( "Reports/report_random", "rb" ))
planner_strings = list (reports[list (reports.keys())[0]].keys())

print (reports)

problem_file_names = reports.keys()

n_groups = len (problem_file_names)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.12
opacity = 0.8

for i, planner_string in enumerate (planner_strings):
    values = []
    plot_values = []
    if planner_string == "backward":
        continue
    for problem_file_name in problem_file_names:
        for r in reports[problem_file_name][planner_string].keys():
            for q in reports[problem_file_name][planner_string][r]:
                values.append(q[0])
        time = min (values) #/ len(values)
        plot_values.append(time)
        print ("aaaa" , plot_values)
    plt.bar(index + bar_width * i, plot_values, bar_width,alpha=opacity,label=planner_string)

plt.xlabel('Problem')
plt.ylabel('Running time')
plt.title('Runtime comparisan for different planners')

# plt.xticks(index + bar_width - 0.05, [s.split (".txt")[0] for s in problem_file_names])
plt.legend()

plt.tight_layout()
plt.show()

# for i, planner_string in enumerate (planner_strings):
#     values = []
#     for problem_file_name in problem_file_names:
#         if reports[problem_file_name][planner_string][2]:
#             values.append(reports[problem_file_name][planner_string][1])
#         else:
#             values.append(0)
            
#     plt.bar(index + bar_width * i, values, bar_width,alpha=opacity,label=planner_string)

# plt.xlabel('Problem')
# plt.ylabel('plan length')
# plt.title('Plan length comparisan for different planners')
# plt.xticks(index + bar_width - 0.05, [s.split (".txt")[0] for s in problem_file_names])
# plt.legend()

# plt.tight_layout()
# plt.show()


reports_random = pickle.load(file=open( "Reports/report_random", "rb" ))
planner_strings = list (reports_random[list (reports_random.keys())[0]].keys())
print ("planner strings:", planner_strings, reports_random[25][planner_strings[0]])
for i, planner_string in enumerate (planner_strings):
    time_values = []
    length_values = []
    total = 0
    unsolved = 0
    for max_length in reports_random.keys():
        for rep in reports_random[max_length][planner_string][1]:
            total += 1
            if rep[2]:
                time_values.append (rep[0])
                length_values.append (rep[1])
            else:
                unsolved += 1

            
    print ("planner" , planner_string, "with mean time:" , np.mean(time_values) , "with mean length:", np.mean(length_values), "num unsolved:", unsolved )