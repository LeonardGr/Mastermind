import random
import Genetic

class MMCodebreaker :
    def __init__ (self,colors, positions) :
        self.responseList = []
        self.compte = 1
        self.couleurs = colors
        self.Nombrepositions = positions
        self.propositions = []
        self.propositions.append(self.PremiereProposition())
        self.actual_prop = self.propositions[(self.compte -1)]
        self.testGenetic = Genetic.Genetic(self.couleurs, self.Nombrepositions)


    def reponse(self, MP,BP) : 
        self.responseList.append((BP,MP))
        self.propositions.append(self.testGenetic.bestCode(self.compte, self.responseList, self.propositions))
        self.compte +=1
        self.actual_prop = self.propositions[self.compte -1]
        
    def NouvellePartie(self) : 
        self.responseList = []
        self.compte = 0
        propositions = []
        self.compte +=1
        self.propositions[self.compte-1] = self.PremiereProposition()
        self.actual_prop =self.propositions[self.compte-1]
    
    def nextMove(self) :
        return (self.actual_prop)


    def PremiereProposition (self) :
        code =[] 
        for i in range (self.Nombrepositions) :
            code.append(random.choice(self.couleurs))
        #print(code)
        return code
