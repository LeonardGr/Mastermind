import random

def fusion(L1,L2):
    n1 = len(L1)
    n2 = len(L2)
    L12 = [0]*(n1+n2)
    i1 = 0
    i2 = 0
    i = 0
    while i1<n1 and i2<n2:
        if L1[i1] < L2[i2]:
            L12[i] = L1[i1]
            i1 += 1
        else:
            L12[i] = L2[i2]
            i2 += 1
        i += 1
    while i1<n1:
        L12[i] = L1[i1]
        i1 += 1
        i += 1
    while i2<n2:
        L12[i] = L2[i2]
        i2 += 1
        i += 1 
    return L12
           
def tri_fusion_recursif(L):
    n = len(L)
    if n > 1:
        p = int(n/2)
        L1 = L[0:p]
        L2 = L[p:n]
        tri_fusion_recursif(L1)
        tri_fusion_recursif(L2)
        L[:] = fusion(L1,L2)


def tri_fusion(L):
    M = list(L)
    tri_fusion_recursif(M)
    return M

def compare(essai,code) :
    Vessai = essai.copy()
    BP = 0
    MP = 0
    for index, couleur in enumerate(code) :
        if couleur == Vessai[index] :
            BP +=1
            Vessai[index] = '0'
        elif couleur in Vessai:
            if Vessai[Vessai.index(couleur)] != code[Vessai.index(couleur)] :
                MP +=1
                Vessai[Vessai.index(couleur)] = '0'

    #print(str(BP) + " bien placé\n" + str(MP) + " mal placé\n")
    return BP,MP

def gen(positions, Couleur) :
    code =[]
    for i in range(positions) : 
        code.append(random.choice(Couleur))
    return code