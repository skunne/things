usage: main.py [-h] [-s SRC] [-t TGT]
               [--icp | --affine3 | --affine | --similitude]

Register two images by clicking on points in both images.

commands:
  ESC          Quit
  CLICK        Add point
  ENTER        Register the images
  DELETE       Reset all points
  BACKSPACE    Reset all points and erase registration.

optional arguments:
  -h, --help         show this help message and exit
  -s SRC, --src SRC  source image, to be registered on the target image
  -t TGT, --tgt TGT  target image, onto which register the source image
  --icp              use Iterative Closest Point algorithm
  --affine3          find affine transformation using only last three points
  --affine           find affine transformation by linear regression
  --similitude       find translation+rotation+dilation using only last 2 points

Unless the ICP algorithm is used, the number of points in the source and target image must coincide, and points will be matched one-to-one in the order they were given.

