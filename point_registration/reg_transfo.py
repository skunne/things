
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

import numpy as np	# solve lin equation
import math			# solve trig equation
from sklearn.linear_model import LinearRegression 	# regression

from PIL import Image	# apply transfo to image
import pygame.image		# apply transfo to image

from time import sleep	# slow down icp

import reg_io 			# display icp

def calculate_similitude(x,y):
	# two points: translation + rotation,dilation centered on first point
	x0, x1 = x[1][0] - x[0][0], x[1][1] - x[0][1]
	y0, y1 = y[1][0] - y[0][0], y[1][1] - y[0][1]
	r = math.sqrt( (y0 * y0 + y1 * y1) / (x0 * x0 + x1 * x1) )
	alpha = - math.atan2(y0, y1) + math.atan2(x0, x1)
	rcosa = r * math.cos(alpha)
	rsina = r * math.sin(alpha)
	a, b, c, d = (rcosa, rsina, -rsina, rcosa)
	t0 = y[0][0] - (a * x[0][0] + c * x[0][1])
	t1 = y[0][1] - (b * x[0][0] + d * x[0][1])
	return ((a,b,c,d), (t0, t1))
		# # two points: add condition (a b c d) x[0] + t = x[0] + t
		# #   solve for a,c,t0
		# t0 = y[0][0] - x[0][0]
		# c = (y[1][0] - t0 - x[1][0]) / (x[1][1] - (x[1][0]*x[0][1])/x[0][0])
		# a = 1 - (c * x[0][1] / x[0][0])
		# #   solve for b, d, t1
		# t1 = y[0][1] - x[0][1]
		# b = (y[1][1]-y[0][1]+x[0][1]-x[1][1]) / (x[1][0] - (x[0][0]*x[1][1])/x[0][1])
		# d = 1 - (b * x[0][0]) / x[0][1]

def calculate_exact_affine(x, y):
	# three points: affine transformation, solve system using first three points
	y = np.array(y[:3])
	x = np.concatenate((np.array(x[:3]), np.array([[1],[1],[1]])), axis=1)
	bdt = np.linalg.solve(x, y[:,1])
	act = np.linalg.solve(x, y[:,0])
	b,d,t1 = bdt[0], bdt[1], bdt[2]
	a,c,t0 = act[0], act[1], act[2]
	return ((a,b,c,d), (t0, t1))
		# #   solve for a,c,t0
		# crh = (y[2][0] - y[0][0] - ((x[2][0]-x[0][0])*(y[1][0]-y[2][0]))/(x[1][0]-x[0][0]))
		# clh = x[2][1] - x[0][1] - ((x[2][0]-x[0][0])*(x[1][1]-x[0][1]))/(x[1][0]-x[0][0])
		# c = crh / clh
		# a = (y[1][0]-y[0][0] - c * (x[1][1]-x[0][1])) / (x[1][0]-x[0][0])
		# t0 = y[0][0] - a * x[0][0] - c * x[0][1]
		# #   solve for b,d,t1
		# drh = (x[2][0]-x[0][0])*(y[1][1]-y[0][1]) - (x[1][0]-x[0][0])*(y[2][1]-y[0][1])
		# dlh = (x[2][0]-x[0][0])*(x[1][1]-x[0][1]) - (x[1][0]-x[0][0])*(x[2][1]-x[0][1])
		# d = drh / dlh
		# brh = (x[2][1]-x[0][1])*(y[1][1]-y[0][1]) - (x[1][1]-x[0][1])*(y[2][1]-y[0][1])
		# blh = (x[2][1]-x[0][1])*(x[1][0]-x[0][0]) - (x[1][1]-x[0][1])*(x[2][0]-x[0][1])
		# b = brh / blh
		# t1 = y[0][1] - d * x[0][1] - b * x[0][0]

def calculate_best_affine(x, y):
	print(x)
	print(y)
	a, b = [], []
	for ((x0, x1), (y0, y1)) in zip(x, y):
		a.append([x0, 0, x1, 0, 1, 0])
		a.append([0, x0, 0, x1, 0, 1])
		b.append(y0)
		b.append(y1)
	reg = LinearRegression(fit_intercept=False).fit(np.array(a), np.array(b))
	(a,b,c,d,t0,t1) = reg.coef_
	return ((a,b,c,d), (t0, t1))

def find_closest_point(x, Y):
	(x0,x1) = x
	p = Y[0]
	dd = (p[0]-x0)**2 + (p[1]-x1)**2
	for (y0, y1) in Y[1:]:
		dd_y = (y0-x0)**2 + (y1-x1)**2
		if dd_y < dd:
			dd = dd_y
			p = (y0,y1)
	return p

