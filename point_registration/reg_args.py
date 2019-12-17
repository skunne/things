
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

import argparse


def parse_args():
	parser = argparse.ArgumentParser(
		description="Register two images by clicking on points in both images.\n\ncommands:\n  ESC          Quit\n  CLICK        Add point\n  ENTER        Register the images\n  DELETE       Reset all points\n  BACKSPACE    Reset all points and erase registration.",
		epilog='Unless the ICP algorithm is used, the number of points in the source and target image must coincide, and points will be matched one-to-one in the order they were given.',
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-s", "--src", default="img/coeur.png", help="source image, to be registered on the target image")
	parser.add_argument("-t", "--tgt", default="img/640x410_coeligur-anti-stress-donneur.jpg", help="target image, onto which register the source image")
	group_technique = parser.add_mutually_exclusive_group()
	group_technique.add_argument("--icp", action="store_true", help="use Iterative Closest Point algorithm")
	group_technique.add_argument("--affine3", action="store_true", help="find affine transformation using only last three points")
	group_technique.add_argument("--affine", action="store_true", help="find affine transformation by linear regression")
	group_technique.add_argument("--similitude", action="store_true", help="find translation+rotation+dilation using only last 2 points")
	args = parser.parse_args()
	return args.src, args.tgt, args
