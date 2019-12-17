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


from PIL import Image
from functools import reduce 	# sum list of tuples
#import math		# pi, cos, sin
import sys		# sys.argv

if len(sys.argv) >= 3:
	inputimgname = sys.argv[1]
	outimgname = sys.argv[2]
else:
	inputimgname = 'img/text.png'
	outimgname = 'img/newsquare.png'
if len(sys.argv) >= 4:
	num_proj = int(sys.argv[3])
else:
	num_proj = 11		# number of projections

img = Image.open(inputimgname)

width, height = img.size
sidelength = min(width, height)
# HERE REFRAME IMAGE SO IT IS SQUARE
width = min(width,height)
height=min(width,height)

black = (0,0,0, 255)


# return the list of points joining points (x0,y0) and (x1,y1)
# assume x1 > x0, y1 > y0, and |x1-x0| >= |y1-y0|
def get_ray_with_assumption(x0,y0, x1,y1, stepy=1):
	dx = x1 - x0
	dy = (y1 - y0) * stepy
	D = 2*dy - dx
	y = y0
	ray = []
	for x in range(x0, x1+1):
		ray.append((x,y))
		if D > 0:
			y = y + stepy
			D = D - 2*dx
		D = D + 2*dy
	return ray

# return the list of points joining points (x0,y0) and (x1,y1)
# no assumption
def get_ray(x0,y0, x1,y1):
	if x1 == x0:
		return [(x0,y) for y in range(y0, y1+1)]
	if x1 < x0:
		(x0,y0, x1,y1) = (x1,y1, x0,y0)
	if x1 - x0 < y1 - y0:
		stepy = 1 if y1 >= y0 else -1
		ray = get_ray_with_assumption(y0,x0, y1,x1, stepy)
		return [(y,x) for (x,y) in ray]
	else:
		stepy = 1 if y1 >= y0 else -1
		return get_ray_with_assumption(x0,y0, x1,y1, stepy)


# def get_rays(k, num_proj, alpha):
# 	if k <= (num_proj + 1) / 4:
# 		wsina = int((width-1) * math.sin(alpha))
# 		(x0,y0) = (0, - wsina)
# 		(x1,y1) = (width-1,0)
# 		return [get_ray(x0,y0+j,x1,y1+j) for j in range(height+wsina)]
# 	elif k <= (num_proj +1) / 2:
# 		wcosa = int((width-1) * math.cos(alpha))
# 		(x0,y0) = (width-1, 0)
# 		(x1,y1) = ( (width-1+wcosa) , height-1 )
# 		return [get_ray(x0-j,y0,x1-j,y1) for j in range(width+wcosa)]
# 	elif k <= 3*(num_proj+1)/4:
# 		wcosa = int((width-1) * math.cos(alpha))
# 		(x0,y0) = (width-1-wcosa, 0)
# 		(x1,y1) = (width-1, height-1)
# 		return [get_ray(x0-j,y0,x1-j,y1) for j in range(width-wcosa)]
# 	else:
# 		wsina = int((width-1) * math.sin(alpha))
# 		(x0,y0) = (0,0)
# 		(x1,y1) = (width-1, - wsina)
# 		return [get_ray(x0,y0+j,x1,y1+j) for j in range(width+wsina)]

def get_rays(k, num_proj):
	if k < (num_proj) / 2:
		z = int(k * (height-1) * 2 / (num_proj))
		(x0,y0) = (0, 0)
		(x1,y1) = (width-1,2*z-height+1)
		return [get_ray(x0,y0+j,x1,y1+j) for j in range(height+height-1-z)]
	# elif k <= (num_proj + 1) / 2:
	# 	z = int(k * (height-1) * 2 / (num_proj))
	# 	(x0,y0) = (width-1, 0)
	# 	(x1,y1) = ( (width-1+z) , height-1 )
	# 	return [get_ray(x0-j,y0,x1-j,y1) for j in range(width+z)]
	else:
		z = int((k-num_proj/2) * (height-1) * 2 / (num_proj))
		(x0,y0) = (0,2*z- width+1)
		(x1,y1) = (0, height-1)
		return [get_ray(x0+j,y0,x1+j,y1) for j in range(width+width-1-z)]


