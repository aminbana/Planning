from action import Action
from graphlayer import Graphlayer
from goal import Goal
from copy import deepcopy
from myutils import get_actions_short_names, count_actions_but_noops
import itertools


def extract_plan (action_layers, state_layers, n, goal:Goal):
    if n==0:
        return [],0
        
    action_layer = action_layers[n]

    action_lists_for_each_goal = []

    for g in goal.propos_pos:
        action_list = []
        for a in action_layer:
            if g in a.eff_pos:
                action_list.append(a)
        
        action_lists_for_each_goal.append(action_list)    

    for g in goal.propos_neg:
        action_list = []
        for a in action_layer:
            if g in a.eff_neg:
                action_list.append(a)
        
        action_lists_for_each_goal.append(action_list)   

    preconditions_pos = set()
    preconditions_neg = set()
    
    best_length = 10000000000000
    best_plan = None

    for actions_at_this_layer in itertools.product(*action_lists_for_each_goal):
        actions_at_this_layer = set (actions_at_this_layer)
        for a in actions_at_this_layer:
            preconditions_pos = preconditions_pos | a.pre_pos
            preconditions_neg = preconditions_neg | a.pre_neg
        new_goal = Goal(preconditions_pos, preconditions_neg)
        plan, length = extract_plan (action_layers, state_layers, n-1, new_goal)

        plan = plan + [actions_at_this_layer]
        length = length + count_actions_but_noops (actions_at_this_layer)
        if length < best_length:
            best_length = length
            best_plan = plan
    
        return best_plan, best_length

            
    



def graphplan(s0, all_action, goal:Goal):
    action_layers = []
    state_layers = []
    
    relaxed_actions = [a.relax_action() for a in deepcopy(all_action)]
    goal = goal.relax_goal()

    for n in range(1000000):
        
        if n == 0:
            state_layers.append(Graphlayer(s0.propositions))
            action_layers.append([]) # adding None to correct indexing of action_layers
            continue
        
        gl = state_layers[n-1]

        all_posible_actions = gl.get_all_possible_actions(relaxed_actions) + gl.get_noops()
        action_layers.append(all_posible_actions)

        new_gl = gl.apply_unified_actions(all_posible_actions)
        state_layers.append(new_gl)
        
        if new_gl == gl or new_gl.hasGoal(goal): #graph leveld off
            break
    
    if new_gl.hasGoal(goal):

        # print("n:", n)
        # for l in range(n):
        #     print ("layer:" , l)
        #     print (get_actions_short_names (action_layers[l]))

        parallel_plan, best_length = extract_plan(action_layers, state_layers, n, goal)

        # print ("parallel_plan with length ", best_length ,":")
        # for i, layer in enumerate (parallel_plan):
        #     print ("layer:", i, "//", get_actions_short_names(layer))

        helpful_actions = [a for a in parallel_plan[0] if a.name != "noop"]
        heuristic = best_length

        unrelaxed_helpful_actions = []

        for h in helpful_actions:
            for a in all_action:
                if h.name == a.name:
                    mapping = {k:v for k,v in zip (a.variables, h.variables)}
                    break

            unrelaxed_helpful_actions.append(a.substitute_and_copy(mapping))

        return True , unrelaxed_helpful_actions, heuristic
    else:
        return False , None, None

            
    
if __name__=="__main__":
    from randomProblemGenerator import get_sample_problem_definition
    from proposition import Proposition as p
    from state import State
    all_actions, s0, goal = get_sample_problem_definition(None)
    goal = Goal([],[p("on", ["a","b"])])

    p_s0 = {p("cl","a"), p("ot" , "d"), p("on", ["a","b"]),p("on", ["b","c"]), p("on", ["c","d"])}
    s0 = State(p_s0)
    success , unrelaxed_helpful_actions, heuristic = graphplan(s0, all_actions, goal)

