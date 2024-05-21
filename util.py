import numpy as np
from PIL import Image # Python library for image processing
from scipy import ndimage

def get_value(t):

	"""
	Returns the value of a pixel as a 2D array
	"""

	return np.array([t[0] + 1, t[1] + 1])
	
def define_grad(img):

	"""
	Returns matrix G of gradients based on the image
	"""

	w,h = img.size

	# get x-gradient
	sx = ndimage.sobel(img, axis=0, mode='constant')

	# get y-gradient
	sy = ndimage.sobel(img, axis=1, mode='constant')

	G = [[(

		100 * np.dot(sx[i][j], sx[i][j]), 100 * np.dot(sy[i][j], sy[i][j])
		
		) for j in range(w)] for i in range(h)]
	
	return G
		
def find_borders(S, w, h):

	"""
	Returns the borders of a partition of S
	"""
	
	# Local utils
	
	# returns the image coordinates (i.e. (x, y)) from a pixel id
	def coord(v):
		return (int(v - w*(v//w)), int(v//w))
	
	# returns whether a and b are in different parts
	def dif(a, b):
		a = a[0] + a[1]*w # converting back to pixel id
		return any([(a in s and b not in s) for s in S])
	
	# returns if pixel is in a border
	def in_border(v):
		i, j = coord(v)
		
		# checking if any of he neighbours are in different parts
		val_right = 		dif((i + 1, j), v) if i < w - 1 else False
		val_left = 			dif((i - 1, j), v) if i > 0 else False
		val_top = 			dif((i, j - 1), v) if j > 0 else False
		val_bottom = 		dif((i, j + 1), v) if j < h - 1 else False
		val_upright = 		dif((i + 1, j - 1), v) if j > 0 and i < w - 1 else False
		val_upleft = 		dif((i - 1, j - 1), v) if j > 0 and i > 0 else False
		val_bottomright = 	dif((i + 1, j + 1), v) if j < h - 1 and i < w - 1 else False
		val_bottomleft = 	dif((i - 1, j + 1), v) if j < h - 1 and i > 0 else False
		
		return (val_right or val_left or val_top or val_bottom or val_bottom or val_upright or val_upleft
				or val_bottomright or val_bottomleft)

	# Initializing algorithm

	borders = []
	for i in range(w*h):
		if in_border(i):
			borders.append(i)

	return borders
	
def coarse_image(I, new_h = 32):

	"""
	Returns image with lower resolution using Bicubic Interpolation
	"""
	
	w, h = I.size
	
	new_w = int(new_h * (w/h))
	
	return I.resize((new_w, new_h), Image.BICUBIC)
	
def scale_partition(S, old_w, old_h, w, h):

	"""
	Returns partition scaled up
	"""

	# Turning tree into a list of parts
	parts = []
	
	def flatten(S):
	
		# arrived at a leaf
		if not isinstance(S[0], list):
			parts.append(S)
			return
		
		for s in S:
			flatten(s)
			
	flatten(S)

	S_new = [[] for i in range(len(parts))] # partition to be returned
	
	# adds pixels to new partition considering old partition
	def add_to_part(new_p, old_p):

		for i in range(len(parts)):
			if old_p in parts[i]:
				S_new[i].append(new_p)
				break

	w_r = w / old_w
	h_r = h / old_h

	# adding new pixels considering a mapping from (old_w, old_h) to (w, h)
	for i in range(w):
		for j in range(h):
			i_ = int(i / w_r)
			j_ = int(j / h_r)
			
			add_to_part(i + j*w, i_ + j_*old_w)
	
	return S_new
	

def print_mat(I):
	
	"""
	Prints a matrix
	"""
	
	return_str = ""

	for i in range(len(I)):
		for j in range(len(I[i])):
			print(I[i][j], end = ' ')
			return_str += str(I[i][j]) + " "
		
		print("")
		return_str += "\n"
	
	print("")
	return_str += "\n"
	
	return return_str
	
def report(txt, report_list):
	print(txt)
	report_list.append(txt)

def create_report(report_list, img_name):
	img_name = img_name.split("/")[1]
	reportfile_name = "reports/report_for_" + img_name.replace(".png", '').replace(".jpg", '') + ".txt"
	
	report_file = open(reportfile_name, 'w', encoding = "utf-8")
	
	for t in report_list:
		report_file.write(t + "\n")
	report_file.close()
	
	return reportfile_name
	
