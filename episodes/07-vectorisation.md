---
title: "Vectorisation"
teaching: 15
exercises: 15
questions:
- "How can I avoid looping over each element of large data arrays?"
objectives:
- "Use surface land fraction data to mask the land or ocean."
- "Use the vectorised operations available in the `numpy` library to avoid looping over array elements."
keypoints:
- "For large arrays, looping over each element can be slow in high-level languages like Python."
- "Vectorised operations can be used to avoid looping over array elements."
---

A useful addition to our `plot_precipitation_climatology.py` script
would be the option to apply a land or ocean mask.
To do this, we need to use the land area fraction file.

~~~
import numpy as np
import xarray as xr

access_sftlf_file = 'data/sftlf_fx_ACCESS1-3_historical_r0i0p0.nc'

dset = xr.open_dataset(access_sftlf_file)
sftlf = dset['sftlf']
print(sftlf)
~~~
{: .language-python}

~~~
<xarray.DataArray 'sftlf' (lat: 145, lon: 192)>
array([[100., 100., 100., ..., 100., 100., 100.],
       [100., 100., 100., ..., 100., 100., 100.],
       [100., 100., 100., ..., 100., 100., 100.],
       ...,
       [  0.,   0.,   0., ...,   0.,   0.,   0.],
       [  0.,   0.,   0., ...,   0.,   0.,   0.],
       [  0.,   0.,   0., ...,   0.,   0.,   0.]], dtype=float32)
Coordinates:
  * lat      (lat) float64 -90.0 -88.75 -87.5 -86.25 -85.0 -83.75 -82.5 ...
  * lon      (lon) float64 0.0 1.875 3.75 5.625 7.5 9.375 11.25 13.12 15.0 ...
Attributes:
    standard_name:     land_area_fraction
    long_name:         Land Area Fraction
    units:             %
    original_units:    1
    cell_measures:     area: areacella
    associated_files:  baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation...
~~~
{: .output}

The data in a sftlf file assigns each grid cell a percentage value
between 0% (no land) to 100% (all land).

~~~
print(sftlf.data.max())
print(sftlf.data.min())
~~~
{: .language-python}

~~~
100.0
0.0
~~~
{: .output}

To apply a mask to our plot,
the value of all the data points we'd like to mask needs to be set to `np.nan`. 
The most obvious solution to applying a land mask, for example,
might therefore be to loop over each cell in our data array and decide whether
it is a land point (and thus needs to be set to `np.nan`).

(For this example, we are going to define land as any grid point that is more than 50% land.)

~~~
dset = xr.open_dataset('data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc')
clim = dset['pr'].mean('time', keep_attrs=True)

nlats, nlons = clim.data.shape
for y in range(nlats):
    for x in range(nlons):
        if sftlf.data[y, x] > 50:
            clim.data[y, x] = np.nan
~~~
{: .language-python}

While this approach technically works,
the problem is that (a) the code is hard to read,
and (b) in contrast to low level languages like Fortran and C,
high level languages like Python and Matlab are built for usability
(i.e. they make it easy to write concise, readable code) as opposed to speed.
This particular array is so small that the looping isn't noticably slow,
but in general looping over every data point in an array should be avoided.

Fortunately, there are lots of numpy functions
(which are written in C under the hood)
that allow you to get around this problem
by applying a particular operation to an entire array at once
(which is known as a vectorised operation).
The `np.where` function, for instance,
allows you to make a true/false decision at each data point in the array
and then perform a different action depending on the answer.

The developers of xarray have built-in the `np.where` functionality,
so creating a new DataArray with the land masked becomes a one-line command:

~~~
clim_ocean = clim.where(sftlf.data < 50)
print(clim_ocean)
~~~
{: .language-python}

~~~
<xarray.DataArray 'pr' (lat: 145, lon: 192)>
array([[         nan,          nan,          nan, ...,          nan,
                 nan,          nan],
       [         nan,          nan,          nan, ...,          nan,
                 nan,          nan],
       [         nan,          nan,          nan, ...,          nan,
                 nan,          nan],
       ...,
       [8.877672e-06, 8.903967e-06, 8.938327e-06, ..., 8.819357e-06,
        8.859161e-06, 8.873179e-06],
       [8.748589e-06, 8.739819e-06, 8.723918e-06, ..., 8.797057e-06,
        8.776324e-06, 8.789103e-06],
       [7.988647e-06, 7.988647e-06, 7.988647e-06, ..., 7.988647e-06,
        7.988647e-06, 7.988647e-06]], dtype=float32)
Coordinates:
  * lon      (lon) float64 0.0 1.875 3.75 5.625 7.5 9.375 11.25 13.12 15.0 ...
  * lat      (lat) float64 -90.0 -88.75 -87.5 -86.25 -85.0 -83.75 -82.5 ...
~~~
{: .output}


