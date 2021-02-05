class Proposition:
    
    def __init__(self, name, variables = []):
        if not isinstance(variables, list):
            variables = [variables]
        self.name = name
        self.vars = variables
    
    def __repr__(self):
        return self.name + "(" + ",".join (self.vars)+")"
   
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Proposition):
            return self.__repr__() == other.__repr__()
        return False
    
    def substitute (self, mapping):
        for key, value in mapping.items():
            if key in self.vars:
                self.vars[self.vars.index(key)] = value
        return self
        
    def __str__(self):
        return self.__repr__()

if __name__=="__main__":
    print (Proposition("on", ["a","b"]))
    print (Proposition("on", ["a","b"]) == Proposition("clear", ["a"]))
    print (Proposition("on", ["a","b"]) == Proposition("on", ["a","b"]))

    p = Proposition("on", ["a","b"])
    p.substitute({"a":"obj"})
    print (p)
    

