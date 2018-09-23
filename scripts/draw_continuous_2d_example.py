import sys
sys.path.insert(0, '../src')
import os
dir_name = os.path.dirname(sys.argv[0])
if(len(dir_name)!=0):
	os.chdir(os.path.dirname(sys.argv[0]))

import continuous_2d as hc
import numpy as np

def main():

	result, iters = hc.continious_hill_climbing_simple_2d_random_move(hc.f,init_pos=-7.125, max_iter=1000, verbose=0)
	print("Steps taken:", len(result)-1)
	print("Num of iterations:", iters)
	print("Local optimum:", hc.f(result[-1]))
	print("Global optimum:", hc.f(3.1))
	hc.draw_graph_2d_and_steps(hc.f,result,save_png=True,filename="continious_2d_f")

	result, iters = hc.continious_hill_climbing_simple_2d_random_move(hc.f2,init_pos=-1.125, max_iter=1000, verbose=0)
	print("Steps taken:", len(result)-1)
	print("Num of iterations:", iters)
	print("Local optimum:", hc.f(result[-1]))
	print("Global optimum (~):", hc.f(9.79771))
	hc.draw_graph_2d_and_steps(hc.f2,result,save_png=True,filename="continious_2d_f2_local")

	result, iters = hc.continious_hill_climbing_simple_2d_random_move(hc.f2,init_pos=1.125, max_iter=1000, verbose=0)
	print("Steps taken:", len(result)-1)
	print("Num of iterations:", iters)
	print("Local optimum:", hc.f(result[-1]))
	print("Global optimum (~):", hc.f(9.79771))
	hc.draw_graph_2d_and_steps(hc.f2,result,save_png=True,filename="continious_2d_f2_global")


#if __name__ == "__main__":
#	main()

main()