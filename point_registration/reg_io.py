
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

import pygame

black = (0,0,0)

class Env:
	def __init__(self, src_img_name, tgt_img_name):
		pygame.init()

		self.size = self.width, self.height = 1000, 1000

		self.screen = pygame.display.set_mode(self.size)

		#source_img = pygame.image.load("img/coeur.png")
		self.source_img = pygame.image.load(src_img_name)
		self.imgwidth, self.imgheight = self.source_img.get_rect().size
		#target_img = pygame.image.load("img/640x410_coeligur-anti-stress-donneur.jpg")
		self.target_img = pygame.image.load(tgt_img_name)
		self.reg_img = self.source_img.copy()
		self.leftrect = self.source_img.get_rect() 	# position source img in topleft corner
		self.rightrect = self.target_img.get_rect()
		self.rightrect.right = self.width				# position target img in topright corner
		self.regrect = self.leftrect.copy()			# initial position of registered image: topleft of target

	def reset(self):
		sourcepoints = []
		targetpoints = []
		print('reset')
		self.screen.fill(black)
		self.screen.blit(self.source_img, self.leftrect)
		self.screen.blit(self.target_img, self.rightrect)
		pygame.display.flip()
		return sourcepoints, targetpoints

	def update(self):#screen, source_img, leftrect, target_img, rightrect, reg_img, regrect):
		self.screen.fill(black)
		self.screen.blit(self.source_img, self.leftrect)
		self.screen.blit(self.target_img, self.rightrect)
		self.screen.blit(self.reg_img, self.regrect)
		pygame.display.flip()

# def init(src_img_name, tgt_img_name):
# 	pygame.init()

# 	size = width, height = 1000, 1000

# 	screen = pygame.display.set_mode(size)

# 	#source_img = pygame.image.load("img/coeur.png")
# 	source_img = pygame.image.load(src_img_name)
# 	imgwidth, imgheight = source_img.get_rect().size
# 	#target_img = pygame.image.load("img/640x410_coeligur-anti-stress-donneur.jpg")
# 	target_img = pygame.image.load(tgt_img_name)
# 	reg_img = source_img.copy()
# 	leftrect = source_img.get_rect() 	# position source img in topleft corner
# 	rightrect = target_img.get_rect()
# 	rightrect.right = width				# position target img in topright corner
# 	regrect = leftrect.copy()			# initial position of registered image: topleft of target
# 	return (
# 		size, width, height,
# 		screen,
# 		source_img,
# 		imgwidth, imgheight,
# 		target_img, reg_img,
# 		reg_img,
# 		leftrect, rightrect, regrect
# 	)

# def reset(screen, source_img, leftrect, target_img, rightrect):
# 	sourcepoints = []
# 	targetpoints = []
# 	print('reset')
# 	screen.fill(black)
# 	screen.blit(source_img, leftrect)
# 	screen.blit(target_img, rightrect)
# 	pygame.display.flip()
# 	return sourcepoints, targetpoints

# def update(screen, source_img, leftrect, target_img, rightrect, reg_img, regrect):
# 	screen.fill(black)
# 	screen.blit(source_img, leftrect)
# 	screen.blit(target_img, rightrect)
# 	screen.blit(reg_img, regrect)
# 	pygame.display.flip()
