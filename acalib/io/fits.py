from astropy.io import fits
from astropy import log
import numpy as np
import astropy.units as u
from astropy.wcs import wcs
import astropy.nddata as ndd
from astropy.table.table import Table
from astropy.vo.samp import SAMPIntegratedClient
import os

def HDU_to_NDData(hdu):
   """
    Create an N-dimensional dataset from an HDU component.

    Parameters
    ----------
    hdu : HDU object
        HDU to transform into an N-dimensional dataset.

    Returns
    -------
    result: numpy.ndarray or astropy.nddata.NDData with data from the HDU object.
   """
   hdu.verify("fix")
   data=hdu.data
   meta=hdu.header
   mask=np.isnan(data)
   # Hack to correct wrong uppercased units generated by CASA
   try:
     bscale=meta['BSCALE']
   except KeyError:
     bscale=1.0
   try:
     bzero=meta['BZERO']
   except KeyError:
     bzero=0.0
   try:
     bsu=meta['BUNIT']
     bsu=bsu.lower()
     bsu=bsu.replace("jy","Jy")
     bunit=u.Unit(bsu,format="fits")
   except KeyError:
     bunit=u.Unit("u.Jy/u.beam")
   rem_list=[]
   for i in meta.items():
      if i[0].startswith('PC00'):
         rem_list.append(i[0])
   for e in rem_list:
      meta.remove(e)

   mywcs=wcs.WCS(meta)
   # Create astropy units
   if len(data.shape) == 4:
       # Put data in physically-meaninful values, and remove stokes
       # TODO: Stokes is removed by summing (is this correct? maybe is averaging?)
       log.info("4D data detected: assuming RA-DEC-FREQ-STOKES (like CASA-generated ones), and dropping STOKES")
       data=data.sum(axis=0)*bscale+bzero
       mywcs=mywcs.dropaxis(3)
   elif len(data.shape) == 3:
       log.info("3D data detected: assuming RA-DEC-FREQ")
       data=data*bscale+bzero
   elif len(data.shape) == 2:
       log.info("2D data detected: assuming RA-DEC")
       data=data*bscale+bzero
   else:
       log.error("Only 3D data allowed (or 4D in case of polarization)")
       raise TypeError
   return ndd.NDData(data, uncertainty=None, mask=mask,wcs=mywcs, meta=meta, unit=bunit)

def HDU_to_Table(hdu):
    """
    Create a data table from a HDU component.

    Parameters
    ----------
    hdu : HDU object
        HDU to transform into a data table.

    Returns
    -------
    result: astropy.table.Table with data from the HDU.
    """
    log.warning("FITS Table ---> AstroPy Table not implemented Yet")
    #return atable.ATable(data=hdu.data,meta=hdu.header)

def Table_to_HDU(tab):
    """
    Create a HDU object from a data table.

    Parameters
    ----------
    tab : astropy.table.Table
        Table to transform into a HDU object.

    Returns
    -------
    result: HDU object with data from the data table.
    """
    #if tab.data.masked:???
    #    dtmp = [col.filled(None) for col in six.itervalues(self.columns)]
    hdu=fits.BinTableHDU.from_columns(np.array(tab))
    if tab.meta is not None:
        for k, v in tab.meta.items():
            hdu.header[k] = v
    return hdu

def NDData_to_HDU(cube,primary=False):
    """
    Create a HDU object from an N-dimensional dataset.

    Parameters
    ----------
    cube : numpy.ndarray or astropy.nddata.NDData
        Astronomical data cube.
    primary : bool
        Whether to pick the primary or an image HDU.

    Returns
    -------
    result: HDU object with data from the data cube.
    """
    header = cube.wcs.to_header()
    if primary==True:
        hdu = fits.PrimaryHDU(cube.data,header=header)
    else:
        hdu = fits.ImageHDU(cube.data,header=header)

    if cube.meta is not None:
        for k, v in cube.meta.items():
            hdu.header[k] = v
    return hdu

