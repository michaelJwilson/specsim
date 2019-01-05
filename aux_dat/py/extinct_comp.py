import numpy as np
import pylab as pl


plot  = True
save  = True

orig  = np.loadtxt('spectra/ZenithExtinction-KPNO.dat')

mkopt = np.loadtxt('MaunaKea_opt-skytrans.txt')
mknir = np.loadtxt('MaunaKea_nearir-skytrans_Airmass_1_Water_1mm.txt')

##  Convert wave[um] to [AA] and convert NIR from transmission to extinction. 
mknir[:,0] *= 1.e4
mknir[:,1]  = -2.5 * np.log10(mknir[:,1])
mknir[:,1][np.isfinite(mknir[:,1]) == False] = -99.

assert np.all(np.isfinite(mknir[:,1])) == True

##  Cut Optical at 1um.
mkopt  = np.c_[mkopt[:,0][mkopt[:,0] < 9.e3], mkopt[:,1][mkopt[:,0] < 9.e3]]

##  Cut to start from 1um.  Downsample NIR to 2A, as per Mauna Kea optical. 
dmknir = np.c_[mknir[:,0][(mknir[:,0] >= 9.e3) & (mknir[:,0] < 2.e4)][::10], mknir[:,1][(mknir[:,0] >= 9.e3) & (mknir[:,0] < 2.e4)][::10]]

print(mkopt)
print(dmknir)

##  Is 2A precision sufficient?
output = np.c_[np.concatenate([mkopt[:,0], dmknir[:,0]]), np.concatenate([mkopt[:,1], dmknir[:,1]])]

if save:
  header = '# Wave [A]  Extinction\n# http://cdsarc.u-strasbg.fr/viz-bin/qcat?J/A+A/549/A8\n# http://www.gemini.edu/sciops/ObsProcess/obsConstraints/atm-models/mktrans_zm_10_10.dat'

  np.savetxt('ZenithExtinction-MKO.dat', output, header=header)

if plot:
  pl.plot(orig[:,0],     orig[:,1], 'k-', label='KPNO')
  pl.plot(dmknir[:,0], dmknir[:,1], 'r-', label='MKO-NIR')
  pl.plot(output[:,0], output[:,1], 'm-', label='MKO')
  pl.plot(mkopt[:,0],   mkopt[:,1], 'c-', label='MKO-OPT')

  pl.xlim(4.e3, 2.e4)
  pl.ylim(0.,     3.)

  pl.xlabel(r'$\lambda$ [$\AA$]')
  pl.ylabel(r'e($\lambda$)')

  pl.legend()
  pl.savefig('plots/extinction_comp.pdf', bbox_inches='tight')
