---
title: "Command line programs"
teaching: 25
exercises: 25
questions:
- "How can I write my own command line programs?"
objectives:
- "Use the `argparse` library to manage command-line arguments in a program."
- "Structure Python scripts according to a simple template."
- "Debug Python scripts using the `pdb` library."
keypoints:
- "Libraries such as `argparse` can be used the efficiently handle command line arguments."
- "Most Python scripts have a similar structure that can be used as a template."
- "The `pdb` library can be used to debug a Python script by stepping through line-by-line."
---

We've arrived at the point where we have successfully defined the functions
required to plot the precipitation data.

We could continue to execute these functions from the Jupyter notebook,
but in most cases notebooks are simply used to try things out
and/or take notes on a new data analysis task.
Once you've scoped out the task (as we have for plotting the precipitation climatology),
that code can be transferred to a Python script so that it can be executed at the command line.
It's likely that your data processing workflows will include command line utilities
from the CDO and NCO projects in addition to Python code,
so the command line is the natural place to manage your workflows
(e.g. using shell scripts or make files).

In general, the first thing that gets added to any Python script is the following:
~~~
if __name__ == '__main__':
    main()
~~~
{: .language-python}

The reason we need these two lines of code
is that running a Python script in bash is very similar to importing that file in Python. 
The biggest difference is that we don’t expect anything to happen when we import a file, 
whereas when running a script we expect to see some output
(e.g. an output file, figure and/or some text printed to the screen).

The `__name__` variable exists to handle these two situations.
When you import a Python file `__name__` is set to the name of that file
(e.g. when importing script.py, `__name__` is `script`),
but when running a script in bash `__name__` is always set to `__main__`.
The convention is to call the function that produces the output `main()`,
but you can call it whatever you like.

