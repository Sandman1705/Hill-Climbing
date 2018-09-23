import sys
sys.path.insert(0, '../src')
import os
dir_name = os.path.dirname(sys.argv[0])
if(len(dir_name)!=0):
	os.chdir(os.path.dirname(sys.argv[0]))

import tsp

import itertools
#from PIL import Image

def main():

	size = 100
	coords = tsp.random_coordinates(size)
	distances = tsp.euclid_distances(coords)
	evaluation = lambda t: tsp.tour_length(distances, t)
	init_func = lambda: tsp.random_tour(len(coords))
	
	result = tsp.tsp_hillclimb_restart_overall_iterations(init_func,evaluation,tsp.swapped_cities_generator,\
                                                  max_iterations=100000,restart_limit=None,verbose=0)
												  
	print("Best evaluation:", result['best_eval'])
	print("Is local optimum:", result['local_optimum'])
	print("Num of evaluations:", result['num_of_evaluations'])
	print("Num of restarts:", result['num_of_restarts'])
	
	tsp.draw_tour(coords,result["best_tour"],img_file="tour_best_swapping_cities.png")
	
	
	size = 100
	coords = tsp.random_coordinates(size)
	distances = tsp.euclid_distances(coords)
	evaluation = lambda t: tsp.tour_length(distances, t)
	init_func = lambda: tsp.random_tour(len(coords))
	
	result = tsp.tsp_hillclimb_restart_overall_iterations(init_func,evaluation,tsp.reversed_sections_generator,\
                                                  max_iterations=100000,restart_limit=None,verbose=0)
												  
	print("Best evaluation:", result['best_eval'])
	print("Is local optimum:", result['local_optimum'])
	print("Num of evaluations:", result['num_of_evaluations'])
	print("Num of restarts:", result['num_of_restarts'])
	
	tsp.draw_tour(coords,result["best_tour"],img_file="tour_best_reversing_sections.png")


#if __name__ == "__main__":
#	main()

main()