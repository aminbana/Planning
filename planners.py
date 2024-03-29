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

def planner_ff_modified_enforced(s0:State, all_actions, goal:Goal):
    return planner_ff(s0, all_actions, goal, version='modified_enforced')

def planner_ff_probabilistic_modified_enforced(s0:State, all_actions, goal:Goal):
    return planner_ff(s0, all_actions, goal, version='probabilistic_modified_enforced')

def planner_ff_enforced(s0:State, all_actions, goal:Goal):
    return planner_ff(s0, all_actions, goal, version='enforced')

def planner_ff_naive_greedy(s0:State, all_actions, goal:Goal):
    return planner_ff(s0, all_actions, goal, version='naive_greedy')

def planner_ff_naive_bestchild(s0:State, all_actions, goal:Goal):
    return planner_ff(s0, all_actions, goal, version='naive_bestchild')


def planner_ff(s0:State, all_actions, goal:Goal, version='modified_enforced', print_h=False):
    
    types = ['naive_greedy', 'naive_bestchild', 'enforced', 'modified_enforced', 'probabilistic_modified_enforced']
    assert(version in types)
    
    if version == 'naive_greedy':
        return ff_search(s0, all_actions, goal, enforced=False, print_h=print_h, naive_greedy=True)
    elif version == 'naive_bestchild':
        return ff_search(s0, all_actions, goal, enforced=False, print_h=print_h, naive_greedy=False)
    elif version == 'enforced':
        return ff_search(s0, all_actions, goal, enforced=True, print_h=print_h, original_version=True)
    elif version == 'modified_enforced':
        return ff_search(s0, all_actions, goal, enforced=True, print_h=print_h, original_version=False)
    elif version == 'probabilistic_modified_enforced':
        return ff_search(s0, all_actions, goal, enforced=True, print_h=print_h, original_version=False, prob=0.4)
    
    
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


def ff_search(s0:State, all_actions, goal:Goal, plan=Plan(), enforced=True, print_h=False, naive_greedy=True,
              original_version=True, history_of_states=[], plateau_max_level=100, prob=None):

    
    if s0.isGoal(goal):
        return plan, True
    
    possible_actions = s0.get_all_possible_actions(all_actions)
    success, helpful_actions, heuristic = graphplan(s0, all_actions, goal)
    
    hist = deepcopy(history_of_states)
    hist.append(s0)
    
    if print_h:
        print('heuristic value:', heuristic)
        
    if not success:
        return None, False
    
    if enforced:
    
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
                    #possible_actions = new_s.get_all_possible_actions(all_actions)
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
                    
                    if original_version:
                        if new_h < heuristic:
                            better_h_exists = True
                            break
                    elif prob == None:
                        if new_h < heuristic or (new_h == heuristic and new_s not in hist):
                            better_h_exists = True
                            break
                    else:
                        if new_h < heuristic or (new_h == heuristic and new_s not in hist and np.random.rand() < prob):
                            better_h_exists = True
                            break
            prev_level_states = deepcopy(cur_level_states)
            prev_level_helpful_actions = deepcopy(cur_level_helpful_actions)
            
            all_level_actions.append(cur_level_actions)
            all_level_actions_father.append(cur_level_actions_father)
            
                        
            if all_actions_failed or len(all_level_actions) > plateau_max_level:
                print('\n:X  *** Failure! ***\n')
                return None, False
            
            
        if better_h_exists: 
            cur_plan = extract_plan(all_level_actions, all_level_actions_father, plan)
            plan, success = ff_search(new_s, all_actions, goal, cur_plan, enforced=enforced, plateau_max_level=plateau_max_level,
                                      print_h=print_h, original_version=original_version, prob=prob)
            
    else: # simple hill climbing without enforce 

        random.shuffle(helpful_actions)
        random.shuffle(possible_actions)
        
        
        cur_level_states = []
        cur_level_hvalues = []
        cur_level_actions = []
        
        
        all_actions_failed = True
        
            
        for act in helpful_actions:
            
            new_s = s0.apply_unified_action(act)
            new_success, _, new_h = graphplan(new_s, all_actions, goal)

            if naive_greedy:
                if not new_success:
                    continue
                
                if new_h < heuristic:
                    
                    cur_level_states.append(new_s)
                    cur_level_hvalues.append(new_h)
                    cur_level_actions.append(act)
                    all_actions_failed = False
                    break
                    
            else:
                
                if new_s in hist:
                    continue
                    
                if new_success:
                    all_actions_failed = False
                else:
                    continue

                cur_level_states.append(new_s)
                cur_level_hvalues.append(new_h)
                cur_level_actions.append(act)
                
            
        if all_actions_failed and not naive_greedy:
            for act in possible_actions:
                new_s = s0.apply_unified_action(act)
                new_success, _, new_h = graphplan(new_s, all_actions, goal)
        
                if new_s in hist:
                    continue
                    
                if new_success:
                    all_actions_failed = False
                else:
                    continue
        
                    
                cur_level_states.append(new_s)
                cur_level_hvalues.append(new_h)
                cur_level_actions.append(act)
                        
        if all_actions_failed:
            print('\n:X  *** Failure! ***\n')
            return None, False
            
        if naive_greedy:
            act_ind = -1
        else:
            act_ind = np.argmin(cur_level_hvalues)
            
        plan.append_after(cur_level_actions[act_ind])
        new_s = cur_level_states[act_ind]
        plan, success = ff_search(new_s, all_actions, goal, plan, enforced=enforced, naive_greedy=naive_greedy,
                                  print_h=print_h, history_of_states=hist)        

    return plan, success




def forward_search (all_actions, s:State, goal:Goal, history_of_states, depth = 0, max_length = 20):

    if s.isGoal(goal):
        plan = Plan()
        return plan, True
    
    if depth >= max_length:
        return [], False
    
    hist = deepcopy (history_of_states)
    hist.append(s)

    possible_actions = s.get_all_possible_actions(all_actions)
    random.shuffle(possible_actions)

    for a in possible_actions:
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

    possible_actions = goal.get_all_possible_backward_actions(all_actions, s0)
    random.shuffle(possible_actions)
    
    for a in possible_actions:
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



