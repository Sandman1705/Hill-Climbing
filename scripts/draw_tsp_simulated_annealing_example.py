import sys
sys.path.insert(0, '../src')
import os
dir_name = os.path.dirname(sys.argv[0])
if(len(dir_name)!=0):
	os.chdir(os.path.dirname(sys.argv[0]))

import tsp
import tsp_simulated_annealing as tsp_sa

import itertools
#from PIL import Image

def main():

	size = 50
	coords = tsp.random_coordinates(size)
	distances = tsp.euclid_distances(coords)
	evaluation = lambda t: tsp.tour_length(distances, t)
	init_func = lambda: tsp.random_tour(len(coords))

	result = tsp_sa.tsp_hillclimb_simulated_annealing_restart(init_func, evaluation, tsp.swapped_cities_generator,\
			 max_iterations=10000000, annealing_prob=tsp_sa.prob, annealing_temp=1.0, annealing_temp_decrease=0.95,\
			 restart_limit=10, verbose=1)

	print("Best evaluation:", result['best_eval'])
	print("Is local optimum:", result['local_optimum'])
	print("Num of evaluations:", result['num_of_evaluations'])
	print("Num of restarts:", result['num_of_restarts'])

	tsp.draw_tour(coords,result["best_tour"],img_file="tour_best_sa_swapping_cities.png")


	size = 50
	coords = tsp.random_coordinates(size)
	distances = tsp.euclid_distances(coords)
	evaluation = lambda t: tsp.tour_length(distances, t)
	init_func = lambda: tsp.random_tour(len(coords))

	result = tsp_sa.tsp_hillclimb_simulated_annealing_restart(init_func, evaluation, tsp.reversed_sections_generator,\
			 max_iterations=10000000, annealing_prob=tsp_sa.prob, annealing_temp=1.0, annealing_temp_decrease=0.95,\
			 restart_limit=10, verbose=1)

	print("Best evaluation:", result['best_eval'])
	print("Is local optimum:", result['local_optimum'])
	print("Num of evaluations:", result['num_of_evaluations'])
	print("Num of restarts:", result['num_of_restarts'])

	tsp.draw_tour(coords,result["best_tour"],img_file="tour_best_sa_reversing_sections.png")


#if __name__ == "__main__":
#	main()

main()