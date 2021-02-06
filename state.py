from proposition import Proposition as p
from utils import convert_set_to_string_list
from goal import Goal
from action import Action
import itertools
from copy import deepcopy

class State:
    def __init__(self, propositions = set()):
        self.propositions = set (propositions)

    def get_vars(self):
        variables = []
        for p in self.propositions:
            variables += p.vars
            
        return list (set (variables))

    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "State" + ": " + ",".join(convert_set_to_string_list(self.propositions))
    
    def isGoal (self, g:Goal):
        for p in g.propos_pos:
            if p not in self.propositions:
                return False
        for p in g.propos_neg:
            if p in self.propositions:
                return False
        return True
    
    def isAppliable (self, a:Action):
        for p in a.pre_pos:
            if p not in self.propositions:
                return False
        for p in a.pre_neg:
            if p in self.propositions:
                return False
        return True
    
    def apply_unified_action(self, a:Action):
        assert self.isAppliable(a), "action:" + str (a) + "is not appliable to state:" + str(self)
        new_pros = (self.propositions - a.eff_neg) | a.eff_pos
        return State (new_pros)
    
    def get_all_unifications(self, action:Action):
        action_vars = action.get_vars()
        state_vars = self.get_vars()
        
        # possible_unifications = [{} for len(state_vars) ** len(action_vars)]
        
        all_perms = []
        for a in action_vars:
            l = []
            for s in state_vars:
                l.append((a,s))
            all_perms.append (l)

        all_mappings = []
        for element in itertools.product(*all_perms):
            mapping = {e[0]:e[1] for e in element}
            unified_action = action.substitute_and_copy(mapping)
            if self.isAppliable(unified_action):
                all_mappings.append (mapping)
        
        return all_mappings
    
    def get_all_possible_actions(self, all_actions):
        unified_actions = []
        for a in all_actions:
            unifications = self.get_all_unifications(a)
            for u in unifications:
                unified_actions.append(a.substitute_and_copy(u))
        return unified_actions

    def __eq__(self, other):
        if isinstance(other, State):
            if len (self.propositions - other.propositions) == 0:
                return True
        return False

if __name__=="__main__":
    p_s = {p("cl","a"), p("he"), p("ot" , "b"), p("on", ["a","b"])}
    s = State(p_s)
    print (s)
    print ("equality check" , s == deepcopy(s))
    p_s = {p("cl","b")}
    p_n = {p("he")}
    g = Goal(p_s,p_n)
    print (g)


    print (s.isGoal(g))


    pre_pos = {p("on" , ["ob1", "ob2"]) , p("cl","ob1"), p("he")}
    pre_neg = {}
    eff_pos = {p("cl","ob2"), p("hol","obj2"),}
    eff_neg = {p("on" , ["ob1", "ob2"]) , p("cl","ob1"), p("he")}
    
    a = Action("unstack", pre_pos, pre_neg, eff_pos, eff_neg)
    
    unifications = s.get_all_unifications(a)

    print ("all possilbe unifications:" , unifications)

    for u in unifications:
        print ("after applying" , u , ":")
        print (s.isAppliable(a))
        unified_action = deepcopy(a).substitute_and_copy(u)
        print (unified_action)
        s_new = s.apply_unified_action(unified_action)
        print ("new_state:" , s_new)
        print (s_new.isGoal(g))


