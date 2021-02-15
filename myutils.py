
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

def print_results(final_plan, success, time=None, standard_print=True):

    if not standard_print:
        if success:
            print()
            print('elapsed time (s):', str(round(time, 4)), ', length of plan:', len(final_plan.actions))
            print(" ====================  final plan with FF search: ============================")
            for i, a in enumerate(final_plan.actions):
                print(str(i) + ':', a.get_short_name())
            print(" =============================================================================")
            
        else:
            print()
            print(" ====================  final plan with FF search: ============================")
            print("failed to find any plan")
            print(" =============================================================================")
    else:
        if success:
            for i, a in enumerate(final_plan.actions):
                print(str(i) + ': (' + a.name, ' '.join(a.get_vars()) + ')')