---
title: Defensive programming
teaching: 15
exercises: 15
---

::::::::::::::::::::::::::::::::::::::: objectives

- Signal errors by raising exceptions.
- Use try-except blocks to catch and handle exceptions.
- Explain what an assertion is.
- Add assertions that check the program's state is correct.
- Use a logging framework to report on program activity.
- Identify sources of more advanced lessons on code testing.

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: questions

- How can I make my programs more reliable?

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::  callout

## Scientist's nightmare

If you needed any motivation to learn and employ the principles of defensive programming,
look no further than [this article](https://science.sciencemag.org/content/314/5807/1856).
It documents the experience of a researcher who had to retract five published papers -
three of which were in *Science* - because his code had inadvertently switched
the rows and columns of a data table.

::::::::::::::::::::::::::::::::::::::::::::::::::

Now that we've written `plot_precipitation_climatology.py`,
how can we be sure that it's producing reliable results?

The first step toward getting the right answers from our programs
is to assume that mistakes *will* happen
and to guard against them.
This is called defensive programming,
and there are a number of tools and approaches at our disposal for doing this.
Broadly speaking, we can raise and handle errors to check and respond to program inputs,
use assertions to make sure nothing crazy or unexpected has happened,
write unit tests to make sure each component of our program produces expected outputs,
and use a logging framework to report on program activity.
In this lesson, we'll look at how error handling, assertions and logging
can make the unit conversion in our program more reliable,
and we'll provide links to further information on unit .

## Types of errors

There are essentially two kinds of errors that can arise in Python:
*syntax errors* and *exceptions*.
You're probably familiar with the former:

```python
rainfall = 5
if rainfall > 10
    print("heavy rainfall")
```

```error
    if rainfall > 10
                    ^
SyntaxError: expected ':'
```

Once a statement or expression is syntactically correct,
it may cause an error when an attempt is made to execute it.
Errors detected during execution are called exceptions
(i.e. an exception from normal behaviour)
and there are lots of different types of exceptions:

```python
10 * (1/0)
```

```error
ZeroDivisionError: division by zero
```

```python
4 + spam*3
```

```error
NameError: name 'spam' is not defined
```

```python
"2" + 2
```

```error
TypeError: can only concatenate str (not "int") to str
```

## Raising errors

With respect to defensive programming,
it can sometimes be useful to raise your own exceptions (using the `raise` keyword).

```python
infile = "temperature_data.txt"
file_format = infile.split(".")[-1]
if file_format != "nc":
    raise ValueError(f"{infile} does not have the netCDF file extension .nc")
```

```error
ValueError                                Traceback (most recent call last)
/var/folders/6v/vrpsky6j509dff7250jyg8240000gp/T/ipykernel_12425/3612736507.py in <module>
      2 file_format = infile.split(".")[-1]
      3 if file_format != "nc":
----> 4     raise ValueError(f"{infile} does not have the netCDF file extension .nc")

ValueError: temperature_data.txt does not have the netCDF file extension .nc
```

In this case we've chosen to raise a `ValueError`,
but we could pick any of the [builtin exception types](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)
(including just a generic `Exception`)
or define our own [custom exception class](https://towardsdatascience.com/how-to-define-custom-exception-classes-in-python-bfa346629bca).

In the context of our `plot_precipitation_climatology.py` script,
we currently multiply our data by 86400 regardless of what the input units are.
It would be better if we modified the `main` function so that the program
multiplied by 86400 if the input units are kg m-2 s-1,
performed no unit conversion if the input units are mm/day,
or halted with an informative error message if the input data have some other units.

```python
input_units = clim.attrs["units"]
if input_units == "kg m-2 s-1":
    clim = convert_pr_units(clim)
elif input_units == "mm/day":
    pass
else:
    raise ValueError("""Input units are not 'kg m-2 s-1' or 'mm/day'""")
```

## Handling errors

As we've seen in the examples above,
if exceptions aren't dealt with the program crashes.
The error message upon crashing is sometimes be easy to understand
(particularly if you wrote the `raise` statement yourself)
but can often be cryptic.

If we'd rather the program didn't crash when a particular exception occurs,
we can use a try-except block to catch and handle the exception.
The syntax of the try-except block is:

```python
try:
    <do something>
except Exception:
    <handle the error>
```

The code in the except block is only executed if an exception occurred in the try block.
The except block is required with a try block, even if it contains only the `pass` statement
(i.e. ignore the exception and carry on).
For example,
let's say there's a calculation in our program where we need to divide
by the number of available weather stations.
If there were no weather stations available,
by default the program would crash.

```python
quantity = 500
n_stations = 0

scaled_quantity = quantity / n_stations
print(scaled_quantity)
```

```error
ZeroDivisionError                         Traceback (most recent call last)
/var/folders/6v/vrpsky6j509dff7250jyg8240000gp/T/ipykernel_12425/3927438267.py in <module>
      2 n_stations = 0
      3 
----> 4 scaled_quantity = quantity / n_stations
      5 print(scaled_quantity)

ZeroDivisionError: division by zero
```

If we'd prefer the program simply continue with a `scaled_quantity` value of NaN,
we could catch and handle the `ZeroDivisionError`.

```python
import numpy as np


quantity = 500
n_stations = 0

try:
    scaled_quantity = quantity / n_stations
except ZeroDivisionError:
    scaled_quantity = np.nan

print(scaled_quantity)
```

```output
nan
```

In the context of our `plot_precipitation_climatology.py` script,
the variable attributes from the input netCDF file are stored in a dictionary
that we access via `clim.attrs`.
The dictionary keys are the names of the variable attributes
(e.g. `standard_name`, `long_name`, `units`)
and the dictionary values are the values corresponding to those keys
(e.g. `precipitation_flux`, `Precipitation`, `kg m-2 s-1`).
If the input data file didn't have a units attribute associated with the precipitation variable,
our program would currently fail with a `KeyError`
(which Python raises when you ask for a key that isn't in a dictionary).

```python
example_dict = {
    "standard_name": "precipitation_flux",
    "long_name": "Precipitation",
}
units = example_dict["units"]
```

```error
KeyError                                  Traceback (most recent call last)
/var/folders/6v/vrpsky6j509dff7250jyg8240000gp/T/ipykernel_12425/2679443625.py in <module>
      1 example_dict = {
      2     "standard_name": "precipitation_flux",
      3     "long_name": "Precipitation",
      4 }
----> 5 units = example_dict["units"]

KeyError: 'units'
```

It's fine that our program would crash in this situation
(we can't continue if we don't know the units of the input data),
but the error message doesn't explicitly tell the user that the
input file requires a units attribute.
To make this crystal clear,
we could use a try-except block in the `main` function to catch the `KeyError`
and re-define a better error message.

```python
try:
    input_units = clim.attrs["units"]
except KeyError:
    raise KeyError(f"Precipitation variable in {inargs.pr_file} does not have a units attribute")
```

## Assertions

Unexpected behaviour in a program can sometimes propagate a long way
before triggering an exception or producing a perplexing result.
For instance,
if a calculation produces a non-physical value for precipitation (e.g. a negative value)
that value could be used in various downstream calculations of drought and fire risk
(combined with values for temperature, wind, humidity, etc).
The final plot of the forest fire danger index might look wrong
(or not, which would be even worse)
to the scientist who wrote and executed the code,
but it wouldn't be immediately obvious that the precipitation calculation
was the source of the problem.

In order to avoid propagation,
it's best to nip unexpected behaviour in the bud right when it occurs.
One way to do this is to add assertions to your code.
An assertion is simply a statement that something must be true at a certain point in a program.
When Python sees one,
it evaluates the assertion's condition.
If it's true,
Python does nothing,
but if it's false,
Python halts the program immediately
and raises an `AssertionError` with a custom error message.

To demonstrate an assertion in action,
consider this piece of code that halts if any precipitation data is negative:

```python
import numpy as np

pr_data = np.array([1.5, 2.3, 0.7, -0.2, 4.4])
assert pr_data.min() >= 0.0, "There is at least one negative precipitation value"
```

```error
---------------------------------------------------------------------------
AssertionError                            Traceback (most recent call last)
<ipython-input-19-33d87ea29ae4> in <module>()
----> 1 assert pr_data.min() >= 0.0, "There is at least one negative precipitation value"

AssertionError: There is at least one negative precipitation value
```

With respect to our command line program,
one thing to check would be that the climatological precipitation values lie within
a sensible range after the unit conversion.
The [world record highest daily rainfall total](https://wmo.asu.edu/content/world-greatest-twenty-four-hour-1-day-rainfall)
is 1825mm (at Reunion Island in 1966),
so climatological values across the globe should be more than 0 but less than 2000 mm/day.
We could add the following assertions to our `convert_pr_units` function
to catch unexpected precipitation values.

```python
assert darray.data.min() >= 0.0, "There is at least one negative precipitation value"
assert darray.data.max() < 2000, "There is a precipitation value/s > 2000 mm/day"
```

Assertions are also used in unit testing
(each test culminates in an assertion),
but that topic is beyond the scope of this lesson.

:::::::::::::::::::::::::::::::::::::::::  callout

## Testing and continuous integration

An assertion checks that something is true at a particular point in the program.
For programs that are more complex (or research critical) than `plot_precipitation_climatology.py`,
it's a good idea to take the next step and check the overall behavior of entire pieces (or units) of code.
Related concepts like unit testing and continuous integration are beyond the scope of this lesson,
but *Research Software Engineering With Python* has a [chapter on testing](https://third-bit.com/py-rse/testing.html)
that is well worth a read.

::::::::::::::::::::::::::::::::::::::::::::::::::

## Logging

So far we've considered how to make our programs halt or handle the situation when things go wrong.
Another option in our defensive programming toolkit is to have our programs report their own activity.

For example,
let's say we're working with relative humidity data.
We wouldn't typically expect to encounter any values over 100%, but it is physically possible.
Rather than halt the program if a value over 100% occurs,
we might therefore want our program to simply report the maximum relative humidity.
We can then decide whether to trust the output or not
(e.g. a value of 100.1% might be ok but not 150%).

To do this reporting,
our first instinct might be to add a `print` statement to the program.

```python
rh_data = np.array([1.5, 20.4, 100.1, 76.3, 54.4])
rh_max = rh_data.max()
print(f"The maximum relative humidity was {rh_max}%")
```

```output
The maximum relative humidity was 100.1%
```

The problem with this approach is that information printed to the screen is lost
once we close our command line session.
Constantly adding, removing or commenting out `print` statements is also tedious and error-prone.

A better approach is to use a logging framework,
such as Python's `logging` library.
This lets us leave debugging statements in our code and turn them on or off at will.
Let's start by replacing our `print` statement with a `logging` command.

```python
import logging

rh_data = np.array([1.5, 20.4, 100.1, 76.3, 54.4])
rh_max = rh_data.max()
logging.debug(f"The maximum relative humidity was {rh_max}%")
```

Whoops!
There's no output because by default the logging library only reports information
at the "warning" level and above.
In order of increasing severity, the available levels are:

- `debug`: very detailed information used for localizing errors.
- `info`: confirmation that things are working as expected.
- `warning`: something unexpected happened, but the program will keep going.
- `error`: something has gone badly wrong, but the program hasn't hurt anything.
- `critical`: potential loss of data, security breach, etc.

If we want to see the output from less severe levels (i.e. turn our debugging statements on),
we'd need to change the minimum level in the logging configuration.
We can also provide the name of a file to write the logging information to,
so that it isn't lost when we finish our command line session.

```python
# for loop only required in notebooks
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    
logging.basicConfig(level=logging.DEBUG, filename="log.txt")) 

rh_data = np.array([1.5, 20.4, 100.1, 76.3, 54.4])
rh_max = rh_data.max()
logging.debug(f"The maximum relative humidity was {rh_max}%")
```

(The for loop is needed to turn off the background logging the notebook does itself.
It's not needed in a Python script.)

Notice that we've used capital `logging.DEBUG` (which is an integer value) to set the logging level,
as opposed to the `logging.debug` function that is used for logging a message.

By setting the logging level to "DEBUG",
our output "log.txt" file will now capture all logging information
with a flag of 'debug' or higher - that is,
all logging outputs will be written to our log file.

```bash
$ cat log.txt
```

```output
DEBUG:root:The maximum relative humidity was 100.1%
```

In the context of the `plot_precipitation_climatology.py` script,
it would be nice to know whether or not unit conversion was performed.
To do this we just need a few small changes to the script.
We need to import the logging library at the top of the script,

```python
import logging
```

and set the logging configuration and add a `logging.info` command in the `main` function.

```python
def main(inargs):
    """Run the program."""
    
    logging.basicConfig(level=logging.DEBUG, filename="log.txt") 
    
    ...
    
    if input_units == 'kg m-2 s-1':
        clim = convert_pr_units(clim)
        logging.info("Units converted from kg m-2 s-1 to mm/day")
    elif input_units == "mm/day":
        pass
    else:
        raise ValueError("""Input units are not 'kg m-2 s-1' or 'mm/day'""")
    
    ...
```

:::::::::::::::::::::::::::::::::::::::  challenge

## Update your script

Update your working copy of `plot_precipitation_climatology.py`
with the changes from this lesson.

This will mean your `main` function will now read as follows,

```python
def main(inargs):
    """Run the program."""

    logging.basicConfig(level=logging.DEBUG, filename="log.txt") 

    ds = xr.open_dataset(inargs.pr_file)
   
    clim = ds["pr"].groupby("time.season").mean("time", keep_attrs=True)

    try:
        input_units = clim.attrs["units"]
    except KeyError:
        raise KeyError(f"Precipitation variable in {inargs.pr_file} must have a units attribute")

    if input_units == "kg m-2 s-1":
        clim = convert_pr_units(clim)
        logging.info("Units converted from kg m-2 s-1 to mm/day")
    elif input_units == "mm/day":
        pass
    else:
        raise ValueError("""Input units are not 'kg m-2 s-1' or 'mm/day'""")

    if inargs.mask:
        sftlf_file, realm = inargs.mask
        clim = apply_mask(clim, sftlf_file, realm)

    create_plot(
        clim,
        dset.attrs["source_id"],
        inargs.season,
        gridlines=inargs.gridlines,
        levels=inargs.cbar_levels
    )    
    plt.savefig(
        inargs.output_file,
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
    )
```

and your `convert_pr_units` as:

```python
def convert_pr_units(da):
    """Convert kg m-2 s-1 to mm day-1.
   
    Args:
      da (xarray.DataArray): Precipitation data
    
    """
    
    da.data = da.data * 86400
    da.attrs["units"] = "mm/day"
   
    assert da.data.min() >= 0.0, "There is at least one negative precipitation value"
    assert da.data.max() < 2000, "There is a precipitation value/s > 2000 mm/day"
    
    return da
```

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge

## Verbose reporting

Add two new command line options to `plot_precipitation_climatology.py`.

The first should change the logging level so reporting from the program is more verbose.

```python
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    default=False,
    help="Change the minimum logging reporting level from WARNING (default) to INFO",
)
```

The second should allow the user to specify the name of the log file.
(If they don't specify a name then the logging information is printed to the screen.)

```python
parser.add_argument(
    "--logfile",
    type=str,
    default=None,
    help="Name of log file (by default logging information is printed to the screen)",
)
```

:::::::::::::::  solution

The basic configuration command at the top of the `main` function
(`logging.basicConfig(level=logging.DEBUG, filename="log.txt")`)
needs to be replaced with the following:

```python
log_lev = logging.INFO if inargs.verbose else logging.WARNING
logging.basicConfig(level=log_lev, filename=inargs.logfile) 
```

:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge

## Error handling for land/ocean masks

In the previous lesson we added an `apply_mask` function to our script.
Update the following if statement in that function
so that it raises a `ValueError` if the realm is not `ocean` or `land`.

```python
if realm == "land":
    masked_da = da.where(ds["sftlf"].data < 50)
else:
    masked_da = da.where(ds["sftlf"].data > 50)
```

:::::::::::::::  solution
 
```python
if realm.lower() == 'land':
    masked_da = da.where(ds["sftlf"].data < 50)
elif realm.lower() == 'ocean':
    masked_da = da.where(ds["sftlf"].data > 50)
else:
    raise ValueError("""Mask realm is not 'ocean' or 'land'""")
```

:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::  challenge

## plot\_precipitation\_climatology.py

At the conclusion of this lesson your `plot_precipitation_climatology.py` script
should look something like the following:

:::::::::::::::  solution

```python
import logging
import argparse

import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import cmocean


def convert_pr_units(da):
    """Convert kg m-2 s-1 to mm day-1.
    
    Args:
      da (xarray.DataArray): Precipitation data
   
    """

    da.data = da.data * 86400
    da.attrs["units"] = "mm/day"
   
    assert da.data.min() >= 0.0, "There is at least one negative precipitation value"
    assert da.data.max() < 2000, "There is a precipitation value/s > 2000 mm/day"

    return da


def apply_mask(da, sftlf_file, realm):
    """Mask ocean or land using a sftlf (land surface fraction) file.
   
    Args:
      da (xarray.DataArray): Data to mask
      sftlf_file (str): Land surface fraction file
      realm (str): Realm to mask
   
    """
  
    ds = xr.open_dataset(sftlf_file)
    if realm.lower() == "land":
        masked_da = da.where(ds["sftlf"].data < 50)
    elif realm.lower() == 'ocean':
        masked_da = da.where(ds["sftlf"].data > 50)   
    else:
        raise ValueError("""Mask realm is not 'ocean' or 'land'""")    

    return masked_da


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
        extend='max',
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

    log_lev = logging.DEBUG if inargs.verbose else logging.WARNING
    logging.basicConfig(level=log_lev, filename=inargs.logfile) 

    ds = xr.open_dataset(inargs.pr_file)
    
    clim = ds['pr'].groupby("time.season").mean("time", keep_attrs=True)

    try:
        input_units = clim.attrs["units"]
    except KeyError:
        raise KeyError(f"Precipitation variable in {inargs.pr_file} does not have a units attribute")

    if input_units == "kg m-2 s-1":
        clim = convert_pr_units(clim)
        logging.info("Units converted from kg m-2 s-1 to mm/day")
    elif input_units == "mm/day":
        pass
    else:
        raise ValueError("""Input units are not 'kg m-2 s-1' or 'mm/day'""")

    if inargs.mask:
        sftlf_file, realm = inargs.mask
        clim = apply_mask(clim, sftlf_file, realm)

    create_plot(
        clim,
        ds.attrs["source_id"],
        inargs.season,
        gridlines=inargs.gridlines,
        levels=inargs.cbar_levels
    )
    plt.savefig(
        inargs.output_file,
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
    )


if __name__ == '__main__':
    description='Plot the precipitation climatology for a given season.'
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
    parser.add_argument(
        "--mask",
        type=str,
        nargs=2,
        metavar=("SFTLF_FILE", "REALM"),
        default=None,
        help="""Provide sftlf file and realm to mask ('land' or 'ocean')""",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Change the minimum logging reporting level from WARNING (default) to DEBUG",
    )
    parser.add_argument(
        "--logfile",
        type=str,
        default=None,
        help="Name of log file (by default logging information is printed to the screen)",
    )

    args = parser.parse_args()
    main(args)

```

:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::: keypoints

- Program defensively, i.e., assume that errors are going to arise, and write code to detect them when they do.
- You can raise exceptions in your own code.
- Put try-except blocks in programs to catch and handle exceptions.
- Put assertions in programs to check their state as they run.
- Use a logging framework instead of `print` statements to report program activity.
- The are more advanced lessons you can read to learn about code testing.

::::::::::::::::::::::::::::::::::::::::::::::::::


