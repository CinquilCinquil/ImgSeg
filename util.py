import numpy as np
from PIL import Image # Python library for image processing


def get_value(t):

	"""
	Returns the value of a pixel as a 2D array
	"""

	return np.array([t[0] + 1, t[1] + 1])
	
def define_grad(A):

	"""
	Returns matrix G of gradients based on the values of matrix A
	"""

	w, h = (len(A[0]), len(A))

	G = [[0 for j in range(w)] for i in range(h)]

	# Local utils

	# returns the image coordinates (i.e. (x, y)) from a pixel id
	def coord(p):
		return (p - w*(p//w), p//w)
	
	# magnitude of 2D array v
	def mag(v):
		return (np.dot(v, v))**(1/2)
	
	# sums 2D arrays in a list
	def sumv(l):
		s = np.array((0, 0))
		for v in l:
			s = s + v
		return s

	# calculating the gradient for each value
	for i in range(h):
		for j in range(w):
		
			v = A[i][j]
	
			# the gradient is based on the neighbouring values
			val_right = 		mag(A[i + 1][j] - v) if i < w - 1 else 0
			val_left = 			mag(A[i - 1][j] - v) if i > 0 else 0
			val_top = 			mag(A[i][j - 1] - v) if j > 0 else 0
			val_bottom = 		mag(A[i][j + 1] - v) if j < h - 1 else 0
			val_upright = 		mag(A[i + 1][j - 1] - v) if j > 0 and i < w - 1 else 0
			val_upleft = 		mag(A[i - 1][j - 1] - v) if j > 0 and i > 0 else 0
			val_bottomright = 	mag(A[i + 1][j + 1] - v) if j < h - 1 and i < w - 1 else 0
			val_bottomleft = 	mag(A[i - 1][j + 1] - v) if j < h - 1 and i > 0 else 0
			
			# vectors representing the variation's direction
			vec_right = 		(val_right, 0)
			vec_left = 			(-val_left, 0)
			vec_top = 			(0, -val_top)
			vec_bottom = 		(0, val_bottom)
			vec_upright = 		(val_upright/2, -val_upright/2)
			vec_upleft = 		(-val_upleft/2, -val_upleft/2)
			vec_bottomright = 	(val_bottomright/2, val_bottomright/2)
			vec_bottomleft = 	(-val_bottomleft/2, val_bottomleft/2)
		
			# the total gradient is the sum of the variations in their respective directions
			G[i][j] = sumv([vec_right, vec_left, vec_top, vec_bottom,
						vec_upleft, vec_upright, vec_bottomright, vec_bottomleft])
						
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
	
def coarse_image(I, new_w = 32):

	"""
	Returns image with lower resolution using Bicubic Interpolation
	"""
	
	w, h = I.size
	
	new_h = int(new_w * (h/w))
	
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

	w_r = w // old_w
	h_r = h // old_h

	# adding new pixels considering a mapping from (old_w, old_h) to (w, h)
	for i in range(w):
		for j in range(h):
			i_ = i // w_r
			j_ = j // h_r
			
			add_to_part(i + j*w, i_ + j_*old_w)
	
	return S_new
	

def print_mat(I):
	
	"""
	Prints a matrix
	"""

	for i in range(len(I)):
		for j in range(len(I[i])):
			print(I[i][j], end = ' ')
		print("")
	print("")
