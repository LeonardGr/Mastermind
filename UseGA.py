import random
import Genetic

#Classe pour deviner un code en utilisant un algorithme génétique
class UseGA :
    def __init__ (self,colors, positions) :
        self.responseList = []
        self.couleurs = colors
        self.Nombrepositions = positions
        self.propositions = []
        self.propositions.append(self.PremiereProposition())
        self.actual_prop = self.propositions[-1]
        self.testGenetic = Genetic.Genetic(self.couleurs, self.Nombrepositions)
    #En fonction des BP, MP qu'on vient d'obtenir, on les ajoute à notre liste de réponse et on utilise le GA pour avoir la meilleure réponse possible  
    def reponse(self, MP,BP) : 
        self.responseList.append((BP,MP))
        self.propositions.append(self.testGenetic.bestCode(len(self.propositions), self.responseList, self.propositions))
        self.actual_prop = self.propositions[-1]

    # Genere un code aléatoire pour le premier test
    def PremiereProposition (self) :
        code =[] 
        for i in range (self.Nombrepositions) :
            code.append(random.choice(self.couleurs))
        return code