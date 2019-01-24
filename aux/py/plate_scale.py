import os 
import numpy as np
import pylab as pl


dat     = np.loadtxt(os.environ['DESIMODEL'] + '/focalplane/platescale.txt') 
wdat    = dat[:,0]

## Assume MPS == SPS 
pscale  = dat[:,6]

## Find radius where DESI ratio to centre is 10%.
index   = np.where(np.abs(pscale / pscale[0] - 1.1).min() == np.abs(pscale / pscale[0] - 1.1))

##  Normalise to platescale to 90.9 at origin.
pscale *= 90.9 / pscale[0]
wdat   *= 224. / wdat[index]

print(pscale[index] / pscale[0])

##  Assume radial and azimuthal platescale are the same.
output  = np.c_[wdat[wdat <= 225.], pscale[wdat <= 225.], pscale[wdat <= 225.]]

np.savetxt(os.environ['AUX'] + '/platescale-pfs.txt', output, header='# Radius [mm], Radial platescale [um/arcsec], Azimuthal platescale [um/arcsec]', fmt='%.6lf')

pl.plot(wdat[wdat <= 225.], pscale[wdat <= 225.])
pl.xlabel(r'$Radius \ [mm]$')
pl.ylabel(r'Plate scale $[\mu \rm{m/arcsec}]$')
pl.savefig(os.environ['AUX'] + '/plots/platescale.pdf')

