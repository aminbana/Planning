from graphplan import graphplan
from graphlayer import Graphlayer
from graphic import Graphic
from file_io import read_domain, read_problem
from planners import planner_ff
from time import time
from myutils import print_results

standard_print = True

parent_path = 'blocks-world/'
domain_file_name = 'domain.txt'
problem_file_name = 'reversal4.txt'

domain_path = parent_path + domain_file_name
problem_path = parent_path + problem_file_name

all_actions, predicates = read_domain(domain_path)
s0, goal = read_problem(problem_path, predicates)

if not standard_print:
    print ("Initial", s0)
    print (goal)
    print()

g = Graphic()

ff_planners = ['naive_greedy', 'naive_bestchild', 'enforced', 'modified_enforced', 'probabilistic_modified_enforced']


t0 = time()
final_plan, success = planner_ff(s0, all_actions, goal, 'enforced', print_h=False)
t1 = time()

print_results(final_plan, success, time=(t1 - t0), standard_print=standard_print)

if success and not standard_print:
    g.plot_plan(s0, final_plan, path_to_save="Results/" + parent_path, filename=problem_file_name.split('.txt')[0])
        

