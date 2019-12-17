#/***************************************************************************
# *   Copyright (C) 2019 by Stephan Kunne                                   *
# *   stephan.kunne@univ-nantes.fr                                          *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 3 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU General Public License for more details.                          *
# *                                                                         *
# *   You should have received a copy of the GNU General Public License     *
# *   along with this program; if not, write to the                         *
# *   Free Software Foundation, Inc.,                                       *
# *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
# ***************************************************************************/

import sys				# Sys.argv
import random			# randomly initialize speeds and positions
from math import sqrt	# normalize speeds

import queue	# useful for colouring pixels in an image


#import numpy
from PIL import Image, ImageDraw

random.seed()

width, height = 1000, 1000

nb_cells_init = 10		# number of cells when animaton starts
cell_radius = 50		# radius of every cell
speed_nperframe = 5		# number of pixels a cell moves per frame
fps = 24				# number of frames per second
nb_frames = 10 * fps	# total number of frames in the animation

mitosis_proba_percellperframe = 1 / (5 * nb_cells_init * fps)	# in average 1 mitosis every 5 seconds... at first

X = [random.randint(0, width-1) for _ in range(nb_cells_init)]
Y = [random.randint(0, height-1) for _ in range(nb_cells_init)]

VX = [random.uniform(.5,1) * random.choice([-1,1]) for _ in range(nb_cells_init)]
VY = [random.uniform(.5,1) * random.choice([-1,1]) for _ in range(nb_cells_init)]
Vnorm = [ sqrt(vx**2 + vy**2) for vx, vy in zip(VX,VY)]
VX = [vx * speed_nperframe / norm for vx, norm in zip(VX, Vnorm)]
VY = [vy * speed_nperframe / norm for vy, norm in zip(VY, Vnorm)]

# VX = [speed_nperframe for _ in range(nb_cells_init)]
# VY = [speed_nperframe for _ in range(nb_cells_init)]

def update_cell_locations(X,Y,VX,VY):
	# mitosis
	for i in range(len(X)):
		if random.random() <= mitosis_proba_percellperframe:
			X.append(X[i])
			Y.append(Y[i])
			VX.append(-VY[i])	# rotation +90°
			VY.append(VX[i])	# rotation +90°
			VX[i],VY[i] = VY[i],-VX[i]	# rotation -90°

	# move
	X = [x + vx for x,vx in zip(X,VX)]
	Y = [y + vy for y,vy in zip(Y,VY)]

	# bounce off walls
	for i in range(len(X)):
		if X[i] < 0:
			X[i] = 0
			VX[i] = abs(VX[i])
		elif X[i] > width-1:
			X[i] = width-1
			VX[i] = - abs(VX[i])
		if Y[i] < 0:
			Y[i] = 0
			VY[i] = abs(VY[i])
		elif Y[i] > height-1:
			Y[i] = height-1
			VY[i] = - abs(VY[i])
	return X,Y,VX,VY

# # print initial speed vectors
# for vx,vy in zip(VX,VY):
# 	print(vx,vy)

def draw_cells(draw, X, Y):
	for x,y in zip(X,Y):
		draw.ellipse((x - cell_radius, y - cell_radius, x+cell_radius, y+cell_radius),
			fill=(255,255,255))

def colour_cell_contagious(img, x,y, colour):
	XY = queue.Queue()
	for i in [-1, 0, 1]:
		if 0 <= x+i and x+i < width:
			for j in [-1, 0, 1]:
				if 0 <= y+j and y+j < height:
					XY.put((x+i,y+j))
	while not XY.empty():
		(x,y) = XY.get()
		if img.getpixel((x,y)) == (255,255,255):
			img.putpixel((x,y), colour)
			for i in [-1, 0, 1]:
				if 0 <= x+i and x+i < width:
					for j in [-1, 0, 1]:
						if 0 <= y+j and y+j < height:
							XY.put((x+i,y+j))
			XY.get()	# remove (x+0,y+0) which has already been coloured

def get_colour_from_neighbours(x,y,img):
	colour = (0,0,0)
	for i in [-1, 0, 1]:
		if 0 <= x+i and x+i < width:
			for j in [-1, 0, 1]:
				if 0 <= y+j and y+j < height:
					newcolour = img.getpixel((x,y))
					if newcolour != (0,0,0) and newcolour != (255,255,255):
						colour = newcolour
	return colour


def get_next_colour():
	get_next_colour.i += 1
	get_next_colour.i = 0 if get_next_colour.i == len(get_next_colour.colours) else get_next_colour.i
	return (get_next_colour.colours[get_next_colour.i])
get_next_colour.colours = [(255,000,000), (255,255,000), (255,000,255),
							(000,255,000), (000,000,255), (000,255,255),
							(100,000,000), (000,100,000), (000,000,100), (100,200,255), ]
get_next_colour.i = -1

def colour_first_frame(img):
	coords = [(x,y) for x in range(width) for y in range(height)]
	for (x,y) in coords:
		colour = img.getpixel((x,y))
		if colour == (255,255,255):
			colour = get_next_colour()
			colour_cell_contagious(img, x,y, colour)

# # this algorithm is terribly inefficient
# def colour_new_frame(old_img, img):
# 	q = queue.Queue()

# 	# colour cell pixels that were already cell pixels
# 	for x in range(width):
# 		for y in range(height):
# 			if img.getpixel((x,y)) == (255,255,255):
# 				colour = old_img.getpixel((x,y))
# 				if colour != (0,0,0):
# 					img.putpixel((x,y), colour)
# 				else:
# 					q.put((x,y))

# 	# colour cell pixels that were background pixels in old_img
# 	while not q.empty():
# 		(x,y) = q.get()
# 		colour = get_colour_from_neighbours(x,y,img)
# 		if colour != (0,0,0) and colour != (255,255,255):
# 			img.putpixel((x,y), colour)
# 		else:
# 			q.put((x,y))

def colour_new_frame(old_img, img):
	# colour cell pixels that were already cell pixels
	for x in range(width):
		for y in range(height):
			if img.getpixel((x,y)) == (255,255,255):
				colour = old_img.getpixel((x,y))
				if colour != (0,0,0):
					img.putpixel((x,y), colour)
	# find adjacent (white, coloured) pixel pair
	for x in range(width):
		for y in range(height - 1):
			if img.getpixel((x,y)) == (255,255,255):
				colour = img.getpixel((x,y+1))
				if colour != (255,255,255) and colour != (0,0,0):
					colour_cell_contagious(img, x,y, colour)

filename = sys.argv[1] if len(sys.argv) > 1 else 'cells.gif'

def make_new_blackwhite_frame():
	img = Image.new('RGB', (width, height))
	draw = ImageDraw.Draw(img)
	draw_cells(draw, X,Y)
	del draw
	return img

frames = []
img = make_new_blackwhite_frame()
colour_first_frame(img)
frames.append(img)
for i in range(nb_frames - 1):
	old_img = img
	img = make_new_blackwhite_frame()
	colour_new_frame(old_img, img)
	#cluster_init(img)
	frames.append(img)
	X,Y,VX,VY = update_cell_locations(X,Y,VX,VY)

frames[0].save(filename, format='GIF', save_all=True,
	append_images=frames[1:],
	duration = 1000 // fps,)
