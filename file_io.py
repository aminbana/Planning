from proposition import Proposition
from action import Action
from state import State
from goal import Goal
import re



def get_name_number(string):
    colon_ind = string.find(':')
    end_ind = string.find('\n')
    name = string[: colon_ind]
    number = int(string[colon_ind + 1: end_ind])
    
    return name, number


def get_predicates(lines):
    
    predicates = {}
    for line in lines:
        
        if 'PREDICATES' in line:
            continue
        
        if line == '\n':
            break
        
        name, number = get_name_number(line)
        predicates[name.lower()] = number
        
    return predicates


def get_predicates_from_strings(lines, predicates):
    
    l = 0
    
    output = []
    
    while l < len(lines):
        
        line = lines[l].rstrip().lower()

        if line in predicates.keys():
            pr_name = line
            pr_n = predicates[pr_name]
            pr_params = [lines[l_].rstrip() for l_ in range(l + 1, l + 1 + pr_n)]
            l += (1 + pr_n)
        else:
            print('ReadError 1')
            
        if pr_n > 1:
            prop = Proposition(pr_name, pr_params)
        elif pr_n == 1:
            prop = Proposition(pr_name, pr_params[0])
        else:
            prop = Proposition(pr_name)
            
        output.append(prop)
        
    
    return set(output)

        

def get_opp_from_strings(lines, predicates):
    
    opp_name = lines[0].rstrip().lower()
    assert('Parameters' in lines[1])
    _, num_of_params = get_name_number(lines[1])
    
    params = []
    j = 2
    for j in range(2, 2 + num_of_params):
        params.append(lines[j].rstrip())
        
    assert(len(params) == num_of_params)
    
    pre_ind = 0
    add_ind = 0
    del_ind = 0
    
    for i in range(j, len(lines)):
        if 'Preconditions' in lines[i]:
            pre_ind = i
        elif 'Add-Effects' in lines[i]:
            add_ind = i
        elif 'Delete-Effects' in lines[i]:
            del_ind = i

    assert(pre_ind < add_ind)
    assert(add_ind < del_ind)
    
    _, num_of_pres = get_name_number(lines[pre_ind])
    _, num_of_adds = get_name_number(lines[add_ind])
    _, num_of_dels = get_name_number(lines[del_ind])
    
    
    pre_pos = get_predicates_from_strings(lines[pre_ind + 1: add_ind], predicates)
    eff_pos = get_predicates_from_strings(lines[add_ind + 1: del_ind], predicates)
    eff_neg = get_predicates_from_strings(lines[del_ind + 1:], predicates)
    
    
    assert(len(pre_pos) == num_of_pres)    
    assert(len(eff_pos) == num_of_adds)    
    assert(len(eff_neg) == num_of_dels)  
    
    #print(pre_pos)
    #print(eff_pos)
    #print(eff_neg)
    
    """ important: """
    pre_neg = {}
    
    action = Action(opp_name, pre_pos, pre_neg, eff_pos, eff_neg, variables=params)
    
    return action
    
    

        
def find_first_pattern(lines, pattern):
    ind = None
    
    for l, line in enumerate(lines):
        
        if pattern in line:
            _, num = get_name_number(line)
            ind = l
            
    assert(ind != None)
    
    return num, ind + 1
    
    

def read_domain(path):
    
    f = open(path,'r')
    lines = f.readlines()
    lines.append('\n')
    
    predicates = get_predicates(lines)
        

    num_of_acts, st_ind = find_first_pattern(lines, 'OPERATORS')

    end_ind = 0
    all_actions = []
    
    for l, line in enumerate(lines):

        if l < st_ind:
            continue
        
        if line == '\n' and st_ind > 0 and st_ind < l:
            end_ind = l
            
            new_action = get_opp_from_strings(lines[st_ind: end_ind], predicates)
            st_ind = end_ind + 1
        
            all_actions.append(new_action)
            
    assert(len(all_actions) == num_of_acts)
       
    f.close()
    
    return all_actions, predicates
    


def read_problem(path, predicates):

    f = open(path,'r')
    lines = f.readlines()
    lines.append('\n')
    
    num_of_objs, st_ind = find_first_pattern(lines, 'OBJECTS')
    end_ind = 0
    
    for l, line in enumerate(lines):

        if l < st_ind:
            continue
        
        if st_ind > 0 and line == '\n':
            end_ind = l
            assert(st_ind < end_ind)
            
            objects = [lll.rstrip() for lll in lines[st_ind: end_ind]]
            st_ind = 0
            break
    
    assert(len(objects) == num_of_objs)

    
    num_of_s0, st_ind = find_first_pattern(lines, 'INITIAL-STATE')
    end_ind = 0
    
    for l, line in enumerate(lines):

        if l < st_ind:
            continue
        
        if st_ind > 0 and line == '\n':
            end_ind = l
            assert(st_ind < end_ind)
            
            s0_pos = get_predicates_from_strings(lines[st_ind: end_ind], predicates)
            s0 = State(s0_pos)
            st_ind = 0
            break
    
    assert(len(s0_pos) == num_of_s0)
    
    num_of_g, st_ind = find_first_pattern(lines, 'GOALS')
    end_ind = 0
    
    for l, line in enumerate(lines):

        if l < st_ind:
            continue
        
        if st_ind > 0 and line == '\n':
            end_ind = l
            assert(st_ind < end_ind)
            
            g_pos = get_predicates_from_strings(lines[st_ind: end_ind], predicates)
            g_neg = {}
            goal = Goal(g_pos, g_neg)
            break
    
    assert(len(g_pos) == num_of_g)
    
    # print(num_of_objs)
    # print(s0)
    # print(goal)
    
    
    return s0, goal, objects

