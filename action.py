from proposition import Proposition as p
from myutils import convert_set_to_string_list
from copy import deepcopy

class Action:
    
    def __init__(self, name, pre_pos, pre_neg, eff_pos, eff_neg):
        self.name = name
        self.pre_pos = set (pre_pos)
        self.pre_neg = set (pre_neg)
        self.eff_pos = set (eff_pos)
        self.eff_neg = set (eff_neg)
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        variables = self.get_vars()
        return self.name + "(" + ",".join (variables) + ")" + ": pre:[" + ",".join(convert_set_to_string_list(self.pre_pos)) + "~,".join(convert_set_to_string_list(self.pre_neg)) + "]" +", eff:[" + ",".join(convert_set_to_string_list(self.eff_pos)) + " |  ~" + "~,".join(convert_set_to_string_list(self.eff_neg)) + "]"

    def get_short_name(self):
        variables = self.get_vars()
        return self.name + "(" + ",".join (variables) + ")"
    def relax_action (self):
        new_a = deepcopy(self)
        new_a.eff_neg = set()
        new_a.pre_neg = set()
        return new_a
    
    def get_vars(self):
        variables = []

        for p in self.pre_pos | self.pre_neg | self.eff_pos | self.eff_neg:
            variables += p.vars
        return list (set (variables))
    
    def substitute_and_copy (self, mapping):
        new_action = deepcopy (self)

        for p in new_action.pre_neg:
            p.substitute(mapping)
        new_action.pre_neg = {d for d in new_action.pre_neg}

        for p in new_action.pre_pos:
            p.substitute(mapping)
        new_action.pre_pos = {d for d in new_action.pre_pos}

        for p in new_action.eff_pos:
            p.substitute(mapping)
        new_action.eff_pos = {d for d in new_action.eff_pos}

        for p in new_action.eff_neg:
            p.substitute(mapping)
        new_action.eff_neg = {d for d in new_action.eff_neg}

        return new_action

if __name__=="__main__":
    pre_pos = {p("on" , ["a", "b"]) , p("cl","a"), p("he")}
    pre_neg = {}
    eff_pos = {p("cl","b")}
    eff_neg = {p("on" , ["a", "b"]) , p("cl","a"), p("he")}
    
    a = Action("unstack", pre_pos, pre_neg, eff_pos, eff_neg)
    print (a)
    print (a.get_short_name())
    print (a.get_vars())
    
    print (a.substitute_and_copy({"a":"obj1", "b":"obj2"}))
    