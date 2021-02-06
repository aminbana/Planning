from state import State
from action import Action
from copy import deepcopy
from utils import get_actions_short_names

class Plan:
    def __init__(self):
        self.actions = []
    def apply_to_state(self, s:State):
        for a in self.actions:
            s = s.apply_unified_action(a)
        return s
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return get_actions_short_names(self.actions)
    def append_after (self, a:Action):
        self.actions = self.actions + [a]
    
    def append_before (self, a:Action):
        self.actions = [a] + self.actions