# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 23:04:43 2022

@author: Silvia
"""
import operator
import time

start = time.time()
F0=[0,0]
Maquinas = range(1,20+1)
Trabajos = range(1,500+1)
#Var(Trabajo, Maquina)
Var = {
}

TotalTimeJob=[]
Secuencia=[]
Tinicio={}
for j in Trabajos:
    h=0
    for m in Maquinas:
        h += Var[(j, m)]
    TotalTimeJob.append((j,h)) #Lista de tiempo total para cada trabajo j
Pj=sorted(TotalTimeJob, key=operator.itemgetter(1), reverse=True)
Secuencia.append(Pj[0][0])
Secuencia.append(Pj[1][0])

for x in range(0,2):
    #Evaluar con 3 primero y luego con 6    
    Tinicio[(Pj[x][0],1)]=0
    
    for m in Maquinas:
        jant=0
        for j in Secuencia:
            if m==1 and j==Pj[x][0]:
                jant=j
                next
            if m==1 and j!=Pj[x][0]:
                Tinicio[(j,m)]=Var[(Pj[x][0],1)]
                jant=j
                next
            if m>1 and j==Pj[x][0]:
                Tinicio[(j,m)]=Tinicio[(j,m-1)]+Var[(j,m-1)]
                jant=j
                next
            if m>1 and j!=Pj[x][0]:
                Tinicio[(j,m)]=max(Tinicio[(j,m-1)]+Var[(j,m-1)], Tinicio[(jant,m)]+Var[(jant,m)])
            jant=j
    
    F0[x]=Tinicio[max(Tinicio.items(), key=operator.itemgetter(1))[0]]+Var[max(Tinicio.items(), key=operator.itemgetter(1))[0]]

    if x==0:  #Evaluar con 6 primero
        Secuencia=[]
        Secuencia.append(Pj[1][0])
        Secuencia.append(Pj[0][0])
      
if F0[0]<F0[1]:
        Secuencia=[]
        Secuencia.append(Pj[0][0])
        Secuencia.append(Pj[1][0])
        Makespan=F0[0]
else:
    Makespan=F0[1]
Pj.pop(0) #Eliminar los 2 trabajos que ya están en la secuencia
Pj.pop(0) 
#Var.pop((1,1)) Eliminar elementos de un diccionario
#Ahora debemos revisar cada trabajo en cada posición
for job in range(0, len(Pj)): #range(0, len(Pj))Trabajos que va a ir agregando a la mejor secuencia
    F0Sol={}
    for ubi in range(0, len(Secuencia)+1): #Escoger la mejor posición para el trabajo
            Tinicio={}
            Secuencia.insert(ubi,Pj[job][0])
           
            for m in Maquinas: 
                for x in Secuencia:    #Evaluar la F0 de toda la sec 
                    if x==Secuencia[0]: #Si está en la primera posición
                        if m==1: 
                            Tinicio[(Secuencia[0],m)]=0
                            jant=x
                            next
                        else:
                            Tinicio[(x,m)]=Tinicio[(x,m-1)]+Var[(x,m-1)]
                            jant=x
                            next
                    if x!=Secuencia[0]: #Para los jobs que no están en la posición 1
                        if m==1:
                            Tinicio[(x,m)]=Tinicio[(jant,m)]+Var[(jant,m)]
                            jant=x
                            next
                        else:
                            Tinicio[(x,m)]=max(Tinicio[(x,m-1)]+Var[(x,m-1)], Tinicio[(jant,m)]+Var[(jant,m)])
                            jant=x
                            next
                    jant=x
                    
            F0Sol[(Tinicio[(x,m)]+Var[(x,m)])]=Secuencia.copy()
            Secuencia.pop(ubi) #Se elimina si la anterior es mejor
            #print("Ttotal: "+str(F0Sol)+" Job:"+str(x)+" Maq: "+str(m))
    Secuencia=F0Sol[(min(F0Sol))]
    
end = time.time()
print(end - start) #2214.1852543354034
#min(F0Sol)

