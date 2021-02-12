from state import State
from proposition import Proposition as p
from myutils import convert_set_to_string_list
from goal import Goal
from action import Action
from copy import deepcopy

class Graphlayer(State):
    def __init__(self, propositions, propositions_negative = {}):
        super().__init__(propositions)
        self.propositions_negative = set (propositions_negative)
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "GraphLayer" + ": " + ",".join(convert_set_to_string_list(self.propositions)) + ",~" + ",~".join(convert_set_to_string_list(self.propositions_negative))

    def isAppliable (self, a:Action):
        for p in a.pre_pos:
            if p not in self.propositions:
                return False
        for p in a.pre_neg:
            if p not in self.propositions_negative:
                return False
        return True

    def apply_unified_action(self, a:Action):
        return self.apply_unified_actions([a])
    
    def apply_unified_actions (self, actions):
        new_pros = set ()
        new_pros_neg = set ()

        for a in actions:
            assert self.isAppliable(a), "action:" + str (a) + "is not appliable to state:" + str(self)
            new_pros = new_pros | a.eff_pos
            new_pros_neg = new_pros_neg | a.eff_neg
        return Graphlayer (new_pros, new_pros_neg)
    
    def isGoal (self, g:Goal):
        assert False, "use has goal for graphlayers"
        
    def hasGoal (self, g:Goal):
        for p in g.propos_pos:
            if p not in self.propositions:
                return False

        for p in g.propos_neg:
            if p not in self.propositions:
                return False
        
        return True
    
    def __eq__(self, other):
        if isinstance(other, Graphlayer):
            if len (self.propositions - other.propositions) == 0 & len (self.propositions_negative - other.propositions_negative):
                return True
        return False

    def get_noops (self):
        noops = []
        for p_pos in self.propositions:
            ac_noop = Action ("noop", {p_pos}, {}, {p_pos}, {})
            noops.append(ac_noop)
        
        for p_neg in self.propositions_negative:
            ac_noop = Action ("noop", {}, {p_neg}, {}, {p_neg})
            noops.append(ac_noop)
        return noops
        
if __name__== "__main__":
    p_s = {p("cl","a"), p("he"), p("ot" , "b"), p("on", ["a","b"])}
    p_n = {}
    gl = Graphlayer(p_s,p_n)

    pre_pos = {p("on" , ["ob1", "ob2"]) , p("cl","ob1"), p("he")}
    pre_neg = {}
    eff_pos = {p("cl","ob2"), p("hol","obj2"),}
    eff_neg = {p("on" , ["ob1", "ob2"]) , p("cl","ob1"), p("he")}
    
    a = Action("unstack", pre_pos, pre_neg, eff_pos, eff_neg)
    all_possible_actions = gl.get_all_possible_actions ([a])


    
    new_gl = gl.apply_unified_actions(all_possible_actions + gl.get_noops())

    print (gl)
    print (new_gl)