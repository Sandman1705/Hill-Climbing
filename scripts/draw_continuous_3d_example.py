import sys
sys.path.insert(0, '../src')
import os
dir_name = os.path.dirname(sys.argv[0])
if(len(dir_name)!=0):
	os.chdir(os.path.dirname(sys.argv[0]))

import continuous_3d as hc
import numpy as np

def draw_imshow(func,init=(0.0,0.0),filename="continuous_3d_imshow_steps"):
	result, iters = hc.continious_hill_climbing_simple_3d_random_move(func,init=init,max_iter=1000,verbose=0)
	print("Steps taken:", len(result)-1)
	print("Num of iterations:", iters)
	print("Local optimum:", func(result[-1][0], result[-1][1]))
	#print("Global optimum:", func(0,0))
	hc.draw_graph_3d_as_imshow_with_path(func, result, cmap='terrain', interpolation='bilinear', scatter_all=True, save_png=True, filename=filename)
	
def draw_imshow_multi(func,filename="continuous_3d_imshow_multi_steps"):
	all_results, best_results, iters = hc.continious_hill_climbing_restarting_3d(func, max_iter=10000, max_restarts=12)
	print("Steps taken for best:", len(best_results)-1)
	print("Num of iterations:", iters)
	print("Num of results:", len(all_results))
	print("Local optimum:", func(best_results[-1][0], best_results[-1][1]))
	#print("Global optimum:", func(0,0))
	hc.draw_graph_3d_as_imshow_with_multi_paths(func, paths=all_results, best_path=best_results, cmap='terrain', interpolation='bilinear', save_png=True, filename=filename)

def main():

	draw_imshow(hc.f,init=(5.3,6.82),filename="continuous_3d_imshow_steps_1")
	draw_imshow(hc.f2,init=(5.3,6.82),filename="continuous_3d_imshow_steps_2")
	draw_imshow(hc.ripple,init=(0.0,0.0),filename="continuous_3d_imshow_steps_3_ripple")
	draw_imshow(lambda x,y: hc.ripple(x,y,ripple_spread=0.1),init=(0.0,0.0),filename="continuous_3d_imshow_steps_4_ripple_2")
	draw_imshow(lambda x,y: hc.bumps(x,y,bump_effect=0.5),init=(-4.12,3.12),filename="continuous_3d_imshow_steps_5_bumps")
	draw_imshow(lambda x,y: hc.top_hat(x,y,hat_spread=10),init=(9.0,9.0),filename="continuous_3d_imshow_steps_6_top_hat")
	draw_imshow(hc.pyramid,init=(9.1,9.1),filename="continuous_3d_imshow_steps_7_pyramid")

	draw_imshow_multi(lambda x,y: hc.bumps(x,y,bump_effect=0.5),filename="continuous_3d_imshow_steps_8_multi_bumps")
	draw_imshow_multi(hc.pyramid,filename="continuous_3d_imshow_steps_9_multi_pyramid")
	


#if __name__ == "__main__":
#	main()

main()