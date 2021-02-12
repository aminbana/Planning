from graphic import Graphic
from file_io import read_domain, read_problem
from planners import planner_ff

domain_path = 'blocks-world/domain.txt'
problem_path = 'blocks-world/sussman-anomaly.txt'

all_actions, predicates = read_domain(domain_path)
s0, goal = read_problem(problem_path, predicates)

g = Graphic()

final_plan, success = planner_ff(s0, all_actions, goal)

if success:
    
    print(" ====================  final plan with FF search: ============================")
    print (final_plan)
    print(" =============================================================================")
    g.plot_plan(s0, final_plan, path_to_save = "Results/" + problem_path.split(".txt")[-1] + ".png")

else:
    print(" ====================  final plan with FF search: ============================")
    print("failed to find any plan")
    print(" =============================================================================")
    

