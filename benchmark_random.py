
from file_io import read_domain, read_problem
from planners import planner_ff, planner_backward, planner_forward
import time
import multiprocessing
from randomProblemGenerator import get_bunch_of_problems

parent_path = 'blocks-world/'
domain_file_name = 'domain.txt'
domain_path = parent_path + domain_file_name

base_problem_file_names = "reversal4.txt"
problem_path = parent_path + base_problem_file_names

all_actions, predicates = read_domain(domain_path)
base_s0, _ = read_problem(problem_path, predicates)

planners = [planner_ff, planner_backward, planner_forward]
planner_strings = ["ff", "backward", "forward"]

reports = {}

def thread_function(planner, s0, all_actions, goal, queue):
    final_plan, success = planner(s0, all_actions, goal)
    queue[0] = final_plan
    queue[1] = success

if __name__ == '__main__':
    for max_length in range(5, 100, 10):
        print ("Solving problems with length" , max_length , "...")
        
        problems = get_bunch_of_problems(all_actions, base_s0, count=5, max_length=max_length)

        reports[max_length] = {}
        
        for planner, planner_string in zip (planners, planner_strings):
            reports[max_length][planner_string] = []
            
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
                reports[max_length][planner_string].append ((elapsed_time , plan_len, success))
                

        print (reports)
    import pickle
    pickle.dump(reports, file=open( "Reports/report_random", "wb" ))

    