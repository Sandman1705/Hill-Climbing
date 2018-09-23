import numpy as np
from matplotlib import pyplot as plt
import random

#Example functions
def f(x): #global maximum x=3.1
	return -((x-3.1)**2)

def f2(x): #global maximum x~=9.79771
	return -((0.75*x+5.5)**2)*((0.1*x-0.95)**2)+x

def draw_graph_2d(f,x_points=np.linspace(-11,11,46),show=False,save_png=False,save_pdf=False,filename="continuous_2d"):
	y_points = [f(x) for x in x_points]
	plt.plot(x_points,y_points)
	if show:
		plt.show()
	if save_png:
		plt.savefig(filename+".png")
		print("Graph saved to:", filename+".png")
	if save_pdf:
		plt.savefig(filename+".pdf", bbox_inches='tight')
		print("Graph saved to:", filename+".pdf")
	plt.gcf().clear()

def draw_graph_2d_and_steps(f,x_steps,x_points=np.linspace(-11,11,46),show=False,\
							save_png=False,save_pdf=False,filename="continuous_2d_steps"):
	y_points = [f(x) for x in x_points]
	y_steps = [f(x) for x in x_steps]
	plt.plot(x_points,y_points,color='teal')
	plt.plot(x_steps,y_steps,color='blue')
	plt.scatter(x_steps,y_steps,color='orange')
	plt.scatter(x_steps[0],y_steps[0],color='green')
	plt.scatter(x_steps[-1],y_steps[-1],color='red')
	#plt.xlim(xmin=-10, xmax=10)
	if show:
		plt.show()
	if save_png:
		plt.savefig(filename+".png")
		print("Graph saved to:", filename+".png")
	if save_pdf:
		plt.savefig(filename+".pdf", bbox_inches='tight')
		print("Graph saved to:", filename+".pdf")
	plt.gcf().clear()


def random_pos(left, right):
	return np.random.rand() * (right-left) + left


def continious_hill_climbing_simple_2d_best_move(f,init_pos=0.0,max_iter=None,step=1.0,step_decrease=2.0,\
												 min_step=0.000001,x_range=(-10,10), verbose=0):
	curr_x = init_pos
	curr_eval = f(curr_x)
	x_steps = [curr_x]
	curr_iter = 0
	while True:
		if (max_iter is not None and curr_iter>max_iter):
			if verbose>=1:
				print("reached max_iter:",max_iter)
			return x_steps
		if verbose>=2:
			print("iter:",curr_iter)
		neighbours = [ x for x in [curr_x + step, curr_x - step] if (x>x_range[0] and x<x_range[1]) ]
		random.shuffle(neighbours)
		next_eval = float("-inf")
		next_x = None
		for n in neighbours:
			n_eval = f(n)
			if (n_eval > next_eval):
				next_eval = n_eval
				next_x = n

		if (next_eval < curr_eval):
			step = step / step_decrease
			if verbose>=1:
				print("step decreased to", step)
			if (step<min_step):
				if verbose>=1:
					print("min step reached")
				return x_steps
		else:
			x_steps.append(next_x)
			curr_x = next_x
			curr_eval = next_eval
		curr_iter = curr_iter + 1


def continious_hill_climbing_simple_2d_random_move(f,init_pos=0.0,max_iter=None,step=1.0,step_decrease=2.0,\
												   min_step=0.000001,x_range=(-10,10), verbose=0, shuffle=True):
	curr_x = init_pos
	curr_eval = f(curr_x)
	x_steps = [curr_x]
	curr_iter = 0
	while max_iter is None or curr_iter<max_iter:
		if verbose>=2:
			print("iter:",curr_iter)
		neighbours = [ x for x in [curr_x + step, curr_x - step] if (x>x_range[0] and x<x_range[1]) ]
		if shuffle:
			random.shuffle(neighbours)
		step_taken = False
		for n in neighbours:
			n_eval = f(n)
			curr_iter += 1
			if (n_eval > curr_eval):
				curr_eval = n_eval
				curr_x = n
				step_taken = True
				x_steps.append(curr_x)
				break

		if not step_taken:
			step = step / step_decrease
			if verbose>=1:
				print("step decreased to", step)
			if (step<min_step):
				if verbose>=1:
					print("min step reached")
				return x_steps, curr_iter

	if verbose>=1:
		print("reached max_iter:",max_iter)
	return x_steps, curr_iter
