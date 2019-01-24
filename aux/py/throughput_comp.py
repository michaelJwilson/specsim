import os 
import pylab as pl
import numpy as np

from astropy.io import fits

overwrite=True

##  Blue Arm.
##  https://pfs.ipmu.jp/research/performance.html
wave  = np.arange(3000., 7000., 0.1)
Thru  = np.zeros_like(wave)

Thru[wave > 3800.] = 0.14
Thru[wave > 4500.] = 0.24
Thru[wave > 5500.] = 0.23
Thru[wave > 6500.] = 0.00

col1 = fits.Column(name='wavelength',   format='D', unit='Angstrom', array=wave)
col2 = fits.Column(name='throughput', format='D', array=Thru)

hdu  = fits.BinTableHDU.from_columns([col1, col2])
hdu.writeto(os.environ['AUX'] + 'thru-b-pfs.fits', overwrite=overwrite)

pl.plot(wave, Thru, label='Blue', c='b')

##  Red low-res arm.                                                                                                                                                                                                   
##  https://pfs.ipmu.jp/research/performance.html                                                                                                                                                                        
wave  = np.arange(5000., 11000., 0.1)
Thru  = np.zeros_like(wave)

Thru[wave > 6300.] = 0.29
Thru[wave > 7500.] = 0.30
Thru[wave > 8500.] = 0.27
Thru[wave > 9700.] = 0.00

col1 = fits.Column(name='wavelength',   format='D', unit='Angstrom', array=wave)
col2 = fits.Column(name='throughput', format='D', array=Thru)

hdu  = fits.BinTableHDU.from_columns([col1, col2])
hdu.writeto(os.environ['AUX'] + 'thru-r-lowres-pfs.fits', overwrite=overwrite)

pl.plot(wave, Thru, label='Red-lowres', c='r')

##  Red mid-res arm.                                                                                                                                                                                                      
##  https://pfs.ipmu.jp/research/performance.html                                                                                                                                                                         
wave  = np.arange(5000., 11000., 0.1)
Thru  = np.zeros_like(wave)

Thru[wave > 7100.] = 0.26
Thru[wave > 7750.] = 0.28
Thru[wave > 8250.] = 0.27
Thru[wave > 8850.] = 0.00

col1 = fits.Column(name='wavelength',   format='D', unit='Angstrom', array=wave)
col2 = fits.Column(name='throughput', format='D', array=Thru)

hdu  = fits.BinTableHDU.from_columns([col1, col2])
hdu.writeto(os.environ['AUX'] + 'thru-r-midres-pfs.fits', overwrite=overwrite)

pl.plot(wave, Thru, label='Red-midres', c='r', alpha=0.4)

##  NIR arm.                                                                                                                                                                                                      
##  https://pfs.ipmu.jp/research/performance.html                                                                                                                                                                         
wave  = np.arange(8000., 14000., 0.1)
Thru  = np.zeros_like(wave)

Thru[wave >  9400.] = 0.17
Thru[wave > 10500.] = 0.19
Thru[wave > 11500.] = 0.17
Thru[wave > 12600.] = 0.00

col1 = fits.Column(name='wavelength',   format='D', unit='Angstrom', array=wave)
col2 = fits.Column(name='throughput', format='D', array=Thru)

hdu  = fits.BinTableHDU.from_columns([col1, col2])
hdu.writeto(os.environ['AUX'] + 'thru-nearir-pfs.fits', overwrite=overwrite)

pl.plot(wave, Thru, label='Near-IR', c='magenta')

##  Compare with DESI.
root = os.environ['DESIMODEL']

for xx in ['b', 'r', 'z']:
    dat  = fits.open(root + '/data/throughput/thru-' + xx + '.fits')
    wave = dat[1].data['wavelength']
    Thru = dat[1].data['Throughput']

    pl.plot(wave, Thru, label='DESI-' + xx)

pl.xlabel(r'Wavelength $[\AA]$')
pl.ylabel(r'Throughput')
pl.legend(ncol=3)
pl.savefig(os.environ['AUX'] + '/plots/throughput_comp.pdf', bbox_inches='tight')
