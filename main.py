from proposition import Proposition as p
from action import Action
from state import State
from goal import Goal
from plan import Plan
from copy import deepcopy
from myutils import get_actions_short_names
from graphplan import graphplan
from file_io import read_domain, read_problem

def get_problem_definition(filepath):
    p_s0 = {p("cl","e"), p("ot" , "b"), p("on", ["a","b"]), p("ot", "c"), p("cl", "c"), p("cl", "d"), p("ot", "d") , p("on", ["e","a"]), p("hol", "x")}
    s0 = State(p_s0)

    all_actions = []
    pre_neg = []

    
    pre_pos = {p("on" , ["ob1", "ob2"]) , p("cl","ob1"), p("he")}
    eff_pos = {p("cl","ob2"), p("hol","ob1"),}
    eff_neg = {p("on" , ["ob1", "ob2"]) , p("cl","ob1"), p("he")}
    a = Action("unstack", pre_pos, pre_neg, eff_pos, eff_neg, variables=['ob1', 'ob2'])
    all_actions.append(a)


    pre_pos = {p("hol" , ["ob1"]) , p("cl","ob2")}
    eff_pos = {p("cl","ob1"), p("on", ["ob1" , "ob2"]), p("he")}
    eff_neg =  {p("hol" , ["ob1"]) , p("cl","ob2")}
    a = Action("stack", pre_pos, pre_neg, eff_pos, eff_neg, variables=['ob1', 'ob2'])
    all_actions.append(a)


    pre_pos = {p("ot" , "ob1",) , p("cl","ob1"), p("he")}
    eff_pos = {p("hol","ob1"),}
    eff_neg = {p("ot" , "ob1",) , p("cl","ob1"), p("he")}
    a = Action("pickup", pre_pos, pre_neg, eff_pos, eff_neg)
    all_actions.append(a)


    pre_pos = {p("hol" , ["ob1"])}
    eff_pos = {p("ot" , "ob1",) , p("cl","ob1"), p("he")}
    eff_neg = {p("hol" , ["ob1"])}
    a = Action("putdown", pre_pos, pre_neg, eff_pos, eff_neg)
    all_actions.append(a)

    g_p = {p("cl","b"), p("on",["b","c"]), p("on",["c","a"]), p("ot","a")}
    g_n = {}
    goal = Goal(g_p,g_n)
    
    return all_actions, s0, goal

def main():
    
    all_actions, predicates = read_domain('blocks-world/domain.txt')
    s0, goal = read_problem('blocks-world/sussman-anomaly.txt', predicates)

    #all_actions, s0, goal = get_problem_definition("temp.txt")
    print (get_actions_short_names (all_actions))
    print (get_actions_short_names (s0.get_all_possible_actions(all_actions)))
    final_plan, success = forward_search(all_actions, s0, goal, [])
    from graphic import Graphic
    g = Graphic()

    if success:
        print(final_plan)
    else:
        print("failed")

    s = s0
    for action in final_plan.actions:
        print (action.get_short_name())
        g.plot_state(s)
        # success, helpful_actions, heuristic = graphplan(s, all_actions, goal)
        # print (heuristic)
        s = s.apply_unified_action(action)

    # success, helpful_actions, heuristic = graphplan(s0, all_actions, goal)
    # if success:
    #     print ("succses, h=", heuristic, get_actions_short_names(helpful_actions))
    # else:
    #     print ("failed")
    # print (success, helpful_actions, heuristic)



def forward_search (all_actions, s:State, goal:Goal, history_of_states, depth = 0):

    if s.isGoal(goal):
        plan = Plan()
        return plan, True
    
    hist = deepcopy (history_of_states)
    hist.append(s)

    posible_actions = s.get_all_possible_actions(all_actions)
    for a in posible_actions:
        new_s = s.apply_unified_action(a)

        if new_s in hist:
            continue
            
        plan , success = forward_search(all_actions, new_s, goal, hist, depth+1)
        if success:
            plan.append_before(a)
            return plan,True
    return None,False


main()

