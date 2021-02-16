

from state import State
from randomProblemGenerator import reversal_n_problem
from graphic import Graphic
from file_io import read_domain, read_problem
from planners import planner_backward, planner_forward, planner_ff_modified_enforced, planner_ff_enforced, planner_ff_probabilistic_modified_enforced, planner_ff_naive_greedy, planner_ff_naive_bestchild
import time
import multiprocessing

max_time_limit = 200

parent_path = 'blocks-world/'
domain_file_name = 'domain.txt'
domain_path = parent_path + domain_file_name

problem_file_names = ["simple.txt", "sussman-anomaly.txt", "reversal4.txt", "twelve-step.txt", "large-a.txt"]

planners = [planner_backward, planner_forward, planner_ff_probabilistic_modified_enforced,
            planner_ff_modified_enforced, planner_ff_enforced, planner_ff_naive_greedy,
            planner_ff_naive_bestchild]

planner_strings = ["backward", "forward", "ff_probabilistic_modified_enforced",
                   "ff_modified_enforced", "ff_enforced", "ff_naive_greedy",
                   "ff_naive_bestchild"]
reports = {}

def thread_function(planner, s0, all_actions, goal, queue):
    final_plan, success = planner(s0, all_actions, goal)
    queue[0] = final_plan
    queue[1] = success

if __name__ == '__main__':
    all_actions, predicates = read_domain(domain_path)
    for n in range(6,10):
        
        problem_file_name = f"reversal_{n}"

        
        s0, goal = reversal_n_problem(n)
                
        g = Graphic()
        g.plot_state(s0)
        g.plot_state(State(goal.propos_pos))
        reports[problem_file_name] = {}
        for planner, planner_string in zip (planners, planner_strings):
            reports[problem_file_name][planner_string] = {}
            for repeats in range (5):
                print (f"solving {problem_file_name} with {planner_string}")

                manager = multiprocessing.Manager()
                return_list = manager.list()
                return_list.append([])
                return_list.append(False)

                th = multiprocessing.Process(target=thread_function, args=(planner, s0, all_actions, goal, return_list, ))

                start_time = time.time()
                th.start()

                
                while True:
                    if not th.is_alive():
                        break
                    elif time.time() - start_time > max_time_limit:
                        th.terminate()
                    
                    time.sleep(0.1)
                            
                stop_time = time.time()
                print ("return_list" , return_list)
                final_plan, success = return_list

                elapsed_time = max_time_limit
                plan_len = 0
                if success:
                    plan_len = len(final_plan.actions)
                    elapsed_time = stop_time - start_time
                    g.plot_plan(s0, final_plan, plot_result = False, path_to_save="Results/" + parent_path, filename=problem_file_name.split('.txt')[0] + planner_string)
                
                reports[problem_file_name][planner_string][repeats] = (elapsed_time , plan_len, success)

        print (reports)
    import pickle
    pickle.dump(reports, file=open( "Reports/report_reversal", "wb" ))