
    
def get_optimal_way(points):
    #return list of dict points sorted , tab of sorted id
    #p,t = get_optimal_way(points)
        
    #create distance graph with preference (*1.1) for y move
    graph = {}
    neighb = {}
    for psrc in points:
        neighb.clear()
        for pdst in points:
            if psrc["id"] != pdst["id"]:
                neighb[pdst["id"]] = sqrt(((psrc["x"]-pdst["x"])**2)*1.1+((psrc["y"]-pdst["y"])**2))
        graph[psrc["id"]] = neighb.copy()

    #sort for min and max points
    points = sorted(points , key=lambda elem: "%02d %s" % (elem['y'], elem['x']))
    id_start = points[0]["id"]
    id_end = points[len(points)-1]["id"]

    #get optimal way tab id
    tab = []
    id_cur = id_start
    while 1:
        tab.append(id_cur)
        if id_cur == id_end:
            break
        for i in graph:
            if id_cur in graph[i]:
                del graph[i][id_cur]    
        id_cur = min(graph[id_cur], key=graph[id_cur].get)

    #create list of dictionary points in optimal way order
    opt_points = []
    for i in tab:
        p = [e for e in points if e["id"] == i]
        opt_points.append(p.copy())

    return opt_points, tab

    
