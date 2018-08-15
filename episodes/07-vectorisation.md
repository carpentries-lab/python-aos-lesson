---
title: "Vectorisation"
teaching: 15
exercises: 15
questions:
- "How can I avoid looping over each element of large data arrays?"
objectives:
- "Use `numpy` masked arrays together with surface land fraction data to mask the land or ocean."
- "Use the vectorised operations available in the `numpy` library to avoid looping over array elements."
keypoints:
- "For large arrays, looping over each element can be slow in high-level languages like Python."
- "Vectorised operations can be used to avoid looping over array elements."
---

A requirement that we haven't yet addressed is the option to apply a land or ocean mask.
To do this, we need to use the land surface fraction file.

~~~
import iris
import numpy

access_sftlf_file = 'data/sftlf_fx_ACCESS1-3_historical_r0i0p0.nc'

sftlf_cube = iris.load_cube(access_sftlf_file, 'land_area_fraction')
print(sftlf_cube)
~~~
{: .language-python}

~~~
land_area_fraction / (%)            (latitude: 145; longitude: 192)
     Dimension coordinates:
          latitude                           x               -
          longitude                          -               x
     Attributes:
          Conventions: CF-1.4
          associated_files: baseURL: http://cmip-pcmdi.llnl.gov/CMIP5/dataLocation gridspecFile: gridspec_atmos_fx_ACCESS1-3_historical_r0i0p0.nc...
          branch_time: 90945.0
          cmor_version: 2.8.0
          contact: The ACCESS wiki: http://wiki.csiro.au/confluence/display/ACCESS/Home. Contact...
          creation_date: 2012-02-15T06:14:44Z
          experiment: historical
          experiment_id: historical
          forcing: GHG, Oz, SA, Sl, Vl, BC, OC, (GHG = CO2, N2O, CH4, CFC11, CFC12, CFC113,...
          frequency: fx
          history: 2012-02-15T06:14:43Z altered by CMOR: Converted units from '1' to '%'....
          initialization_method: 0
          institute_id: CSIRO-BOM
          institution: CSIRO (Commonwealth Scientific and Industrial Research Organisation, Australia),...
          model_id: ACCESS1.3
          modeling_realm: atmos
          original_units: 1
          parent_experiment: pre-industrial control
          parent_experiment_id: piControl
          parent_experiment_rip: r1i1p1
          physics_version: 0
          product: output
          project_id: CMIP5
          realization: 0
          references: See http://wiki.csiro.au/confluence/display/ACCESS/ACCESS+Publications
          source: ACCESS1-3 2011. Atmosphere: AGCM v1.0 (N96 grid-point, 1.875 degrees EW...
          table_id: Table fx (01 February 2012) 4a159bff0ec5e3f2ffff0b0475e89009
          title: ACCESS1-3 model output prepared for CMIP5 historical
          tracking_id: 50a2eb82-3b87-43df-bcb9-2fe82590a424
          version_number: v20120413
~~~
{: .output}

The data in a sftlf file assigns each grid cell a percentage value
between 0% (no land) to 100% (all land).

~~~
print(sftlf_cube.data.max())
print(sftlf_cube.data.min())
~~~
{: .language-python}

~~~
100.0
0.0
~~~
{: .output}

To create a [numpy masked array](https://docs.scipy.org/doc/numpy/reference/maskedarray.html),
we need to assign each grid cell a `True` (apply mask) or `False` (do not apply mask) value.
For this example, we are going to define the ocean as any cell that is less than 50% land
(and the land as any cell greater than 50%).

The most obvious solution to creating an ocean mask, for example,
might then be to loop over each cell in the sftlf array. e.g.

~~~
nlats, nlons = sftlf_cube.data.shape
mask = numpy.zeros([nlats, nlons])
for y in range(nlats):
    for x in range(nlons):
        if sftlf_cube.data[y, x] < 50:
            mask[y, x] = True
        else:
            mask[y, x] = False
~~~
{: .language-python}

While this approach would technically work,
the problem is that (a) the code is hard to read,
and (b) in contrast to low level languages like Fortran and C,
high level languages like Python and Matlab are built for usability
(i.e. they make it easy to write concise, readable code) as opposed to speed.
This particular array is so small that the looping isn't noticably slow,
but in general looping over every data point in an array should be avoided.

Fortunately, there are lots of numpy functions that allow you to get around this problem
by applying a particular operation to an entire array at once
(which is known as a vectorised operation).
The `numpy.where` function, for instance,
allows us to make a true/false decision at each data point in the array
and then perform a different action depending on the answer:

~~~
ocean_mask = numpy.where(sftlf_cube.data < 50, True, False)
land_mask = numpy.where(sftlf_cube.data > 50, True, False)
~~~
{: .language-python}


For a given iris cube (e.g. containing precipitation data from the ACCESS1-3 model),
we could then replace the current data mask (which is false at all points)
with our new ocean mask:

~~~
cube = iris.load_cube('data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc',
                      'precipitation_flux')
type(cube.data)
~~~
{: .language-python}

~~~
numpy.ma.core.MaskedArray
~~~
{: .output}

~~~
cube.data.mask = ocean_mask
~~~
{: .language-python}

By printing the array we can see that some values are now masked:

~~~
print(cube.data[0, 100:110, 0:10])
~~~
{: .language-python}

~~~
[[2.4865681552910246e-05 1.7857040802482516e-05 1.4409809409698937e-05
  1.365557181998156e-05 9.77409854385769e-07 1.6724919760235935e-07 -- --
  -- --]
 [-- 3.080878741457127e-05 2.1845595256309025e-05 2.4051765649346635e-05
  1.7585027308086865e-05 1.6222168142121518e-06 -- -- -- --]
 [-- -- -- -- -- -- -- -- -- --]
 [2.005224087042734e-05 -- -- -- -- -- -- -- 3.166760870954022e-05
  1.2054460967192426e-05]
 [1.4890032616676763e-05 -- -- -- -- 2.3196560505311936e-05 -- --
  6.278240471147001e-05 2.7597512598731555e-05]
 [1.0251545063511003e-05 -- -- -- -- 3.0613329727202654e-05 -- --
  2.898933416872751e-05 --]
 [1.4132613614492584e-05 7.409330464724917e-06 -- -- -- -- --
  3.593934889067896e-05 -- --]
 [4.693903247243725e-05 3.182605723850429e-05 1.990660712181125e-05
  8.492984306940343e-06 -- -- 2.465165925968904e-05 -- --
  0.0001078539207810536]
 [6.071893949410878e-05 6.422175647458062e-05 5.667455116054043e-05
  2.7484224119689316e-05 9.198953193845227e-06 1.1014224583050236e-05
  1.7008713257382624e-05 -- -- 5.8094596170121804e-05]
 [4.4121807150077075e-05 5.2677831263281405e-05 6.721866520820186e-05
  7.12903929525055e-05 3.726803697645664e-05 1.741481537465006e-05
  2.0027844584546983e-05 2.576560655143112e-05 3.483034743112512e-05
  3.593379369704053e-05]]
~~~
{: .output}

> ## Mask option
>
> Modify `plot_precipitation_climatology.py` so that the user can choose to apply a mask
> via the following `argparse` option.
> This should involve defining a new function called `apply_mask()`,
> in order to keep `main()` short and readable.
>
> ~~~
> parser.add_argument("--mask", type=str, nargs=2,
>                     metavar=('SFTLF_FILE', 'REALM'), default=None,
>                     help='Apply a land or ocean mask (specify the realm to mask)')
> ~~~
> {: .language-python}
>
> Test to see if your mask worked by plotting the ACCESS1-3 climatology for January:
>
> ~~~
> $ python plot_precipitation_climatology.py data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc Jan pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512-jan-clim_land-mask.png --mask data/sftlf_fx_ACCESS1-3_historical_r0i0p0.nc land
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
> > def apply_mask(pr_cube, sftlf_cube, realm):
> >     """Mask ocean using a sftlf (land surface fraction) file."""
> >    
> >     if realm == 'land':
> >         mask = numpy.where(sftlf_cube.data > 50, True, False)
> >     else:
> >         mask = numpy.where(sftlf_cube.data < 50, True, False)
> >    
> >     pr_cube.data.mask = mask
> > 
> > ...
> >
> > def main(inargs):
> >     """Run the program."""
> >
> >     cube = read_data(inargs.infile, inargs.month)  
> >     cube = convert_pr_units(cube)
> >     clim = cube.collapsed('time', iris.analysis.MEAN)
> >
> >     if inargs.mask:
> >         sftlf_file, realm = inargs.mask
> >         sftlf_cube = iris.load_cube(sftlf_file, 'land_area_fraction')
> >         clim = apply_mask(clim, sftlf_cube, realm) 
> >
> >     ...
> >
> > if __name__ == '__main__':
> >
> >     description='Plot the precipitation climatology.'
> >     parser = argparse.ArgumentParser(description=description)
> >
> >     ...
> >    
> >     parser.add_argument("--mask", type=str, nargs=2, metavar=('SFTLF_FILE', 'REALM'), default=None,
> >                            help='Apply a land or ocean mask (specify the realm to mask)')
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
>     cube.data = cube.data * 86400
>     cube.units = 'mm/day'
>    
>     return cube
>
>
> def apply_mask(pr_cube, sftlf_cube, realm):
>     """Mask ocean using a sftlf (land surface fraction) file."""
>    
>     if realm == 'land':
>         mask = numpy.where(sftlf_cube.data > 50, True, False)
>     else:
>         mask = numpy.where(sftlf_cube.data < 50, True, False)
>    
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
>         sftlf_cube = iris.load_cube(sftlf_file, 'land_area_fraction')
>         clim = apply_mask(clim, sftlf_cube, realm)
>
>     plot_data(clim, inargs.month, gridlines=inargs.gridlines,
>               levels=inargs.cbar_levels)
>     plt.savefig(inargs.outfile)
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
