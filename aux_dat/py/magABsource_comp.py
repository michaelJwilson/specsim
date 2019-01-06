import os 
import numpy              as np
import pylab              as pl

import astropy.units      as u
import astropy.constants  as const


mag     =  22.
norm    =  3631. * 1e-23

ls      =  np.arange(2000., 2.e4, 0.1) * u.AA
vs      =  ls.to(u.Hz, equivalencies = u.spectral())

Fv      =  norm * 10. ** ( - 0.4 * mag) * np.ones_like(vs)   ## ergs/s/Hz.
Fl      =  Fv * vs / ls
Fl     *=  1.e17

pl.plot(ls, Fl, 'k-')

AUX     = os.environ['AUX']
np.savetxt(AUX + '/spec-ABmag22.0-nearir.dat', np.c_[ls, Fl], fmt='%.6lf \t %.6le', header='# Wave [A], Flambda [1.e-17 ergs/s/cm2/A]')


##  Compare with SpecSim original.
DMODEL  =  os.environ['DESIMODEL']
data    =  np.loadtxt(DMODEL + '/data/spectra/spec-ABmag22.0.dat')

ls      =  data[:,0]                                         ## [Angstroms]                                                                                                                                                          
Fl      =  data[:,1]                                         ## [1.e-17 ergs/s/cm2/A]                                                                                                                                                

pl.plot(ls, Fl, 'r--', label='SpecSim')
pl.xlabel(r'Wavelength [$\AA$]')
pl.ylabel(r'$F_{\lambda}$ [$10^{-17}$ ergs/s/cm$^2$/$\AA$] ')
pl.legend(ncol=2)
pl.savefig(AUX + '/plots/spec-magABsource_22.0_comp.pdf', bbox_inches='tight') 

