import numpy as np
import random
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
#import functools

def f(x,y):
	return -x*x-y*y

def f2(x,y):
	return -(x+5)*(x+5)-(y+5)*(y+5)

def ripple(x,y,ripple_spread=0.025): #z_range=(-100.01,100.01) for default ripple
	return np.sin(ripple_spread*(x*x+y*y))/ripple_spread

def bumps(x,y,bump_effect=0.5):
	return np.sin(bump_effect*x)*np.cos(bump_effect*y)/bump_effect

def top_hat(x,y,hat_spread=10,ratio=3.0):
	return (np.sign(2-(x*x/hat_spread+y*y/hat_spread)) + np.sign(2-(x*x/(hat_spread*ratio)+y*y/(hat_spread*ratio))))/1-2

def pyramid(x,y): #z_range=(-10.01,10.01)
	return 1-np.abs(x+y)-np.abs(y-x)

def draw_graph_3d(f, x_range=(-10.0,10.0), y_range=(-10.0,10.0), z_range=(-1.01,1.01),\
				  x_step=0.25, y_step=0.25, antialiasing=False, show=False, \
				  save_png=False, save_pdf=False, filename="continuous_3d_graph", cmap=cm.coolwarm):
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	X = np.arange(x_range[0], x_range[1], x_step)
	Y = np.arange(y_range[0], y_range[1], y_step)
	X, Y = np.meshgrid(X, Y)
	Z = f(X,Y)

	surf = ax.plot_surface(X, Y, Z, cmap=cmap, linewidth=0, antialiased=antialiasing)

	ax.set_zlim(z_range[0],z_range[1])
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

	fig.colorbar(surf, shrink=0.75, aspect=15)

	if show:
		plt.show()
	if save_png:
		fig.savefig(filename+".png")
		print("Graph saved to:", filename+".png")
	if save_pdf:
		fig.savefig(filename+".pdf", bbox_inches='tight')
		print("Graph saved to:", filename+".pdf")
	plt.gcf().clear()

def draw_graph_3d_and_steps(f, steps, x_range=(-10.0,10.0), y_range=(-10.0,10.0), z_range=(-1.01,1.01), \
							x_step=0.25, y_step=0.25, antialiasing=False, show=False, \
							save_png=False, save_pdf=False, filename="continuous_3d_graph_steps", stride=10):
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	X = np.arange(x_range[0], x_range[1], x_step)
	Y = np.arange(y_range[0], y_range[1], y_step)
	X, Y = np.meshgrid(X, Y)
	Z = f(X,Y)

	#surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=antialiasing)
	wire = ax.plot_wireframe(X, Y, Z, rstride=stride, cstride=stride)

	SX = np.array([p[0] for p in steps])
	SY = np.array([p[1] for p in steps])
	SZ = f(SX,SY)
	#SZ = SZ + 1
	scat = ax.scatter(SX, SY, SZ, c='red')

	ax.set_zlim(z_range[0],z_range[1])
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

	#fig.colorbar(surf, shrink=0.75, aspect=15)

	if show:
		plt.show()
	if save_png:
		fig.savefig(filename+".png")
		print("Graph saved to:", filename+".png")
	if save_pdf:
		fig.savefig(filename+".pdf", bbox_inches='tight')
		print("Graph saved to:", filename+".pdf")
	plt.gcf().clear()


def draw_graph_3d_as_imshow(f, x_range=(-10.0,10.0), y_range=(-10.0,10.0), z_range=(-1.01,1.01), \
							x_step=0.25, y_step=0.25, antialiasing=False, show=False, \
							save_png=False, save_pdf=False, filename="continuous_3d_imshow", cmap=cm.coolwarm, \
							interpolation=None):

	X = np.arange(x_range[0], x_range[1], x_step)
	Y = np.arange(y_range[0], y_range[1], y_step)
	X, Y = np.meshgrid(X, Y)
	Z = f(X,Y)

	plt.figure(figsize = (10,10))
	#plt.xticks(range(len(X)))
	#plt.yticks(range(len(Y)))
	plt.imshow(Z, cmap=cmap, interpolation=interpolation)

	if show:
		plt.show()
	if save_png:
		fig.savefig(filename+".png")
		print("Graph saved to:", filename+".png")
	if save_pdf:
		fig.savefig(filename+".pdf", bbox_inches='tight')
		print("Graph saved to:", filename+".pdf")
	plt.gcf().clear()


