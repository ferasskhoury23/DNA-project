DNA-Project

We expect  inputs as follows:
	(1) json file that defines the shortmers, the keys should be with the format of (X1 , X2 , X3...) and sorted by order. the values is a sequence of DNA reads . all dna reads should have the same length.
	(2) .dna file that contains the sequence to simulate.
	
for now , the output you will get is :
	(1) a file that defines the alphabets as we generate it according to the shortmers we got from user.
	(2) output_sequence.josn : json file that has the simulation result as a json file . while the reads are described as the full sequences.
	(3) output_symbols.josn : json file that has the simulation result as a json file . while the reads are described as the symbols.


to run the simulation , change the path of the input files in the main.py file , and run it. the output files will be saved in the files dir.