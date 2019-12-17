#!/usr/bin/env python3

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

import sys			# sys.exit()
import pygame		# handle pygame events: interaction with user
from time import sleep	# because infinite loops make my computer overheat

import reg_args		# parse arguments
import reg_transfo	# calculate and apply transformation
import reg_io		# display images to screen

# parse arguments and get filenames for two images
src_img_name, tgt_img_name, args = reg_args.parse_args()

# init screen and everything pygame-related
env = reg_io.Env(src_img_name, tgt_img_name)

# (
# 	size, width, height,
# 	screen,
# 	source_img,
# 	imgwidth, imgheight,
# 	target_img, reg_img,
# 	reg_img,
# 	leftrect, rightrect, regrect
# ) = reg_io.init(src_img_name, tgt_img_name)
#env = reg_io.init(src_img_name, tgt_img_name)

# display images
sourcepoints, targetpoints = env.reset()
#sourcepoints, targetpoints = reg_io.reset(screen, source_img, leftrect, target_img, rightrect)

while True:
	sleep(0.05)
	for event in pygame.event.get():
		# PRESS ESCAPE: QUIT
		if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			sys.exit()

		# PRESS BACKSPACE: RESET POINT LISTS AND REGISTRATION
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
			sourcepoints, targetpoints = env.reset()#reg_io.reset(screen, source_img, leftrect, target_img, rightrect)

		# PRESS DEL: RESET POINTS BUT NOT REGISTRATION
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
			sourcepoints, targetpoints = [], []

		# CLICK: ADD POINT
		elif event.type == pygame.MOUSEBUTTONUP:
			#x, y = event.pos[0] + s0, event.pos[1] + s1
			x, y = event.pos
			if event.pos[0] < env.rightrect.left:
				print('src: ', event.pos)
				sourcepoints.append((x,y))
			else:
				print('tgt: ', event.pos)
				targetpoints.append((x,y))

		# PRESS ENTER: REGISTER IMAGES
		elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN) and (len(sourcepoints) == len(targetpoints) or args.icp):
			rotation,translation = reg_transfo.calculate(sourcepoints, targetpoints, args, env)
			(a,b,c,d), (t0, t1) = rotation, translation
			if not args.icp:
				print('points:')
				for (x0,x1),(y0,y1) in zip(sourcepoints, targetpoints):
					print('  ', x0,x1,' -> ',y0,y1)
				print('transfo:')
				print('  ', a, ' ', c, '  ', t0)
				print('  ', b, ' ', d, '  ', t1)
				reg_transfo.print_points(rotation, translation, sourcepoints, targetpoints)
				del env.reg_img
				env.reg_img = reg_transfo.apply(rotation, translation, env.source_img, env.imgwidth, env.imgheight)
				#reg_io.update(screen, source_img, leftrect, target_img, rightrect, reg_img, regrect)
				env.update()#reg_io.update(env)