# def get_ray(k, num_proj):
# 	if k == 0 or k == 4:
# 		return [(x,0) for x in range(sidelength)]
# 	elif k == 2:
# 		return [(0,y) for y in range(sidelength)]
# 	elif k == 1:
# 		return [(-x, x) for x in range(sidelength)]
# 	elif k == 3:
# 		return [(x,sidelength-1+x) for x in range(sidelength)]


# def get_proj_size(k):
# 	if k in [0, 2, 4]:
# 		return sidelength
# 	elif k in [1, 3]:
# 		return 2*sidelength-1
# 	assert False, "get_proj_size(): out of bounds"

# def get_incr(k):
# 	return get_incr.l[k]
# get_incr.l = [(0,1), (1,0), (1,0), (0,-1), (0,1)]

# def get_rays(k, num_proj):
# 	ray = get_ray(k, num_proj)
# 	incrx, incry = get_incr(k)
# 	return [[(x+j*incrx, y+j*incry) for (x,y) in ray] for j in range(get_proj_size(k))]

# getpixel and newpixel handling out of range pixels
def getpixel(img, coord):
	(x,y) = coord
	return img.getpixel((x,y)) if 0 <= x and x < width and 0 <= y and y < height else black

def putpixel(img, coord, newpixel):
	(x,y) = coord
	if 0 <= x and x < width and 0 <= y and y < height:
		img.putpixel(coord, newpixel)

def addpixels(p, q):
	rp,gp,bp,ap = p
	rq,gq,bq,aq = q
	return (rp+rq,gp+gq,bp+bq, 255)#(ap+aq)//2)

# COMPUTE PROJECTIONS
lst_of_projections = []
#lst_of_lst_of_rays = [get_rays(k, num_proj) for k in range(num_proj)]
#lst_of_lst_of_rays = [get_rays(k, num_proj, math.pi * k / (num_proj+1)) for k in range(num_proj)]
lst_of_lst_of_rays_0 = [get_rays(k, num_proj) for k in range(num_proj)]
lst_of_lst_of_rays_1 = [[[(x,y) for (x,y) in ray if 0 <= x and x < width and 0 <= y and y < height] for ray in lst_of_rays] for lst_of_rays in lst_of_lst_of_rays_0]
lst_of_lst_of_rays = [[ray for ray in lst_of_rays if len(ray) > 0] for lst_of_rays in lst_of_lst_of_rays_1]

print('succesfully built list of rays')