# apply transformation f(x) = m x + t to source image
def apply(m, t, srcimg, imgwidth, imgheight):
	(a,b,c,d), (t0,t1) = m, t
	srctxt = pygame.image.tostring(srcimg, 'RGBA')
	#print(srctxt)
	pilimg = Image.frombytes('RGBA', (imgwidth,imgheight), srctxt)
	square_transfo = np.array([[a,c,t0],[b,d,t1],[0,0,1]])
	square_invert_transfo = np.linalg.inv(square_transfo)
	rectangle_invert_transfo = square_invert_transfo.flatten()[:6]
	(a,c,t0,b,d,t1) = rectangle_invert_transfo
	#det = a*d-b*c
	#(a,b,c,d) = (d/det, -b/det, c/det, a/det)
	#(t0,t1) = (-a*t0-c*t1, -b*t0-d*t1)
	print('inverse transfo:')
	print('  ', a, ' ', c, '  ', t0)
	print('  ', b, ' ', d, '  ', t1)
	newpilimg = pilimg.transform(
		(1000,1000),
		Image.AFFINE,
		data=rectangle_invert_transfo,#(a,c,t0,b,d,t1), #rectangle_invert_transfo,
		resample=Image.BICUBIC
	)
	newtxt = newpilimg.tobytes()
	newimg = pygame.image.fromstring(newtxt, (1000,1000),'RGBA')
	return newimg

def calculate_icp(X,Y, env):
	# translate X once to align center of mass with center of mass of Y
	bary_x0 = sum((x0 for (x0, x1) in X)) // len(X)
	bary_x1 = sum((x1 for (x0, x1) in X)) // len(X)
	bary_y0 = sum((y0 for (y0, y1) in Y)) // len(Y)
	bary_y1 = sum((y1 for (y0, y1) in Y)) // len(Y)
	((A,B,C,D),(T0,T1)) = ((1,0,0,1),(bary_y0-bary_x0,bary_y1-bary_x1))
	X = [(x0+T0, x1+T1) for (x0,x1) in X]


	del env.reg_img
	env.reg_img = apply((A,B,C,D), (T0,T1), env.source_img, env.imgwidth, env.imgheight)
	env.update()
	sleep(0.5)

	# loop until satisfied
	for j in range(20):
		Z = [find_closest_point(x,Y) for x in X]
		((a,b,c,d),(t0,t1)) = calculate_best_affine(X,Z)
		X = [(a*x0 + c*x1+t0, b*x0+d*x1+t1) for (x0,x1) in X]
		# compose transforms
		((A,B,C,D),(T0,T1)) = ((A*a+C*b,B*a+D*b,A*c+C*d,B*c+D*d), (A*t0+C*t1+T0,B*t0+D*t1+T1))
		del env.reg_img
		env.reg_img = apply((A,B,C,D), (T0,T1), env.source_img, env.imgwidth, env.imgheight)
		env.update()
		sleep(0.5)
	return ((A,B,C,D),(T0,T1))

# calculate transformation given point list x and its image y
def calculate(x, y, args, env):
	if len(x) == 0 or len(y) == 0:
		# no point: identity matrix and null translation
		((a,b,c,d), (t0, t1)) = ((1,0,0,1), (0,0))

	elif args.icp:
		# run icp algorithm
		((a,b,c,d), (t0, t1)) = calculate_icp(x, y, env)

	elif len(x) == 1:
		# one point: just a translation
		t0 = y[0][0] - x[0][0]
		t1 = y[0][1] - x[0][1]
		a,b,c,d = (1,0,0,1) # identity matrix

	elif len(x) == 2 or args.similitude:
		# two points: translation + rotation + dilation using last two points
		((a,b,c,d), (t0, t1)) = calculate_similitude(x[-2:],y[-2:])

	elif len(x) == 3 or args.exact_affine:
		# three points: affine transformation, solve system using last three points
		((a,b,c,d), (t0, t1)) = calculate_exact_affine(x[-3:],y[-3:])

	elif len(x) > 3:
		# more than three points: affine using linear regression
		((a,b,c,d), (t0, t1)) = calculate_best_affine(x,y)

	return ((a,b,c,d), (t0, t1))

# print numerical values of registered points
def print_points(m, t, X, Y):
	(a,b,c,d), (t0,t1) = m, t
	print('checking transfo:')
	print(' src_x', ' src_y', '  reg_x', '  reg_y', '  tgt_x', '  tgt_y  ')
	for (x0,x1),(y0,y1) in zip(X,Y):
		z0 = a * x0 + c * x1 + t0
		z1 = b * x0 + d * x1 + t1
		print('  ', x0, '  ', x1, '  ', z0, '  ', z1, '  ', y0, '  ', y1, '  ')
