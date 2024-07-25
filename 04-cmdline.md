---
title: Command line programs
teaching: 20
exercises: 30
---

::::::::::::::::::::::::::::::::::::::: objectives

- Use the `argparse` library to manage command-line arguments in a program.
- Structure Python scripts according to a simple template.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- How can I write my own command line programs?

::::::::::::::::::::::::::::::::::::::::::::::::::

We've arrived at the point where we have successfully defined the functions
required to plot the precipitation data.

We could continue to execute these functions from the Jupyter notebook,
but in most cases notebooks are simply used to try things out
and/or take notes on a new data analysis task.
Once you've scoped out the task (as we have for plotting the precipitation climatology),
that code can be transferred to a Python script so that it can be executed at the command line.
It's likely that your data processing workflows will include command line utilities
from the [CDO](https://code.mpimet.mpg.de/projects/cdo) and
[NCO](https://nco.sourceforge.net/) projects in addition to Python code,
so the command line is the natural place to manage your workflows
(e.g. using shell scripts or make files).

In general, the first thing that gets added to any Python script is the following:

```python
if __name__ == "__main__":
    main()
```

The reason we need these two lines of code
is that running a Python script in bash is very similar to importing that file in Python.
The biggest difference is that we don't expect anything to happen when we import a file, whereas when running a script we expect to see some output
(e.g. an output file, figure and/or some text printed to the screen).

The `__name__` variable exists to handle these two situations.
When you import a Python file `__name__` is set to the name of that file
(e.g. when importing script.py, `__name__` is `script`),
but when running a script in bash `__name__` is always set to `__main__`.
The convention is to call the function that produces the output `main()`,
but you can call it whatever you like.

The next thing you'll need is a library to parse the command line for input arguments.
The most widely used option is [argparse](https://docs.python.org/3/library/argparse.html).

Putting those together,
here's a template for what most python command line programs look like:

```bash
$ cat script_template.py
```

```python
import argparse

#
# All your functions (that will be called by main()) go here.
#

def main(inargs):
    """Run the program."""

    print("Input file: ", inargs.infile)
    print("Output file: ", inargs.outfile)


if __name__ == "__main__":

    description = "Print the input arguments to the screen."
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("infile", type=str, help="Input file name")
    parser.add_argument("outfile", type=str, help="Output file name")

    args = parser.parse_args()            
    main(args)
```

By running `script_template.py` at the command line
we'll see that `argparse` handles all the input arguments:

```bash
$ python script_template.py in.nc out.nc
```

```output
Input file:  in.nc
Output file:  out.nc
```

It also generates help information for the user:

```bash
$ python script_template.py -h
```

```output
usage: script_template.py [-h] infile outfile

Print the input arguments to the screen.

positional arguments:
  infile      Input file name
  outfile     Output file name

optional arguments:
  -h, --help  show this help message and exit
```

and issues errors when users give the program invalid arguments:

```bash
$ python script_template.py in.nc
```

```output
usage: script_template.py [-h] infile outfile
script_template.py: error: the following arguments are required: outfile
```

Using this template as a starting point,
we can add the functions we developed previously to a script called
`plot_precipitation_climatology.py`.

```bash
$ cat plot_precipitation_climatology.py
```

```python
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import cmocean
import argparse


def convert_pr_units(da):
    """Convert kg m-2 s-1 to mm day-1.
    
    Args:
      da (xarray.DataArray): Precipitation data
    
    """
    
    da.data = darray.data * 86400
    da.attrs["units"] = "mm/day"
    
    return da


def create_plot(clim, model, season, gridlines=False):
    """Plot the precipitation climatology.
    
    Args:
      clim (xarray.DataArray): Precipitation climatology data
      model (str): Name of the climate model
      season (str): Season
      
    Kwargs:  
      gridlines (bool): Select whether to plot gridlines    
    
    """
        
    fig = plt.figure(figsize=[12,5])
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
    clim.sel(season=season).plot.contourf(
        ax=ax,
        levels=np.arange(0, 13.5, 1.5),
        extend="max",
        transform=ccrs.PlateCarree(),
        cbar_kwargs={"label": clim.units},
        cmap=cmocean.cm.haline_r,
    )
    ax.coastlines()
    if gridlines:
        plt.gca().gridlines()
    
    title = f"{model} precipitation climatology ({season})"
    plt.title(title)


def main(inargs):
    """Run the program."""

    ds = xr.open_dataset(inargs.pr_file)
    
    clim = ds["pr"].groupby("time.season").mean("time", keep_attrs=True)
    clim = convert_pr_units(clim)

    create_plot(clim, ds.attrs["source_id"], inargs.season)
    plt.savefig(
        inargs.output_file,
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
    )


if __name__ == "__main__":
    description='Plot the precipitation climatology.'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("pr_file", type=str, help="Precipitation data file")
    parser.add_argument("season", type=str, help="Season to plot")
    parser.add_argument("output_file", type=str, help="Output file name")

    args = parser.parse_args()
    
    main(args)
```

... and then run it at the command line:

```bash
$ python plot_precipitation_climatology.py data/pr_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_201001-201412.nc MAM pr_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_201001-201412-MAM-clim.png
```

:::::::::::::::::::::::::::::::::::::::  challenge

## Choices

For this series of challenges,
you are required to make improvements to the `plot_precipitation_climatology.py` script
that you downloaded earlier from the setup tab at the top of the page.

For the first improvement,
edit the line of code that defines the season command line argument
(`parser.add_argument("season", type=str, help="Season to plot")`)
so that it only allows the user to input a valid three letter abbreviation
(i.e. `["DJF", "MAM", "JJA", "SON"]`).

(Hint: Read about the `choices` keyword argument
at the [argparse tutorial](https://docs.python.org/3/howto/argparse.html).)

:::::::::::::::  solution

```python
parser.add_argument(
    "season",
    type=str,
    choices=["DJF", "MAM", "JJA", "SON"], 
    help="Season to plot",
)
```

:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge

## Gridlines

Add an optional command line argument that allows the user to add gridlines to the plot.

(Hint: Read about the `action="store_true"` keyword argument
at the [argparse tutorial](https://docs.python.org/3/howto/argparse.html).)

:::::::::::::::  solution

Make the following additions to `plot_precipitation_climatology.py`
(code omitted from this abbreviated version of the script is denoted `...`):

```python
...

def main(inargs):

   ... 

   create_plot(
       clim,
       ds.attrs["source_id"],
       inargs.season,
       gridlines=inargs.gridlines,
    )

...

if __name__ == "__main__":

    ... 

    parser.add_argument(
        "--gridlines",
        action="store_true",
        default=False,
        help="Include gridlines on the plot",
    )

... 

```

:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge

## Colorbar levels

Add an optional command line argument that allows the user to specify the tick levels used in the colourbar

(Hint: You'll need to use the `nargs='*'` keyword argument.)

:::::::::::::::  solution

## Solution

Make the following additions to `plot_precipitation_climatology.py`
(code omitted from this abbreviated version of the script is denoted `...`):

```python
...

def create_plot(clim, model_name, season, gridlines=False, levels=None):
    """Plot the precipitation climatology.
      ...
      Kwargs:
        gridlines (bool): Select whether to plot gridlines
        levels (list): Tick marks on the colorbar      
   
    """

    if not levels:
        levels = np.arange(0, 13.5, 1.5)

    ...

    clim.sel(season=season).plot.contourf(
        ax=ax,
        ...,
    )

...

def main(inargs):

    ... 

    create_plot(
        clim,
        ds.attrs["source_id"],
        inargs.season,
        gridlines=inargs.gridlines,
        levels=inargs.cbar_levels,
    )

...

if __name__ == "__main__":

    ... 

    parser.add_argument(
        "--cbar_levels",
        type=float,
        nargs="*",
        default=None,
        help="list of levels / tick marks to appear on the colorbar",
    )

... 

```

:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge

## Free time

Add any other options you'd like for customising the plot (e.g. title, axis labels, figure size).

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge

## plot\_precipitation\_climatology.py

At the conclusion of this lesson your `plot_precipitation_climatology.py` script
should look something like the following:

:::::::::::::::  solution

```python
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import cmocean
import argparse


def convert_pr_units(da):
    """Convert kg m-2 s-1 to mm day-1.
   
    Args:
      da (xarray.DataArray): Precipitation data
    
    """
    
    da.data = darray.data * 86400
    da.attrs["units"] = "mm/day"
   
    return da


def create_plot(clim, model, season, gridlines=False, levels=None):
    """Plot the precipitation climatology.
   
    Args:
      clim (xarray.DataArray): Precipitation climatology data
      model (str): Name of the climate model
      season (str): Season
      
    Kwargs:
      gridlines (bool): Select whether to plot gridlines
      levels (list): Tick marks on the colorbar    
    
    """

    if not levels:
        levels = np.arange(0, 13.5, 1.5)
        
    fig = plt.figure(figsize=[12,5])
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
    clim.sel(season=season).plot.contourf(
        ax=ax,
        levels=levels,
        extend="max",
        transform=ccrs.PlateCarree(),
        cbar_kwargs={"label": clim.units},
        cmap=cmocean.cm.haline_r,
    )
    ax.coastlines()
    if gridlines:
        plt.gca().gridlines()
    
    title = f"{model} precipitation climatology ({season})"
    plt.title(title)


def main(inargs):
    """Run the program."""

    ds = xr.open_dataset(inargs.pr_file)
    
    clim = ds["pr"].groupby("time.season").mean("time", keep_attrs=True)
    clim = convert_pr_units(clim)

    create_plot(
        clim,
        ds.attrs["source_id"],
        inargs.season,
        gridlines=inargs.gridlines,
        levels=inargs.cbar_levels,
    )
    plt.savefig(
        inargs.output_file,
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
    )


if __name__ == "__main__":
    description = "Plot the precipitation climatology."
    parser = argparse.ArgumentParser(description=description)
   
    parser.add_argument("pr_file", type=str, help="Precipitation data file")
    parser.add_argument("season", type=str, help="Season to plot")
    parser.add_argument("output_file", type=str, help="Output file name")

    parser.add_argument(
        "--gridlines",
        action="store_true",
        default=False,
        help="Include gridlines on the plot",
    )
    parser.add_argument(
        "--cbar_levels",
        type=float,
        nargs="*",
        default=None,
        help="list of levels / tick marks to appear on the colorbar",
    )

    args = parser.parse_args()
    main(args)

```

:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: keypoints

- Libraries such as `argparse` can be used the efficiently handle command line arguments.
- Most Python scripts have a similar structure that can be used as a template.

::::::::::::::::::::::::::::::::::::::::::::::::::


