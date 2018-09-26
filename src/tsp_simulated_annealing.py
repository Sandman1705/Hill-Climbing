import random
import math

#import tsp

def prob(curr_eval,next_eval,temp):
	if next_eval < curr_eval:
		return 1.0
	else:
		if temp < 1e-64: #failsafe for low temp
			return 0.0
		return math.exp( -abs(next_eval-curr_eval)/temp )


def tsp_hillclimb_simulated_annealing(init,evaluation_function,next_generator,max_iterations=1000,\
									  annealing_prob=prob,annealing_temp=1.0,annealing_temp_decrease=0.95,\
									  verbose=0):

	curr_tour = init
	curr_eval = evaluation_function(curr_tour)
	curr_temp = annealing_temp

	curr_iter = 0
	num_of_nexts = 0
	num_of_worse_nexts = 0
	local_optimum = False
	while curr_iter<max_iterations:

		changed_tour = False
		exceeded_iterations = False
		i=0
		for next_tour in next_generator(curr_tour):
			if verbose>=3:
				print("iteration:",curr_iter)
			curr_iter += 1
			i=i+1
			next_eval = evaluation_function(next_tour)
			r = random.random()
			p = prob(curr_eval,next_eval,curr_temp)
			if r<p:
				if verbose>=3:
					print("changed tour after", i)
				if (next_eval>=curr_eval):
					num_of_worse_nexts += 1
					#print("taken worse on iter:", curr_iter, curr_temp, p)
				changed_tour = True
				num_of_nexts += 1
				curr_eval = next_eval
				curr_tour = next_tour
				curr_temp = curr_temp*annealing_temp_decrease
				break
			if curr_iter>max_iterations:
				exceeded_iterations = True
				if verbose>=2:
					print("inner max iterations")
				break

		if not exceeded_iterations and not changed_tour:
			local_optimum = True
			if verbose>=2:
				print("local optimum")
			break

	result = {}
	result["num_of_evaluations"] = curr_iter
	result["best_tour"] = curr_tour
	result["best_eval"] = curr_eval
	result["num_of_nexts"] = num_of_nexts
	result["num_of_worse_nexts"] = num_of_worse_nexts
	result["local_optimum"] = local_optimum
	return result

def tsp_hillclimb_simulated_annealing_restart(init_function,evaluation_function,next_generator,max_iterations=1000000,\
											  annealing_prob=prob,annealing_temp=1.0,annealing_temp_decrease=0.95,\
											  restart_limit=None,verbose=0):

	curr_tour = None
	curr_eval = float("inf")
	curr_lo = False
	curr_nn = 0

	curr_iter = 0
	i=0
	while curr_iter < max_iterations and (restart_limit is None or i<restart_limit):
		if verbose>=1:
			print("restart", i)
		i+=1

		init_tour = init_function()

		result = tsp_hillclimb_simulated_annealing(init=init_tour, evaluation_function=evaluation_function, \
					 next_generator=next_generator, max_iterations=max_iterations-curr_iter, \
					 annealing_prob=annealing_prob, annealing_temp=annealing_temp,\
					 annealing_temp_decrease=annealing_temp_decrease, verbose=verbose)

		curr_iter += result["num_of_evaluations"]

		if verbose>=1:
			print("result eval:", result["best_eval"], "num_of_nexts:", result["num_of_nexts"], "num_of_iterations:", curr_iter)
		if result["best_eval"] < curr_eval or curr_tour is None:
			if verbose>=1:
				print("new best")
			curr_tour = result["best_tour"]
			curr_eval = result["best_eval"]
			curr_lo = result["local_optimum"]
			curr_nn = result["num_of_nexts"]

	final_result = {}
	final_result["best_tour"] = curr_tour
	final_result["best_eval"] = curr_eval
	final_result["num_of_evaluations"] = curr_iter
	final_result["local_optimum"] = curr_lo
	final_result["num_of_nexts"] = curr_nn
	final_result["num_of_restarts"] = i

	return final_result
