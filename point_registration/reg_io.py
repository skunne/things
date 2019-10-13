import pygame

black = (0,0,0)

def init(src_img_name, tgt_img_name):
	pygame.init()

	size = width, height = 1000, 1000

	screen = pygame.display.set_mode(size)

	#source_img = pygame.image.load("img/coeur.png")
	source_img = pygame.image.load(src_img_name)
	imgwidth, imgheight = source_img.get_rect().size
	#target_img = pygame.image.load("img/640x410_coeligur-anti-stress-donneur.jpg")
	target_img = pygame.image.load(tgt_img_name)
	reg_img = source_img.copy()
	leftrect = source_img.get_rect() 	# position source img in topleft corner
	rightrect = target_img.get_rect()
	rightrect.right = width				# position target img in topright corner
	regrect = leftrect.copy()			# initial position of registered image: topleft of target
	return (
		size, width, height,
		screen,
		source_img,
		imgwidth, imgheight,
		target_img, reg_img,
		reg_img,
		leftrect, rightrect, regrect
	)

def reset(screen, source_img, leftrect, target_img, rightrect):
	sourcepoints = []
	targetpoints = []
	print('reset')
	screen.fill(black)
	screen.blit(source_img, leftrect)
	screen.blit(target_img, rightrect)
	pygame.display.flip()
	return sourcepoints, targetpoints

def update(screen, source_img, leftrect, target_img, rightrect, reg_img, regrect):
	screen.fill(black)
	screen.blit(source_img, leftrect)
	screen.blit(target_img, rightrect)
	screen.blit(reg_img, regrect)
	pygame.display.flip()


