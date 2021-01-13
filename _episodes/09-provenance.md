---
title: "Data provenance"
teaching: 10
exercises: 20
questions:
- "How can keep track of my data processing steps?"
objectives:
- "Automate the process of recording the history of what was entered at the command line to produce a given data file or image."
keypoints:
- "It is possible (in only a few lines of code) to record the provenance of a data file or image."
---

We've now successfully created a command line program - `plot_precipitation_climatology.py` -
that calculates and plots the precipitation climatology for a given season.
The last step is to capture the provenance of that plot.
In other words, we need a log of all the data processing steps
that were taken from the intial download of the data file to the end result
(i.e. the .png image).

The simplest way to do this is to follow the lead of the
[NCO](http://nco.sourceforge.net/)
and [CDO](https://code.mpimet.mpg.de/projects/cdo) command line tools,
which insert a record of what was executed at the command line
into the history attribute of the output netCDF file.

~~~
import xarray as xr

esm_pr_file = 'data/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc'
dset = xr.open_dataset(esm_pr_file)

print(dset.attrs['history'])
~~~
{: .language-python}

~~~
Tue Jan 12 14:50:35 2021: ncatted -O -a history,pr,d,, pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc
Tue Jan 12 14:48:10 2021: cdo seldate,2010-01-01,2014-12-31 /g/data/fs38/publications/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/Amon/pr/gn/latest/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_185001-201412.nc pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc
2019-11-15T04:32:57Z ; CMOR rewrote data to be consistent with CMIP6, CF-1.7 CMIP-6.2 and CF standards.
~~~
{: .output}

Fortunately, there is a Python package called [cmdline-provenance](http://cmdline-provenance.readthedocs.io/en/latest/)
that creates NCO/CDO-style records of what was executed at the command line.
We can use it to generate a new command line record:

~~~
import cmdline_provenance as cmdprov
new_record = cmdprov.new_log()
print(new_record)
~~~
{: .language-python}

~~~
2017-12-08T14:05:34: /Applications/anaconda/envs/pyaos-lesson/bin/python /Applications/anaconda/envs/pyaos-lesson/lib/python3.6/site-packages/ipykernel_launcher.py -f /Users/dirving/Library/Jupyter/runtime/kernel-7183ce41-9fd9-4d30-9e46-a0d16bc9bd5e.json
~~~
{: .output}

(i.e. This is the command that was run to launch the jupyter notebook we're using.)


> ## Generate a log file
>
> In order to capture the complete provenance of the precipitation plot,
> add a few lines of code to the end of the `main` function
> in `plot_precipitation_climatology.py` so that it:
> 
> 1. Extracts the history attribute from the input file and combines it with the current command line entry (using the `cmdprov.new_log` function)
> 2. Outputs a log file containing that information (using `cmdprov.write_log`; the file should have name as the plot, replacing .png with .txt)
>
> (Hint: The documentation for [cmdline-provenance](http://cmdline-provenance.readthedocs.io/en/latest/)
> explains the process.)
>
> > ## Solution
> >
> > Make the following additions to `plot_precipitation_climatology.py`
> > (code omitted from this abbreviated version of the script is denoted `...`):
> >
> > ~~~
> > ...
> > import cmdline_provenance as cmdprov
> >
> > ...
> >
> > def main(inargs):
> >
> >     ...
> >
> >     new_log = cmdprov.new_log(infile_history={inargs.pr_file: dset.attrs['history']})
> >     fname, extension = inargs.output_file.split('.')
> >     cmdprov.write_log(fname+'.txt', new_log)
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
> import pdb
> import argparse
>
> import numpy as np
> import matplotlib.pyplot as plt
> import xarray as xr
> import cartopy.crs as ccrs
> import cmocean
> import cmdline_provenance as cmdprov
>
>
> def convert_pr_units(darray):
>     """Convert kg m-2 s-1 to mm day-1.
>     
>     Args:
>       darray (xarray.DataArray): Precipitation data
>    
>    """
>    
>    assert darray.units == 'kg m-2 s-1', "Program assumes input units are kg m-2 s-1"
>
>    darray.data = darray.data * 86400
>    darray.attrs['units'] = 'mm/day'
>    
>    return darray
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
>     assert realm in ['land', 'ocean'], """Valid realms are 'land' or 'ocean'"""
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
>     create_plot(clim, dset.attrs['source_id'], inargs.season,
>                 gridlines=inargs.gridlines, levels=inargs.cbar_levels)
>     plt.savefig(inargs.output_file, dpi=200)
>
>     new_log = cmdprov.new_log(infile_history={inargs.pr_file: dset.attrs['history']})
>     fname, extension = inargs.output_file.split('.')
>     cmdprov.write_log(fname+'.txt', new_log)
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
