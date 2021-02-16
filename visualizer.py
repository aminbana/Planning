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
plt.ylim([0,60])
plt.show()
    


reports = pickle.load(file=open( "Reports/report_random", "rb" ))
del reports[15]["ff_naive_greedy"]
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

    for problem_file_name in problem_file_names:
        for r in reports[problem_file_name][planner_string].keys():
            for q in reports[problem_file_name][planner_string][r]:
                values.append(q[0])
        time = sum (values) / len(values)
        plot_values.append(time)
    plt.bar(index + bar_width * i, plot_values, bar_width,alpha=opacity,label=planner_string)

plt.xlabel('Problem')
plt.ylabel('Running time')
plt.title('Runtime comparisan for different planners')

plt.xticks(index + bar_width - 0.05, [""])
plt.legend()

plt.tight_layout()
plt.show()

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

    for problem_file_name in problem_file_names:
        for r in reports[problem_file_name][planner_string].keys():
            for q in reports[problem_file_name][planner_string][r]:
                if q[2]:
                    values.append(q[1])
    if len (values) > 0:
        
        print ("------" , values)
        time = sum (values) / len(values)
        plot_values.append(time)
        # print ("aaaa" , plot_values)
        plt.bar(index + bar_width * i, plot_values, bar_width,alpha=opacity,label=planner_string)
    

plt.xlabel('Problem')
plt.ylabel('Plan Length')
plt.title('Plan length comparisan for different planners')

plt.xticks(index + bar_width - 0.05, [""])
plt.legend()

plt.tight_layout()
plt.show()
