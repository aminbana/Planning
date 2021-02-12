from graphic import Graphic
from file_io import read_domain, read_problem
from planners import planner_ff, planner_backward, planner_forward
import time

parent_path = 'blocks-world/'
domain_file_name = 'domain.txt'
domain_path = parent_path + domain_file_name

problem_file_names = ["reversal4.txt", "simple.txt", "sussman-anomaly.txt", "twelve-step.txt"]#, "large-a.txt"]

planners = [planner_ff, planner_backward, planner_forward]
planner_strings = ["ff", "backward", "forward"]

reports = {}

for problem_file_name in problem_file_names:
    print ("Solving problem" , problem_file_name , "...")
    problem_path = parent_path + problem_file_name

    all_actions, predicates = read_domain(domain_path)
    s0, goal = read_problem(problem_path, predicates)

    g = Graphic()
    reports[problem_file_name] = {}
    for planner, planner_string in zip (planners, planner_strings):
        start_time = time.time()
        final_plan, success = planner(s0, all_actions, goal)
        stop_time = time.time()
        
        elapsed_time = -1
        plan_len = -1
        if success:
            plan_len = len(final_plan.actions)
            elapsed_time = stop_time - start_time
            g.plot_plan(s0, final_plan, plot_result = False, path_to_save="Results/" + parent_path, filename=problem_file_name.split('.txt')[0] + planner_string)
        
        reports[problem_file_name][planner_string] = (elapsed_time , plan_len)

        print (reports)



            

