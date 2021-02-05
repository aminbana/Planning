class Proposition:
    def __init__(self, name, variables):
        self.name = name
        self.vars = variables
    def __repr__(self):
        return self.name + "(" + ",".join (self.vars)+")"

if __name__=="__main__":
    print (Proposition("on", ["a","b"]))
