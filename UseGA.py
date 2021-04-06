import random
import GeneticTrue

#Classe pour deviner un code en utilisant un algorithme génétique
class UseGA :
    def __init__ (self,colors, positions, ponderation, depart, pourcentage, TailleEligible, TaillePopu, NombreGen) :
        self.responseList = []
        self.couleurs = colors
        self.Nombrepositions = positions
        self.propositions = []
        if depart == 0 :
            self.propositions.append(self.PremiereProposition())
        else :
            self.propositions.append(self.PremierePropositionTest())
        self.actual_prop = self.propositions[-1]
        self.testGenetic = GeneticTrue.Genetic(self.couleurs, self.Nombrepositions, ponderation, pourcentage, TailleEligible, TaillePopu, NombreGen)
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

    def PremierePropositionTest (self) :
        code =[] 
        for i in range (self.Nombrepositions) :
            if i <(self.Nombrepositions/2) :
                code.append(self.couleurs[0])
            else : 
                code.append(self.couleurs[1])
        return code

