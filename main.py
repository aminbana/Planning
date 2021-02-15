from graphplan import graphplan
from graphlayer import Graphlayer
from graphic import Graphic
from file_io import read_domain, read_problem
from planners import planner_ff
from time import time
from myutils import print_results

standard_print = False

parent_path = 'blocks-world/'
domain_file_name = 'domain.txt'
domain_path = parent_path + domain_file_name

problem_file_name = 'twelve-step.txt'
problem_path = parent_path + problem_file_name

all_actions, predicates = read_domain(domain_path)
s0, goal = read_problem(problem_path, predicates)

if not standard_print:
    print ("Initial", s0)
    print (goal)
    print()

g = Graphic()

t0 = time()
final_plan, success = planner_ff(s0, all_actions, goal, 'probabilistic_modified_enforced', print_h=True)
t1 = time()

print_results(final_plan, success, time=(t1 - t0), standard_print=standard_print)

if not standard_print:
    g.plot_plan(s0, final_plan, path_to_save="Results/" + parent_path, filename=problem_file_name.split('.txt')[0])
        

