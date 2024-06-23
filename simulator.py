import random
import itertools

class shortMers:
    dna_components = ['A', 'C', 'G', 'T']


    def _init_(self, length_of_shortmer,numberOfSet):
        self.length_of_shortmer = length_of_shortmer
        #self.shortmers = []
        #self.letters = []
        self.numberOfSet = numberOfSet


    def generate_all_combinations_of_shortmers(self):
        """
        Generates all possible combinations of shortmers of a given length.
        """
        return [''.join(p) for p in itertools.product(shortMers.dna_components, repeat=self.length_of_shortmer)]

    def generate_random_set_of_shortmers(self):
        all_combination = self.generate_all_combinations_of_shortmers()
        selected_shortmers = random.sample(all_combination,self.numberOfSet) #return a list of shortmers
        return selected_shortmers



if _name_ == "_main_":
    param1 = 3
    param2 = 16
    shortmers = shortMers(param1,param2)
    print(shortmers.generate_all_combinations_of_shortmers())
    print("////////////////")
    print(shortmers.generate_random_set_of_shortmers())