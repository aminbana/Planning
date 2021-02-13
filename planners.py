from graphplan import graphplan
from goal import Goal
from state import State
from action import Action
from plan import Plan
from copy import deepcopy
from myutils import get_actions_short_names
import random


def planner_forward(s0:State, all_actions, goal:Goal):
    return forward_search (all_actions, s0, goal, [], max_length=30)

def planner_backward(s0:State, all_actions, goal:Goal):
    return backward_search (all_actions, s0, goal, [], max_length=30)


def planner_ff(s0:State, all_actions, goal:Goal):
    # ================================== write here hosein :) =================================
    # you may use this as heuristic:
    
        # success, helpful_actions, heuristic = graphplan(s0, all_actions, goal)
        # if success:
        #     print ("succses, h=", heuristic, get_actions_short_names(helpful_actions))
        # else:
        #     print ("failed")
        # print (success, helpful_actions, heuristic)


    plan, success = forward_search (all_actions, s0, goal, [], max_length=30)
    return plan, success
    #==========================================================================================

def forward_search (all_actions, s:State, goal:Goal, history_of_states, depth = 0, max_length = 20):

    if s.isGoal(goal):
        plan = Plan()
        return plan, True
    
    if depth >= max_length:
        return [], False
    
    hist = deepcopy (history_of_states)
    hist.append(s)

    posible_actions = s.get_all_possible_actions(all_actions)
    random.shuffle(posible_actions)

    for a in posible_actions:
        new_s = s.apply_unified_action(a)

        if new_s in hist:
            continue
            
        plan , success = forward_search(all_actions, new_s, goal, hist, depth+1)
        if success:
            plan.append_before(a)
            return plan,True
    return None,False


def backward_search (all_actions, s0:State, goal:Goal, history_of_states, depth = 0, max_length = 20):

    if s0.isGoal(goal):
        plan = Plan()
        return plan, True
        
    if depth >= max_length:
        return [], False

    hist = deepcopy (history_of_states)
    hist.append(goal)

    posible_actions = goal.get_all_possible_backward_actions(all_actions, s0)
    random.shuffle(posible_actions)
    
    for a in posible_actions:
        new_goal = goal.apply_inverse_unified_action(a)

        repeated_state = False
        for h_g in hist:
            if new_goal.propos_pos.issubset(h_g.propos_pos) and new_goal.propos_neg.issubset(h_g.propos_neg):
                repeated_state = True
                break
        if repeated_state:
            continue
            
        plan , success = forward_search(all_actions, s0, new_goal, hist, depth+1)
        if success:
            plan.append_after(a)
            return plan,True
    return None,False



