import numpy as np
import pylab as pl

from desispec.interpolation import resample_flux


save         = True
plot         = True

wehrli       = np.loadtxt('wehrli85.txt')
wehrli[:,0] *= 10.  ##  nm to AA. 
wehrli[:,1] /= 10.  ##  W / m2 / nm to W / m2 / A. 
wehrli[:,1] *= 1.e3 ##  ergs/s/cm2/A

moon       = np.loadtxt('sky/solarspec.txt')
moon[:,2] *= 1.e-4  ## W/m2/um to W/m2/A
moon[:,2] *= 1.e3   ##  ergs/s/cm2/A                     

owaves = np.arange(0., 2.e4, 0.1)
oflux  = resample_flux(owaves, wehrli[:,0], wehrli[:,1], ivar=None, extrapolate=False)

output = np.c_[owaves, oflux]

if save:
  np.savetxt('solarspec-nearir.txt', output, header='#  Wave [A]  Flux [ergs/s/cm2/A]\n#  https://www.nrel.gov/grid/solar-resource/assets/data/wehrli85.txt', fmt='%.6lf \t %.6le')

if plot:
  pl.plot(owaves, oflux, 'k-', label='Near-ir')
  pl.plot(moon[:,1], moon[:,2], 'c--', alpha=1.0, label='Original')
  ## pl.plot(wehrli[:,0], wehrli[:,1], 'c', alpha=0.4, label='Wehrli 1985')

  pl.xlabel(r'$\AA$')
  pl.ylabel(r'ergs/s/cm$^2$/$\AA$')
  pl.xlim(0., 2.e4)

  pl.savefig('plots/moon_comp.pdf')
