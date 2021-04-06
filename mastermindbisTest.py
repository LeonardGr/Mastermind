import UsePSO
import random
import UseGA
import Lourd
import time
import util
import sys
Couleur =  (('J','B','R','V','L','N','A','Z','E','T','Y','U','I','O','P','Q','S','D','F','G'))
juste = False
positions = 4
i = 1
essai =""




def gen() :
    code =[]
    for i in range(positions) : 
        code.append(random.choice(Couleur))
    return code

def test(essai) :
    if len(essai) != 4 :
        if len(essai) != 0 :
            #print ("Mauvaise taille d'entrée")
            return False
    for t in essai :
        if t not in Couleur :
            #print ("Combo non valable")
            return False
    return True

def jeu(essai, code) :
    Vessai = essai.copy()
    Vcode = code.copy()
    BPlist = []
    BP = 0
    MP = 0
    for i in range(len(Vessai)) :
        if Vessai[i] == Vcode[i] :
            BP += 1
            BPlist.append(i)
    Bessai =[]
    Bcode = []
    for i in range(len(Vessai)) :
        if i not in (BPlist) :
            Bessai.append(Vessai[i])
            Bcode.append(Vcode[i])
    Vessai = Bessai
    Vcode = Bcode
    for i in range(len(Vessai)) :
        if Vessai[i] in Vcode :
            MP +=1
            Vcode.remove(Vessai[i])
    #print(str(BP) + " bien placé\n" + str(MP) + " mal placé\n")
    return(BP,MP)


debut = time.time()


BP = 0
MP = 0
i = 1
NombreCouleur = int(sys.argv[3])
positions = int(sys.argv[2])
Couleur = Couleur[:NombreCouleur]
code = gen()
#print("code to find:" + str(code))
if sys.argv[1]  == 'GA' :
    ponderation = 2
    depart = 0
    pourcentage = 2
    TailleEligible = 15*positions
    TaillePopu = 35*positions
    NombreGen = 40*positions
    GA = UseGA.UseGA(Couleur, positions, ponderation, depart, pourcentage, TailleEligible, TaillePopu, NombreGen)
    while BP != positions :
        #print ("Proposition n° : "+ str(GA.compte) + " -> " + str(GA.nextMove()))
        BP,MP = util.compare(GA.actual_prop, code)
        GA.reponse(MP,BP)
        i += 1

if sys.argv[1]  == 'PSO' :
    NbreCluster = 10
    NbreAgent = 5
    Distmin = 2
    distmax = 4
    distpull = 3
    MaxGen = 10
    PSO = UsePSO.UsePSO(Couleur, positions,NbreCluster, NbreAgent, Distmin, distmax, distpull,MaxGen )
    while BP != positions :
        #print ("Proposition n° : "+ str(len(PSO.propositions)) + " -> " + str(PSO.actual_prop))
        BP,MP = util.compare(PSO.actual_prop, code)
        if BP != positions : 
                PSO.reponse(MP,BP)
        i += 1

if sys.argv[1] == 'Linear' :
    possibilites = Lourd.genPoss(Couleur, positions) 
    proposition = Lourd.PremiereProposition(Couleur, positions)
    while BP != positions : 
        #print( " Il reste " + str(len(possibilites)) + " possibilités")
        #print("propositions n°" + str(i) + " : " + str(proposition))
        BP,MP = jeu(proposition, code)
        possibilites = Lourd.reduce(proposition,possibilites,BP,MP)
        if sys.argv[2] == 'MaxMin' :
            proposition = Lourd.MaxMin(possibilites)
        elif sys.argv[2] == 'Entropy' :
            proposition = Lourd.Entropy(possibilites)
        i +=1
temps = time.time() - debut
print(str(temps) + "    " + str(i-1))