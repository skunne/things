import numpy as np	# solve lin equation
import math			# solve trig equation

from PIL import Image	# apply transfo to image
import pygame.image		# apply transfo to image

# calculate transformation given point list x and its image y
def calculate(x, y):
	if len(x) == 0:
		# no point: identity matrix and null translation
		((a,b,c,d), (t0, t1)) = ((1,0,0,1), (0,0))
	elif len(x) == 1:
		# one point: just a translation
		t0 = y[0][0] - x[0][0]
		t1 = y[0][1] - x[0][1]
		a,b,c,d = (1,0,0,1) # identity matrix
	elif len(x) == 2:
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
		# # two points: add condition (a b c d) x[0] + t = x[0] + t
		# #   solve for a,c,t0
		# t0 = y[0][0] - x[0][0]
		# c = (y[1][0] - t0 - x[1][0]) / (x[1][1] - (x[1][0]*x[0][1])/x[0][0])
		# a = 1 - (c * x[0][1] / x[0][0])
		# #   solve for b, d, t1
		# t1 = y[0][1] - x[0][1]
		# b = (y[1][1]-y[0][1]+x[0][1]-x[1][1]) / (x[1][0] - (x[0][0]*x[1][1])/x[0][1])
		# d = 1 - (b * x[0][0]) / x[0][1]
	elif len(x) >= 3:
		# three points: affine transformation, solve system using first three points
		y = np.array(y[:3])
		x = np.concatenate((np.array(x[:3]), np.array([[1],[1],[1]])), axis=1)
		bdt = np.linalg.solve(x, y[:,1])
		act = np.linalg.solve(x, y[:,0])
		b,d,t1 = bdt[0], bdt[1], bdt[2]
		a,c,t0 = act[0], act[1], act[2]
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
	return ((a,b,c,d), (t0, t1))

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

# print numerical values of registered points
def print_points(m, t, X, Y):
	(a,b,c,d), (t0,t1) = m, t
	print('checking transfo:')
	print(' src_x', ' src_y', '  reg_x', '  reg_y', '  tgt_x', '  tgt_y  ')
	for (x0,x1),(y0,y1) in zip(X,Y):
		z0 = a * x0 + c * x1 + t0
		z1 = b * x0 + d * x1 + t1
		print('  ', x0, '  ', x1, '  ', z0, '  ', z1, '  ', y0, '  ', y1, '  ')


