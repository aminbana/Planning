

from graphic import Graphic
from file_io import read_domain, read_problem
from planners import planner_ff, planner_backward, planner_forward
import time
import multiprocessing


parent_path = 'blocks-world/'
domain_file_name = 'domain.txt'
domain_path = parent_path + domain_file_name

problem_file_names = ["simple.txt", "sussman-anomaly.txt", "reversal4.txt", "twelve-step.txt", "large-a.txt"]

planners = [planner_ff, planner_backward, planner_forward]
planner_strings = ["ff", "backward", "forward"]

reports = {}

def thread_function(planner, s0, all_actions, goal, queue):
    final_plan, success = planner(s0, all_actions, goal)
    queue[0] = final_plan
    queue[1] = success

if __name__ == '__main__':
    for problem_file_name in problem_file_names:
        print ("Solving problem" , problem_file_name , "...")
        problem_path = parent_path + problem_file_name

        all_actions, predicates = read_domain(domain_path)
        s0, goal = read_problem(problem_path, predicates)

        g = Graphic()
        reports[problem_file_name] = {}
        for planner, planner_string in zip (planners, planner_strings):

            manager = multiprocessing.Manager()
            return_list = manager.list()
            return_list.append([])
            return_list.append(False)

            th = multiprocessing.Process(target=thread_function, args=(planner, s0, all_actions, goal, return_list))

            start_time = time.time()
            th.start()

            
            while True:
                if not th.is_alive():
                    break
                elif time.time() - start_time > 60:
                    th.terminate()
                
                time.sleep(0.1)
                        
            stop_time = time.time()

            final_plan, success = return_list

            elapsed_time = 60
            plan_len = 0
            if success:
                plan_len = len(final_plan.actions)
                elapsed_time = stop_time - start_time
                g.plot_plan(s0, final_plan, plot_result = False, path_to_save="Results/" + parent_path, filename=problem_file_name.split('.txt')[0] + planner_string)
            
            reports[problem_file_name][planner_string] = (elapsed_time , plan_len, success)

            print (reports)
    import pickle
    pickle.dump(reports, file=open( "Reports/report", "wb" ))


    import numpy as np
    import matplotlib.pyplot as plt

    # data to plot
    n_groups = len (problem_file_names)

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.3
    opacity = 0.8

    for i, (planner, planner_string) in enumerate (zip (planners, planner_strings)):
        values = [reports[problem_file_name][planner_string][0] for problem_file_name in problem_file_names]    
        plt.bar(index + bar_width * i, values, bar_width,alpha=opacity,label=planner_string)

    plt.xlabel('Problem')
    plt.ylabel('Running time')
    plt.title('Runtime comparisan for different planners')
    plt.xticks(index + bar_width - 0.05, problem_file_names)
    plt.legend()

    plt.tight_layout()
    plt.show()

