import util
import random
import secrets
import itertools
import copy

class PSO :
    # paramètres globaux
    NbreCluster = 10
    NbreAgent = 10
    distmin = 2
    distmax = 4
    distpull = 2



    def __init__(self, couleurs, NbrePosition ) :
        self.CouleurPossible = couleurs
        self.ensemble = []
        self.reponse = []
        self.valid = [[(True) for i in range(len(self.CouleurPossible))]for i in range(NbrePosition)]
        self.PrecedentTry = []
        self.TryNumber = 0
        self.positions = NbrePosition
        self.createensemble()
    

    def evaluation(self, test, i ) :
        BP,MP = util.compare(test, self.PrecedentTry[i])
        #e = abs(self.score(self.reponse[i][0],self.reponse[i][1]) - self.score(BP,MP)) + Genetic.B * i
        e = abs(self.reponse[i][0] - BP) + abs(self.reponse[i][1] - MP) 
        return e



    # Calcul du fitness, taux de probabilité d'être le code, donc en fonction de BP et MP commun avec ceux testés, que l'on pondère par le nombre de test
    def fitness(self, test) :
        fitness = 0
        for i in range(self.TryNumber) :
            fitness += self.evaluation(test, i)
        return fitness
    
    def mutation(self, code, di) :
        index = di
        couleur = secrets.choice(self.CouleurPossible)
        while self.valid[di][self.CouleurPossible.index(couleur)] == False :
            couleur = secrets.choice(self.CouleurPossible)
        nouveau = copy.copy(code)
        nouveau[index] = couleur
        return nouveau
    
    def permutation(self, code, di, dj) :
        index1 = di
        index2 = dj
        new = copy.copy(code)
        t = new[index1]
        new[index1] = new[index2]
        new[index2] =  t
        return new

    def triswap1(self, code, di, dj, dk) :
        index1 = di
        index2 = dj
        index3 = dk
        new = copy.copy(code)
        if self.valid[di][self.CouleurPossible.index(code[dk])] == True and  self.valid[dj][self.CouleurPossible.index(code[di])] == True and self.valid[dk][self.CouleurPossible.index(code[dj])] == True: 
            t1 = new[index1]
            t2 = new[index2]
            new[index1] = new[index3] 
            new[index2] = t1
            new[index3] = t2
        return new
    def triswap2(self, code, di, dj, dk) :
        index1 = di
        index2 = dj
        index3 = dk
        new = copy.copy(code)
        if self.valid[di][self.CouleurPossible.index(code[dj])] == True and  self.valid[dj][self.CouleurPossible.index(code[dk])] == True and self.valid[dk][self.CouleurPossible.index(code[di])] == True: 
            t1 = new[index1]
            t2 = new[index2]
            new[index1] = t2
            new[index2] = new[index3]
            new[index3] = t1
        return new
    def localfunction1(self,code) :
        fitness = self.fitness(code)
        bestcode = code
        for i in range(self.positions) :
            new = self.mutation(code,i)
            f = self.fitness(new)
            if f < fitness :
                fitness = f
                bestcode = new
        return fitness, bestcode

    def localfunction2(self,code) :
        fitness = self.fitness(code)
        bestcode = code
        pos = list(itertools.combinations(list(range(0,len(code))), 2))
        for i in range(len(pos)) :
            if self.valid[pos[i][0]][self.CouleurPossible.index(code[pos[i][1]])] == True and  self.valid[pos[i][1]][self.CouleurPossible.index(code[pos[i][0]])] == True: 
                new = self.permutation(code,pos[i][0], pos[i][1])
                f = self.fitness(new)
                if f <= fitness :
                    fitness = f
                    bestcode = new
        return fitness, bestcode

    def localfunction3(self,code) :
        fitness = self.fitness(code)
        bestcode = code
        pos = list(itertools.combinations(list(range(0,len(code))), 3))
        for i in range(len(pos)) :
            new = self.triswap1(code,pos[i][0], pos[i][1], pos[i][2])
            f = self.fitness(new)
            if f <= fitness :
                fitness = f
                bestcode = new
            new = self.triswap2(code,pos[i][0], pos[i][1], pos[i][2])
            f = self.fitness(new)
            if f <= fitness :
                fitness = f
                bestcode = new
        return fitness, bestcode

    def findbettercode(self, code) :
        fitness = self.fitness(code)
        Newfitness = 0
        localmin = 0
        while localmin == 0 :
            Newfitness, bestcode = self.localfunction1(code)
            if Newfitness >= fitness :
                Newfitness, bestcode = self.localfunction2(code)
                if Newfitness >= fitness :
                    Newfitness, bestcode = self.localfunction3(code)
                    if Newfitness >= fitness :
                        localmin = 1
        return Newfitness, bestcode
    
    def disperse(self, code) :
        distance = random.randint(PSO.distmin, PSO.distmax)
        for i in range(distance) :
            value = random.random()
            if value < 0.5 : 
                index1 = random.randint(0, (self.positions-1))
                index2 = random.randint(0, (self.positions-1))
                while self.valid[index1][self.CouleurPossible.index(code[index2])] == False and  self.valid[index2][self.CouleurPossible.index(code[index1])] == False:
                    index1 = random.randint(0, (self.positions-1))
                    index2 = random.randint(0, (self.positions-1))
                    while index2 == index1 :
                        index2 = random.randint(0, (self.positions-1))
                new = self.permutation(code, index1, index2)
            else :
                index1 = random.randint(0, (self.positions-1))
                new = self.mutation(code, index1)
        return new

    def pull(self, code1, cible) :
        new = copy.copy(code1)
        for i in range(PSO.distpull) :
            index = random.randint(0,self.positions)    
            while self.valid[index][self.CouleurPossible.index(cible[index])] == False :
                index = random.randint(0,self.positions)    
            code1[index] = cible[index]

    def createensemble(self) :
        for i in range (PSO.NbreCluster) :
            self.ensemble.append([])

        for i in range (PSO.NbreCluster) :
            new = util.gen(self.positions,self.CouleurPossible)
            while new in self.ensemble :
                new = util.gen(self.positions,self.CouleurPossible)
            self.ensemble[i].append(copy.copy(new))
            for j in range (1,PSO.NbreAgent) :
                new2 = self.disperse(self.ensemble[i][0])
                while new2 in self.ensemble[i] :
                    new2 = self.disperse(self.ensemble[i][0])
                self.ensemble[i].append(copy.copy(new2))

    def bestcode(self, Count, response, PrecedentTry) :
        self.reponse = response
        self.TryNumber = Count 
        self.PrecedentTry = PrecedentTry
        bestFitness = 0
        Fitnessancient = 10
        while (bestFitness < Fitnessancient) :
            Fitnessancient = bestFitness
            fitarray=[]
            codearray = []
            for i in range (PSO.NbreCluster) :
                fitarray.append([])
                codearray.append([])
            bestFitness = 10^5
            for i in range (PSO.NbreCluster) :
                for j in range (PSO.NbreAgent) :
                    Newfitness, code = self.findbettercode(self.ensemble[i][j])
                    fitarray[i].append(Newfitness)
                    codearray[i].append(code)

                    if Newfitness == 0 :
                        return code
                    if Newfitness < bestFitness :
                        bestFitness = Newfitness
                        bestcode = code
            for i in range (PSO.NbreCluster) :
                codemax = codearray(fitarray.index(min(fitarray)))
                for j in range (PSO.NbreAgent) :
                    if self.ensemble[i][j] == codemax :
                        new = util.gen(self.positions,self.CouleurPossible)
                        while new in self.ensemble :
                            new = util.gen(self.positions,self.CouleurPossible)
                        self.ensemble[i][j] = copy.copy(new)
                    else : 
                        new2 = self.disperse(codemax)
                        while new2 in self.ensemble[i] :
                            new2 = self.disperse(codemax)
                        self.ensemble[i][j] = copy.copy(new2)

            for i in range (PSO.NbreCluster) :
                for j in range (PSO.NbreAgent) :
                    self.pull(self.ensemble[i][j], bestcode)
        return bestcode
    def updatevalid(self, code, BP, MP) :
        if BP == 0 and MP == 0 :
            for i in range(self.positions) :
                index = self.CouleurPossible.index(code[i])
                for j in range(self.positions) :
                    self.valid[j][index] = False
        elif BP == 0 :
            for i in range(self.positions) :
                self.valid[i][self.CouleurPossible.index(code[i])] = False
        elif BP+MP == self.positions :
            for i in range(self.positions) :
                for j in range(len(self.CouleurPossible)) :
                    if self.CouleurPossible[i] not in code :
                        self.valid[i][j] = False

    def checkifvalid (self, code) :
        for index, color in enumerate(code) :
            if self.valid[index][self.CouleurPossible.index(color)] == False :
                return False
        return True




#Todo :
# Générer premier code :
# Trouver meilleur code :
# Avoir réponse :
# Update valid :
# Trouver meilleur code



