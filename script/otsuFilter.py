"""
@purpose: Feature extraction from Geotiff images
@author: Kemeng Liu
@contact: kemeng.liu@stud-mail.uni-wuerzburg.de
"""


import os
from glob import glob
import cv2


def ostuFilter(inpath, outpath):
    """Extract features using Ostu-filter of CV2 module.
    
    
    Parameters
    ----------
    inpath : string
        The path to the directory containing all input Geotiff files.
    outpath : string
        The path to the directory where the output files should be located.
    
    
    Returns
    -------
    A printed message indicating the location of the output files.
    """
    
    
    # List all images
    tiles = glob(os.path.join(inpath, '*'))
    
    for i in range(len(tiles)):
        
        # Read the fist band of image
        img = cv2.imread(tiles[i],0)
        
        # Otsu's thresholding after Gaussian filtering
        blur = cv2.GaussianBlur(img,(5,5),0)
        ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        # Write
        new_name = tiles[i].split(".")[0].split("\\")[-1]+"_ostu"+".tif"
        output = os.path.join(outpath, new_name)
        cv2.imwrite(output, th3)
        
    return print("The output files are located at ", outpath)

   
            
path_input = "C:/EAGLE/trace_gfz/tile_analysis/sample/input/vessel"  
path_output = "C:/EAGLE/trace_gfz/tile_analysis/sample/output/otsuFilter/vessel"

ostuFilter(inpath = path_input, outpath = path_output)