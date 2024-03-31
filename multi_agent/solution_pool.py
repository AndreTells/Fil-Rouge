
#TODO: MAKE ABSTRACT CLASS
class solution_pool_simple:
    def __init__(self, difference_function, max_size=30, radious = 4):
        self.pool = []
        self.difference_function = difference_function
        self.radious = radious
        self.max_size = max_size
    
    #TODO: MAKE THE RETURN BE WHAT HAPPEND TO THE STEP ??
    def add_solution(self, step):
        new_sol = step.get_best_sol()
        new_sol_value = step.get_best_sol_value()

        smallest_diff: float = float('inf')
        closest_sol = None
        closest_sol_value = None
        i = -1

        for pool_step in self.pool:
            pool_sol = pool_step.get_best_sol()
            diff = self.difference_function(new_sol, pool_sol)
            if(diff< smallest_diff):
                smallest_diff = diff
                closest_sol = pool_sol
                closest_sol_value = pool_step.get_best_sol_value()
        
        if(smallest_diff>= self.radious):
            self.pool.append(step)

        elif((smallest_diff< self.radious) and (new_sol_value < closest_sol_value) ):
            self.pool[i] = step
        
        return

    def get_best_sol():
        return max(self.pool, key= lambda x:x.get_best_sol_value())