"""
import copy
from math import sqrt
from operator import itemgetter

def Get_Optimal_Way(points):
    #return list of dict points sorted , tab of sorted id
    #p,t = get_optimal_way(points)
        
    #create distance graph with preference for y move (x*1.000001)
    graph = {}
    neighb = {}
    for psrc in points:
        neighb.clear()
        for pdst in points:
            if psrc["id"] != pdst["id"]:
                neighb[pdst["id"]] = sqrt(((psrc["x"]-pdst["x"])**2)*1.000001+((psrc["y"]-pdst["y"])**2))
        graph[psrc["id"]] = neighb.copy()

    #sort each each dict in dict and keep original copy
    for e in graph:
        graph[e] = dict(sorted(graph[e].items(),key=itemgetter(1)))
    graphcopy = copy.deepcopy(graph)

    #sort for min and max points
    points = sorted(points , key=lambda elem: "%02d %s" % (elem['y'], elem['x']))
    id_start = points[0]["id"]
    id_end = points[len(points)-1]["id"]

    #debug
    #id_start = 426
    #id_end = 465

    ####DEBUG
    #print(id_start)
    #print(id_end)

    #for p in points:
    #    print(p)
    #print(len(points))
    ####DEBUG


    #get optimal way tab id (shortest way with max points)
    #print("----------------------------")
    tab = []
    id_cur = id_start
    
    while 1:
        tab.append(id_cur)
        if id_cur == id_end:
            break
        id_next = min(graph[id_cur], key=graph[id_cur].get)
        
        #print(id_cur)
        #print(id_next)
        #print(graph[id_cur])
        
        for i in graph:
            if id_cur in graph[i]:
                del graph[i][id_cur]
        id_cur = id_next    
    
    #insert lost points by proximity
    tablost = []
    for k in graph[id_end].keys():
        tablost.append(k)

    #debug / security
    no_infinite = 5
    #debug

    while len(tablost) != 0:
        if no_infinite == 0:
            break

        #print(graphcopy)
        #print(tablost)

        for i in tablost:
            for m in graphcopy[i]:
                id_prox = m
                #print(id_prox)
                try:
                    ind_id_prox = tab.index(id_prox)
                    #print(ind_id_prox)
                    if ind_id_prox >= 1:
                        id_prox_bef = tab[ind_id_prox-1]
                        dist_bef = graphcopy[i][id_prox_bef]
                    else:
                        dist_bef = float('inf')
                    
                    if ind_id_prox < len(tab)-1:
                        id_prox_aft = tab[ind_id_prox+1]
                        dist_aft = graphcopy[i][id_prox_aft]
                    else:
                        dist_aft = float('inf')
                    
                    if dist_bef < dist_aft:
                        tab.insert(ind_id_prox,i)    
                    else:
                        tab.insert(ind_id_prox+1,i)
                    
                    tablost.remove(i)

                    
            
                    for j in graph:
                        if i in graph[j]:
                            del graph[j][i]
                    
                    #print(graph[i])

                    break
                except:
                    #print("error")
                    pass
    no_infinite -= 1

    #print(tablost)      
    #print("----------------------------")
    #print(graph)
    #print(len(graph))
    

    #create list of dictionary points in optimal way order
    opt_points = []
    for i in tab:
        p = [e for e in points if e["id"] == i]
        opt_points.append(p.copy()[0])
    return opt_points, tab

"""
    
def Filter_Points(points,name='',openfarm_slug='',age_min_day=0,age_max_day=365,meta_key='',meta_value='',pointer_type='Plant'):
    filtered_points = []
    for p in points:
        if p['pointer_type'].lower() == pointer_type.lower() and (p['name'].lower() == name.lower() or name == '') and (p['openfarm_slug'].lower() == openfarm_slug.lower() or openfarm_slug == ''):
            filtered_points.append(p.copy())
    return filtered_points


