import util
import random
import secrets
import itertools
import copy

class PSO :
    # paramètres globaux


    def __init__(self, couleurs, NbrePosition, NbreCluster, NbreAgent, Distmin, distmax, distpull,MaxGen ) :
        self.NbreCluster = NbreCluster
        self.NbreAgent = NbreAgent
        self.distmin = Distmin
        self.distmax = distmax
        self.distpull = distpull
        self.MaxGen = MaxGen
        self.CouleurPossible = list(couleurs)
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
    
    #Mutation d'un code, on change le code à l'index di, en modifiant la couleur à l'index di par une couleur aléatoire
    def mutation(self, code, di) :
        index = di
        couleur = secrets.choice(self.CouleurPossible)
        p=0
        nouveau = copy.copy(code)
        while self.valid[di][self.CouleurPossible.index(couleur)] == False and p <100 :
            p+=1
            couleur = secrets.choice(self.CouleurPossible)
        if p !=100 :
            nouveau[index] = couleur
        return nouveau
    
    #Permutation de deux couleurs dans un code
    def permutation(self, code, di, dj) :
        index1 = di
        index2 = dj
        new = copy.copy(code)
        t = new[index1]
        new[index1] = new[index2]
        new[index2] =  t
        return new

    #Permutation de trois couleurs dans un code en partant de l'odre di,dj,dk jusqu'à dk di dj
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
   
    #Permutation de trois couleurs dans un code en partant de l'odre di,dj,dk jusqu'à dj dk di
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
    
    # Pour un code, on effectue toute les mutations d'ordre 1 et on retourne celle ayant la meilleure fitness
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
   
    # Pour un code, on effectue toute les mutations d'ordre 2 et on retourne celle ayant la meilleure fitness
    def localfunction2(self,code) :
        fitness = self.fitness(code)
        bestcode = code
        pos = list(itertools.combinations(list(range(0,len(code))), 2))
        for i in range(len(pos)) :
            try :
                if self.valid[pos[i][0]][self.CouleurPossible.index(code[pos[i][1]])] == True and  self.valid[pos[i][1]][self.CouleurPossible.index(code[pos[i][0]])] == True: 
                    new = self.permutation(code,pos[i][0], pos[i][1])
                    f = self.fitness(new)
                    if f <= fitness :
                        fitness = f
                        bestcode = new
            except :
                pass
        return fitness, bestcode

        # Pour un code, on effectue toute les mutations d'ordre 2 et on retourne la meilleure
    
    # Pour un code, on effectue toute les mutations d'ordre 3 et on retourne celle ayant la meilleure fitness

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

    #Pour un certain code, nous allons appliquer successivement les différentes mutations jusqu'à en trouver une avec un fitness de 0 ou un minimum local
    def findbettercode(self, code) :
        fitness = self.fitness(code)
        Newfitness = 2
        localmin = 0
        while (localmin == 0 and Newfitness != 0) :
            Newfitness, bestcode = self.localfunction1(code)
            if Newfitness >= fitness :
                Newfitness, bestcode = self.localfunction2(code)
                if Newfitness >= fitness :
                    Newfitness, bestcode = self.localfunction3(code)
                    if Newfitness >= fitness :
                        localmin = 1
                    else :
                        fitness = Newfitness
                        code = bestcode
                else :
                    fitness = Newfitness
                    code = bestcode
            else :
                fitness = Newfitness
                code = bestcode
        return Newfitness, bestcode
    
    #Pour un certain code, nous allons retourner un code proche de celui ci, c'est à dire ayant effectué x mutations autour
    def disperse(self, code) :
        new = copy.copy(code)
        distance = random.randint(self.distmin, self.distmax)
        for i in range(distance) :
            value = random.random()
            if value < 0.5 : 
                index1 = random.randint(0, (self.positions-1))
                index2 = random.randint(0, (self.positions-1))
                p=0
                try :
                    while self.valid[index1][self.CouleurPossible.index(code[index2])] == False and  self.valid[index2][self.CouleurPossible.index(code[index1])] == False and p<100:
                        index1 = random.randint(0, (self.positions-1))
                        index2 = random.randint(0, (self.positions-1))
                        p+=1
                        while index2 == index1 :
                            index2 = random.randint(0, (self.positions-1))
                    if p!=100 : 
                        new = self.permutation(code, index1, index2)
                except  :
                    index1 = random.randint(0, (self.positions-1))
                    new = self.mutation(code, index1)
            else :
                index1 = random.randint(0, (self.positions-1))
                new = self.mutation(code, index1)
        return new

    #Nous allons rapprocher un code d'un second code cible, pour cela nous allons effectuer x mutations remplacant les couleurs du code original par les couleurs du code cible
    def pull(self, code1, cible) :
        new = copy.copy(code1)
        for i in range(self.distpull) :
            index = random.randint(0,self.positions-1) 
            p = 0   
            while self.valid[index][self.CouleurPossible.index(cible[index])] == False and p <100 :
                p+=1
                index = random.randint(0,self.positions-1)   
            if p!=100 :
                code1[index] = cible[index]


    #Création d'un ensemble de départ
    def createensemble(self) :
        for i in range (self.NbreCluster) :
            self.ensemble.append([])

        for i in range (self.NbreCluster) :
            new = util.gen(self.positions,self.CouleurPossible)
            while new in self.ensemble :
                new = util.gen(self.positions,self.CouleurPossible)
            self.ensemble[i].append(copy.copy(new))
            for j in range (1,self.NbreAgent) :
                new2 = self.disperse(self.ensemble[i][0])
                while new2 in self.ensemble[i] :
                    new2 = self.disperse(self.ensemble[i][0])
                self.ensemble[i].append(copy.copy(new2))

    #Recherche du meilleur code, nous allons parcourir l'entiereté des codes, trouver leur version optimal 
    # puis dans chaque cluster re répartir les codes autour du code ayant la meilleur fitness
    # Finalement, nous allons tirer l'ensemble des codes dans la direction de celui ayant la meilleur fitness

    def bestcode(self, Count, response, PrecedentTry) :
        #print("searching for best code")
        self.reponse = response
        self.TryNumber = Count 
        self.PrecedentTry = PrecedentTry
        bestFitness = 0
        h=0
        while (h < self.MaxGen) :
            fitarray=[]
            codearray = []
            for i in range (self.NbreCluster) :
                fitarray.append([])
                codearray.append([])
            bestFitness = 10^5
            #print("optimize each code")
            for i in range (self.NbreCluster) :
                for j in range (self.NbreAgent) :
                    Newfitness, code = self.findbettercode(self.ensemble[i][j])
                    fitarray[i].append(Newfitness)
                    codearray[i].append(code)

                    if Newfitness == 0 :
                        return code
                    if Newfitness < bestFitness :
                        bestFitness = Newfitness
                        bestcode = code
            
            #print("disperse from each best code")
            for i in range (self.NbreCluster) :
                #print("trying to find best code for cluster" + str(i))
                codemax = codearray[i][fitarray[i].index(min(fitarray[i]))]
                #print("find best code for cluster" + str(i))
                for j in range (self.NbreAgent) :
                    if self.ensemble[i][j] == codemax :
                        new = util.gen(self.positions,self.CouleurPossible)
                        p = 0
                        while new in self.ensemble[i] and p<10:
                            p+=1
                            new = util.gen(self.positions,self.CouleurPossible)
                        self.ensemble[i][j] = copy.copy(new)
                    else : 
                        #print("dispsere code n°" + str(j) + str(self.ensemble[i][j])+ " from code " + str(codemax))
                        new2 = self.disperse(codemax)
                        p = 0
                        while new2 in self.ensemble[i] and p <10 :
                            p+=1
                            new2 = self.disperse(codemax)
                        self.ensemble[i][j] = copy.copy(new2)

            #print("pull from best code")
            for i in range (self.NbreCluster) :
                for j in range (self.NbreAgent) :
                    self.pull(self.ensemble[i][j], bestcode)
            h +=1
        return bestcode


    # Nous allons update l'ensemble des matrices des codes possibles
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
                    if self.CouleurPossible[j] not in code :
                        self.valid[i][j] = False

    #Permet de vérifier si un code est éligible
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



