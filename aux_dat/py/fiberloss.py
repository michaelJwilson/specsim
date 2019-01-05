import os
import numpy              as     np
import pylab              as     pl

from   scipy.interpolate  import interp1d


files = ['fiberloss-elg.dat',\
         'fiberloss-qso.dat',\
         'fiberloss-lrg.dat',\
         'fiberloss-sky.dat',\
         'fiberloss-perfect.dat',\
         'fiberloss-star.dat']

for fname in files:
    root       = os.environ['DESIMODEL'] + '/data/throughput/'

    ttype      = fname.split('.')[0]                                                                                                                                                                                            
    ttype      = ttype.split('-')[1]                                                                                                                                                                                             
    print("Solving for %s" % ttype)

    ## Wavelength, Fiber acceptance fraction (wavelength)
    data       = np.loadtxt(root + fname)                                                                                                                                                               
    lambdas    = data[:,0]
    fiberloss  = data[:,1]

    crit       = (lambdas > 3.5e3) & (lambdas < 1.e4)

    interp     = interp1d(lambdas[crit], fiberloss[crit], fill_value="extrapolate")

    elambdas   = np.arange(3500., 1.5e4)
    efiberloss = interp(elambdas)

    pl.plot(elambdas, efiberloss, '-', label=ttype.upper())
    pl.plot( lambdas,  fiberloss, 'o--')

    np.savetxt(os.environ['AUX'] + '/fiberloss-%s-pfs.dat' % ttype, np.c_[elambdas, efiberloss], fmt='%.6le', header='# Wave [A]  Fiber acceptance fraction')

pl.xlabel('Wavelength [AA]')
pl.ylabel('Fiber acceptance fraction')
pl.legend(ncol=3)
pl.savefig(os.environ['AUX'] + '/plots/fiberloss.pdf')    
