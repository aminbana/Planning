from graphplan import graphplan
from graphlayer import Graphlayer
from graphic import Graphic
from file_io import read_domain, read_problem
from planners import planner_ff
from time import time
from myutils import print_results
import planners

standard_print = True

parent_path = 'problems 2/'
domain_file_name = 'domain - Gripper.txt'
problem_file_name = '2-gripper.txt'

domain_path = parent_path + domain_file_name
problem_path = parent_path + problem_file_name

all_actions, predicates = read_domain(domain_path)
s0, goal, objects = read_problem(problem_path, predicates)

from proposition import Proposition as p
from state import State

new_prop = s0.propositions
new_prop = new_prop.union({p ("object",obj) for obj in objects})
s0 = State(new_prop)

print (goal)
print (all_actions)

if not standard_print:
    print ("Initial", s0)
    print (goal)
    print()

g = Graphic()

ff_planners = ['naive_greedy', 'naive_bestchild', 'enforced', 'modified_enforced', 'probabilistic_modified_enforced']


t0 = time()
final_plan, success = planner_ff(s0, all_actions, goal, 'modified_enforced', print_h=True)
#final_plan, success = planners.planner_backward(s0, all_actions, goal)
t1 = time()


print_results(final_plan, success, time=(t1 - t0), standard_print=standard_print)

if success and not standard_print:
    g.plot_plan(s0, final_plan, path_to_save="Results/" + parent_path, filename=problem_file_name.split('.txt')[0])
        

