from proposition import Proposition as p
from utils import convert_set_to_string_list

class Goal:
    def __init__(self, propos_pos, propos_neg):
        self.propos_pos = propos_pos
        self.propos_neg = propos_neg

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "GOAL: " + ",".join(convert_set_to_string_list(self.propos_pos)) + ", ~" + ",".join(convert_set_to_string_list(self.propos_neg))  
