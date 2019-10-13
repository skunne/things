import argparse


def parse_args():
	parser = argparse.ArgumentParser(description="Register two images by clicking on points in both images.\n\ncommands:\n  ESC          Quit\n  CLICK        Add point\n  ENTER        Register the images\n  BACKSPACE    Reset all points.", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("--src", default="img/coeur.png", help="source image, to be registered on the target image")
	parser.add_argument("--tgt", default="img/640x410_coeligur-anti-stress-donneur.jpg", help="target image, onto which register the source image")
	args = parser.parse_args()
	return args.src, args.tgt