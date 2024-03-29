from state import State
from action import Action
from proposition import Proposition as p
from goal import Goal
import numpy as np
import random


def reversal_n_problem (n):
    assert n >= 2
    propositions = []
    propositions_goal = []

    objects = ["a"+str(i) for i in range (n)]


    propositions.append(p("arm-empty"))
    propositions.append(p("on-table",[objects[0]]))
    
    propositions_goal.append(p("arm-empty"))
    propositions_goal.append(p("on-table",[objects[-1]]))
    
    for i in range (n-1):
        propositions.append(p("on", [objects[i+1],objects[i]]))
    for i in range (1,n):
        propositions_goal.append(p("on", [objects[-i-1],objects[-i]]))
    
    
    propositions.append(p("clear", objects[-1]))
    propositions_goal.append(p("clear", objects[0]))

    s0 = State(propositions)
    goal = Goal(propositions_goal, {})

    return s0, goal


def get_sample_problem_definition(filepath):
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

def generate_random_problem (s:State, all_actions, seed = 15, max_length = 20):
    random.seed(seed)
    np.random.seed(seed)

    plan_length = max_length #np.random.randint(low = 1, high = max_length)
    hist = []
    
    for i in range (plan_length):
        all_possible_actions = s.get_all_possible_actions(all_actions)
        new_action = np.random.choice(all_possible_actions,size=1)[0]
        hist.append(s)
        s = s.apply_unified_action(new_action)
    

    pos_count = np.random.randint(1,high=len(list (s.propositions)))
    
    pros_pos = set (random.choices(list (s.propositions), k=pos_count))
    
    all_negative_propositions = set ([propos for st in hist for propos in st.propositions if propos not in s.propositions])
    neg_count = np.random.randint(0,high=len(list (all_negative_propositions)))

    # pros_neg = set (random.choices(list (all_negative_propositions), k=neg_count))

    # goal = Goal(pros_pos,pros_neg)
    
    goal = Goal(hist[-1].propositions, {})
    
    s0 = hist[0] #random.choices(hist , k = 1)[0]
    
    return s0, goal

def generate_flat_n_cubes(n = 5):
    assert n >= 2
    propositions = []
    
    objects = ["a"+str(i) for i in range (n)]

    propositions.append(p("arm-empty"))
    
    for i in range (n):
        propositions.append(p("clear", objects[i]))    
        propositions.append(p("on-table",[objects[i]]))
        
    
    
    s0 = State(propositions)
    
    return s0


def get_bunch_of_problems(all_actions,  count, init_seed = 2, max_length = 20):
    problems = []
    s0 = generate_flat_n_cubes()
    from copy import deepcopy
    
    for c in range (count):
        s0, goal = generate_random_problem(deepcopy (s0), all_actions, seed=init_seed + c, max_length = max_length)
        if s0.isGoal(goal):
            c -= 1
            continue
        problems.append((s0,goal))
        
    return problems
