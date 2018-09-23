import random
import numpy as np
from matplotlib import pyplot as plt

#EXAMPLE FUNCTION
def f_2d_0(sizes=(20,20)):
	return [[0 for x in range(sizes[0])] for y in range(sizes[1])]

#RANDOM FUNCTION
def f_2d_randint(sizes=(20,20),max_value=100):
	return np.random.randint(max_value, size=sizes)


def distance_to_point_squared(s,d):
	first = s[0]-d[0]
	second = s[1]-d[1]
	return first*first+second*second

def distance_to_point(s,d):
	return np.sqrt(distance_to_point_squared(s,d))

#RANDOM SINGLE HILL FUNCTION
def f_2d_int_hill(sizes=(20,20),max_value=100,max_pos=None):
	if max_pos is None:
		x = np.random.randint(sizes[0])
		y = np.random.randint(sizes[1])
		max_pos = (x,y)
	return [[max_value-distance_to_point_squared((x,y),max_pos) for x in range(sizes[0])] for y in range(sizes[1])]

def draw_2d_discrete(f,show=False,save_png=False,save_pdf=False,filename="discrete_2d"):
	plt.figure(figsize = (10,10))
	h, w = f.shape
	#plt.xticks(range(h))
	#plt.yticks(range(w))
	plt.imshow(f, cmap='gray')
	#plt.colorbar(orientation='horizontal')
	if show:
		plt.show()
	if save_png:
		plt.savefig(filename+".png")
		print("Graph saved to:", filename+".png")
	if save_pdf:
		plt.savefig(filename+".pdf", bbox_inches='tight')
		print("Graph saved to:", filename+".pdf")
	plt.gcf().clear()

def draw_2d_discrete_with_path(f,path,draw_steps=False,show=False,save_png=False,save_pdf=False,filename="discrete_2d_steps"):
	list1= [ x[0] for x in path ]
	list2= [ x[1] for x in path ]
	plt.figure(figsize = (10,10))
	h, w = f.shape
	#plt.xticks(range(h))
	#plt.yticks(range(w))
	plt.plot(list1,list2)
	if draw_steps:
		plt.scatter(list1,list2,c='orange')
	plt.scatter(list1[0],list2[0],c='green')
	plt.scatter(list1[-1],list2[-1],c='red')
	plt.imshow(f.T, cmap='gray')
	#plt.colorbar(orientation='horizontal')
	if show:
		plt.show()
	if save_png:
		plt.savefig(filename+".png")
		print("Graph saved to:", filename+".png")
	if save_pdf:
		plt.savefig(filename+".pdf", bbox_inches='tight')
		print("Graph saved to:", filename+".pdf")
	plt.gcf().clear()

def discrete_hill_climbing_simple_2d_best_move(f,x0=None,max_iter=None,step=5,step_decrease=1,verbose=0,shuffle=True):
	curr_x = (f.shape[0]//2, f.shape[1]//2)
	if x0 is not None:
		curr_x = x0
	curr_eval = f[curr_x]
	x_steps = [curr_x]
	curr_iter = 0
	while True:
		if (max_iter is not None and curr_iter>max_iter):
			if verbose>=1:
				print("reached max_iter:",max_iter)
			return x_steps
		if verbose>=1:
			print("iter:",curr_iter)
		x,y = curr_x
		neighbours = [ (x+step,y), (x-step,y), (x,y+step), (x,y-step) ]
		neighbours = [ n for n in neighbours if (n[0]>=0 and n[1]>=0 and n[0]<f.shape[0] and n[1]<f.shape[1])]
		if shuffle:
			random.shuffle(neighbours)

		next_eval = float("-inf")
		next_x = None
		for n in neighbours:
			n_eval = f[n]
			if verbose>=2:
				print("neighbour",n,"eval",n_eval)
			if (n_eval > next_eval):
				next_eval = n_eval
				next_x = n

		if verbose>=2:
			print("next_eval",next_eval,"curr_eval",curr_eval)
		if (next_eval <= curr_eval):
			step = step - step_decrease
			if verbose>=1:
				print("step decreased to", step)
			if (step<=0):
				if verbose>=1:
					print("min step reached")
				return x_steps
		else:
			x_steps.append(next_x)
			curr_x = next_x
			curr_eval = next_eval
		curr_iter = curr_iter + 1


def discrete_hill_climbing_simple_2d_random_move(f,init_pos=None,max_iter=None,step=5,step_decrease=1,verbose=0,shuffle=True):
	curr_pos = (f.shape[0]//2, f.shape[1]//2)
	if init_pos is not None:
		curr_pos = init_pos
	curr_eval = f[curr_pos]
	steps = [curr_pos]
	curr_iter = 0
	while max_iter is None or curr_iter<max_iter:
		if verbose>=1:
			print("iter:",curr_iter)
		x,y = curr_pos
		neighbours = [ (x+step,y), (x-step,y), (x,y+step), (x,y-step) ]
		neighbours = [ n for n in neighbours if (n[0]>=0 and n[1]>=0 and n[0]<f.shape[0] and n[1]<f.shape[1])]
		if shuffle:
			random.shuffle(neighbours)

		step_taken= False
		for n in neighbours:
			n_eval = f[n]
			curr_iter += 1
			if verbose>=2:
				print("neighbour",n,"eval",n_eval)
			if (n_eval > curr_eval):
				curr_eval = n_eval
				curr_pos = n
				step_taken=True
				steps.append(curr_pos)
				break

		if not step_taken:
			step = step - step_decrease
			if verbose>=1:
				print("step decreased to", step)
			if (step<=0):
				if verbose>=1:
					print("min step reached")
				return steps, curr_iter

	if verbose>=1:
		print("reached max_iter:",curr_iter)
	return steps, curr_iter

