import sys
import os
from math import *
import random

def PRINT(MATRIX):
    for i in MATRIX:
        count = 0
        aux = "|"
        for j in i:
            aux += str(j)
            count += 1
            if(count != len(i)):
                aux += " "
        aux += "|"
        print aux

def MULTIPLY(A,B):
    if(len(A[0])!=len(B)):
        print "Fatal Error: Matrices have incorrect dimensions!"
        sys.exit()
    
    #for i in range(1,len(A)): # for(int i=1, i< 39,i++){}
        #A[i] # this works
    C = []
    cj = 0
    ck = 0
    for i in A: # A --> Looks for elements and iterate over them 
        Row = []
        for j in B[0]:
            Cij = 0   # --> ci cj
            for k in i: # in B:
                #print 'The indices are = (',ck,',',cj,')'
                Cij += k*B[ck][cj]
                ck += 1
            Row.append(Cij)
            ck = 0
            cj += 1
        C.append(Row)
        cj = 0
    return C

#Genera un numero aleatorio entre 0 y 1

def aleatorio():
    r = random.random()#*(x+1) x veces mas probable de que salga un 1
    if r >0.5:
        return 1
    else:
        return 0

#Funcion para generar un valor entero aleatorio entre a y b

def aleatorio(a,b):
    return int(a + (b-a)*random.random())


#Funcion que crea un grafo dado su dimension y sus aristas


def crear(Vertices,Aristas):
    if Aristas > Vertices*(Vertices-1)/2:
        print('Error : Revisa tu vaina manito.')
        return []
    #Funcion para llenar en funcion de si hay mas ceros o mas unos quien sea mayor se llenara primero
    default = 0
    insert = 1
    if Aristas > Vertices*(Vertices-1)/4:
        default = 1
        insert = 0 
        Aristas = Vertices*(Vertices-1)/2 - Aristas
    matriz = []
    #inicializar la matriz 
    for i in range(Vertices):
        row = []
        for j in range(Vertices):
            row.append(default)
        matriz.append(row)
    for i in range(Vertices):
        matriz[i][i] = 0
    a = {}
    b = ''
    #Asignar valores a la matriz
    while len(a) < Aristas:
        #Crear coordenadas aleatorias
        r1 = aleatorio(0,Vertices)
        r2 = aleatorio(0,Vertices)
        if r1 > r2:
            b = str(r2) + ',' + str(r1)
        elif r2 > r1:
            b = str(r1) + ',' + str(r2)
        else:
            continue

        if not b in a.keys():
            a[b] = 1
        else:
            continue
        #Insertar en la matriz
        matriz[r1][r2] = insert
        matriz[r2][r1] = insert
    return matriz



def create_latex(n):
    
    # Ring graph 
    
    f  = open("Graph.tex","w")
    l  = ''
    l += '\\begin{center}\n'
    l += '\\begin{tikzpicture}[>=stealth\',shorten >=0.5pt,auto,node distance=1.5cm,semithick]\n'
    l += '\\tikzstyle{every state}=[fill=red,draw=red,minimum size=3mm]\n'
    
    for i in range(n):
        l += '\\node[state] ('+str(i)+') at ('+str(cos(2*pi*i/n))+','+str(sin(2*pi*i/n))+') [] {};\n'
         
    l += '\\draw[red]\n'
    
    for i in range(n):
        l += '('+str((i)%n)+') edge  node {} ('+str((i+1)%n)+')\n'
    
    l += ';\n'
    
    l += '\\end{tikzpicture}\n'
    l += '\\end{center}\n'
    f.write(l)

def create_graph(adjmat):
    
    n = len(adjmat)
    
    f  = open("Graph.tex","w")
    l  = ''
    l += '\\begin{center}\n'
    l += '\\begin{tikzpicture}[>=stealth\',shorten >=0.5pt,auto,node distance=1.5cm,semithick]\n'
    l += '\\tikzstyle{every state}=[fill=red,draw=red,minimum size='+str(3*pow(n,-1./2.))+'mm]\n'
    
    r = pow(n,1./2.)
    
    for i in range(n):
        l += '\\node[state] ('+str(i)+') at ('+str(r*cos(2*pi*i/n))+','+str(r*sin(2*pi*i/n))+') [] {'+str(i+1)+'};\n'
         
    l += '\\draw[red]\n'
    
    for i in range(n):
        for j in range(n):
            if(i<j):
                continue
            if(adjmat[i][j]==1):
                l += '('+str((i)%n)+') edge  node {} ('+str((j)%n)+')\n'
    
    l += ';\n'
    
    l += '\\end{tikzpicture}\n'
    l += '\\end{center}\n'
    f.write(l)
    
    
    
    
    

    
#  
#  La cantidad de circuitos cerrados de tamano n 
#  es igual a Tr((Matriz de Adyacencia)^n)
#  
#   A.B = C -->  Cij = Aik Bkj 
#   Ej: C11 = A11B11 + A12B21 + A13B31 
#  

A = [[1,2,3,4]]
B = [[0],[-1],[1],[2]]

C = MULTIPLY(A,B)
print 'The matrix A is'
PRINT(A)
print 'The matrix B is'
PRINT(B)
print 'The matrix A.B is'
PRINT(C)


C = MULTIPLY(B,A)
print 'The matrix A is'
PRINT(A)
print 'The matrix B is'
PRINT(B)
print 'The matrix B.A is'
PRINT(C)


D = [[0,1,2,3],[1,2,3,4]]
E = [[0,1],[1,2],[3,4],[5,6]]
F = MULTIPLY(D,E)
G = MULTIPLY(E,D)
print 'The matrix D is'
PRINT(D)
print 'The matrix E is'
PRINT(E)
print 'The matrix D.E is'
PRINT(F)
print 'The matrix E.D is'
PRINT(G)

MyMat = crear(50,1225)

create_graph(MyMat)
PRINT(MyMat)

