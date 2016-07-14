import sys
sys.path.append('../../')
from acalib import *
from acalib.cupid import clumpfind


"""
loading data
"""
binpath = '../../../bindata/fits/cubes/'

# Data from ALMA science verification 
orion_path = binpath + 'Orion.methanol.cbc.contsub.image.fits'
container = load_fits(orion_path)
orion = container.primary


data3D = orion.data.astype(np.float64)
rms3D = np.sqrt((data3D*data3D).sum()/data3D.size)

data2D = data3D.sum(axis=0)
rms2D = np.sqrt((data2D*data2D).sum()/data2D.size)


"""
CUPID's clumpfind call
"""
ret = []
for i in range(100):
    ret.append(clumpfind(data2D, dict(), rms2D).max())
print ret
