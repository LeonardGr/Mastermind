import random
import Genetic

class UseGA :
    def __init__ (self,colors, positions) :
        self.responseList = []
        self.couleurs = colors
        self.Nombrepositions = positions
        self.propositions = []
        self.propositions.append(self.PremiereProposition())
        self.actual_prop = self.propositions[-1]
        self.testGenetic = Genetic.Genetic(self.couleurs, self.Nombrepositions)
        
    def reponse(self, MP,BP) : 
        self.responseList.append((BP,MP))
        self.propositions.append(self.testGenetic.bestCode(len(self.propositions), self.responseList, self.propositions))
        self.actual_prop = self.propositions[-1]

    def PremiereProposition (self) :
        code =[] 
        for i in range (self.Nombrepositions) :
            code.append(random.choice(self.couleurs))
        return code
