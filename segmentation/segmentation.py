import numpy as np
import scipy.ndimage
from scipy.stats import norm
from scipy.signal import convolve2d
from PIL import Image

def save_as_black_and_white_image(matrix, filename):
	Image.fromarray((matrix * 255 / np.max(matrix)).astype('uint8')).save(filename)

def sobel(array, save=False):
	"apply horizontal and vertical Sobel partial derivative filter"
	# axis 0 is vertical, so it detects horizontal edges (E_h)
	# axis 1 is horizontal, so it detects vertical edges (E_v)
	sobel_horizontal_3d = scipy.ndimage.sobel(array[:,:,:3], axis=0)
	sobel_vertical_3d = scipy.ndimage.sobel(array[:,:,:3], axis=1)

	# aggregate 3 channels (RGB) by taking Euclidean distance sqrt(r^2 + g^2 + b^2)
	sobel_horizontal = np.linalg.norm(sobel_horizontal_3d, axis=2)
	sobel_vertical = np.linalg.norm(sobel_vertical_3d, axis=2)

	if save:
		save_as_black_and_white_image(sobel_horizontal, 'sobel_h.png')
		save_as_black_and_white_image(sobel_vertical, '.sobel_v.png')

	return sobel_horizontal, sobel_vertical

def salience(sobel_horizontal, sobel_vertical, save=False):
	"Salience of Sobel partial derivatives"
	window_w = 3
	window_size = 2 * window_w + 1

	# construct half-aware neighbor structure
	kernel_average_u = np.zeros((window_size, window_size))
	kernel_average_u[0:window_w,0:window_size] = 1
	kernel_average_u[window_w,window_w] = 1
	kernel_average_u /= window_w * window_size + 1

	# construct other 3 kernels
	kernel_average_d = kernel_average_u[::-1,...] # D is equivalent to U flipped upside down
	kernel_average_l = kernel_average_u.T # L is equivalent to transposed U
	kernel_average_r = kernel_average_d.T # R is equivalent to transposed D

	def __salience(matrix, kernel):
		matrix2 = matrix**2
		E_X = convolve2d(matrix, kernel, mode='same', boundary='symm')
		E_X2 = convolve2d(matrix2, kernel, mode='same', boundary='symm')
		SD_X = np.maximum(1, np.maximum(0, E_X2 - E_X**2)**0.5)
		Z = (matrix - E_X) / SD_X
		return norm.cdf(Z)

	salience_horizontal = np.maximum(__salience(sobel_horizontal, kernel_average_u),
								     __salience(sobel_horizontal, kernel_average_d))
	salience_vertical = np.maximum(__salience(sobel_vertical, kernel_average_l),
							       __salience(sobel_vertical, kernel_average_r))

	if save:
		save_as_black_and_white_image(salience_horizontal, 'salience_h.png')
		save_as_black_and_white_image(salience_vertical, 'salience_v.png')

	return salience_horizontal, salience_vertical

def edge_probility(salience_horizontal, salience_vertical):
	"Edge Probability" #TODO
	edge_prob_horizontal = salience_horizontal
	edge_prob_vertical = salience_vertical
	
	return edge_prob_horizontal, edge_prob_vertical

def line_probability(edge_prob_horizontal, edge_prob_vertical):
	"Probability that a given horizontal/vertical line contains edges"
	
	#line_prob_horizontal = np.exp(np.sum(np.log(salience_horizontal), axis=1))
	#line_prob_vertical = np.exp(np.sum(np.log(salience_vertical), axis=0))

	line_prob_horizontal = np.sum(edge_prob_horizontal, axis=1)
	line_prob_vertical = np.sum(edge_prob_vertical, axis=0)

	line_prob_horizontal = scipy.ndimage.gaussian_filter(line_prob_horizontal, 1, truncate=3.0)
	line_prob_vertical = scipy.ndimage.gaussian_filter(line_prob_vertical, 1, truncate=3.0)

	return line_prob_horizontal, line_prob_vertical

def candidate_boundary(line_prob_horizontal, line_prob_vertical):
	thr = 3
	delta = 0.5

	while True:
		HP = np.extract(line_prob_horizontal > np.mean(line_prob_horizontal) + thr * np.std(line_prob_horizontal), line_prob_horizontal)
		VP = np.extract(line_prob_vertical > np.mean(line_prob_vertical) + thr * np.std(line_prob_vertical), line_prob_vertical)
		if (len(HP) + 1) * (len(VP) + 1) <= 35:
			break
		elif len(HP) * len(VP) == 0 and max(len(HP), len(VP)) <= 23:
			break
		else:
			thr += delta
	
	is_border_horizontal = np.isin(line_prob_horizontal, HP)
	is_border_vertical = np.isin(line_prob_vertical, VP)

	border_horizontal = np.tile(np.array([is_border_horizontal]), (is_border_vertical.shape[0], 1)).T
	border_vertical = np.tile(np.array([is_border_vertical]), (is_border_horizontal.shape[0], 1))

	border = np.logical_or(border_horizontal, border_vertical).astype(int)
	cand_bound_horizontal = np.where(is_border_horizontal)
	cand_bound_vertical = np.where(is_border_vertical)

	return border, cand_bound_horizontal, cand_bound_vertical


def segmentation(array, depth=0, max_depth=6):
	array = array[:,:,:3] # detach A channel (RGB only)
	sobel_horizontal, sobel_vertical = sobel(array)
	salience_horizontal, salience_vertical = salience(sobel_horizontal, sobel_vertical)
	edge_prob_horizontal, edge_prob_vertical = edge_probility(salience_horizontal, salience_vertical)
	line_prob_horizontal, line_prob_vertical = line_probability(edge_prob_horizontal, edge_prob_vertical)
	border, cand_bound_horizontal, cand_bound_vertical = candidate_boundary(line_prob_horizontal, line_prob_vertical)

	result = np.copy(array)
	border_color = [0, 0, 0]
	border_color[depth % 3] = 255
	result[border == 1] = border_color

	index_is = np.append(np.insert(cand_bound_horizontal, 0, -1), array.shape[0])
	index_js = np.append(np.insert(cand_bound_vertical, 0, -1), array.shape[1])	

	if depth < max_depth:
		for left_i, right_i in list(zip(index_is[:-1], index_is[1:])):
			for left_j, right_j in list(zip(index_js[:-1], index_js[1:])):
				if right_i - left_i < 15 or right_j - left_j < 15:
					continue
				seg = segmentation(result[left_i+1:right_i,left_j+1:right_j], depth + 1, max_depth)
				result[left_i+1:right_i,left_j+1:right_j] = seg

	return result

import sys
import time

dataname = sys.argv[1]
image = Image.open('./sample_data/%s' % dataname) # Image mode should be 'RGB' or 'RGBA'
for i in range(6):
	ta = time.time()
	result = segmentation(np.array(image), max_depth=i)
	Image.fromarray(result.astype('uint8')).save('./sample_data/[%s]_result_depth_%d.png' % (dataname, i))
	tb = time.time()
	print("Segmentation of depth %d was done in %d seconds" % (i, tb - ta))
