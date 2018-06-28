---
title: "Data provenance"
teaching: 25
exercises: 15
questions:
- "How can keep track of my data processing steps?"
objectives:
- "Automate the process of recording the history of what was entered at the command line to produce a given data file or image."
keypoints:
- "It is possible (in only a few lines of code) to record the provenance of a data file or image."
---

We've now successfully created a command line program - `plot_precipitation_climatology.py` -
that calculates and plots the precipitation climatology for a given month.
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
import iris

access_pr_file = 'data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc'
cube = iris.load_cube(access_pr_file, 'precipitation_flux')
previous_history = cube.attributes['history']

print(previous_history)
~~~
{: .language-python}

~~~
Fri Dec  8 10:05:47 2017: ncatted -O -a history,pr,d,, pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc
Fri Dec 01 07:59:16 2017: cdo seldate,2001-01-01,2005-12-31 /g/data/ua6/DRSv2/CMIP5/ACCESS1-3/historical/mon/atmos/r1i1p1/pr/latest/pr_Amon_ACCESS1-3_historical_r1i1p1_185001-200512.nc pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc
CMIP5 compliant file produced from raw ACCESS model output using the ACCESS Post-Processor and CMOR2. 2012-02-08T06:45:54Z CMOR rewrote data to comply with CF standards and CMIP5 requirements. Fri Apr 13 09:55:30 2012: forcing attribute modified to correct value Fri Apr 13 12:13:10 2012: updated version number to v20120413. Fri Apr 13 12:29:34 2012: corrected model_id from ACCESS1-3 to ACCESS1.3
~~~
{: .output}

Fortunately, there is a Python package called [cmdline-provenance](http://cmdline-provenance.readthedocs.io/en/latest/)
that creates NCO/CDO-style records of what was executed at the command line.
We can install that package from the command line (Mac, Linux) or Anaconda Prompt (Windows),

~~~
$ pip install cmdline-provenance
~~~   
{: .language-bash}

and use it to generate a new command line record:

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
> >     new_log = cmdprov.new_log(infile_history={inargs.infile: cube.attributes['history']})
> >     fname, extension = inargs.outfile.split('.')
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
> import calendar
>
> import numpy
> import matplotlib.pyplot as plt
> import iris
> import iris.plot as iplt
> import iris.coord_categorisation
> import cmocean
> import cmdline_provenance as cmdprov
>
>
> def read_data(fname, month):
>     """Read an input data file"""
>    
>     cube = iris.load_cube(fname, 'precipitation_flux')
>    
>     iris.coord_categorisation.add_month(cube, 'time')
>     cube = cube.extract(iris.Constraint(month=month))
>    
>     return cube
>
>
> def convert_pr_units(cube):
>     """Convert kg m-2 s-1 to mm day-1"""
>    
>     assert cube.units == 'kg m-2 s-1', "Program assumes that input units are kg m-2 s-1"
>    
>     cube.data = cube.data * 86400
>     cube.units = 'mm/day'
>    
>     return cube
>
>
> def apply_mask(pr_cube, sftlf_cube, realm):
>     """Mask ocean using a sftlf (land surface fraction) file."""
>    
>     assert pr_cube.shape == sftlf_cube.shape 
>    
>     if realm == 'land':
>         mask = numpy.where(sftlf_cube.data > 50, True, False)
>     else:
>         mask = numpy.where(sftlf_cube.data < 50, True, False)
>    
>     pr_cube.data = numpy.ma.asarray(pr_cube.data)
>     pr_cube.data.mask = mask
>    
>     return pr_cube
>
>
> def plot_data(cube, month, gridlines=False, levels=None):
>     """Plot the data."""
>
>     if not levels:
>         levels = numpy.arange(0, 10)
>
>     fig = plt.figure(figsize=[12,5])    
>     iplt.contourf(cube, cmap=cmocean.cm.haline_r, 
>                   levels=levels,
>                   extend='max')
>
>     plt.gca().coastlines()
>     if gridlines:
>         plt.gca().gridlines()
>     cbar = plt.colorbar()
>     cbar.set_label(str(cube.units))
>    
>     title = '%s precipitation climatology (%s)' %(cube.attributes['model_id'], month)
>     plt.title(title)
>
>
> def main(inargs):
>     """Run the program."""
>
>     cube = read_data(inargs.infile, inargs.month)   
>     cube = convert_pr_units(cube)
>     clim = cube.collapsed('time', iris.analysis.MEAN)
>
>     if inargs.mask:
>         sftlf_file, realm = inargs.mask
>         assert realm in ['land', 'ocean']
>         sftlf_cube = iris.load_cube(sftlf_file, 'land_area_fraction')
>         clim = apply_mask(clim, sftlf_cube, realm)
>
>     plot_data(clim, inargs.month, gridlines=inargs.gridlines,
>               levels=inargs.cbar_levels)
>     plt.savefig(inargs.outfile)
>     write_metadata(inargs.outfile, cube.attributes['history'])
>
>     new_log = cmdprov.new_log(infile_history={inargs.infile: cube.attributes['history']})
>     fname, extension = inargs.outfile.split('.')
>     cmdprov.write_log(fname+'.txt', new_log)
>
>
> if __name__ == '__main__':
>
>     description='Plot the precipitation climatology for a given month.'
>     parser = argparse.ArgumentParser(description=description)
>     
>     parser.add_argument("infile", type=str, help="Input file name")
>     parser.add_argument("month", type=str, choices=calendar.month_abbr[1:], help="Month to plot")
>     parser.add_argument("outfile", type=str, help="Output file name")
>
>     parser.add_argument("--gridlines", action="store_true", default=False,
>                         help="Include gridlines on the plot")
>     parser.add_argument("--cbar_levels", type=float, nargs='*', default=None,
>                         help='list of levels / tick marks to appear on the colourbar')
>     parser.add_argument("--mask", type=str, nargs=2, metavar=('SFTLF_FILE', 'REALM'), default=None,
>                         help='Apply a land or ocean mask (specify the realm to mask: "land" or "ocean")')
>
>     args = parser.parse_args()            
>     main(args)
> ~~~
> {: .language-python}
{: .solution}