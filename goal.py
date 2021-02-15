from copy import deepcopy
from proposition import Proposition as p
from myutils import convert_set_to_string_list
from action import Action
import itertools

class Goal:
    def __init__(self, propos_pos, propos_neg):
        self.propos_pos = set (propos_pos)
        self.propos_neg = set (propos_neg)

    def get_vars(self):
        variables = []
        for p in self.propos_pos:
            variables += p.vars
        for p in self.propos_neg:
            variables += p.vars            
        return list (set (variables))

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "GOAL: " + ",".join(convert_set_to_string_list(self.propos_pos)) + ",~" + ",~".join(convert_set_to_string_list(self.propos_neg))  

    def __eq__(self, other):
        if isinstance(other, Goal):
            if self.propos_pos == other.propos_pos and self.propos_neg == other.propos_neg:
                return True
        return False
    
    def relax_goal(self):
        new_goal = deepcopy(self)
        new_goal.propos_neg = set()
        return new_goal
        
    def isBackwardAppliable (self, a:Action):
        if len (a.eff_pos.intersection(self.propos_neg)) != 0 or len (a.eff_neg.intersection(self.propos_pos)) != 0:
            return False
        if len (a.eff_pos.intersection(self.propos_pos)) == 0 and len (a.eff_neg.intersection(self.propos_neg)) == 0:
            return False
        
        return True
    
    def apply_inverse_unified_action(self, a:Action):
        assert self.isBackwardAppliable(a), "action:" + str (a) + "is not appliable to state:" + str(self)
        new_pros_pos = (self.propos_pos - a.eff_pos) | a.pre_pos
        new_pros_neg = (self.propos_neg - a.eff_neg) | a.pre_neg
        return Goal(new_pros_pos, new_pros_neg)
    
    def get_all_backward_unifications(self, action:Action, s):
        action_vars = action.get_vars()
        state_vars = s.get_vars()
        
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
            if self.isBackwardAppliable(unified_action):
                all_mappings.append (mapping)
        
        return all_mappings
    
    def get_all_possible_backward_actions(self, all_actions, s):
        unified_actions = []
        for a in all_actions:
            unifications = self.get_all_backward_unifications(a, s)
            for u in unifications:
                unified_actions.append(a.substitute_and_copy(u))
        return unified_actions

if __name__ == "__main__":
    p_s = {p("cl","b")}
    p_n = {}
    g = Goal(p_s,p_n)
    print (g)


    pre_pos = {p("on" , ["ob1", "ob2"]) , p("cl","ob1"), p("he")}
    pre_neg = {}
    eff_pos = {p("cl","ob2"), p("hol","ob2"),}
    eff_neg = {p("on" , ["ob1", "ob2"]) , p("cl","ob1"), p("he")}
    
    a = Action("unstack", pre_pos, pre_neg, eff_pos, eff_neg)

    from state import State
    p_s = {p("cl","a"), p("he"), p("ot" , "b"), p("on", ["a","b"])}
    s = State(p_s)
    

    print (g.get_all_possible_backward_actions([a], s))