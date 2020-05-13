import sys

class Particle:    
    
    def __init__(self,Name,Color,Charge,HyperCharge,Spin,Mass):
        self.nam = Name
        self.col = Color
        self.chg = Charge
        self.hyp = HyperCharge
        self.mas = Mass
        self.spn = Spin
        
    def __str__(self):
        return self.nam
    
    def __eq__(self,oth):
        if(self.nam == oth.nam and self.col == oth.col and self.chg == oth.chg and self.hyp == oth.hyp and self.mas == oth.mas and self.spn == oth.spn):
            return True
        else:
            return False
        
    def Cross_Symmetry(Particle):
        self.chg = -self.chg


class CompositeParticle:
    
    def __init__(self,Name,Subparticles):
        self.sub = Subparticles
        self.nam = Name
    
    def __str__(self):
        return self.nam

class Process:           

    def __init__(self,Initial_State,Final_State):
        if(len(Initial_State)!=2):
            print "Error: The initial state must have 2 particles."
            sys.exit()
        else:
            self.ini = Initial_State
        if(len(Final_State)<2):
            print "Error: The final state must have at least 2 particles"
            sys.exit()
        else:
            self.fin = Final_State
        
        self.proc = []
        for i in self.ini:
            self.proc.append(i)
        for i in self.fin:
            self.proc.append(i)
        
    def __str__(self):
        aux = ""
        for i in self.ini:
            aux += i.nam +" "
        aux += " --> "
        for i in self.fin:
            aux += i.nam + " "
        return aux
    
    #def SubProcesses(self,SubProc):
        #RedProc = []
        ##print self.proc
        #if (len(self.proc)>1):
            #for i in xrange(1,len(self.proc)):
                ##print self.proc[i].nam
                #RedProc.append(self.proc[i])
        #else 
            #RedProc = self.proc
        
        #SubProcesses(RedProc,RedProc)
        
        #for i in self.proc[1].sub:
                #for j in RedProc:
                ##print i.nam
                    #SubProc.append(i)
                
            
            


b = Particle("b",1,-1,1/2,1/2,True)
s = Particle("s",1,-1,1/2,1/2,False)
d = Particle("d",1,-1,1/2,1/2,False)
u = Particle("u",1,2,1/2,1/2,False)
c = Particle("c",1,2,1/2,1/2,False)
g = Particle("g",1,0,0,1,False)

#proton = CompositeParticle("p",[g,d,u,s,c,b])

#jet = CompositeParticle("j",[g,d,u,s,c])


#MyProc=Process([proton,proton],[jet,jet,jet])

s = []

#MyProc.SubProcesses(s)

#print MyProc

#a = {"Name":"Juan","Age":14,"Dict":{"Hello":"World"}}
#print a
#a["List"] = [1,2,3,4,5]
#a["W"] = 11
#a["AAA"] = 33
#del a["List"]
#g = "Age"
#if g in a.keys():
    #del a[g]
#for i in a.keys():
    #print "The key is:",i,"while the value is:",a[i]
#h = a.keys()
#print h


def PRINT(MATRIX):
    for i in MATRIX:
        count = 0
        aux = "|"
        for j in i:
            aux += str(j)
            count += 1
            if(count != len(i)):
                aux += ","
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

    
