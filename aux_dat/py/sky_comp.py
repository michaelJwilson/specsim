import numpy as np
import pylab as pl

from desispec.interpolation import resample_flux

save = False

##  1.e-17 erg / (Angstrom arcsec2 cm2 s)
dat = np.loadtxt('spectra/spec-sky.dat')
pl.plot(dat[:,0], dat[:,1], label=r'Sky-spec, $\lambda<10^4\AA$', c='k')

ss  = np.loadtxt('SullivanSimcoe.txt')
ss[:,1] *= 1.e17  ##  1.e-17 erg / (Angstrom arcsec2 cm2 s)

##  wavelength cut Simcoe.
ss = ss[ss[:,0] < 1.5e4, :]
pl.plot(ss[:,0], ss[:,1], label='Sullivan-Simcoe', c='g')

##  extend wavelength coverage on sky-spec.
ewaves = np.arange(1.e4, 1.5e4, 0.1)

## Resample flux.  Set to zero outside the range. 
eflux  = resample_flux(ewaves, ss[:,0], ss[:,1], ivar=None, extrapolate=False)
output = np.c_[np.concatenate([dat[:,0], ewaves]), np.concatenate([dat[:,1], eflux])]

if save:
  pl.savetxt('spec-sky-nearir.dat', output, header='#  Wave[A]  Flux [1.e-17 erg / (Angstrom arcsec2 cm2 s)]\n#  Extended with Sullivan and Simcoe (https://arxiv.org/abs/1207.0817)')

pl.plot(output[:,0], output[:,1], 'r--', label='Joint', alpha=0.5)

pl.xlim(8.e3, 1.5e4)
pl.ylim(0., 1.e3)

pl.legend()
pl.savefig('plots/sky_comp.pdf')
