DNA-Project

We expect  inputs as follows:
	(1) json file that defines the shortmers, the keys should be with the format of (X1 , X2 , X3...) and sorted by order. the values is a sequence of DNA reads .
	(2) dna file that contains the sequence.
	
The output you will get is :
	(1) files/alphabets.json : json file that defines the alphabets as we generate it according to the shortmers we got from user.
	(2) files/output_sequence_str.josn : json file that has the simulation result as a json file . while the reads are described as the full sequences.
	(3) files/output_symbols_str.josn : json file that has the simulation result as a json file . while the reads are described as the symbols.
	(4) files/out1put_statistics.json : The simulation stats  is written to json file.
	(5) files/output_errors_cluster.json : The clusters after planting the errors. 
	(6) files/final_result.json : The result of fixing the errors (by clusters).
	(7) files/result_strand.json : The final fixed strand.


to run the simulation , make sure you have the input files as described (you can use the input files , they are inside files dir) , change the path of your input files in the main.py file , and run it. the output files will be saved in the files dir.
 
