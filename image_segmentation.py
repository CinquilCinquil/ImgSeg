import numpy as np
from PIL import Image # Python library for image processing

from util import *  # Local library of utility functions


def spectral_segmentation(img, smallest_segment_size = 256):
	
	""" 
	Given an image, this algorithm returns a binary tree of partitions
	with the objective of highlighting elements present on it.
	
	The partition is a set of sets of pixel ids.
	A pixel id is the index of a pixel in an image counting from 
	left to right, top to bottom.
	
	This algorithm relies on knowledge from the field of 
	Spectral Graph Theory and was heavely inspired on the algorithm
	shown in the following paper:
	
	'Spectral Image Segmentation using Image Decomposition and
	Inner Product-based metric'.
	
	By Wallace Casaca et al.
	"""
	
	### Extracting data from image
	
	# image dimensions w,h and number n of pixels
	w, h = img.size
	n = w * h
	
	# w by h matrix with pixel values
	I_ = [[get_value(img.getpixel((j, i))) for j in range(w)] for i in range(h)]
	
	# w by h matrix with gradient values
	grad = define_grad(I_)
	
	# all necessary data extracted, image not needed anymore
	img.close()
	
	### Local utility functions
	
	# returns the image coordinates (i.e. (x, y)) from a pixel id
	def coord(p):
		return (int(p - w*(p//w)), int(p//w))
	
	# returns the pixel value from a pixel id
	def value_at(p):
		j, i = coord(p)
		return I_[i][j]
		
	# returns the gradient value from a pixel id
	def grad_at(p):
		j, i = coord(p)
		return grad[i][j]
	
	# --- Initializing algorithm ---
	
	### Converting image to graph
	
	V = [i for i in range(n)] # Vertices
	E = [] # Edges
	
	# creating horizontal edges
	for i in range(h):
		for j in range(w - 1):
			E.append((j + w*i, j + w*i + 1))
	
	# creating vertical edges
	for i in range(w):
		for j in range(h - 1):
			E.append((i + w*j, i + w*(j + 1)))
			
	# creating diagonal edges
	for i in range(h - 1):
		for j in range(w - 1):
			E.append((j + w*i, j + w*(i + 1) + 1)) # \
			E.append((j + w*(i + 1), j + w*i + 1)) # /
	
	## Calculating edge weights
	
	Ew = [] # List of edges with weights
	
	for i in range(len(E)):
		a, b = E[i]
		
		va = value_at(a)
		vb = value_at(b)
		
		# normalized vector ab
		dab = ( vb - va )/( (np.dot(va, vb))**(1/2) )
		
		# directional derivative of a and b
		d1 = np.dot(grad_at(a), dab)
		d2 = np.dot(grad_at(b), dab)
		
		g = np.max([d1, d2, 0])
		nn = 0.00001 #tuning parameter
		
		weight = 1/(1 + nn*g*g)
		
		Ew.append((a, b, weight))
	
	### Recursively partitioning graph
	
	def recursive_partition(V, depth = 0):
	
		n = len(V)
		
		if n <= smallest_segment_size:
			return V
	
		## Calculate Laplacian Matrix
		
		L = [[0 for j in range(n)] for i in range(n)]
		
		for e in Ew:
			a, b, weight = e
			
			if a in V and b in V:
				a_, b_ = (V.index(a), V.index(b))
				L[a_][b_] = -weight
				L[b_][a_] = -weight
		
		# weights in the diagonals
		for i in V:
			l = [(e[2] if i in (e[0], e[1]) else 0) for e in Ew]
			i_ = V.index(i)
			L[i_][i_] = np.sum(l)
			
		## Calculate L's Fiedler Vector
		
		eigen_values, eigen_vectors = np.linalg.eigh(L)
		F = eigen_vectors[:, 1]
		
		## Partition
		
		s_plus = [] #vertices that are associated with a non negative value in F
		s_minus = [] #vertices that are associated with a negative value in F
		
		# value that represents how evenly matched the distribution is
		dif = abs( abs(np.max(F)) - abs(np.min(F)) )
		
		# stopping recursion if the distribution is evenly matched
		# i.e. there likely is no element in the current part
		if dif < 0.01 and depth > 0:
			return V
		
		# distributing vertices in their respective parts
		for i in V:
			if F[V.index(i)] < 0:
				s_minus.append(i)
			else:
				s_plus.append(i)
		
		return [recursive_partition(s_minus, depth + 1), recursive_partition(s_plus, depth + 1)]
	
	return recursive_partition(V)

def draw_segmentation(filename, borders):

	I = Image.open(filename)
	w, h = I.size

	for v in borders:
		j, i = (int(v - w*(v//w)), int(v//w)) # image coordinates
		I.putpixel((j, i), (255, 0, 0))

	new_name = filename.replace(".png", '') + "_partioned.png"

	I.save(new_name)
	I.close()
	
	return new_name

def image_segmentation(filename, smallest_segment_size = 256):

	# loading image as matrix of pixels
	I = Image.open(filename)
	w_, h_ = I.size
	
	# generating coarsed image for faster processing
	I_coarsed = coarse_image(I)
	w, h = I_coarsed.size
	
	graph_partition = spectral_segmentation(I_coarsed, smallest_segment_size)
	
	# scaling partition to original image dimensions
	scaled_partition = scale_partition(graph_partition, w, h, w_, h_)
	
	borders = find_borders(scaled_partition, w_, h_)
	
	return draw_segmentation(filename, borders) #saving copy of image with borders drawn