> ## Mask option
>
> Modify `plot_precipitation_climatology.py` so that the user can choose to apply a mask
> via the following `argparse` option:
>
> ~~~
> parser.add_argument("--mask", type=str, nargs=2,
>                     metavar=('SFTLF_FILE', 'REALM'), default=None,
>                     help="""Provide sftlf file and realm to mask ('land' or 'ocean')""")
> ~~~
> {: .language-python}
>
> This should involve defining a new function called `apply_mask()`,
> in order to keep `main()` short and readable.
>
> Test to see if your mask worked by plotting the ACCESS1-3 climatology for JJA:
>
> ~~~
> $ python plot_precipitation_climatology.py data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc JJA pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512-JJA-clim_land-mask.png --mask data/sftlf_fx_ACCESS1-3_historical_r0i0p0.nc ocean
> ~~~
> {: .language-bash}
>
> Commit the changes to git and then push to GitHub.
>
> > ## Solution
> >
> > Make the following additions to `plot_precipitation_climatology.py`
> > (code omitted from this abbreviated version of the script is denoted `...`):
> >
> > ~~~
> > def apply_mask(darray, sftlf_file, realm):
> >     """Mask ocean or land using a sftlf (land surface fraction) file.
> >    
> >     Args:
> >      darray (xarray.DataArray): Data to mask
> >      sftlf_file (str): Land surface fraction file
> >      realm (str): Realm to mask
> >    
> >     """
> >   
> >     dset = xr.open_dataset(sftlf_file)
> >   
> >     if realm == 'land':
> >         masked_darray = darray.where(dset['sftlf'].data < 50)
> >     else:
> >         masked_darray = darray.where(dset['sftlf'].data > 50)   
> >   
> >     return masked_darray
> > 
> > ...
> >
> > def main(inargs):
> >     """Run the program."""
> >
> >     dset = xr.open_dataset(inargs.pr_file)
> >    
> >     clim = dset['pr'].groupby('time.season').mean('time', keep_attrs=True)
> >     clim = convert_pr_units(clim)
> >
> >     if inargs.mask:
> >         sftlf_file, realm = inargs.mask
> >         clim = apply_mask(clim, sftlf_file, realm)
> >
> >     ...
> >
> > if __name__ == '__main__':
> >
> >     description='Plot the precipitation climatology for a given season.'
> >     parser = argparse.ArgumentParser(description=description)
> >
> >     ...
> >    
> >     parser.add_argument("--mask", type=str, nargs=2, metavar=('SFTLF_FILE', 'REALM'), default=None,
> >                            help="""Provide sftlf file and realm to mask ('land' or 'ocean')""")
> >
> >     args = parser.parse_args()            
> >     main(args)
> >
> > ~~~
> > {: .language-python}
> {: .solution}     
{: .challenge}

> ## plot_precipitation_climatology.py
>
> At the conclusion of this lesson your `plot_precipitation_climatology.py` script
> should look something like the following:
>
> ~~~
> import argparse
>
> import numpy as np
> import matplotlib.pyplot as plt
> import xarray as xr
> import cartopy.crs as ccrs
> import cmocean
>
>
> def convert_pr_units(darray):
>     """Convert kg m-2 s-1 to mm day-1.
>     
>     Args:
>       darray (xarray.DataArray): Precipitation data
>    
>     """
>    
>     darray.data = darray.data * 86400
>     darray.attrs['units'] = 'mm/day'
>    
>     return darray
>
>
> def apply_mask(darray, sftlf_file, realm):
>     """Mask ocean or land using a sftlf (land surface fraction) file.
>    
>     Args:
>       darray (xarray.DataArray): Data to mask
>       sftlf_file (str): Land surface fraction file
>       realm (str): Realm to mask
>    
>     """
>   
>     dset = xr.open_dataset(sftlf_file)
>   
>     if realm == 'land':
>         masked_darray = darray.where(dset['sftlf'].data < 50)
>     else:
>         masked_darray = darray.where(dset['sftlf'].data > 50)   
>    
>     return masked_darray
>
>
> def create_plot(clim, model_name, season, gridlines=False, levels=None):
>     """Plot the precipitation climatology.
>     
>     Args:
>       clim (xarray.DataArray): Precipitation climatology data
>       model_name (str): Name of the climate model
>       season (str): Season
>      
>     Kwargs:
>       gridlines (bool): Select whether to plot gridlines
>       levels (list): Tick marks on the colorbar    
>     
>     """
>
>     if not levels:
>         levels = np.arange(0, 13.5, 1.5)
>        
>     fig = plt.figure(figsize=[12,5])
>     ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
>     clim.sel(season=season).plot.contourf(ax=ax,
>                                           levels=levels,
>                                           extend='max',
>                                           transform=ccrs.PlateCarree(),
>                                           cbar_kwargs={'label': clim.units},
>                                           cmap=cmocean.cm.haline_r)
>     ax.coastlines()
>     if gridlines:
>         plt.gca().gridlines()
>     
>     title = '%s precipitation climatology (%s)' %(model_name, season)
>     plt.title(title)
>
>
> def main(inargs):
>     """Run the program."""
> 
>     dset = xr.open_dataset(inargs.pr_file)
>     
>     clim = dset['pr'].groupby('time.season').mean('time', keep_attrs=True)
>     clim = convert_pr_units(clim)
> 
>     if inargs.mask:
>         sftlf_file, realm = inargs.mask
>         clim = apply_mask(clim, sftlf_file, realm)
>
>     create_plot(clim, dset.attrs['model_id'], inargs.season,
>                 gridlines=inargs.gridlines, levels=inargs.cbar_levels)
>     plt.savefig(inargs.output_file, dpi=200)
>
>
> if __name__ == '__main__':
>     description='Plot the precipitation climatology for a given season.'
>     parser = argparse.ArgumentParser(description=description)
>    
>     parser.add_argument("pr_file", type=str, help="Precipitation data file")
>     parser.add_argument("season", type=str, help="Season to plot")
>     parser.add_argument("output_file", type=str, help="Output file name")
> 
>     parser.add_argument("--gridlines", action="store_true", default=False,
>                         help="Include gridlines on the plot")
>     parser.add_argument("--cbar_levels", type=float, nargs='*', default=None,
>                         help='list of levels / tick marks to appear on the colorbar')
>     parser.add_argument("--mask", type=str, nargs=2,
>                         metavar=('SFTLF_FILE', 'REALM'), default=None,
>                         help="""Provide sftlf file and realm to mask ('land' or 'ocean')""")
>
>     args = parser.parse_args()
>   
>     main(args)
>
> ~~~
> {: .language-python}
{: .solution}
