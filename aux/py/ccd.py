import  os
import  copy
import  numpy  as  np
import  pylab  as  pl
import  astropy.io.fits as fits

from    astropy.io.fits import Column

#  Blue and Red are 4k x 2k CCDs, NIR is 4k x 4k.  For desi and pfs, 15um pixels.
#  Dispersion:  0.7, 0.9, 0.4, 0.8 [A/pix] for B, LR, HR (galactic archaeology) and NIR.
#  wave:  [3569., 3569.5, ...,  5949.]).
#  Angstroms per row:  (MaxBWave-MinBWave) / 4k. [Angstroms per pixel];  e.g, for desi, (3569.0, 5949.0)/4k. = 0.595;  Sampled every 0.5A.
#  neff_spatial:       Effective number of cross-dispersion pixels, e.g., for desi, [3.548, 3.73] in pixels;  For PFS, 0.4765, 0.357, 0.341 pixels, see fwhm_resolution.
#  fwhm_resolution:    Wavelength dispersion FWHM [Angstrom], e.g., for desi, 1.7A.
#                      From KG, nominal RMS Spot Radius: 7.148, 5.360, 5.116 um = 0.4765, 0.357, 0.341 pixels; dispersion * pixels -> 0.334, 0.3213 (low res), 0.272 A.

BlueMin =  3800.
BlueMax =  6500.

##  Low res. 
RedMin  =  6300.
RedMax  =  9700.

NIRMin  =  9400.
NIRMax  = 12600.

##  Load fits to be overwritten, and rename to NIR.                                                                                                                                                                                        
dat                     = fits.open(os.environ['AUX'] + '/_psf-quicksim.fits')

index                   = dat.index_of('QUICKSIM-Z')
dummy                   = dat.pop(index)
dummy.header['EXTNAME'] = 'QUICKSIM-NIR'

dat.append(dummy)

del dat[index]

print(dat.info())

primary_hdu         = fits.PrimaryHDU(header=dat[0].header)
hdul                = fits.HDUList([primary_hdu])

for (min_wave, max_wave, neff_spatial, fwhm_resolution, color, label) in [(BlueMin, BlueMax, 0.4765, 0.334, 'b', 'B'), (RedMin, RedMax, 0.357, 0.3213, 'r', 'R'), (NIRMin, NIRMax, 0.341, 0.272, 'indigo', 'NIR')]:
  wave              =  np.arange(min_wave, max_wave, 0.5)

  ##  Note:  4k wavelength, 2k  spatial!
  AngPerRow         =  np.ones_like(wave) * (max_wave - min_wave) / 4.e3   ##  [A/pixel] in the wavelength (column) direction. 
  neff_spatials     =  np.ones_like(wave) *  neff_spatial                  ##  [pixels] 
  fwhm_resolutions  =  np.ones_like(wave) *  fwhm_resolution               ##  [A]

  pl.plot(wave, AngPerRow, c=color, label=label+' dispersion [A/pixel]')
  pl.plot(wave, neff_spatials, '--', c=color, label=label+' neff [pix]')
  pl.plot(wave, fwhm_resolutions, '^',  c=color, label=label+r' fwhm$_{\lambda}$ [A]', markersize=3)

  c1 = Column(name = 'wavelength',          unit = 'Angstrom',       format='D', array = wave)
  c2 = Column(name = 'neff_spatial',        unit = 'pixel',          format='D', array = neff_spatials)
  c3 = Column(name = 'angstroms_per_row',   unit = 'Angstrom/pixel', format='D', array = AngPerRow)
  c4 = Column(name = 'fwhm_wave',           unit = 'Angstrom',       format='D', array = fwhm_resolutions)

  '''
  ##  Potentially addable attributes to each HDU.
  PSFFILE  = 'psf-b.fits'                               / Input PSF file                                 
  PSFSHA1  = 'a88fbc9ab3567518a5c89bb6a15055e68bc4b94e' / SHA1 checksum input PSF  
  WMIN_ALL =                 3569                       / Starting wavelength [Angstroms]                
  WMAX_ALL =                 5949                       / Last wavelength [Angstroms] 
  '''

  t  = fits.BinTableHDU.from_columns([c1, c2, c3, c4], name='QUICKSIM-%s' % label)

  hdul.append(t)

pl.xlabel(r'wavelength $[\AA]$')
pl.yscale('linear')
pl.legend(ncol=2)
pl.show()

hdul.writeto(os.environ['AUX'] + 'psf-quicksim-PFS.fits', overwrite=True)
