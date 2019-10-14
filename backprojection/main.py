from PIL import Image

img = Image.open('img/square.png')
width, height = img.size
sidelength = max(width, height)
# HERE REFRAME IMAGE SO IT IS SQUARE

num_proj = 5		# number of projections

# COMPUTE PROJECTIONS
lst_of_projections = []
lst_of_rays = [get_ray(get_angle(k), k) for k in range(num_proj)]
for k,ray0 in enumerate(lst_of_rays):
	#alpha = get_angle(k)
	#ray0 = get_ray(alpha, k)
	incrx,incry = get_incr(k)
	proj = [sum((img.getpixel(x+incrx,y+incry) for (x,y) in ray0)) for j in range(sidelength)]
	lst_of_projections.append(proj)

# make nice display with original image and projections
display1 = build_projection_drawing(img, lst_of_projections)
dislay1.save('out/display1.png')

# RECONSTRUCT IMAGE
newimg = Image.new('RGB', (sidelength, sidelength))
for k,(ray0, proj) in enumerate(zip(lst_of_rays, lst_of_projections)):
	incrx, incry = get_incr(k)
	for (x,y) in ray0:
		for pixel in proj:
			newpixel = pixel + newimg.getpixel(x,y)
			newimg.putpixel(newpixel)
			x += incrx
			y += incry

newimg.save('out/newsquare.png')

## TODO :
##  - replace sum with averages
##  - make sure adding pixels works correctly with RGB
##  - write functions get_ray(), get_incr(), get_angle()
##  - calculate background and remove it from new image
##  - reframe image so it is square
