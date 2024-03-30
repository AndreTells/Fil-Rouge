from numpy import exp

def probability_standard(energy_of_s: float,energy_of_s_new: float, temp: float)->float:
    if(energy_of_s_new < energy_of_s):
        return 1
    return exp(-(energy_of_s_new-energy_of_s)/temp)
