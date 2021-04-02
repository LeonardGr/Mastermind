import random
import UseGA
import Lourd
Couleur =  (('J','B','R','V','L','N'))
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
            print ("Mauvaise taille d'entrée")
        return False
    for t in essai :
        if t not in Couleur :
            print ("Combo non valable")
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
    print(str(BP) + " bien placé\n" + str(MP) + " mal placé\n")
    return(BP,MP)

#Un code est généré, et l'on utilise après le GA ou le linéaire MM ou EN
while 1==1 :
    code = gen()
    print ("\nCode à trouver : " + str(code) + "\n")
    BP = 0
    MP = 0
    i = 1
    good = False
    while good == False :
        print ("Jouer avec GA(1) ou avec linear(2) ? ")
        jeu1 = input()
        if jeu1 == '1' or jeu1 == '2' : 
           good = True
        else : 
            print("mauvaise entrée ! ")
    if jeu1  == '1' :
        GA = UseGA.UseGA(Couleur, positions)
        while BP != positions :
            print ("Proposition n° : "+ str(len(GA.propositions)) + " -> " + str(GA.actual_prop))
            BP,MP = jeu(GA.actual_prop, code)
            GA.reponse(MP,BP)
            i += 1
    if jeu1 == '2' :
        good = False
        while good == False :
            print ("Jouer avec Max/min (1) ou avec Entropy(2) ou avec MinMax(3) ou avec EntropyBis(4)? ")
            jeu2 = input()
            if jeu2 == '1' or jeu2 == '2' or jeu2 == '3' or jeu2 == '4': 
                good = True
            else : 
                print("mauvaise entrée ! ")

                
        possibilites = Lourd.genPoss(Couleur, positions) 
        proposition = Lourd.PremiereProposition(Couleur, positions)
        while BP != positions : 
            print( " Il reste " + str(len(possibilites)) + " possibilités")
            print("propositions n°" + str(i) + " : " + str(proposition))
            BP,MP = jeu(proposition, code)
            possibilites = Lourd.reduce(proposition,possibilites,BP,MP)
            if jeu2 == '1' :
                proposition = Lourd.MaxMin(possibilites)
            elif jeu2 == '2' :
                proposition = Lourd.Entropy(possibilites)
            if jeu2 == '3' :
                proposition = Lourd.MinMax(possibilites)
            elif jeu2 == '4' :
                proposition = Lourd.Entropybis(possibilites)
            i +=1

    ("Partie finie en " + str(i-1) + " essai(s) ! ")
    print("______________________________________")

    
    good = False
    while good == False :
        print("\nNouvelle partie ? Y/N ")
        jeu3 = input()
        if jeu3 == 'Y' or jeu3 == 'N' : 
            good = True
        else : 
            print("mauvaise entrée ! ")
    if jeu3 == 'N' : break