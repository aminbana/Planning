
from file_io import read_domain, read_problem
from planners import planner_backward, planner_forward, planner_ff_modified_enforced, planner_ff_enforced, planner_ff_probabilistic_modified_enforced, planner_ff_naive_greedy, planner_ff_naive_bestchild
from planners import planner_ff_modified_enforced, planner_ff_enforced
from planners import planner_ff_naive_greedy, planner_ff_naive_bestchild
import time
import multiprocessing
from randomProblemGenerator import get_bunch_of_problems

max_time_limit = 200

parent_path = 'blocks-world/'
domain_file_name = 'domain.txt'
domain_path = parent_path + domain_file_name

all_actions, predicates = read_domain(domain_path)


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
    for max_length in range(15, 20, 10):
        print ("Solving problems with length" , max_length , "...")
        
        problems = get_bunch_of_problems(all_actions, count=2, max_length=max_length)

        reports[max_length] = {}
        
        for planner, planner_string in zip (planners, planner_strings):
            reports[max_length][planner_string] = {}
            print ("planner:", planner_string)
            for repeats in range (2):
                reports[max_length][planner_string][repeats] = []
                for problem in problems:
                    s0, goal = problem

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
                        elif time.time() - start_time > max_time_limit:
                            th.terminate()
                        time.sleep(0.1)
                            
                    stop_time = time.time()
                    print ("return_list" , return_list)
                    final_plan, success = return_list
                    print ()
                    elapsed_time = max_time_limit
                    plan_len = 0
                    if success:
                        plan_len = len(final_plan.actions)
                        if plan_len == 0:
                            print (s0, goal, final_plan)

                    elapsed_time = stop_time - start_time
                    reports[max_length][planner_string][repeats].append ((elapsed_time , plan_len, success))
                    

        print (reports)
    import pickle
    pickle.dump(reports, file=open( "Reports/report_random", "wb" ))

    