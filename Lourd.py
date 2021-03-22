import math
import random 
import statistics
import itertools

def genPoss (couleur, positions) :
    all = list(itertools.product(couleur, repeat = positions))
    for i in range(len(all)) :
        t = list(all[i]).copy()
        all[i] = t
    return all

def jeu(essai, code) :
    #code = self.previousGess(Nmbtest-1)s
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
    return(BP,MP)

def PremiereProposition (couleur, positions) :
        code =[] 
        for i in range (positions) :
            code.append(random.choice(couleur))
        #print(code)
        return code

def reduce (code, ensemble, BP, MP) :
    newensemble = []
    for elements in ensemble :
        elements = list(elements)
        BPT,MPT = jeu(list(code), elements)
        #print("code de base : " + str(code) + " code test : " + str(elements) + "\n Resultats :" + str(BP) + " contre " + str(BPT) + " et " +str(MP) + " contre " + str(MPT))
        if BPT == BP and MPT == MP :
            newensemble.append(elements)
    return newensemble

def information(ensemble, code, BP, MP) :
    newensemble = reduce(code, ensemble, BP, MP)
    info = len(newensemble)/len(ensemble)
    if info != 0 :
        info = math.log2(info)
    return info

def multipleInfo(code, ensemble, nbrPositions) :
    """
        To do : Pour un code, calculer pour chaque combo de MP/BP, les infos
        Tester toutes les positions :
    """
    info = []
    for i in range(nbrPositions + 1 ) :
        good = True
        for j in range(nbrPositions) :
            if (i+j)<= nbrPositions  :
                if j ==(nbrPositions - 1) :
                    if i!=0 :
                        good = False
                if good == True  :
                    MP = i
                    BP = j
                    info.append(information(ensemble, code, BP, MP))
                    #print("Bien placé : " + str(BP) + " \nMal placé : " + str(MP)+ "\n")
    return info

def MaxMin(ensemble) :
    info = []
    listinfo =[]
    for element in ensemble :
        info = multipleInfo(element, ensemble, 6)
        listinfo.append(min(info))
    IndexBC = listinfo.index(max(listinfo))
    bestchoice = ensemble[IndexBC]
    return bestchoice

def Entropy(ensemble) : 
    info = []
    listinfo =[]
    for element in ensemble :
        info = multipleInfo(element, ensemble, 6)
        #print(statistics.mean(info))
        listinfo.append(statistics.mean(info))
    IndexBC = listinfo.index(max(listinfo))
    bestchoice = ensemble[IndexBC]
    return bestchoice
"""
TO DO :
Calculer l'information gagnable de chaque possibilité
Il faut donc pour chaque code dans l'ensemble possible :
    1- Calculer pour chaque réponse possible l'ensemble que ça donnerait et sa taille
    2- Diviser par la taille totale de l'ensemble
    3- Calculer le log2

MaxMin Strategy :
1- Calculer pour chaque code dans l'ensemble toutes les informations pour chaque réponse
2- Retenir le minimum
3- Prendre le code avec le plus grand minimum

Max Entropy Strategy :
1- Calculer pour chaque code dans l'ensemble toutes les informations pour chaque réponse
2- Calculer la moyenne de chacun
3- Prendre celui avec la moyenne la plus haute
"""
