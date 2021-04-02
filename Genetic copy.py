import random
import secrets
import util

class Genetic :
    # paramètres globaux
    TaillePopu = 150 
    MaxGen = 100
    MaxSize = 60
    A = 1 # poids des MP
    B = 2 #poids des BP

    def __init__(self, couleurs, NbrePosition ) :
        self.CouleurPossible = couleurs
        self.popu = []
        self.reponse = []
        self.PrecedentTry = []
        self.TryNumber = 0
        self.positions = NbrePosition
        self.CreateGenetic(self.CouleurPossible)
    
    #Verification qu'un code exist dans un ensemble
    def TestCodeExist(self, ensemble, test) :
        if len(ensemble) != 0 :
            if test in ensemble :
                return True 
            else :
                return False
    # crée un code aléatoire et l'insere dans l'ensemble à l'indice donnée
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
    # crée une population aléatoire de taille TaillePopu
    def CreateGenetic(self, couleurs) :
        self.CouleurPossible = couleurs
        self.popu = []
        for i in range(Genetic.TaillePopu) :
            self.addRandomCode(i, self.popu)
        
    #Choisi le meilleur code dans la population
    #Pour cela on fait se développer la population, puis on sélectionne ceux pouvant être le code(BP ou MP égaux), et on en choisit un aléatoire dedans
    def bestCode(self, Count, response, PrecedentTry) :
        self.reponse = response
        self.TryNumber = Count 
        self.PrecedentTry = PrecedentTry

        h = 1
        eligible = []
        A = 1
        B = 2
        #On fait se développer la population tant que l'on a pas assez d'evenement éligible
        while(h <= Genetic.MaxGen and len(eligible)<=Genetic.MaxSize) :
            self.DevGenetic()
            for i in range(Genetic.TaillePopu) :
                difBP = 0
                difMP = 0
                dif = self.fitness(self.popu[i])

                """ for j in range(len(self.PrecedentTry)) : 
                    BP,MP = util.compare(self.PrecedentTry[j], self.popu[i])
                    difBP += Genetic.A * abs(BP - self.reponse[j][0])
                    difMP += abs(MP - self.reponse[j][1])
                
                if difBP == 0 and difMP == 0 : """
                if dif == 0 :
                    if self.TestCodeExist(eligible, self.popu[i]) == False : 

                        """ exists = False
                        for elements in eligible : 
                            if elements == self.popu[i] : 
                                exists = True   
                        if exists == False : """

                        eligible.append(self.popu[i])
            h +=1

        for i in range(len(eligible)) :
            if self.TestCodeExist(self.popu, eligible[i]) == False : 
                index = random.randint(0,len(self.popu))
                self.popu[index] = eligible[i]


        bestguess = eligible[0]
        mostSimilarity = 0
        similarity = 0
        # On choisit celui le plus semblable au code de base
        for elements in eligible :
            for elements2 in eligible :
                if (elements != elements2) :
                    BP,MP = util.compare(elements2, elements)
                    similarity += BP + MP
                    if (similarity >= mostSimilarity) :
                        mostSimilarity = similarity
                        bestguess = elements
        return bestguess


    # developpement de la population, on classe les membres selon leur fitness(probabilité d'être le code), on en choisit 2, on en tire un enfant
    # l'enfant est soi moitié père moitié mère soit il y a 2 points de rotation
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
        
        fitnessarray = util.tri_fusion(fitnessarray)

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
                children = self.SwitchOnePoint(parent1,parent2)
                if (self.TestCodeExist(NextGeneration, children)) :
                    self.addRandomCode(i, NextGeneration)
                else :
                    NextGeneration[i] = children
            else :
                children = self.SwitchTwoPoint(parent1,parent2)
                if (self.TestCodeExist(NextGeneration, children)) :
                    self.addRandomCode(i, NextGeneration)
                else :
                    NextGeneration[i] = children

        self.popu = NextGeneration

        # On finit par mélanger notre population puis on effectue diverses mutations
        #self.Mix()
        self.mutation()
        self.permutation()
        self.inversion()

    # fonction pour faire un enfant moitié père moité mère
    def SwitchOnePoint(self, parent1, parent2) :
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

    # fonction pour faire 2 points de rotation père/mère
    def SwitchTwoPoint(self, parent1,parent2) :
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

    # Mutation propable à 2%, on change une couleur à un emplacement aléatoire d'un code
    def mutation(self) :
        for i in range(Genetic.TaillePopu) :
            proba = random.randint(0,100)
            if proba <= 2 :
                index = random.randint(0, (self.positions-1))
                couleur = secrets.choice(self.CouleurPossible)
                nouveau =self.popu[i]
                nouveau[index] = couleur
                if self.TestCodeExist(self.popu, nouveau) : 
                    self.addRandomCode(i, self.popu)
                else :
                    self.popu[i][index] =  couleur

    # Mutation probable à 2%, on inverse de place le sens d'un code à partir d'un index
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
    # mutation probable à 2%, on inverse deux couleurs d'un code
    def permutation(self) :
        for i in range(Genetic.TaillePopu) :
            proba = random.randint(0,100)
            if proba <= 2 :
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

    """     #On mélange la population
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
                print(str(index1) + " exchange with " + str(index2) + "gone wrong") """

    def evaluation(self, test, i ) :
        BP,MP = util.compare(test, self.PrecedentTry[i])
        #e = abs(self.score(self.reponse[i][0],self.reponse[i][1]) - self.score(BP,MP)) + Genetic.B * i
        e = abs(self.score(self.reponse[i][0],self.reponse[i][1]) - self.score(BP,MP)) 
        return e

    def score(self,BP,MP) :
        e = 2*BP + MP
        return e

    # Calcul du fitness, taux de probabilité d'être le code, donc en fonction de BP et MP commun avec ceux testés, que l'on pondère par le nombre de test
    def fitness(self, test) :
        fitness = 0
        for i in range(self.TryNumber) :
            fitness += self.evaluation(test, i)
            #BP,MP = util.compare(test, self.PrecedentTry[i])
            #fitness += Genetic.A * abs(BP - self.reponse[i][0]) + abs(MP - self.reponse[i][1])
        #fitness += Genetic.B * self.positions * (self.TryNumber)
        return fitness

    #Fonction permettant de calculer les MP/BP
    """ def jeu(self, essai, code) :
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
        return(BP,MP) """


