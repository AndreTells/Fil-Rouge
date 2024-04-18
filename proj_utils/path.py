import matplotlib.pyplot as plt
Path = list[int]

# transforms a list of the type [0,1,2,3,4,0,5,6,7,8,9,0] into a list like
# [[0,1,2,3,4,0],[0,5,6,7,8,9,,0]]
def split_paths(paths: Path)->list[Path]:
    path_list: list[Path]= []
    path_id = -1
    for i in paths:
        if(i == 0):
            if(path_id != -1):
                path_list[path_id].append(i)    
            path_list.append([])
            path_id+=1
        path_list[path_id].append(i)
        


    return path_list[:-1]

# uses matplot lib to show the path given as a line connecting points in a 2d plane
def print_path(points: list[tuple[int,int]], sol: Path):
    x = list(map(lambda x: points[x][0], sol))
    y = list(map(lambda x: points[x][1], sol))

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.35)

    ax.scatter(x,y, marker='x', color = 'red', )

    path_graphs = []
    for path in split_paths(sol):
        x = list(map(lambda x: points[x][0], path))
        y = list(map(lambda x: points[x][1], path))
        path_graph, = ax.plot(x,y)
        path_graphs.append(path_graph)