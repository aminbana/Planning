from proposition import Proposition as p
from utils import convert_set_to_string_list
    
class Action:
    
    def __init__(self, name, pre, eff_pos, eff_neg):
        self.name = name
        self.pre = set (pre)
        self.eff_pos = set (eff_pos)
        self.eff_neg = set (eff_neg)
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name + ":    pre:[" + ",".join(convert_set_to_string_list(self.pre)) + "]" +",  eff:[" + ",".join(convert_set_to_string_list(self.eff_pos)) + "   |    ~" + "~,".join(convert_set_to_string_list(self.eff_neg)) + "]"
    
    def relax_action (self):
        self.eff_neg = []
    
    def get_vars(self):
        variables = []

        for p in self.pre | self.eff_pos | self.eff_neg:
            variables += p.vars
        return list (set (variables))
    
    def substitue (self, mapping):

        for p in self.pre:
            p.substitute(mapping)
        self.pre = {d for d in self.pre}


        for p in self.eff_pos:
            p.substitute(mapping)
        self.eff_pos = {d for d in self.eff_pos}

        for p in self.eff_neg:
            p.substitute(mapping)
        self.eff_neg = {d for d in self.eff_neg}

        return self

if __name__=="__main__":
    pre = {p("on" , ["a", "b"]) , p("cl","a"), p("he")}
    eff_pos = {p("cl","b")}
    eff_neg = {p("on" , ["a", "b"]) , p("cl","a"), p("he")}
    
    a = Action("unstack", pre, eff_pos, eff_neg)

    print (a.get_vars())
    print (a)
    print (a.substitue({"a":"obj1", "b":"obj2"}))
    