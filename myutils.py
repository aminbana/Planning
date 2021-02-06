
def convert_set_to_string_list (l:set):
    return [str(p) for p in l]

def get_actions_short_names(l:list):
    return "/".join ([a.get_short_name() for a in l])

def count_actions_but_noops(actions):
    l = 0
    for a in actions:
        if a.name != "noop":
            l += 1
    
    return l