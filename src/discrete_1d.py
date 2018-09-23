import random
from matplotlib import pyplot as plt

#EXAMPLE FUNCTION
def f_1d():
	return [3,4,5,4,3,2,1,0,-1,-2,
			-3,-3,-2,-1,0,1,2,3,4,5,
			6,7,8,9,8,7,6,5,4,3,
			2,1,0]

def draw_discrete_1d(f,show=False,save_png=False,save_pdf=False,filename="discrete_1d"):
	plt.scatter(list(range(len(f))),f)
	if show:
		plt.show()
	if save_png:
		plt.savefig(filename+".png")
		print("Graph saved to:", filename+".png")
	if save_pdf:
		plt.savefig(filename+".pdf", bbox_inches='tight')
		print("Graph saved to:", filename+".pdf")
	plt.gcf().clear()

def draw_discrete_1d_and_steps(f,steps,line=True,show=False,save_png=False,save_pdf=False,filename="discrete_1d_steps"):
	plt.scatter(list(range(len(f))),f,color='blue')
	if line:
		plt.plot(steps,[f[s] for s in steps],color='blue')
	else:
		plt.scatter(steps,[f[s] for s in steps],color='orange')
	plt.scatter(steps[0],f[steps[0]],color='green')
	plt.scatter(steps[-1],f[steps[-1]],color='red')
	if show:
		plt.show()
	if save_png:
		plt.savefig(filename+".png")
		print("Graph saved to:", filename+".png")
	if save_pdf:
		plt.savefig(filename+".pdf", bbox_inches='tight')
		print("Graph saved to:", filename+".pdf")
	plt.gcf().clear()

def discrete_hill_climbing_simple_1d(f,x0=None,max_iter=None,step=10,step_decrease=1,verbose=0):
	curr_x = len(f)//2
	if x0 is not None:
		curr_x = x0
	curr_eval = f[curr_x]
	x_steps = [curr_x]
	curr_iter = 0
	while True:
		if (max_iter is not None and curr_iter>max_iter):
			if verbose>=1:
				print("reached max_iter:",max_iter)
			return x_steps, curr_iter
		if verbose>=1:
			print("iter:",curr_iter)
		neighbours = [ x for x in [curr_x + step, curr_x - step] if (x>=0 and x<len(f))]
		random.shuffle(neighbours)
		next_eval = float("-inf")
		next_x = None
		for n in neighbours:
			n_eval = f[n]
			curr_iter += 1
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
				return x_steps, curr_iter
		else:
			x_steps.append(next_x)
			curr_x = next_x
			curr_eval = next_eval



