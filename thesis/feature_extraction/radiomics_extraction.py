# radiomics-based feature extraction

import numpy as np
import collections
import SimpleITK as sitk
from scipy.ndimage import zoom
import os,sys
import pandas as pd
import radiomics
from radiomics import featureextractor

# Hand-crafted radiomics

## Set GPU
#os.environ["CUDA_VISIBLE_DEVICES"]="0"

# Input data
imgDir = r'L:\basic\divi\jstoker\slicer_pdac\Master Students SS 23\Mattia\keras_feature_extraction'
dirlist = os.listdir(imgDir)[1:]
print(dirlist)

# read images in Nifti format 
def loadSegArraywithID(fold,iden):
    
    path = fold
    pathList = os.listdir(path)
    
    segPath = [os.path.join(path,i) for i in pathList if ('seg' in i.lower()) & (iden in i.lower())][0]
    seg = sitk.ReadImage(segPath)
    return seg
# read regions of interest (ROI) in Nifti format 
def loadImgArraywithID(fold,iden):
    
    path = fold
    pathList = os.listdir(path)
    
    imgPath = [os.path.join(path,i) for i in pathList if ('im' in i.lower()) & (iden in i.lower())][0]
    img = sitk.ReadImage(imgPath)    
    return img

# Feature Extraction
featureDict = {}
for ind in range(len(dirlist)):
    try:
        path = os.path.join(imgDir,dirlist[ind])

        # you can make your own pipeline to import data, but it must be SimpleITK images
        mask = loadSegArraywithID(path,'seg')  # see line 26 !
        img = loadImgArraywithID(path,'im')      # see line 35 !
        params = 'C://Users//mcintioli//Thesis_Project//feature_extraction//tumor.yaml'

        extractor = featureextractor.RadiomicsFeatureExtractor(params)

        result = extractor.execute(img,mask)
        key = list(result.keys())
        key = key[1:] 

        feature = []
        for jind in range(len(key)):
            feature.append(result[key[jind]])

        featureDict[dirlist[ind]] = feature
        dictkey = key
        print(dirlist[ind])
    
    except ValueError as e:
        print(path, "PASSED due to ValueError")
        print(e)
        pass

# Output  
dataframe = pd.DataFrame.from_dict(featureDict, orient='index', columns=dictkey)

#save directory
feature_dir = r"L:\basic\divi\jstoker\slicer_pdac\Master Students SS 23\Mattia\keras_feature_extraction_OUTPUT"
#dataframe.to_csv(feature_dir + "\\radiomics_features.csv")
