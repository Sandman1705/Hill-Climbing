import sys
sys.path.insert(0, '../src')
import os
dir_name = os.path.dirname(sys.argv[0])
if(len(dir_name)!=0):
	os.chdir(os.path.dirname(sys.argv[0]))

import discrete_1d as hc


def main():

	test_array = hc.f_1d()
	maximum=max(test_array)

	result, iters = hc.discrete_hill_climbing_simple_1d(test_array, x0=10, step=5, max_iter=100, verbose=0)
	print("Path:",result, "\nNum of iterations:", iters, \
          "\nValue of found local optimum:", test_array[result[-1]], \
          "\nValue of global optimum:", maximum)
	hc.draw_discrete_1d_and_steps(test_array,result,save_png=True,filename="discrete_1d_e1")
	
	result, iters = hc.discrete_hill_climbing_simple_1d(test_array, x0=11, step=10, max_iter=100, verbose=0)
	print("Path:",result, "\nNum of iterations:", iters, \
          "\nValue of found local optimum:", test_array[result[-1]], \
          "\nValue of global optimum:", maximum)
	hc.draw_discrete_1d_and_steps(test_array,result,save_png=True,filename="discrete_1d_e2")

	result, iters = hc.discrete_hill_climbing_simple_1d(test_array, x0=11, step=20, max_iter=100, verbose=0)
	print("Path:",result, "\nNum of iterations:", iters, \
          "\nValue of found local optimum:", test_array[result[-1]], \
          "\nValue of global optimum:", maximum)
	hc.draw_discrete_1d_and_steps(test_array,result,save_png=True,filename="discrete_1d_e3")

#if __name__ == "__main__":
#	main()

main()