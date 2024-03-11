from numpy import exp

def standard_calculate_temperature_function(x):
    return 100*((-exp(-x/8))+1)+0.01