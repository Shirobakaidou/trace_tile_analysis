# trace_tile_analysis

This repository presents the following approaches to extract features from satellite image tiles:
<br>
1. __Thresholding__ Method: Based on histogram of pixel values, the pixels of 2.5% highest values are extracted as masks.
2. __Ostu-Filter__: This is a built-in function of "cv2" package. (reference: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#otsus-binarization) *It's noteworthy that "cv2" doesn't support georeferencing images.*

<br>

### Usage

1. **Clone this repository to local**
2. *Place input image tiles into a directory.* please don't put the images tiles into any subdirectory.
3. *Modify the `input_path` and `output_path` in the python script of each approach.* Let the `input_path` be the path to the directory containing input image tiles.

<br>
Some pre- and post-processing sample data is located in `/sample`; the python scripts and jupyter notebooks of each approach can be found in `/script`
