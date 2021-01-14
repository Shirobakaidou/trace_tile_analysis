"""
@purpose: Feature extraction from Geotiff images
@author: Kemeng Liu
@contact: kemeng.liu@stud-mail.uni-wuerzburg.de
"""


import os
from glob import glob
import numpy as np
from scipy import ndimage, stats
import rasterio


def thdFilter(inpath, outpath):
    """From each input image tile, extract a mask from pixels 
    of the highest 2.5% of the histogram of pixel values, and 
    output the binary masks as Geotiff files.
    
    
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


    # Function to get z-score
    def normalize(img):
        z_score = np.zeros(img.shape)
        for i in range(0, len(img)):
            mu = float(img[i].mean())
            sigma = float(img[i].std())
            z_score[i] = (img[i]-mu)/sigma
        return z_score
    
    # Function to get statistical Mode of numpy array
    def getMode(x):
        return float(stats.mode(x)[0])
            
        
    # List Files
    tiles = glob(os.path.join(inpath, '*'))
    
    for j in range(len(tiles)):
        # Read Raster Files
        with rasterio.open(tiles[j]) as src:
            img = src.read()
            kwargs = src.meta.copy()
        
        # 1. Standardize Image
        img_nor = normalize(img)
        
        
        # 2. Reclassify with threshold 97.5% (z-score >1.96)
        binary = np.where(img_nor > 1.96, 1, 0)
        # Select only One Band
        binary = binary[0]
        
        
        # 3. Spatial Filter (3x3, mode)
        # Apply 3x3 spatial filter (moving window)
        binary_flt = ndimage.generic_filter(binary, function=getMode, size=3)
        
        
        # 4. Export Filtered Raster
        binary_flt = binary_flt.astype('uint8')
        # Update Metadata
        kwargs.update({
            "driver": "GTiff",
            "count": 1,
            "height": binary_flt.shape[0],
            "width": binary_flt.shape[1],
            "transform": kwargs['transform'],
            "crs": kwargs['crs']
        })
        # Export Masked DEM
        outpath_msk = os.path.join(outpath, tiles[j].split('.')[0].split('\\')[-1]+"_msk.tif")
        with rasterio.open(outpath_msk, "w", **kwargs) as dest:
            dest.write(binary_flt, indexes=1)
            
    return print("The output files are located at ", outpath)

            
            
path_input = "C:/EAGLE/trace_gfz/tile_analysis/sample/input/vessel"  
path_output = "C:/EAGLE/trace_gfz/tile_analysis/sample/output/thdFilter/vessel"    
    
thdFilter(inpath=path_input, outpath=path_output)