def draw_graph_3d_as_imshow_with_path(f, path, x_range=(-10.0,10.0), y_range=(-10.0,10.0), z_range=(-1.01,1.01), \
									   x_step=0.25, y_step=0.25, antialiasing=False, show=False, \
									   save_png=False, save_pdf=False, \
									   filename="continuous_3d_imshow_steps", cmap=cm.coolwarm, interpolation=None, scatter_all=False):

	X = np.arange(x_range[0], x_range[1], x_step)
	Y = np.arange(y_range[0], y_range[1], y_step)

	#x_ticks_number = len(X)//20
	#y_ticks_number = len(Y)//20

	fig = plt.figure(figsize = (10,10))
	plt.xticks(range(len(X)),X,rotation='vertical')
	plt.yticks(range(len(Y)),Y)

	#plt.xticks(range(20),X[::x_ticks_number])
	#plt.yticks(range(20),Y[::y_ticks_number])

	X, Y = np.meshgrid(X, Y)
	Z = f(X,Y)
	plt.imshow(Z, cmap=cmap, interpolation=interpolation)

	list1= [ (x[0]-x_range[0])//x_step for x in path ]
	list2= [ (x[1]-y_range[0])//y_step for x in path ]

	plt.plot(list1,list2)
	if scatter_all:
		plt.scatter(list1[1:-1],list2[1:-1],c='orange')
	plt.scatter(list1[0],list2[0],c='green')
	plt.scatter(list1[-1],list2[-1],c='red')

	if show:
		plt.show()
	if save_png:
		fig.savefig(filename+".png")
		print("Graph saved to:", filename+".png")
	if save_pdf:
		fig.savefig(filename+".pdf", bbox_inches='tight')
		print("Graph saved to:", filename+".pdf")
	plt.gcf().clear()

def draw_graph_3d_as_imshow_with_multi_paths(f, paths=None, best_path=None, x_range=(-10.0,10.0), y_range=(-10.0,10.0), \
											 z_range=(-1.01,1.01), x_step=0.25, y_step=0.25, antialiasing=False, \
											 show=False, save_png=False, save_pdf=False, filename="continuous_3d_imshow_multi_steps", \
											 cmap=cm.coolwarm, interpolation=None, scatter_all=False):

	#plt.close('all')

	X = np.arange(x_range[0], x_range[1], x_step)
	Y = np.arange(y_range[0], y_range[1], y_step)

	#fig = plt.figure(figsize = (10,10))
	fig, axes = plt.subplots(figsize=(10,10))
	plt.xticks(range(len(X)),X,rotation='vertical')
	plt.yticks(range(len(Y)),Y)

	X, Y = np.meshgrid(X, Y)
	Z = f(X,Y)
	plt.imshow(Z, cmap=cmap, interpolation=interpolation)

	if paths is not None:
		for path in paths:
			list1= [ (x[0]-x_range[0])//x_step for x in path ]
			list2= [ (x[1]-y_range[0])//y_step for x in path ]

			plt.plot(list1,list2,c='teal')
			if scatter_all:
				plt.scatter(list1[1:-1],list2[1:-1],c='orange')
			plt.scatter(list1[0],list2[0],c='green')
			plt.scatter(list1[-1],list2[-1],c='red')

	if best_path is not None:
		list1= [ (x[0]-x_range[0])//x_step for x in path ]
		list2= [ (x[1]-y_range[0])//y_step for x in path ]

		plt.plot(list1,list2,c='blue')
		if scatter_all:
			plt.scatter(list1[1:-1],list2[1:-1],c='orange')
		plt.scatter(list1[0],list2[0],c='green')
		plt.scatter(list1[-1],list2[-1],c='red')

	if show:
		plt.show()
	if save_png:
		fig.savefig(filename+".png")
		print("Graph saved to:", filename+".png")
	if save_pdf:
		fig.savefig(filename+".pdf", bbox_inches='tight')
		print("Graph saved to:", filename+".pdf")
	plt.gcf().clear()




def continious_hill_climbing_simple_3d_best_move(f,init=(0.0,0.0),max_iter=None,step=1.0,step_decrease=2.0,\
												 min_step=0.000001,f_range=((-10,10),(-10,10)), verbose=0):
	curr_pos = init
	curr_eval = f(curr_pos[0],curr_pos[1])
	steps = [curr_pos]
	curr_iter = 0
	while True:
		if (max_iter is not None and curr_iter>max_iter):
			if verbose>=2:
				print("reached max_iter:",max_iter)
			return steps
		if verbose>=3:
			print("iter:",curr_iter)
		x,y = curr_pos
		neighbours = [ (x+step,y), (x-step,y), (x,y+step), (x,y-step) ]
		neighbours = [ n for n in neighbours \
					  if (n[0]>f_range[0][0] and n[0]<f_range[0][1] and n[1]>f_range[1][0] and n[1]<f_range[1][1]) ]
		next_eval = float("-inf")
		next_pos = None
		for n in neighbours:
			n_eval = f(n[0],n[1])
			if (n_eval > next_eval):
				next_eval = n_eval
				next_pos = n
		if (next_eval < curr_eval):
			step = step / step_decrease
			if verbose>=2:
				print("step decreased to", step)
			if (step<min_step):
				if verbose>=2:
					print("min step reached")
				return steps
		else:
			steps.append(next_pos)
			curr_pos = next_pos
			curr_eval = next_eval
		curr_iter = curr_iter + 1


def continious_hill_climbing_simple_3d_random_move(f, init=(0.0,0.0), \
		max_iter=None, step=1.0, step_decrease=2.0, min_step=0.000001, \
		f_range=((-10,10),(-10,10)), platou_check=True, platou_move=True, \
		shuffle=True, verbose=0):
	curr_pos = init
	curr_eval = f(curr_pos[0],curr_pos[1])
	steps = [curr_pos]
	curr_iter = 0
	max_step = max(f_range[0][1]-f_range[0][0],f_range[1][1]-f_range[1][0])

	while max_iter is None or curr_iter<max_iter:
		if verbose>=3:
			print("iter:",curr_iter)
		x,y = curr_pos
		neighbours = [ (x+step,y), (x-step,y), (x,y+step), (x,y-step) ]
		neighbours = [ n for n in neighbours \
					  if (n[0]>f_range[0][0] and n[0]<f_range[0][1] and n[1]>f_range[1][0] and n[1]<f_range[1][1]) ]
		if shuffle:
			random.shuffle(neighbours)

		step_taken = False
		best_eval = None
		best_n = None
		for n in neighbours:
			n_eval = f(n[0],n[1])
			curr_iter += 1
			if (n_eval > curr_eval):
				curr_eval = n_eval
				curr_pos = n
				step_taken = True
				steps.append(curr_pos)
				break
			if best_eval is None or n_eval>best_eval: #platou check
				best_eval = n_eval
				best_n = n

		if not step_taken:
			if best_eval is None:
				if verbose>=2:
					print("no neighbours")
				return steps, curr_iter
			if best_eval<curr_eval: # possibly near optimum an overreaching, decreasing step
				step = step / step_decrease
				if verbose>=2:
					print("step decreased to", step)
				if (step<min_step):
					if verbose>=2:
						print("min step reached")
					return steps, curr_iter
			else: #best_eval==curr_eval #possibly on a platou
				if platou_check:
					if platou_move:
						#move just in case
						curr_eval = best_eval
						curr_pos = best_n
						steps.append(curr_pos)

					step = step * step_decrease
					if verbose>=2:
						print("platou? step increased to", step)
					if (step>max_step):
						if verbose>=2:
							print("max step reached")
						return steps, curr_iter
	if verbose>=2:
		print("reached max_iter:",curr_iter)
	return steps, curr_iter


def continious_hill_climbing_restarting_3d(f, max_iter=10000, max_restarts=15, step=1.0, step_decrease=2.0, \
										   min_step=0.000001, f_range=((-10,10),(-10,10)), \
										   platou_check=True, platou_move=True, shuffle=True, verbose=0):

	all_results = []
	best_results = None
	best_eval = float("-inf")
	(xl,xr),(yl,yr) = f_range
	curr_iter = 0
	i = 0
	while i<max_restarts and (max_iter is None or curr_iter<max_iter):
		i += 1
		init_x = (np.random.rand() * (xr-xl)) + xl
		init_y = (np.random.rand() * (yr-yl)) + yl

		if verbose>=1:
			print("init:", init_x, init_y)

		result, iters = continious_hill_climbing_simple_3d_random_move(\
						f, init=(init_x,init_y), max_iter=max_iter-curr_iter, step=step, \
						step_decrease=step_decrease, min_step=min_step, f_range=f_range, \
						platou_check=platou_check, platou_move=platou_move, \
						shuffle=shuffle, verbose=verbose)
		curr_iter += iters

		all_results.append(result)
		new_eval = f(result[-1][0],result[-1][1])
		if new_eval > best_eval:
			best_eval = new_eval
			best_results = result

		if verbose>=1:
			print("result",new_eval,"pos",(result[-1][0],result[-1][1]),"iters spent:", curr_iter, "restarting")

	return all_results, best_results, curr_iter