for k,lst_of_rays in enumerate(lst_of_lst_of_rays):
	#alpha = get_angle(k)
	#ray0 = get_ray(alpha, k)
	#incrx,incry = get_incr(k)
	#proj = [sum((getpixel(img, (x+incrx,y+incry)) for (x,y) in ray0), start=black) for j in range(get_proj_size(k))]
	proj = [reduce(
			(addpixels),
			(getpixel(img, (x,y)) for (x,y) in ray),
			black
		) for ray in lst_of_rays]
	proj = [(r//len(ray), g//len(ray), b//len(ray), 255) for (r,g,b,a),ray in zip(proj, lst_of_rays)]
	# proj = [
	# 	reduce(
	# 		(addpixels),
	# 		(getpixel(img, (x+incrx,y+incry)) for (x,y) in ray0),
	# 		black
	# 	) for j in range(get_proj_size(k))]
	lst_of_projections.append(proj)

print('calculated all projections')

# for proj in lst_of_projections:
# 	print(proj)

# def build_projection_drawing(img, lst_of_projections):
# 	image = Image.new('RGBA', (4*sidelength+1, 4*sidelength))

# 	#with lst_of_projections[0] as proj:
# 	proj = lst_of_projections[0]
# 	for x,pixel in enumerate(proj):
# 			image.putpixel((0,x), pixel)
# 	proj = lst_of_projections[1]
# 	for x,pixel in enumerate(proj):
# 			image.putpixel((x, sidelength), pixel)
# 	proj = lst_of_projections[2]
# 	for x,pixel in enumerate(proj):
# 			image.putpixel((sidelength+1+x,sidelength+1), pixel)
# 	proj = lst_of_projections[3]
# 	for x,pixel in enumerate(proj):
# 			image.putpixel((2*sidelength+2-x,2*sidelength+2-x), pixel)
# 	return image




# make nice display with original image and projections
# display1 = build_projection_drawing(img, lst_of_projections)
# display1.save('out/display1.png')

# RECONSTRUCT IMAGE
newimg = Image.new('RGBA', (sidelength, sidelength))
# newimg.save('out/blankimg.png')
# print('pixels from blank img:')
# for coord in [(0,0), (12,20), (sidelength-1,sidelength-1)]:
# 	print(newimg.getpixel(coord))


newdata = [[(0,0,0,255) for x in range(width)] for y in range(height)]
#countpixels = [[0 for x in range(width)] for y in range(height)]

for k, (lst_of_rays, proj) in enumerate(zip(lst_of_lst_of_rays, lst_of_projections)):
	for ray,pixel in zip(lst_of_rays, proj):
		for (x,y) in ray:
			#newpixel = addpixels(pixel,getpixel(newimg,(x,y)))
			#putpixel(newimg, (x,y), newpixel
			if 0 <= x and x < width and 0 <= y and y < height:
				newdata[y][x] = addpixels(pixel, newdata[y][x])
				#countpixels[y][x] += len(ray)

#newdata = [[(r//(num_proj-1), g//(num_proj-1), b//(num_proj-1), 255) for (r,g,b,a) in [newdata[y][x]] for x in range(width)] for y in range(height)]
#newdata_aslist = [(r//(num_proj-1), g//(num_proj-1), b//(num_proj-1), 255) for row in newdata for (r,g,b,a) in row]
#newdata_aslist = [(r//num_proj, g//num_proj, b//num_proj, 255) for row,countingrow in zip(newdata,countpixels) for ((r,g,b,a),c) in zip(row,countingrow)]
newdata_aslist = [(r//num_proj, g//num_proj, b//num_proj, 255) for row in newdata for (r,g,b,a) in row]
#newimg.paste(newdata, box=(0,width,0,height))

print('reconstructed image; about to renormalize variance')

import statistics
newr,newg,newb = zip(newdata_aslist)
newmeanr,newmeang,newmeanb = (statistics.mean(l) for l in (newr,newg,newb))
newstddevr, newstddevg,newstddevb = (statistics.stddev(l, mean) for l, mean in ((newr,newmeanr), (newg, newmeang), (newb, newmeanb)))

oldlst = [img.getpixel((x,y)) for y in range(height) for x in range(width)]
oldr,oldg,oldb = zip(oldlst)
oldmeanr,newmeang,newmeanb = (statistics.mean(l) for l in (newr,newg,newb))
newstddevr, newstddevg,newstddevb = (statistics.stddev(l, mean) for l, mean in ((newr,newmeanr), (newg, newmeang), (newb, newmeanb)))

newimg.putdata(newdata_aslist)
print('reconstructed image')
# for k,(ray0, proj) in enumerate(zip(lst_of_rays, lst_of_projections)):
# 	incrx, incry = get_incr(k)
# 	for (x,y) in ray0:
# 		for pixel in proj:
# 			newpixel = addpixels(pixel, getpixel(newimg,(x,y)))
# 			putpixel(newimg, (x,y), newpixel)
# 			x += incrx
# 			y += incry

# print('counting pixels:')
# for row in countpixels:
# 	print(row)

# print('pixels from reconstructed image:')
# for coord in [(0,0), (12,20), (sidelength-1,sidelength-1)]:
# 	print(newimg.getpixel(coord))
newimg.save(outimgname)
print('saved image as', outimgname)
## TODO :
##  - replace sum with averages
##  - make sure adding pixels works correctly with RGB
##  - write functions get_ray(), get_incr(), get_angle()
##  - calculate background and remove it from new image
##  - reframe image so it is square
