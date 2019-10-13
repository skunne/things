#!/usr/bin/env python3

import pygame

import reg_args
import reg_transfo
import reg_io

source_img, target_img = reg_args.parse_args()

(
	size, width, height,
	screen,
	source_img,
	imgwidth, imgheight,
	target_img, reg_img,
	leftrect, rightrect, regrect
) = reg_io.init()

sourcepoints, targetpoints = reg_io.reset(screen, source_img, leftrect, target_img, rightrect)

while True:
	for event in pygame.event.get():
		# PRESS ESCAPE: QUIT
		if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			sys.exit()

		# PRESS BACKSPACE: RESET POINT LISTS AND REGISTRATION
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
			sourcepoints, targetpoints = reg_io.reset(screen, source_img, leftrect, target_img, rightrect)

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
			rotation,translation = reg_transfo.calculate(sourcepoints, targetpoints)
			(a,b,c,d), (t0, t1) = rotation, translation
			print('transfo:')
			print('  ', a, ' ', c, '  ', t0)
			print('  ', b, ' ', d, '  ', t1)
			reg_transfo.print_points(rotation, translation, sourcepoints, targetpoints)
			del reg_img
			reg_img = reg_transfo.apply(rotation, translation, source_img, imgwidth, imgheight)
			reg_io.update(screen, source_img, leftrect, target_img, rightrect, reg_img, regrect)