The next thing you'll need is a library to parse the command line for input arguments.
The most widely used option is 
[argparse](https://docs.python.org/3/library/argparse.html).

Putting those together,
here's a template for what most python command line programs look like:

~~~
$ cat code/script_template.py
~~~
{: .language-bash}

~~~
import argparse

#
# All your functions (that will be called by main()) go here.
#

def main(inargs):
    """Run the program."""

    print('Input file: ', inargs.infile)
    print('Output file: ', inargs.outfile)


if __name__ == '__main__':

    description='Print the input arguments to the screen.'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("infile", type=str, help="Input file name")
    parser.add_argument("outfile", type=str, help="Output file name")

    args = parser.parse_args()            
    main(args)
~~~
{: .language-python}

By running `script_template.py` at the command line
we'll see that `argparse` handles all the input arguments:

~~~
$ python script_template.py in.nc out.nc
~~~
{: .language-bash}

~~~
Input file:  in.nc
Output file:  out.nc
~~~
{: .output}

It also generates help information for the user:

~~~
$ python script_template.py -h
~~~
{: .language-bash}

~~~
usage: script_template.py [-h] infile outfile

Print the input arguments to the screen.

positional arguments:
  infile      Input file name
  outfile     Output file name

optional arguments:
  -h, --help  show this help message and exit
~~~
{: .output}

and issues errors when users give the program invalid arguments:

~~~
$ python script_template.py in.nc
~~~
{: .language-bash}

~~~
usage: script_template.py [-h] infile outfile
script_template.py: error: the following arguments are required: outfile
~~~
{: .output}

Using this template as a starting point,
we can add the functions we developed previously to a script called
`plot_precipitation_climatology.py`.

~~~
$ cat plot_precipitation_climatology.py
~~~
{: .language-bash}

~~~
import argparse
import iris
iris.FUTURE.netcdf_promote = True
import matplotlib.pyplot as plt
import iris.plot as iplt
import iris.coord_categorisation
import cmocean
import numpy


def read_data(fname, month):
    """Read an input data file"""
    
    cube = iris.load_cube(fname, 'precipitation_flux')
    
    iris.coord_categorisation.add_month(cube, 'time')
    cube = cube.extract(iris.Constraint(month=month))
    
    return cube


def convert_pr_units(cube):
    """Convert kg m-2 s-1 to mm day-1"""
    
    cube.data = cube.data * 86400
    cube.units = 'mm/day'
    
    return cube


def plot_data(cube, month, gridlines=False):
    """Plot the data."""
        
    fig = plt.figure(figsize=[12,5])    
    iplt.contourf(cube, cmap=cmocean.cm.haline_r, 
                  levels=numpy.arange(0, 10),
                  extend='max')

    plt.gca().coastlines()
    if gridlines:
        plt.gca().gridlines()
    cbar = plt.colorbar()
    cbar.set_label(str(cube.units))
    
    title = '%s precipitation climatology (%s)' %(cube.attributes['model_id'], month)
    plt.title(title)


def main(inargs):
    """Run the program."""

    cube = read_data(inargs.infile, inargs.month)    
    cube = convert_pr_units(cube)
    clim = cube.collapsed('time', iris.analysis.MEAN)
    plot_data(clim, inargs.month)
    plt.savefig(inargs.outfile)


if __name__ == '__main__':
    description='Plot the precipitation climatology.'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("infile", type=str, help="Input file name")
    parser.add_argument("month", type=str, help="Month to plot")
    parser.add_argument("outfile", type=str, help="Output file name")

    args = parser.parse_args()
    
    main(args)
~~~
{: .language-python}

... and then run it at the command line: 

~~~
$ python plot_precipitation_climatology.py data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc May pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512-may-clim.png
~~~
{: .language-bash}

> ## Debugging
>
> If you want know what your code is doing while it's running,
> insert a tracer using the Python debugger:
> ~~~
> import pdb
> 
> ...
> cube = read_data(inargs.infile, inargs.month)    
> pdb.set_trace()
> cube = convert_pr_units(cube)
> ...
> ~~~
> {: .language-python}
>
> When you run the script,
> it will stop at the tracer and allow you to interrogate the code:
> ~~~
> $ python plot_precipitation_climatology.py data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc May pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512-may-clim.png 
> /Users/damienirving/Documents/Volunteer/teaching/amos-icshmo/plot_precipitation_climatology.py(73)main()
> -> cube = convert_pr_units(cube)
>
> (Pdb) print(inargs.month)
> May
> ~~~
> {: .language-bash}
>
> You can then enter `n` to go to the next command,
> `s` to step into the next function,
> `c` to run the rest of the script or
> `q` to quit.
>
{: .callout}


> ## Choices
>
> Take (i.e. cut and paste to create a new file)
> the `plot_precipitation_climatology.py` script shown above
> and save it in your `data-carpentry` directory.
>
> Using the [argparse tutorial](https://docs.python.org/3/howto/argparse.html) as a guide
> and `pdb` to debug where necessary,
> now make the following improvement to `plot_precipitation_climatology.py`: 
>
> The `parser.add_argument()` function has an optional `choices` keyword argument.
> Use it to define the valid input months (i.e. `['Jan', 'Feb', ...]`).
>
> > ## Solution
> >
> > ~~~
> > parser.add_argument("month", type=str,
> >                     choices=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 
> >                     help="Month to plot")
> > ~~~                         
> > {: .language-python}
> >
> > OR
> >
> > ~~~
> > import calendar
> > parser.add_argument("month", type=str, choices=calendar.month_abbr[1:], 
> >                     help="Month to plot")
> > ~~~                         
> > {: .language-python}
> {: .solution}
{: .challenge}

> ## Gridlines
> 
> Add a true/false optional `argparse` argument to allow the user to add gridlines to the plot.
> 
> > ## Solution
> > ~~~
> > if gridlines:
> >     plt.gca().gridlines()
> >
> > ...
> >
> > parser.add_argument("--gridlines", action="store_true", default=False,
> >                     help="Include gridlines on the plot")
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}

> ## Colorbar levels
>
> Add an optional `argparse` argument that allows the user to specify the tick levels used in the colourbar 
>
> > ## Solution
> > ~~~
> > parser.add_argument("--cbar_levels", type=float, nargs='*', default=None,
> >                     help='list of levels / tick marks to appear on the colourbar') 
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}

> ## Free time
>
> Add any other options you'd like for customising the plot (e.g. title, axis labels, figure size).
> 
{: .challenge}

> ## plot_precipitation_climatology.py
>
> At the conclusion of this lesson your `plot_precipitation_climatology.py` script
> should look something like the following:
>
> ~~~
> import argparse
> import iris
> iris.FUTURE.netcdf_promote = True
> import matplotlib.pyplot as plt
> import iris.plot as iplt
> import iris.coord_categorisation
> import cmocean
> import numpy
> import pdb
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
>     cube.data = cube.data * 86400
>     cube.units = 'mm/day'
>    
>     return cube
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
>     plot_data(clim, inargs.month, gridlines=inargs.gridlines,
>               levels=inargs.cbar_levels)
>     plt.savefig(inargs.outfile)
>
>
> if __name__ == '__main__':
>
>     description='Plot the precipitation climatology.'
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
>
>     args = parser.parse_args()            
>     main(args)
> ~~~
> {: .language-python}
{: .solution}
