from graphplan import graphplan
from goal import Goal
from state import State
from action import Action
from plan import Plan
from copy import deepcopy
from myutils import get_actions_short_names
import numpy as np
import random


def planner_forward(s0:State, all_actions, goal:Goal):
    return forward_search (all_actions, s0, goal, [], max_length=30)

def planner_backward(s0:State, all_actions, goal:Goal):
    return backward_search (all_actions, s0, goal, [], max_length=30)


def extract_plan(all_level_actions, all_level_actions_father, plan):
    n_levels = len(all_level_actions)
    
    plan_ind = len(all_level_actions[-1]) - 1
    
    partial_plan = Plan()
    for l in range(n_levels)[::-1]:
        partial_plan.append_before(all_level_actions[l][plan_ind])
        plan_ind = all_level_actions_father[l][plan_ind]
        
    for l in range(n_levels):
        plan.append_after(partial_plan.actions[l])
        
    return plan


def unify_helpful_actions(state, helpful_actions):
    # unified_actions = state.get_all_possible_actions(helpful_actions)
    return np.random.permutation(helpful_actions).tolist()


def planner_ff(s0:State, all_actions, goal:Goal, plan=Plan()):

    
    if s0.isGoal(goal):
        return plan, True
    
    posible_actions = s0.get_all_possible_actions(all_actions)
    success, helpful_actions, heuristic = graphplan(s0, all_actions, goal)
    
    if not success:
        return None, False
    
    
    prev_level_states = [deepcopy(s0)]
    prev_level_helpful_actions = [unify_helpful_actions(s0, helpful_actions)]
    
    
    all_level_actions = []
    all_level_actions_father = []

    

    better_h_exists = False
    
    while not better_h_exists:
        cur_level_states = []
        cur_level_actions = []
        cur_level_actions_father = {}
        
        cur_level_helpful_actions = []
        
        all_actions_failed = True
        
        j = 0
        for i, old_s in enumerate(prev_level_states):
            if better_h_exists:
                break
            
            for act in prev_level_helpful_actions[i]:
                if better_h_exists:
                    break
                
                new_s = old_s.apply_unified_action(act)
                new_success, new_helpful_actions, new_h = graphplan(new_s, all_actions, goal)

                
                if new_success:
                    all_actions_failed = False
                else:
                    continue
                
                cur_level_states.append(new_s)
                cur_level_actions.append(act)
                cur_level_actions_father[j] = i
                
                cur_level_helpful_actions.append(unify_helpful_actions(new_s, new_helpful_actions))
                
                j += 1
                
                if new_h < heuristic:
                    better_h_exists = True
                    break
        
        prev_level_states = deepcopy(cur_level_states)
        prev_level_helpful_actions = deepcopy(cur_level_helpful_actions)
        
        all_level_actions.append(cur_level_actions)
        all_level_actions_father.append(cur_level_actions_father)
        
                    
        if all_actions_failed:
            print(':X  *** Dead-End! ***')
            return None, False
        
        
    if better_h_exists: 
        cur_plan = extract_plan(all_level_actions, all_level_actions_father, plan)
        plan, success = planner_ff(new_s, all_actions, goal, cur_plan)

    return plan, success


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



