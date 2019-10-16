from PIL import Image
from functools import reduce

img = Image.open('img/text.png')
width, height = img.size
sidelength = max(width, height)
# HERE REFRAME IMAGE SO IT IS SQUARE
width = min(width,height)
height=min(width,height)

black = (0,0,0, 255)

num_proj = 5		# number of projections

def get_rays(k, num_proj):
	if k == 0:
		return [[(x,y) for x in range(width)] for y in range(height)]
	elif k == 2:
		return [[(x,y) for y in range(height)] for x in range(width)]
	elif k == 1:
		return [[(j-x,x) for x in range(j+1)] for j in range(width)] + [[(width-x,j+x) for x in range(height-j)] for j in range(1,height)]
	elif k == 3:
		return [[(x,j+x) for x in range(height-j)] for j in range(height)] + [[(j+x,x) for x in range(width-j)] for j in range(1,width)]
	else:
		assert False, "get_rays(): out of bounds"

# def get_ray(k, num_proj):
# 	if k == 0 or k == 4:
# 		return [(x,0) for x in range(sidelength)]
# 	elif k == 2:
# 		return [(0,y) for y in range(sidelength)]
# 	elif k == 1:
# 		return [(-x, x) for x in range(sidelength)]
# 	elif k == 3:
# 		return [(x,sidelength-1+x) for x in range(sidelength)]
	

def get_proj_size(k):
	if k in [0, 2, 4]:
		return sidelength
	elif k in [1, 3]:
		return 2*sidelength-1
	assert False, "get_proj_size(): out of bounds"

# def get_incr(k):
# 	return get_incr.l[k]
# get_incr.l = [(0,1), (1,0), (1,0), (0,-1), (0,1)]

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
lst_of_lst_of_rays = [get_rays(k, num_proj) for k in range(num_proj-1)]
for k,lst_of_rays in enumerate(lst_of_lst_of_rays):
	for j,ray in enumerate(lst_of_rays):
		if len(ray) == 0:
			print('This ray has no pixels: k=', k, 'j=', j)
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

for proj in lst_of_projections:
	print(proj)
# make nice display with original image and projections
#display1 = build_projection_drawing(img, lst_of_projections)
#dislay1.save('out/display1.png')

# RECONSTRUCT IMAGE
newimg = Image.new('RGBA', (sidelength, sidelength))
newimg.save('out/blankimg.png')
print('pixels from blank img:')
for coord in [(0,0), (12,20), (sidelength-1,sidelength-1)]:
	print(newimg.getpixel(coord))


newdata = [[(0,0,0,255) for x in range(width)] for y in range(height)]

for k, (lst_of_rays, proj) in enumerate(zip(lst_of_lst_of_rays, lst_of_projections)):
	for ray,pixel in zip(lst_of_rays, proj):
		for (x,y) in ray:
			#newpixel = addpixels(pixel,getpixel(newimg,(x,y)))
			#putpixel(newimg, (x,y), newpixel
			if 0 <= x and x < width and 0 <= y and y < height:
				newdata[y][x] = addpixels(pixel, newdata[y][x])

#newdata = [[(r//(num_proj-1), g//(num_proj-1), b//(num_proj-1), 255) for (r,g,b,a) in [newdata[y][x]] for x in range(width)] for y in range(height)]
newdata_aslist = [(r//(num_proj-1), g//(num_proj-1), b//(num_proj-1), 255) for row in newdata for (r,g,b,a) in row]
#newimg.paste(newdata, box=(0,width,0,height))
newimg.putdata(newdata_aslist)
# for k,(ray0, proj) in enumerate(zip(lst_of_rays, lst_of_projections)):
# 	incrx, incry = get_incr(k)
# 	for (x,y) in ray0:
# 		for pixel in proj:
# 			newpixel = addpixels(pixel, getpixel(newimg,(x,y)))
# 			putpixel(newimg, (x,y), newpixel)
# 			x += incrx
# 			y += incry

print('pixels from reconstructed image:')
for coord in [(0,0), (12,20), (sidelength-1,sidelength-1)]:
	print(newimg.getpixel(coord))
newimg.save('out/newsquare.png')

## TODO :
##  - replace sum with averages
##  - make sure adding pixels works correctly with RGB
##  - write functions get_ray(), get_incr(), get_angle()
##  - calculate background and remove it from new image
##  - reframe image so it is square
