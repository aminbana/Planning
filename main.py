from graphplan import graphplan
from graphlayer import Graphlayer
from graphic import Graphic
from file_io import read_domain, read_problem
from planners import planner_ff

parent_path = 'blocks-world/'
domain_file_name = 'domain.txt'
domain_path = parent_path + domain_file_name

problem_file_name = 'twelve-step.txt'
problem_path = parent_path + problem_file_name

all_actions, predicates = read_domain(domain_path)
s0, goal = read_problem(problem_path, predicates)
print ("Initial", s0)
print (goal)

g = Graphic()

final_plan, success = planner_ff(s0, all_actions, goal, enforced=False)

if success:
    
    print(" ====================  final plan with FF search: ============================")
    print (final_plan)
    print(" =============================================================================")
    g.plot_plan(s0, final_plan, path_to_save="Results/" + parent_path, filename=problem_file_name.split('.txt')[0])

else:
    print(" ====================  final plan with FF search: ============================")
    print("failed to find any plan")
    print(" =============================================================================")


