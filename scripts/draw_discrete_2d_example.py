import sys
sys.path.insert(0, '../src')
import os
dir_name = os.path.dirname(sys.argv[0])
if(len(dir_name)!=0):
	os.chdir(os.path.dirname(sys.argv[0]))

import discrete_2d as hc
import numpy as np

def main():

	test_matrix = np.array(hc.f_2d_int_hill(sizes=(20,20),max_value=0))
	result, iters = hc.discrete_hill_climbing_simple_2d_random_move(test_matrix,init_pos=(0,0),verbose=False,step=10)
	print("Num of steps:", len(result)-1, "Iterations:", iters, "Local optimum:", test_matrix[result[-1]], "Global optimum:", 0)
	hc.draw_2d_discrete_with_path(test_matrix,result,draw_steps=True,save_png=True,filename="discrete_2d_s20")
	
	test_matrix = np.array(hc.f_2d_int_hill(sizes=(50,50),max_value=0))
	result, iters = hc.discrete_hill_climbing_simple_2d_random_move(test_matrix,init_pos=(0,0),verbose=False,step=20,shuffle=False)
	print("Num of steps:", len(result)-1, "Iterations:", iters, "Local optimum:", test_matrix[result[-1]], "Global optimum:", 0)
	hc.draw_2d_discrete_with_path(test_matrix,result,draw_steps=True,save_png=True,filename="discrete_2d_s50")
	
	test_matrix = np.array(hc.f_2d_int_hill(sizes=(100,100),max_value=0))
	result, iters = hc.discrete_hill_climbing_simple_2d_random_move(test_matrix,init_pos=(0,0),verbose=False,step=50,shuffle=False)
	print("Num of steps:", len(result)-1, "Iterations:", iters, "Local optimum:", test_matrix[result[-1]], "Global optimum:", 0)
	hc.draw_2d_discrete_with_path(test_matrix,result,draw_steps=True,save_png=True,filename="discrete_2d_s100")

#if __name__ == "__main__":
#	main()

main()