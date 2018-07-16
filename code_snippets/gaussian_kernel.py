"""
Apply a Gaussian filter on image
- dependency: numpy, scipy, pillow
"""

import numpy
import scipy.ndimage
from PIL import Image

image = Image.open('test.png') # Image mode should be 'RGB' or 'RGBA'
as_array = numpy.array(image)
for i in range(3):
	as_array[:,:,i] = scipy.ndimage.filters.gaussian_filter(as_array[:,:,i], 1, truncate=3.0)
Image.fromarray(as_array).save('result.png')
