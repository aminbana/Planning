from proposition import Proposition as p

def convert_list_to_string (l):
    return [str(p) for p in l]
    
class Action:
    
    def __init__(self, name, pre_pos, pre_neg, eff_pos, eff_neg):
        self.name = name
        self.pre_pos = pre_pos
        self.pre_neg = pre_neg
        self.eff_pos = eff_pos
        self.eff_neg = eff_neg
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name + ":    pre:[" + ",".join(convert_list_to_string(self.pre_pos)) + "|~" + "~,".join(convert_list_to_string(self.pre_neg)) + "]" +",  eff:[" + ",".join(convert_list_to_string(self.eff_neg)) + "|~" + "~,".join(convert_list_to_string(self.eff_pos)) + "]"
    
    def relax_action (self):
        self.pre_neg = []
        self.eff_neg = []
    
    def get_vars(self):
        variables = []

        for p in self.pre_pos + self.pre_neg + self.eff_pos + self.eff_neg:
            variables += p.vars
        
        return list (set (variables))
    
    def substitue (self, mapping):
        for p in self.pre_pos + self.pre_neg + self.eff_pos + self.eff_neg:
            p.substitute(mapping)
        return self

if __name__=="__main__":
    pre_pos = [p("on" , ["a", "b"]) , p("cl","a"), p("he")]
    pre_neg = []
    eff_pos = [p("cl","b")]
    eff_neg = [p("on" , ["a", "b"]) , p("cl","a"), p("he")]
    
    a = Action("unstack", pre_pos, pre_neg, eff_pos, eff_neg)
    print (set([1,2,2,4]))
    print (a.get_vars())
    print (a)
    print (a.substitue({"a":"obj1"}))
    