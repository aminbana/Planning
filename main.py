from graphplan import graphplan
from graphlayer import Graphlayer
from graphic import Graphic
from file_io import read_domain, read_problem
from planners import planner_ff

parent_path = 'blocks-world/'
domain_file_name = 'domain.txt'
domain_path = parent_path + domain_file_name

problem_file_name = 'large-a.txt'
problem_path = parent_path + problem_file_name

all_actions, predicates = read_domain(domain_path)
s0, goal = read_problem(problem_path, predicates)
print ("Initial", s0)
print (goal)
print()

g = Graphic()

final_plan, success = planner_ff(s0, all_actions, goal, 'modified_enforced')

if success:
    print()
    print(" ====================  final plan with FF search: ============================")
    for i, a in enumerate(final_plan.actions):
        print(str(i) + ':', a.get_short_name())
    print(" =============================================================================")
    g.plot_plan(s0, final_plan, path_to_save="Results/" + parent_path, filename=problem_file_name.split('.txt')[0])

else:
    print()
    print(" ====================  final plan with FF search: ============================")
    print("failed to find any plan")
    print(" =============================================================================")


