import random
import CodeBreaker
import Lourd
import time
import sys
Couleur =  (('J','B','R','V','L','N'))
juste = False
positions = 4
i = 1
essai =""




def gen() :
    code =[]
    for i in range(4) : 
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
code = gen()
BP = 0
MP = 0
i = 1
if sys.argv[1]  == 'GA' :
    gameBreaker = CodeBreaker.MMCodebreaker(Couleur, positions)
    while BP != positions :
        #print ("Proposition n° : "+ str(gameBreaker.compte) + " -> " + str(gameBreaker.nextMove()))
        BP,MP = jeu(gameBreaker.nextMove(), code)
        gameBreaker.reponse(MP,BP)
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
            proposition = Lourd.MinMax(possibilites)
        elif sys.argv[2] == 'Entropy' :
            proposition = Lourd.Entropybis(possibilites)
        i +=1
temps = time.time() - debut
print(str(temps) + "    " + str(i-1))