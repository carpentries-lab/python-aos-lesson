---
title: "Defensive programming"
teaching: 15
exercises: 15
questions:
- "How can I make my programs more reliable?"
objectives:
- Signal errors by raising exceptions
- Use `try`/`except` blocks to catch and handle exceptions 
- "Explain what an assertion is."
- "Add assertions that check the program's state is correct."
- "Debug Python scripts using the `pdb` library."
- "Identify sources of more advanced lessons on code testing."
keypoints:
- "Program defensively, i.e., assume that errors are going to arise, and write code to detect them when they do."
- "Put assertions in programs to check their state as they run, and to help readers understand how those programs are supposed to work."
- "The `pdb` library can be used to debug a Python script by stepping through line-by-line."
- "Software Carpentry has more advanced lessons on code testing."
---

> ## Scientist's nightmare
>
> If you needed any motivation to learn and employ the principles of defensive programming,
> look no further than [this article](http://science.sciencemag.org/content/314/5807/1856).
> It documents the experience of a researcher who had to retract five published papers -
> three of which were in *Science* - because his code had inadvertently switched
> the rows and columns of a data table.
>
{: .callout}

Now that we've written a command line program to plot precipitation climatologies,
it is inevitable that people (including our future selves)
will misunderstand (or misremember) how to use the program.
We should therefore plan from the start to detect and handle errors.

There are (at least) two distinguishable kinds of errors that can arise:
syntax errors and exceptions.
We are all very familiar with the former:

~~~
rainfall = 5
if rainfall > 5
    print('heavy rainfall')
~~~
{: .language-python}

~~~
    if rainfall > 10
                    ^
SyntaxError: expected ':'
~~~
{: .error}

Once a statement or expression is syntactically correct,
it may cause an error when an attempt is made to execute it.
Errors detected during execution are called exceptions
(i.e. an exception from normal behaviour)
and there are lots of [different types](https://docs.python.org/3/library/exceptions.html#exception-hierarchy):

~~~
10 * (1/0)
~~~
{: .language-python}

~~~
ZeroDivisionError: division by zero
~~~
{: .error}

~~~
4 + spam*3
~~~
{: .language-python}

~~~
NameError: name 'spam' is not defined
~~~
{: .error}

~~~
'2' + 2
~~~
{: .language-python}

~~~
TypeError: can only concatenate str (not "int") to str
~~~
{: .error}


> ## Testing and continuous integration
>
> An assertion checks that something is true at a particular point in the program.
> For programs that are more complex (or research critical) than `plot_precipitation_climatology.py`, 
> it's a good idea to take the next step and check the overall behavior of entire pieces (or units) of code.
> Related concepts like unit testing and continuous integration are beyond the scope of this lesson,
> but *Research Software Engineering With Python* has a [chapter on testing](https://merely-useful.github.io/py-rse/testing.html)
> that is well worth a read. 
>
{: .callout}

> ## Add your own assertions
>
> Add some more assertions to your copy of `plot_precipitation_climatology.py`.
> Once you're done, commit the changes to git and push to GitHub.
>
> > ## Solution
> >
> > There are many examples of assertions that could be added,
> > but the most critical is to check the units of the input data
> > before converting from kg m-2 s-1 to mm day-1.
> >
> > ~~~
> > ...
> >
> > def convert_pr_units(darray):
> >     """Convert kg m-2 s-1 to mm day-1.
> >    
> >     Args:
> >       darray (xarray.DataArray): Precipitation data
> >    
> >     """
> >    
> >     assert darray.units == 'kg m-2 s-1', "Program assumes input units are kg m-2 s-1"
> >    
> >     darray.data = darray.data * 86400
> >     darray.attrs['units'] = 'mm/day'
> >    
> >     return darray
> >
> > ...
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
> import xarray as xr
> import cartopy.crs as ccrs
> import matplotlib.pyplot as plt
> import numpy as np
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
