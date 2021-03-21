import random
import secrets
import trifusion

class Genetic :
    TaillePopu = 150
    MaxGen = 100
    MaxSize = 60
    A = 1
    B = 2

    def __init__(self, couleurs, NbrePosition ) :
        self.CouleurPossible = couleurs
        self.popu = []
        self.reponse = []
        self.PrecedentTry = []
        self.TryNumber = 0
        self.positions = NbrePosition
        self.CreateGenetic(self.CouleurPossible)

    def TestCodeExist(self, ensemble, test) :
        if len(ensemble) != 0 :
            if test in ensemble :
                return True
            else :
                return False

    def addRandomCode(self, indice, ensemble) :
        mot =[]
        Exist = True
        while (Exist == True):
            mot = []
            for i in range(4) : 
                mot.append(random.choice(self.CouleurPossible))
            Exist = self.TestCodeExist(ensemble, mot)
        try : 
            ensemble[indice] = mot  
        except :
            ensemble.append(mot)

    def CreateGenetic(self, couleurs) :
        self.CouleurPossible = couleurs
        self.popu = []
        for i in range(Genetic.TaillePopu) :
            self.addRandomCode(i, self.popu)
        

    def bestCode(self, Count, response, PrecedentTry) :
        self.reponse = response
        self.TryNumber = Count 
        self.PrecedentTry = PrecedentTry

        h = 1
        eligible = []
        A = 1
        B = 2

        while(h <= Genetic.MaxGen and len(eligible)<=Genetic.MaxSize) :
            self.DevGenetic()
            for i in range(Genetic.TaillePopu) :
                difBP = 0
                difMP = 0
                for j in range(len(self.PrecedentTry)) : 
                    BP,MP = self.jeu(self.PrecedentTry[j], self.popu[i])
                    difBP += Genetic.A * abs(BP - self.reponse[j][0])
                    difMP += abs(MP - self.reponse[j][1])
                
                if difBP == 0 and difMP == 0 :
                    exists = False
                    for elements in eligible : 
                        if elements == self.popu[i] : 
                            exists = True   
                    if exists == False :
                        eligible.append(self.popu[i])
            h +=1
        if len(eligible) == 0 :
            print("Erreur")
            return -1

        bestguess = eligible[0]
        mostSimilarity = 0
        similarity = 0

        for elements in eligible :
            for elements2 in eligible :
                if (elements != elements2) :
                    BP,MP = self.jeu(elements2, elements)
                    similarity += BP + MP
                    if (similarity >= mostSimilarity) :
                        mostSimilarity = similarity
                        bestguess = elements
        return bestguess

    def DevGenetic(self) :
        NextGeneration = []
        fitnessarray =[]
        for i in range(Genetic.TaillePopu) :
            NextGeneration.append((''))
            fitnessarray.append(0)
        
        totalFitness = 0
        for i in range(Genetic.TaillePopu) :
                fitnessarray[i] = self.fitness(self.popu[i])
                totalFitness += fitnessarray[i]
        for i in range(Genetic.TaillePopu) :
            fitnessarray[i] = fitnessarray[i]/totalFitness
        
        fitnessarray = trifusion.tri_fusion(fitnessarray)

        totalFitness = 0
        for i in range(Genetic.TaillePopu) :
            totalFitness += fitnessarray[i]
            fitnessarray[i] = totalFitness

        fitnessarray[Genetic.TaillePopu -1 ] = 1

        for i in range(Genetic.TaillePopu) :
            randomNum = random.random()
            for j in range(Genetic.TaillePopu) :
                if fitnessarray[j] >= randomNum :
                    parent1 = self.popu[j]
                    break
            randomNum = random.random()
            for j in range(Genetic.TaillePopu) :
                if fitnessarray[j] >= randomNum :
                    parent2 = self.popu[j]
                    break
            
            if random.random() > .5 :
                children = self.onePointcrossover(parent1,parent2)
                if (self.TestCodeExist(NextGeneration, children)) :
                    self.addRandomCode(i, NextGeneration)
                else :
                    NextGeneration[i] = children
            else :
                children = self.twoPointCrossover(parent1,parent2)
                if (self.TestCodeExist(NextGeneration, children)) :
                    self.addRandomCode(i, NextGeneration)
                else :
                    NextGeneration[i] = children

        self.popu = NextGeneration

        self.Mix()
        self.mutation()
        self.permutation()
        self.inversion()

    def onePointcrossover(self, parent1, parent2) :
        point =random.randint(0, (self.positions-1))
        couleur = []
        for i in range(self.positions) : couleur.append(0)
        for i in range(self.positions) :
            if i < point :
                couleur[i] = parent1[i]
            else :
                couleur[i] = parent2[i]
        child = couleur
        return child

    def twoPointCrossover(self, parent1,parent2) :
        index1 = random.randint(0, (self.positions-1))
        index2 = random.randint(0, (self.positions-1))
        while index2 == index1 :
            index2 = random.randint(0, (self.positions-1))
        
        if index1 > index2 :
            t = index1
            index1 = index2
            index2 = t
        couleur = []
        for i in range(self.positions) : couleur.append(0)
        for i in range(self.positions) :
            if i <= index1 and i< index2 :
                couleur[i] = parent1[i]
            elif i > index1 and i <= index2 :
                couleur[i] = parent2[i]
            elif i > index1 and i > index2 :
                couleur[i] = parent1[i]

        child = couleur
        return child

    def mutation(self) :
        for i in range(Genetic.TaillePopu) :
            proba = random.randint(0,100)
            if proba <= 3 :
                index = random.randint(0, (self.positions-1))
                couleur = secrets.choice(self.CouleurPossible)
                nouveau =self.popu[i]
                nouveau[index] = couleur
                if self.TestCodeExist(self.popu, nouveau) : 
                    self.addRandomCode(i, self.popu)
                else :
                    self.popu[i][index] =  couleur

    def inversion(self) : 
        for i in range(Genetic.TaillePopu) :
            proba = random.randint(0,100)
            if proba <= 2 :
                new = self.popu[i]
                index1 = random.randint(0, (self.positions-1))
                index2 = random.randint(0, (self.positions-1))
                while index2 == index1 :
                    index2 = random.randint(0, (self.positions-1))
                if index1 > index2 :
                    t = index1
                    index1 = index2
                    index2 = t
                while index1 < index2 :
                    t = new[index1]
                    new[index1] = new[index2]
                    new[index2] = t
                    index1 += 1
                    index2 -= 1
                if self.TestCodeExist(self.popu, new) :
                    self.addRandomCode(i, self.popu)
                else : 
                    self.popu[i] = new

    def permutation(self) :
        for i in range(Genetic.TaillePopu) :
            proba = random.randint(0,100)
            if proba <= 3 :
                index1 = random.randint(0, (self.positions-1))
                index2 = random.randint(0, (self.positions-1))
                while index2 == index1 :
                    index2 = random.randint(0, (self.positions-1))
                new = self.popu[i]
                t = new[index1]
                new[index1] = new[index2]
                new[index2] =  t
                if self.TestCodeExist(self.popu, new) : 
                    self.addRandomCode(i, self.popu)
                else :
                    self.popu[i] = new
    
    def Mix(self) :
        for i in range(500) :
            index1 = random.randint(0,(len(self.popu) - 1)) 
            index2 = random.randint(0,(len(self.popu) - 1)) 
            while index2 == index1 :
                index2 = random.randint(0,(len(self.popu) - 1)) 
            try :
                t = self.popu[index1]
                self.popu[index1] = self.popu[index2]
                self.popu[index2] = t
            except :
                print(str(index1) + " exchange with " + str(index2) + "gone wrong")

    def fitness(self, test) :
        fitness = 0
        for i in range(self.TryNumber) :
            BP,MP = self.jeu(test, self.PrecedentTry[i])
            fitness += Genetic.A * abs(BP - self.reponse[i][0]) + abs(MP - self.reponse[i][1])
        fitness += Genetic.B * self.positions * (self.TryNumber)
        return fitness

    def jeu(self, essai, code) :
        #code = self.PrecedentTry(Nmbtest-1)
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


