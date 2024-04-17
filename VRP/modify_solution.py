import random

Path = list[int]


# swaps n nodes the place of n nodes in the path
def rand_opt_n(path: Path, num_of_nodes: int, n: int = 1) -> Path:
    new_state = path[:]  # fastest way to copy a list in python
    for k in range(n):
        i = (
            int((num_of_nodes - 1) * random.random()) + 1
        )  # generate a random number between 1 and num_of_nodes
        j = (
            int((num_of_nodes - 1) * random.random()) + 1
        )  # generate a random number between 1 and num_of_nodes

        if new_state[j] == 0 or new_state[i] == 0:
            return path

        new_state[i], new_state[j] = new_state[j], new_state[i]

    return new_state


# randomly chooses a section of the path and reverses it
def rand_reverse_section(path: Path, num_of_nodes: int) -> Path:
    i = (
        int((num_of_nodes - 1) * random.random()) + 1
    )  # generate a random number between 1 and num_of_nodes
    j = min(
        i + int((num_of_nodes - 1) * random.random()) + 1, num_of_nodes
    )  # generate a random number between 1 and num_of_nodes

    path_slice = list(reversed(path[i:j]))
    new_path = path[:i] + path_slice + path[j:]

    return new_path


# uses the rand_opt_n and rand_reverse_section at random (50% each)
def combined_rand_modification(path: Path, num_of_nodes: int) -> Path:
    decider = random.random()
    if decider >= 0.5:
        return rand_opt_n(path, num_of_nodes)

    return rand_reverse_section(path, num_of_nodes)


def shift_solution(path: Path) -> Path:
    """Shifts the route of each truck to left or right, randomly.
    Params: Path : flat solution sequence.
    Returns: Path : flat solution sequence.
    """
    subarrays = []
    start = -1

    # Identify subarrays between 0s
    for i in range(len(path) + 1):
        if i == len(path) or path[i] == 0:
            if start != -1:  # Ensure a valid subarray is found
                subarrays.append(path[start:i])
                start = -1  # Reset start for the next subarray
        elif start == -1:
            start = i  # Start of a new subarray

    # Shift subarrays and replace element
    shifted_arrays = []
    for subarray in subarrays:
        if random.random() > 0.5:
            # Shift left
            shifted = subarray[1:] + [subarray[0]]
        else:
            # Shift right
            shifted = [subarray[-1]] + subarray[:-1]
        shifted_arrays.append(shifted)
    # Construct the final array with zeroes
    final_array = []
    index = 0
    for i in range(len(path)):
        if path[i] == 0:
            final_array.append(0)
            if index < len(shifted_arrays):
                final_array.extend(shifted_arrays[index])
                index += 1

    return final_array
