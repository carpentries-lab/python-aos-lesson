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
(i.e. the PNG image).

The simplest way to do this is to follow the lead of the
[NCO](http://nco.sourceforge.net/)
and [CDO](https://code.mpimet.mpg.de/projects/cdo) command line tools,
which insert a record of what was executed at the command line
into the history attribute of the output netCDF file.
If fact,
they were both used in the pre-processing of the data files
used in these lessons:

~~~
import xarray as xr

accessesm15_pr_file = 'data/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc'
dset = xr.open_dataset(accessesm15_pr_file)

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
We can use it to add to the command log,
before inserting the updated log into the metadata associated with our output image file.

To start, let's import the `cmdline_provenance` library with the other imports at the top of our
`plot_precipitation_climatology.py` script,

~~~
import cmdline_provenance as cmdprov
~~~
{: .language-python}

and then make the following updates to the original line of code
responsible for saving the image to file:

~~~
new_log = cmdprov.new_log(infile_logs={inargs.pr_file: dset.attrs['history']})
pdb.set_trace()
plt.savefig(inargs.output_file, metadata={'History': new_log}, dpi=200)
~~~
{: .language-python}

When we execute `plot_precipitation_climatology.py`,
`cmdprov.new_log` will create a record of what was entered at the command line.
The name of the input precipitation file and its history attribute
have been provided using the `infile_logs` argument,
so that `cmdprov.new_log` can append the history of that file to the new command log.
The `metadata` argument for `plt.savefig`
has then been used to save the new command log to the image metadata.

To see this in action,
we've added a Python debugger tracer to the script:

~~~
$ python plot_precipitation_climatology.py data/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc SON pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412-SON-clim.png
~~~ 
{: .language-bash}

~~~
> /Users/damien/Desktop/data-carpentry/plot_precipitation_climatology.py(98)main()
-> plt.savefig(inargs.output_file, metadata={'History': new_log}, dpi=200)
~~~
{: .output}

~~~
(Pdb) new_log
~~~
{: .language-bash}

~~~
'Mon Feb 08 09:45:17 2021: /Users/damien/opt/anaconda3/envs/pyaos-lesson/bin/python plot_precipitation_climatology.py data/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc SON pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412-SON-clim.png\nTue Jan 12 14:50:35 2021: ncatted -O -a history,pr,d,, pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc\nTue Jan 12 14:48:10 2021: cdo seldate,2010-01-01,2014-12-31 /g/data/fs38/publications/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/Amon/pr/gn/latest/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_185001-201412.nc pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc\n2019-11-15T04:32:57Z ; CMOR rewrote data to be consistent with CMIP6, CF-1.7 CMIP-6.2 and CF standards. \n'
~~~
{: .output}

The log has been successfully updated,
so let's have the debugger continue to the end of the script:

~~~
(Pdb) c
~~~
{: .language-bash}

Now that we've written the command log to our PNG file,
we need a way to view the metadata of image files.
There are a number of different programs available to do this,
but they can often be tricky to install.
Fortunately,
`conda` is used to install programs written in many different languages,
not just Python.
There are [installation recipes](https://anaconda.org/conda-forge/exiftool)
for a command line program called [`exiftool`](https://exiftool.org/) on anaconda.org,
so let's go ahead and install that:

~~~
$ conda install exiftool
~~~
{: .language-bash}

Once installed,
we can use it to view the metadata associated with our image file:

~~~
$ exiftool pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412-SON-clim.png
~~~
{: .language-bash}

~~~
ExifTool Version Number         : 12.17
File Name                       : pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412-SON-clim.png
Directory                       : .
File Size                       : 315 KiB
File Modification Date/Time     : 2021:02:08 10:16:56+11:00
File Access Date/Time           : 2021:02:08 10:16:58+11:00
File Inode Change Date/Time     : 2021:02:08 10:16:56+11:00
File Permissions                : rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 2400
Image Height                    : 1000
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Software                        : Matplotlib version3.3.3, https://matplotlib.org/
History                         : Mon Feb 08 09:45:17 2021: /Users/damien/opt/anaconda3/envs/pyaos-lesson/bin/python code/plot_precipitation_climatology.py data/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc SON pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412-SON-clim.png.Tue Jan 12 14:50:35 2021: ncatted -O -a history,pr,d,, pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc.Tue Jan 12 14:48:10 2021: cdo seldate,2010-01-01,2014-12-31 /g/data/fs38/publications/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/Amon/pr/gn/latest/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_185001-201412.nc pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc.2019-11-15T04:32:57Z ; CMOR rewrote data to be consistent with CMIP6, CF-1.7 CMIP-6.2 and CF standards. .
Pixels Per Unit X               : 7874
Pixels Per Unit Y               : 7874
Pixel Units                     : meters
Image Size                      : 2400x1000
Megapixels                      : 2.4
~~~
{: .output}

Now that we've successfully added a command log to our PNG image,
we might want to think about how our script should handle other image formats (e.g. PDF, EPS)?
For PNG files you can pick whatever metadata keys you like (hence we picked "History"),
but other formats only allow specific keys.
For now we can add an assertion so that the program halts
if someone tries to generate a format that isn't PNG,
and in the exercises we'll add more valid formats to the script.

~~~
image_format = inargs.output_file.split('.')[-1])
assert image_format == 'png', 'Only valid output format is .png'
~~~
{: .language-python}

Putting this altogether
(and removing the debugging tracer),
here's what the `main` function in `plot_precipitation_climatology.py` looks like:

~~~
def main(inargs):
    """Run the program."""

    dset = xr.open_dataset(inargs.pr_file)
    
    clim = dset['pr'].groupby('time.season').mean('time', keep_attrs=True)
    clim = convert_pr_units(clim)

    if inargs.mask:
        sftlf_file, realm = inargs.mask
        clim = apply_mask(clim, sftlf_file, realm)

    create_plot(clim, dset.attrs['source_id'], inargs.season,
                gridlines=inargs.gridlines, levels=inargs.cbar_levels)
    
    image_format = inargs.output_file.split('.')[-1]
    assert image_format == 'png', 'Only valid image format is .png'
    new_log = cmdprov.new_log(infile_logs={inargs.pr_file: dset.attrs['history']})
    plt.savefig(inargs.output_file, metadata={'History': new_log}, dpi=200)
~~~
{: .language-python}

> ## Handling different image formats
>
> The [`plt.savefig` documentation](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html)
> provides information on the metadata keys accepted by
> PNG, PDF, EPS and PS image formats.
>
> Using that information as a guide,
> add a new function called `get_log_and_key`
> to the `plot_precipitation_climatology.py` script.
> It should take the precipitation file name, history attribute,
> and plot type as arguments and return the updated command log and
> the appropriate metadata key for PNG, PDF, EPS or PS image formats.
>
> When you're done,
> the final lines of the `main` function should read as follows:  
>
> ~~~
> log_key, new_log = get_log_and_key(inargs.pr_file,
>                                    dset.attrs['history'],
>                                    inargs.output_file.split('.')[-1])
> plt.savefig(inargs.output_file, metadata={log_key: new_log}, dpi=200)
> ~~~
> {: .language-python}
>
> > ## Solution
> >
> > The new function could read as follows:
> > ~~~
> > def get_log_and_key(pr_file, history_attr, plot_type):
> >    """Get key and command line log for image metadata.
> >   
> >    Different image formats allow different metadata keys.
> >   
> >    Args:
> >      pr_file (str): Input precipitation file
> >      history_attr (str): History attribute from pr_file
> >      plot_type (str): File format for output image
> >   
> >    """
> >    
> >    valid_keys = {'png': 'History',
> >                  'pdf': 'Title',
> >                  'eps': 'Creator',
> >                  'ps' : 'Creator'}    
> >
> >    assert plot_type in valid_keys.keys(), f"Image format not one of: {*[*valid_keys],}"
> >    log_key = valid_keys[plot_type]
> >    new_log = cmdprov.new_log(infile_logs={pr_file: history_attr})
> >    
> >    return log_key, new_log
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}

> ## Writing the command log to netCDF files
>
> Instead of calculating the seasonal climatology and creating a plot all in the one script,
> we could have decided to make it a two step process.
> The first script in the process could take the original precipitation data file and
> output a new netCDF file containing the seasonal climatology,
> and the second script could take the seasonal climatology file
> and create a plot from that. 
>
> If the first script reads as follows,
> how would you edit it so that an updated command log
> is included in the history attribute of the output netCDF file?
>
> ~~~
> import argparse
> 
> import numpy as np
> import xarray as xr
>
>
> def convert_pr_units(darray):
>     """Convert kg m-2 s-1 to mm day-1.
>     
>     Args:
>       darray (xarray.DataArray): Precipitation data
>     """
>     assert darray.units == 'kg m-2 s-1', "Program assumes input units are kg m-2 s-1"
>     darray.data = darray.data * 86400
>     darray.attrs['units'] = 'mm/day'
>   
>     return darray
>
>
> def main(inargs):
>     """Run the program."""
>     in_dset = xr.open_dataset(inargs.pr_file)
>     clim = in_dset['pr'].groupby('time.season').mean('time', keep_attrs=True)
>     clim = convert_pr_units(clim)
>     out_dset = clim.to_dataset()
>     out_dset.attrs = in_dset.attrs
>     out_dset.to_netcdf(inargs.output_file)
>    
>
> if __name__ == '__main__':
>     description='Calculate the seasonal precipitation climatology.'
>     parser = argparse.ArgumentParser(description=description)
>     parser.add_argument("pr_file", type=str, help="Precipitation data file")
>     parser.add_argument("output_file", type=str, help="Output file name")
>     args = parser.parse_args()  
>     main(args)
> ~~~
> {: .language-python}
>
> > ## Solution
> >
> > The beginning of the script would need to be updated to import
> > the `cmdline_provenance` library:
> > ~~~
> > import cmdline_provenance as cmdprov
> > ~~~
> > {: .language-python}
> > 
> > The body of the `main` function would then need to be updated
> > to write the new command log to the history attribute of the output dataset:
> > ~~~
> > out_dset.attrs = in_dset.attrs
> > new_log = cmdprov.new_log(infile_logs={inargs.pr_file: in_dset.attrs['history']})
> > out_dset.attrs['history'] = new_log
> > out_dset.to_netcdf(inargs.output_file)
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
> import xarray as xr
> import cartopy.crs as ccrs
> import matplotlib.pyplot as plt
> import numpy as np
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
>     """
>    
>     assert darray.units == 'kg m-2 s-1', "Program assumes input units are kg m-2 s-1"
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
>     assert realm in ['land', 'ocean'], """Valid realms are 'land' or 'ocean'"""
>     if realm == 'land':
>         masked_darray = darray.where(dset['sftlf'].data < 50)
>     else:
>         masked_darray = darray.where(dset['sftlf'].data > 50)   
>    
>     return masked_darray
>
>
> def create_plot(clim, model, season, gridlines=False, levels=None):
>     """Plot the precipitation climatology.
>     
>     Args:
>       clim (xarray.DataArray): Precipitation climatology data
>       model (str): Name of the climate model
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
>     title = f'{model} precipitation climatology ({season})'
>     plt.title(title)
>
>
> def get_log_and_key(pr_file, history_attr, plot_type):
>     """Get key and command line log for image metadata.
>    
>     Different image formats allow different metadata keys.
>    
>     Args:
>       pr_file (str): Input precipitation file
>       history_attr (str): History attribute from pr_file
>       plot_type (str): File format for output image
>    
>     """
>     
>     valid_keys = {'png': 'History',
>                   'pdf': 'Title',
>                   'eps': 'Creator',
>                   'ps' : 'Creator'}    
> 
>     assert plot_type in valid_keys.keys(), f"Image format not one of: {*[*valid_keys],}"
>     log_key = valid_keys[plot_type]
>     new_log = cmdprov.new_log(infile_logs={pr_file: history_attr})
>     
>     return log_key, new_log
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
>     log_key, new_log = get_log_and_key(inargs.pr_file,
>                                        dset.attrs['history'],
>                                        inargs.output_file.split('.')[-1])
>     plt.savefig(inargs.output_file, metadata={log_key: new_log}, dpi=200)
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