def save_fits_from_cont(filepath,acont):
    if isinstance(acont.primary,Table):
        raise NotImplementedError("FITS Format do now support tables as primary HDU! You can set primary = None")
    if acont.primary == None:
        phdu=fits.PrimaryHDU()
    else:
        phdu=NDData_to_HDU(acont.primary,primary=True)
    nlist=[phdu]
    count=0
    for elm in acont.images:
        count+=1
        hdu=NDData_to_HDU(elm)
        hdu.header['EXTNAME'] = 'SCI'
        hdu.header['EXTVER'] = count
        nlist.append(hdu)
    count=0
    for elm in acont.tables:
        count+=1
        hdu=Table_to_HDU(elm)
        hdu.header['EXTNAME'] = 'TAB'
        hdu.header['EXTVER'] = count
        nlist.append(hdu)
    hdulist = fits.HDUList(nlist)
    hdulist.writeto(filepath,clobber=True)

def load_fits_to_cont(filePath,acont):
    hdulist = fits.open(filePath)
    for counter,hdu in enumerate(hdulist):
        if isinstance(hdu,fits.PrimaryHDU) or isinstance(hdu,fits.ImageHDU):
            log.info("Processing HDU "+str(counter)+" (Image)")
            try:
                ndd=HDU_to_NDData(hdu)
                if isinstance(hdu,fits.PrimaryHDU):
                    acont.primary = ndd
                acont.images.append(ndd)
            except TypeError:
                log.info(str(counter)+" (Image) wasn't an Image")
        if isinstance(hdu, fits.BinTableHDU):
            table = HDU_to_Table(hdu)
            acont.tables.append(table)
    if acont.primary is None:
        if len(acont.images)==0:
            acont.primary = acont.tables[0]
        else:
            acont.primary = acont.images[0]

def loadFITS_PrimmaryOnly(fitsfile):
    hduobject = None
    hdulist = fits.open(fitsfile)
    for idx, hdu in enumerate(hdulist):
        if isinstance(hdu, fits.PrimaryHDU):
            log.info('Processing PrimaryHDU Object '+str(idx))
            hduobject = hdu
            break
    #Check if hduobject is None??
    bscale = 1.0
    bunit = u.Unit('u.Jy/u.beam')
    bzero = 0.0
    mask = np.isnan(hduobject.data)
    if 'BSCALE' in hduobject.header:
        bscale = hduobject.header['BSCALE']
    if 'BZERO' in hduobject.header:
        bzero = hduobject.header['BZERO']
    if 'BUNIT' in hduobject.header:
        unit = hduobject.header['BUNIT'].lower().replace('jy','Jy')
        bunit = u.Unit(unit, format='fits')
    for item in hduobject.header.items():
        if item[0].startswith('PC00'):
            hduobject.header.remove(item[0])
    coordinateSystem = wcs.WCS(hduobject.header)
    if len(hduobject.data.shape) == 4:
        log.info('4D Detected: Assuming RA-DEC-FREQ-STOKES, and dropping STOKES')
        coordinateSystem = coordinateSystem.dropaxis(3)
        hduobject.data = hduobject.data.sum(axis=0)*bscale+bzero
        hduobject.data = (hduobject.data*bscale) + bzero
    elif len(hduobject.data.shape) == 3:
        log.info('3D Detected: Assuming RA-DEC-FREQ')
        hduobject.data = (hduobject.data*bscale) + bzero
    elif len(hduobject.data.shape) == 2:
        log.info('2D Detected: Assuming RA-DEC')
        hduobject.data = (hduobject.data*bscale) + bzero
    else:
        log.error('Only 2-4D data allowed')
        raise TypeError
    return ndd.NDData(hduobject.data, uncertainty=None, mask=mask, wcs=coordinateSystem, meta=hduobject.header, unit=bunit)


def SAMP_send_fits(filename,longname):
    client = SAMPIntegratedClient()
    client.connect()
    params = {}
    params["url"] = 'file://'+os.getcwd()+'/'+filename
    params["name"] = longname
    message = {}
    message["samp.mtype"] = "image.load.fits"
    message["samp.params"] = params
    client.notify_all(message)
    client.disconnect()
