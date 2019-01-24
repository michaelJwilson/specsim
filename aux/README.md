1.  New repo of specsim.

2.  quickspectra -i $DESIMODEL/data/spectra/sn-spec-lya-21.25.dat -o ./test.dat --specsimconfig pfs

3.  Sullivan and Simcoe near-ir sky model
    https://arxiv.org/abs/1207.0817
    https://www.jstor.org/stable/get_asset/10.1086/668849?supp_index=0&refreqid=excelsior%3Ab4864ea7b3d4aca653a4bcb001e58d31

    --  Removed grey and bright atmosphere paths. 

4.  base_path: '/global/homes/m/mjwilson/desi/BEAST/sandbox/aux_dat' i.e. $AUX

5.  Moon spectra to Wehrli85.  
    https://www.nrel.gov/grid/solar-resource/spectra-wehrli.html
    https://www.nrel.gov/grid/solar-resource/assets/data/wehrli85.txt

    Comments: quoted units include /sm.  Interpreted as m2. Seems to be consistent. 

6.  Extinction extension to near-ir.

    -- Mauna-Kea --
    Optical 

    Table 6 of https://www.aanda.org/articles/aa/pdf/2013/01/aa19834-12.pdf    
    http://cdsarc.u-strasbg.fr/viz-bin/qcat?J/A+A/549/A8
        
    Near-IR.  
    http://www.gemini.edu/sciops/telescopes-and-sites/observing-condition-constraints/ir-transmission-spectra

    Air mass of unity, water vapor column of 1mm. 
    http://www.gemini.edu/sciops/ObsProcess/obsConstraints/atm-models/mktrans_zm_10_10.dat

    https://specsim.readthedocs.io/en/stable/guide.html#atmosphere-model
    Attenuated flux = input flux * 10 ** (- Extinction(lambda) * AIRMASS / 2.5)

    Optical is already extinction, eqn. (5) of https://www.aanda.org/articles/aa/pdf/2013/01/aa19834-12.pdf
    K \equiv e(lambda) * X  where X is the airmass.  See Specsim read the docs. 

  
    Necessary to convert near-ir from Transmission to extinction.  
    Downsampled to 2A to match MKO optical.

    Is this sufficient?    
    Should extinction be applied to the sky emission?

7.  PFS basic instrument:
        Mirror eff. area: 8.2m
    	As effective, set support_width and obscuration to 0.0;  
    	Is this really true of obscuration?

    field_radius:  How to treat hexagon to cicular comparison?  Stick with greatest distance across or equate
                   area?

    plate scale:   According to the plate scale without microlens, 100um subtends 1.1 arcsec on the sky; i.e. 90.9 um/'' platescale.
    	  	   Assuming a 1.102 increase to field radius, this is 100.17 um/'' at the radius. 
    	           (1) below Table on https://pfs.ipmu.jp/research/parameters.html

		   With microlens, 113um = 1 arcsec at field centre; 124.51um = 1 arcsec at field radius.
		   Corresponds to 10.2% increase (with microlens).
		   
  		   For DESI, the increase is 4% percent. 

		   --  I've renormalised the curve to have central MPS of 90.9 
                       and rescaled wavelength to give 10% difference across field (radius).
		       Radial and azimuthal directions treated similarly. 
 
    fiber loss     Linear extrapolation in wavelength. 
    
    blur values:   Stick with DESI files?  No need for wavelength extension?  Assumed zero? 
    offset values: Stick with DESI files?  No need for wavelength extension?  Assumed zero?

8.  22 Mag AB source.
    Extended range to [2.e3, 2.e4] AA.

9.  Left source profile and location alone.

10. NAOJ Observatory. 
    Added NAOJ to SpecSim.transform. 

    https://www.subarutelescope.org/Observing/Telescope/Parameters/
    https://subarutelescope.org/Introduction/specifications.

    "The differences between these two datums for North America is not discernible with mapping/GIS grade or consumer grade GPS equipment.html"
    i.e. within a ~ meter.
    https://www.esri.com/arcgis-blog/products/arcgis-desktop/mapping/wgs84-vs-nad83/
    
    Latitude: +19 deg N  49' 32'' N (NAD83 / WGS84)
    Longitude: +155 deg W 28' 34'' W (NAD83 / WGS84)
    Altitude: 4139 m (Elevation axis is at 4163 m)

    'NAOJ': astropy.coordinates.EarthLocation.from_geodetic(
    lat='19d49m32s', lon='-155d28m34s', height=4139.*u.m, ellipsoid='WGS84')

    As per https://subarutelescope.org/Introduction/specifications.html, 
    Mean humidity: - 40%

    How does this get mapped to [0,1]?

11. Throughput values.    
    https://pfs.ipmu.jp/research/performance.html

    Resulting warnings:

    /global/homes/m/mjwilson/desi/BEAST/sandbox/specsim/specsim/simulator.py:551: RuntimeWarning: divide by zero encountered in true_divide
    source_flux_to_photons * camera.throughput.reshape(-1, 1)))

    /global/homes/m/mjwilson/desi/BEAST/sandbox/specsim/specsim/simulator.py:555: RuntimeWarning: invalid value encountered in multiply
    output['flux_calibration'] * output['num_source_electrons'])

12.  Basic Camera values
     Table 1 of https://arxiv.org/pdf/1206.0737.pdf
     
                                            b                 r           IR            
     read noise [e- rms / pix]              3.                3.          4.
     dark current [e-/pix/sec]            3.89e-4           3.89e-4       0.01
     dark current [e-/pix/hr]	          1.40040           1.40040       36.0
     gain [e- / adu]                        --                --          -- 
     pixel size / pixel scale [A/pix]       0.71              0.85        0.81

     How significant is the gain?  How likely to be different from 1 (in near-ir).

13.  -- CCD --      
     Note:  arrays defining the CCD properties must all have identical wavelength coverage
     Dispersion and Resolution available from Table 1 of https://arxiv.org/pdf/1608.01075.pdf

     See py/ccd.py
