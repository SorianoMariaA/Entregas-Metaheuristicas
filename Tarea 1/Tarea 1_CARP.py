import igraph as ig
import matplotlib.pyplot as plt
import operator

F0=[1]
Lij = {(1,1):0}
Dij = {}
V = 12
G = [ ( 1, 2), ( 1, 4), ( 1, 7), ( 1, 10), ( 1, 12), ( 2, 3), ( 2, 4), ( 2, 9), ( 3, 4), ( 3, 5), ( 3, 11), ( 4, 11), ( 5, 6), ( 5, 11), ( 5, 12), ( 6, 7), ( 6, 12), ( 7, 8), ( 7, 12), ( 8, 10), ( 9, 10), ( 12, 11)]
Gprima=G
# Construct the graph
g = ig.Graph(G)
g.es["weight"] = [ 13, 17, 19, 19, 4 , 18, 9 , 2 , 20, 5 , 22, 6 , 7 , 17, 11, 4 , 3 , 8 , 18, 3 , 16, 19]


distance = 0

for j in range(2,V+1):
    #Distancia de 1 a i = j a 1
    resultsL = g.get_shortest_paths(1, to=j, weights=g.es["weight"], output="epath", )
    for i in resultsL[0]: 
        distance += g.es[i]["weight"]
        
    Lij[(1, j)]=distance
    distance=0

for i in Gprima:
   Dij[i] = Lij[(1,i[0])] + Lij[(1,i[1])]


'-------------------------------------------------------------------------------------------------------'
while len(Gprima)>0:
    Toneladas=0
    distance=0
    max_key = max(Dij.items(), key=operator.itemgetter(1))[0]
    #print(max_key)
    SP_0i = g.get_shortest_paths(1, to= max_key[0], weights=g.es["weight"], output="vpath", )
    SP_j0 = g.get_shortest_paths(max_key[1], to=1, weights=g.es["weight"], output="vpath", )
    
    C = SP_0i[0] + SP_j0[0]
    #Cuando llegue al deposito vaciar el camion
    print(" ")
    print("Ruta: "+str(C))

    C.pop(0) #Eliminar el primer nodo del deposito
    F0=F0+C
    
    print("Se limpio el arco: ",max_key)
    Gprima.remove(max_key)
    Barrer=max_key
    Toneladas +=1
    del Dij[max_key]
    
    if len(SP_0i[0])<=5:
        first=SP_0i[0][0]
        for x in range(1, len(SP_0i[0])):
            last=SP_0i[0][x]
            
            try:
                Gprima.remove((first,last))
                print("Se limpio el arco: (",first,",",last,")")
                Toneladas+=1
                del Dij[(first,last)]
                
            except:
                #print("Run Except 1")
                if (last,first) in Gprima:
                    Gprima.remove((last,first))
                    print("Se limpio el arco: (",first,",",last,")")
                    Toneladas+=1
                    del Dij[(last,first)]
    
            first=last
            
    if len(SP_j0[0])<=(6-Toneladas):
        #print("No")
        first=SP_j0[0][0]
        for x in range(1, len(SP_j0[0])):
            last=SP_j0[0][x]
            
            try:
                Gprima.remove((first,last))
                print("Se limpio el arco: (",first,",",last,")")
                Toneladas+=1
                del Dij[(first,last)]
            except:
                #print("Run Except 2 ")
                if (last,first) in Gprima:
                    Gprima.remove((last,first))
                    print("Se limpio el arco: (",first,",",last,")")
                    Toneladas+=1
                    del Dij[(last,first)]
                
            first=last
    
G = [ ( 1, 2), ( 1, 4), ( 1, 7), ( 1, 10), ( 1, 12), ( 2, 3), ( 2, 4), ( 2, 9), ( 3, 4), ( 3, 5), ( 3, 11), ( 4, 11), ( 5, 6), ( 5, 11), ( 5, 12), ( 6, 7), ( 6, 12), ( 7, 8), ( 7, 12), ( 8, 10), ( 9, 10), ( 12, 11)]
print("  ")
print("Ruta completa")
print(F0)
    
for i in range(0,len(F0)-1):
    #print("first ", F0[i],", ", F0[i+1])
    try: distance+=g.es[G.index((F0[i],F0[i+1]))]["weight"]
    except: distance+=g.es[G.index((F0[i+1],F0[i]))]["weight"]
print("  ")
print("Distancia total:", distance)


'-------------------------------------------------------------------------------------------------------'
# Get a shortest path along edges
results = g.get_shortest_paths(1, to=11, weights=g.es["weight"], output="vpath", )

# Plot graph
g.es['width'] = 0.5
g.es[results[0]]['width'] = 2.5

fig, ax = plt.subplots()
ig.plot(
    g,
    target=ax,
    layout='circle',
    vertex_color='steelblue',
    vertex_label=range(g.vcount()),
    #edge_width=g.es['width'],
    edge_label=g.es["weight"],
    edge_color='#666',
    edge_align_label=True,
    edge_background='white'
)