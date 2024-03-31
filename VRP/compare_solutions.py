Path = list[int]

def num_different_edges(path_1: Path, path_2: Path):
    path_1_edges = set([(i,j) for i,j in zip(path_1[:-1], path_1[1:])])
    path_2_edges = set([(i,j) for i,j in zip(path_2[:-1], path_2[1:])])
    num_diff_edges: int = 0
    for edge in path_1_edges:
        if(not(edge in path_2_edges)):
            num_diff_edges +=1

    return num_diff_edges