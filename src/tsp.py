import random
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

def random_coordinates(length, coord_range=None, seed=None):
	if seed is not None:
		random.seed(seed)
	if coord_range is None:
		return [(random.random(),random.random()) for i in range(length)]
	else:
		l,r = coord_range
		s = r-l
		return [(random.random()*s+l, random.random()*s+l) for i in range(length)]

def random_tour(length):
	tour = list(range(length))
	random.shuffle(tour)
	return tour

def distance_2d(a,b):
	p1 = a[0]-b[0]
	p2 = a[1]-b[1]
	return math.sqrt(p1*p1+p2*p2)

def euclid_distances(coordinates):
	return [[ distance_2d(i,j) for i in coordinates ] for j in coordinates ]

def tour_length(distances,tour):
	length=0
	num_cities=len(tour)
	for i in range(num_cities-1):
		length+=distances[tour[i]][tour[i+1]]
	length+=distances[tour[num_cities-1]][tour[0]]
	return length

def pair_generator(size,shuffle=True):
	l1=list(range(size))
	l2=list(range(size))
	if shuffle:
		random.shuffle(l1)
		random.shuffle(l2)
	for i in l1:
		for j in l2:
			yield (i,j)

def reversed_sections_generator(tour):
	for i,j in pair_generator(len(tour)):
		if i != j:
			rev_sec=tour[:]
			if i < j:
				rev_sec[i:j+1]=reversed(tour[i:j+1])
			else:
				rev_sec[i+1:]=reversed(tour[:j])
				rev_sec[:j]=reversed(tour[i+1:])
			if rev_sec != tour:
				yield rev_sec

def swapped_cities_generator(tour):
	for i,j in pair_generator(len(tour)):
		if i < j:
			swap=tour[:]
			swap[i],swap[j]=tour[j],tour[i]
			yield swap

def draw_tour(coords,tour,title="",img_file="tsp.png",scale=1000,margin=20,city_scale=1.0,ssaa=2.0,draw_city_id=True):
	cs = ssaa*city_scale
	coords = [(x*scale*ssaa+margin*ssaa, y*scale*ssaa+margin*ssaa) for (x,y) in coords]
	max_x = np.max([x for (x,y) in coords])
	max_y = np.max([y for (x,y) in coords])

	img_w = max_x+2*margin*ssaa
	img_h = max_y+2*margin*ssaa

	img = Image.new("RGB",(int(img_w),int(img_h)),color=(255,255,255))
	font = ImageFont.truetype("arial.ttf")
	font_size = font.getsize("0123456789")
	font = ImageFont.truetype("arial.ttf",int(font_size[1]*cs*1.5))
	draw = ImageDraw.Draw(img);

	num_cities=len(tour)
	for i in range(num_cities):
		j=(i+1)%num_cities
		x1,y1 = coords[tour[i]]
		x2,y2 = coords[tour[j]]
		draw.line((int(x1),int(y1),int(x2),int(y2)),fill=(0,0,0))
		if draw_city_id:
			draw.text((int(x1)+10*cs,int(y1)-8*cs),str(i),font=font,fill=(32,32,32))

	for x,y in coords:
		x,y=int(x),int(y)
		draw.ellipse((x-8*cs,y-8*cs,x+8*cs,y+8*cs),outline=(0,0,0),fill=(196,196,196))

	draw.text((1,1),title,font=font,fill=(0,0,0))

	del draw

	if ssaa is not None and ssaa!=1.0:
		img = ImageOps.fit(img, (int(img_w/ssaa),int(img_h/ssaa)), Image.ANTIALIAS)
	img.save(img_file, "PNG")



def tsp_hillclimb(init,evaluation_function,next_generator,max_iterations=1000,verbose=0):

	curr_tour = init
	curr_eval = evaluation_function(curr_tour)

	curr_iter = 0
	num_of_nexts = 0
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
			if (next_eval<curr_eval):
				if verbose>=3:
					print("changed tour after",i)
				changed_tour = True
				num_of_nexts += 1
				curr_eval = next_eval
				curr_tour = next_tour
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
	result["local_optimum"] = local_optimum
	return result


def tsp_hillclimb_restart(init_function,evaluation_function,next_generator,max_iterations=1000,\
						  num_of_restarts=50,verbose=0):

	curr_tour = None
	curr_eval = float("inf")
	curr_lo = False

	curr_iter = 0
	while curr_iter < num_of_restarts:
		if verbose>=1:
			print("restart", curr_iter)
		curr_iter += 1
		init_tour = init_function()

		result = tsp_hillclimb(init=init_tour, evaluation_function=evaluation_function, \
							  next_generator=next_generator, max_iterations=max_iterations)

		if verbose>=1:
			print("result", result["best_eval"], result["num_of_nexts"])
		if result["best_eval"] < curr_eval or curr_tour is None:
			if verbose>=1:
				print("new best")
			curr_tour = result["best_tour"]
			curr_eval = result["best_eval"]
			curr_lo = result["local_optimum"]

	final_result = {}
	final_result["best_tour"] = curr_tour
	final_result["best_eval"] = curr_eval
	final_result["local_optimum"] = curr_lo

	return final_result#(curr_tour,curr_eval)


def tsp_hillclimb_restart_overall_iterations(init_function,evaluation_function,next_generator,max_iterations=100000,\
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

		result = tsp_hillclimb(init=init_tour, evaluation_function=evaluation_function, \
							  next_generator=next_generator, max_iterations=max_iterations-curr_iter, verbose=verbose)

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

	return final_result#(curr_tour,curr_eval)
