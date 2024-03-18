def capacity_add(a,b):
    return (a[0]+b[0],a[1]+b[1])

def capacity_null_value():
    return (0,0)

def capacity_condition(current_load,capacity):
    if(current_load[0]>= capacity[0] or current_load[1]>= capacity[1]):
        return False
    return True