import time
import numpy as np
from PIL import Image # Python library for image processing

from util import *  # Local library of utility functions


report_list = [] # list of reports made during the program execution

def spectral_segmentation(img, smallest_segment_size = 256):
	
	""" 
	Given an image, this algorithm returns a binary tree of partitions
	with the objective of highlighting elements present on it.
	
	The partition is a set of sets of pixel ids.
	A pixel index is the index of a pixel in an image counting from 
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
	
	# w by h matrix with gradient values
	grad = define_grad(img)
	
	report("Matriz gradiente da imagem feita.", report_list)
	
	# all necessary data extracted, image not needed anymore
	img.close()
	
	### Local utility functions
	
	# returns the image coordinates (i.e. (x, y)) from a pixel index
	def coord(p):
		return (int(p - w*(p//w)), int(p//w))
		
	# returns the gradient value from a pixel index
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
			
	report("Grafo feito simples feito.", report_list)
	
	## Calculating edge weights
	
	Ew = [] # List of edges with weights
	
	for i in range(len(E)):
		a, b = E[i]
		
		# a and b coordinates
		ca = np.array(coord(a))
		cb = np.array(coord(b))
		
		# normalized vector ab
		d = cb - ca
		dab = d/((np.dot(d, d))**(1/2))
		
		# directional derivative of a and b
		d1 = np.dot(grad_at(a), dab)
		d2 = np.dot(grad_at(b), -dab)
		
		g = np.max([d1, d2, 0])
		nn = 0.00001 #tuning parameter
		
		weight = 1/(1 + nn*g*g)
		
		Ew.append((a, b, weight))
		
	report("Peso das arestas calculado.", report_list)
	
	### Recursively partitioning graph
	
	def recursive_partition(V, depth = 0):
	
		report("Executando partição recursiva: ", report_list)
	
		n = len(V)
		
		report("-- Tamanho da partição a ser analisada: " + str(n), report_list)
		
		if n <= smallest_segment_size:
		
			report("-- Partição pequena demais, caso base antigido.", report_list)
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
			
		report("-- Matriz Laplaciana criada:", report_list)
			
		## Calculate L's Fiedler Vector
		
		eigen_values, eigen_vectors = np.linalg.eigh(L)
		F = eigen_vectors[:, 1]
		
		report("-- Vetor de Fiedler calculado:", report_list)
		
		## Partition
		
		s_plus = [] #vertices that are associated with a non negative value in F
		s_minus = [] #vertices that are associated with a negative value in F

		# distributing vertices in their respective parts
		for i in V:
			if F[V.index(i)] < 0:
				s_minus.append(i)
			else:
				s_plus.append(i)
				
		report("-- Vetores particionados.", report_list)

		# checking if the next partition is too small
		if len(s_minus) <= 4 or len(s_plus) <= 4:
			return V
		else:
			return [recursive_partition(s_minus, depth + 1), recursive_partition(s_plus, depth + 1)]
	
	return recursive_partition(V)

def draw_segmentation(filename, borders):

	I = Image.open(filename)
	I = I.convert('RGB')
	w, h = I.size

	for v in borders:
		j, i = (int(v - w*(v//w)), int(v//w)) # image coordinates
		I.putpixel((j, i), (255, 0, 0))
		
	report("Bordas desenhadas.", report_list)

	# saving the image

	filename = filename.split("/")[-1]
	new_name = to_filename(filename, path = "results", sufix = "_partitioned", filetype = ".png")

	I.save(new_name)
	I.close()
	
	report("Imagem final salva.", report_list)
	
	return new_name

def image_segmentation(filename, smallest_segment_size = 256):

	start_time = time.time()
	report("Timer inicializado.", report_list)

	# loading image as matrix of pixels
	I = Image.open(filename)
	I = I.convert('RGB')
	w_, h_ = I.size
	
	report("Imagem aberta.", report_list)
	
	# generating coarsed image for faster processing
	I_coarsed = coarse_image(I)
	w, h = I_coarsed.size
	
	report("Imagem em menor resolução feita.", report_list)
	
	graph_partition = spectral_segmentation(I_coarsed, smallest_segment_size)
	
	report("Partição espectral do grafo feita.", report_list)

	# scaling partition to original image dimensions
	scaled_partition = scale_partition(graph_partition, w, h, w_, h_)
	
	report("Tamanho da partição aumentado para imagem original.", report_list)
	
	borders = find_borders(scaled_partition, w_, h_)
	
	report("Bordas das partições feitas.", report_list)
	
	#saving copy of image with borders drawn
	final_image_name = draw_segmentation(filename, borders)
	
	report("Execução finalizada após " + str((time.time() - start_time)) + " segundos.", report_list)
	
	return (final_image_name, create_report(report_list, final_image_name))
