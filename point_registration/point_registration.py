from PIL import Image
# from PIL import ImageDraw

# target_img = Image.open('a.png')
# source_img = Image.open('b.png')

import sys			# sys.exit()
import pygame		# user interaction

import numpy as np	# matrix inversion

pygame.init()

size = width, height = 1000, 1000
black = 0, 0, 0

screen = pygame.display.set_mode(size)

source_img = pygame.image.load("img/Coeur-190615.jpg")
imgwidth, imgheight = source_img.get_rect().size
target_img = pygame.image.load("img/640x410_coeligur-anti-stress-donneur.jpg")
reg_img = source_img.copy()
leftrect = source_img.get_rect() 	# position source img in topleft corner
rightrect = target_img.get_rect()
rightrect.right = width				# position target img in topright corner
regrect = leftrect.copy()			# initial position of registered image: topleft of target
#regrect.move_ip(200,200)

# solve the system of 2n equations:
#   (a c) (x[j]0) + (t0) = (y[j]0)
#   (b d) (x[j]1)   (t1)   (y[j]1)
#     j = 0 .. n-1

s0,s1 = 10000,10000

def calculate_transfo(x, y):
	if len(x) == 0:
		# no point: identity matrix and null translation
		return ((1,0,0,1), (0,0))
	elif len(x) == 1:
		# one point: just a translation
		t0 = y[0][0] - x[0][0]
		t1 = y[0][1] - x[0][1]
		a,b,c,d = (1,0,0,1) # identity matrix
	elif len(x) == 2:
		# two points: add condition (a b c d) x[0] + t = x[0] + t
		#   solve for a,c,t0
		t0 = y[0][0] - x[0][0]
		c = (y[1][0] - t0 - x[1][0]) / (x[1][1] - (x[1][0]*x[0][1])/x[0][0])
		a = 1 - (c * x[0][1] / x[0][0])
		#   solve for b, d, t1
		t1 = y[0][1] - x[0][1]
		b = (y[1][1]-y[0][1]+x[0][1]-x[1][1]) / (x[1][0] - (x[0][0]*x[1][1])/x[0][1])
		d = 1 - (b * x[0][0]) / x[0][1]
	elif len(x) >= 3:
		# three points: solve system exactly using only first three points
		print('x')
		print(x)
		print('y')
		print(y)
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

def apply_transfo(m, t, srcimg):
	(a,b,c,d), (t0,t1) = m, t
	srctxt = pygame.image.tostring(srcimg, 'RGBA')
	#print(srctxt)
	pilimg = Image.frombytes('RGBA', (imgwidth,imgheight), srctxt)
	square_transfo = np.array([[a,c,t0],[b,d,t1],[0,0,1]])
	square_invert_transfo = np.linalg.inv(square_transfo)
	rectangle_invert_transfo = square_invert_transfo.flatten()[:6]
	(a,c,t0,b,d,t1) = rectangle_invert_transfo
	print('inverse transfo:')
	print('  ', a, ' ', c, '  ', t0)
	print('  ', b, ' ', d, '  ', t1)
	newpilimg = pilimg.transform(
		(1000,1000),
		Image.AFFINE,
		data=rectangle_invert_transfo,
		resample=Image.BICUBIC
	)
	newtxt = newpilimg.tobytes()
	newimg = pygame.image.fromstring(newtxt, (1000,1000),'RGBA')
	return newimg


def check_if_transfo_is_correct(m, t, X, Y):
	(a,b,c,d), (t0,t1) = m, t
	print('checking transfo:')
	print('  ', 'x0', '   ', 'x1', '   ', 'z0', '   ', 'z1', '   ', 'y0', '   ', 'y1', '   ')
	for (x0,x1),(y0,y1) in zip(X,Y):
		z0 = a * x0 + c * x1 + t0
		z1 = b * x0 + d * x1 + t1
		print('  ', x0, '  ', x1, '  ', z0, '  ', z1, '  ', y0, '  ', y1, '  ')

screen.fill(black)
screen.blit(source_img, leftrect)
screen.blit(target_img, rightrect)
#screen.blit(reg_img, regrect)
pygame.display.flip()

sourcepoints = []
targetpoints = []

while True:
	for event in pygame.event.get():
		# PRESS ESCAPE: QUIT
		if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			sys.exit()

		# PRESS BACKSPACE: RESET POINT LISTS AND REGISTRATION
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
			sourcepoints = []
			targetpoints = []
			print('reset')
			screen.fill(black)
			screen.blit(source_img, leftrect)
			screen.blit(target_img, rightrect)
			pygame.display.flip()

		# CLICK: ADD POINT
		elif event.type == pygame.MOUSEBUTTONUP:
			#x, y = event.pos[0] + s0, event.pos[1] + s1
			x, y = event.pos
			if event.pos[0] < rightrect.left:
				print('src: ', event.pos)
				sourcepoints.append((x,y))
			else:
				print('tgt: ', event.pos)
				targetpoints.append((x,y))

		# PRESS ENTER: REGISTER IMAGES
		elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN) and len(sourcepoints) == len(targetpoints):
			print('points:')
			for (x0,x1),(y0,y1) in zip(sourcepoints, targetpoints):
				print('  ', x0,x1,' -> ',y0,y1)
			rotation,translation = calculate_transfo(sourcepoints, targetpoints)
			(a,b,c,d), (t0, t1) = rotation, translation
			#regrect.topleft = translation
			print('transfo:')
			print('  ', a, ' ', c, '  ', t0)
			print('  ', b, ' ', d, '  ', t1)
			check_if_transfo_is_correct(rotation, translation, sourcepoints, targetpoints)
			reg_img = apply_transfo(rotation, translation, reg_img)
			screen.fill(black)
			screen.blit(source_img, leftrect)
			screen.blit(target_img, rightrect)
			screen.blit(reg_img, regrect)
			pygame.display.flip()


