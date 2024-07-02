import random
import itertools
from itertools import combinations
from math import comb




#comb(n,k)  n b7ar k (n nCr k) returns the number itself
#combinations returns the whole combinations


class shortMers:
    dna_components = ['A', 'C', 'G', 'T']


    def __init__(self , length_of_shortmer , numberOfSet , length_of_sequences):
        self.length_of_shortmer = length_of_shortmer
        self.shortmers = []
        #self.letters = []
        self.numberOfSet = numberOfSet
        self.lengthOfSequences = length_of_sequences


    def generate_shortmers(self):
        """
        Generates all possible combinations of shortmers of a given length.
        """
        return [''.join(p) for p in itertools.product(shortMers.dna_components, repeat=self.length_of_shortmer)]

    def generate_random_set_of_shortmers(self):
        all_combination = self.generate_shortmers()
        self.shortmers = random.sample(all_combination , self.numberOfSet) #return a list of shortmers
        return self.shortmers

    def generate_all_combinations_of_sequences(self):
        return [''.join(p) for p in itertools.product(self.shortmers, repeat=self.lengthOfSequences)]


if __name__ == "__main__" :
    param1 = 3
    param2 = 16
    param3 = 5
    shortmers = shortMers(param1 , param2 , param3)
    listOfShortmers = shortmers.generate_shortmers()
    smair = shortmers.generate_all_combinations_of_sequences()
    print(len(smair))
    print(listOfShortmers)
    print(len(listOfShortmers))
    print("////////////////")
    #print(shortmers.generate_random_set_of_shortmers())
    print("////////////////")
    #print(len(shortmers.generate_all_combinations_of_sequences()))
