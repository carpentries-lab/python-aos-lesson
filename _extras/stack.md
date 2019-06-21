---
layout: page
title: PyAOS stack
---

It would be an understatement to say that Python has exploded onto the data science scene in recent years.
PyCon and SciPy conferences are held somewhere in the world every few months now,
at which loads of new and/or improved data science libraries are showcased to the community 
(check out [pyvideo.org](pyvideo.org) for conference recordings).
The ongoing rapid development of new libraries means that data scientists are (hopefully)
continually able to do more and more cool things with less and less time and effort,
but at the same time it can be difficult to figure out how they all relate to one another.
To assist in making sense of this constantly changing landscape,
this page summarises the current state of the weather and climate Python software “stack”
(i.e. the collection of libraries used for data analysis and visualisation).
The focus is on libraries that are widely used and that have good (and likely long-term) support.

![PyAOS stack](../fig/01-pyaos-stack.png)

## Core

The dashed box in the diagram represents the core of the stack, so let’s start this tour there.
The default library for dealing with numerical arrays in Python is [NumPy](http://www.numpy.org/).
It has a bunch of built in functions for reading and writing common data formats like .csv,
but if your data is stored in netCDF format then the default library for getting data
into/out of those files is [netCDF4](http://unidata.github.io/netcdf4-python/netCDF4/index.html).

Once you’ve read your data in, you’re probably going to want to do some statistical analysis.
The NumPy library has some built in functions for calculating very simple statistics
(e.g. maximum, mean, standard deviation),
but for more complex analysis
(e.g. interpolation, integration, linear algebra)
the [SciPy](https://www.scipy.org/scipylib/index.html) library is the default.

If you’re dealing with a particularly large dataset,
you may get memory errors (and/or slow performance)
when trying to read and process your data.
[Dask[(https://dask.org/) works with the existing Python ecosystem (i.e. NumPy, SciPy etc)
to scale your analysis to multi-core machines and/or distributed clusters
(i.e. parallel processing).

The NumPy library doesn’t come with any plotting capability,
so if you want to visualise your NumPy data arrays then the default library is [matplotlib](https://matplotlib.org/).
As you can see at the [matplotlib gallery](https://matplotlib.org/gallery.html),
this library is great for any simple (e.g. bar charts, contour plots, line graphs),
static (e.g. .png, .eps, .pdf) plots.
The [cartopy](https://scitools.org.uk/cartopy/docs/latest/) library
provides additional functionality for common map projections,
while [Bokeh](http://bokeh.pydata.org/) allows for the creation of interactive plots
where you can zoom and scroll.

While pretty much all data analysis and visualisation tasks
could be achieved with a combination of these core libraries,
their highly flexible, all-purpose nature means relatively common/simple tasks
can often require quite a bit of work (i.e. many lines of code).
To make things more efficient for data scientists,
the scientific Python community has therefore built a number of libraries on top of the core stack.
These additional libraries aren’t as flexible
– they can’t do *everything* like the core stack can –
but they can do common tasks with far less effort.

## Generic additions

Let’s first consider the generic additional libraries.
That is, the ones that can be used in essentially all fields of data science.
The most popular of these libraries is undoubtedly [pandas](http://pandas.pydata.org/),
which has been a real game-changer for the Python data science community.
The key advance offered by pandas is the concept of labelled arrays.
Rather than referring to the individual elements of a data array using a numeric index
(as is required with NumPy),
the actual row and column headings can be used.
That means Fred’s information for the year 2005
could be obtained from a medical dataset by asking for `data(name=’Fred’, year=2005)`,
rather than having to remember the numeric index corresponding to that person and year.
This labelled array feature,
combined with a bunch of other features that simplify common statistical and plotting tasks
traditionally performed with SciPy and matplotlib,
greatly simplifies the code development process (read: less lines of code).

One of the limitations of pandas
is that it’s only able to handle one- or two-dimensional (i.e. tabular) data arrays.
The [xarray](http://xarray.pydata.org/) library was therefore created
to extend the labelled array concept to x-dimensional arrays.
Not all of the pandas functionality is available
(which is a trade-off associated with being able to handle multi-dimensional arrays),
but the ability to refer to array elements by their actual latitude (e.g. 20 South),
longitude (e.g. 50 East), height (e.g. 500 hPa) and time (e.g. 2015-04-27), for example,
makes the xarray data array far easier to deal with than the NumPy array.
(As an added bonus, xarray also builds on netCDF4 to make netCDF input/output easier.)

## Discipline-specific additions

While the xarray library is a good option for those working in the atmosphere and ocean sciences
(especially those dealing with large multi-dimensional arrays from model simulations),
the [SciTools](https://scitools.org.uk/) project (led by the MetOffice)
has taken a different approach to building on top of the core stack.
Rather than striving to make their software generic
(xarray is designed to handle any multi-dimensional data),
they explicitly assume that users of their [Iris](https://scitools.org.uk/iris/docs/latest/)
library are dealing with weather/ocean/climate data.
Doing this allows them to make common weather/climate tasks super quick and easy,
and it also means they have added functionality specific to atmosphere and ocean science.
(The SciTools project is also behind cartopy
and a number of other useful libraries for analysing earth science data.)

In addition to Iris, you may also come across [CDAT](https://cdat.llnl.gov),
which is maintained by the team at Lawrence Livermore National Laboratory.
It was the precursor to xarray and Iris in the sense that it was the first package
for atmosphere and ocean scientists built on top of the core Python stack.
For a number of years the funding and direction of that project shifted towards
developing a graphical interface ([VCDAT](https://vcdat.llnl.gov))
for managing large workflows and visualising data
(i.e. as opposed to further developing the capabilities of the underlying Python libraries),
but it seems that CDAT is now once again under [active development](https://github.com/CDAT/cdat/wiki).
The VCDAT application also now runs as a JupyterLab extension, which is an exciting development.

> ## How to choose
>
> In terms of choosing between xarray and Iris,
> some people like the slightly more atmosphere/ocean-centric experience offered by Iris,
> while others don’t like the restrictions that places on their work
> and prefer the generic xarray experience
> (e.g. to use Iris your netCDF data files have to be CF compliant or close to it).
> Either way, they are both a vast improvement on the netCDF/NumPy/matplotlib experience.
{: .callout}

## Simplifying data exploration

While the plotting functionality associated with xarray and Iris
speeds up the process of visually exploring data (as compared to matplotlib),
there’s still a fair bit of messing around involved in tweaking the various aspects of a plot
(e.g. colour schemes, plot size, labels, map projections, etc).
This tweaking burden is an issue across all data science fields and programming languages,
so developers of the latest generation of visualisation tools
are moving towards something called *declarative visualisation*.
The basic concept is that the user simply has to describe the characteristics of their data,
and then the software figures out the optimal way to visualise it
(i.e. it makes all the tweaking decisions for you).

The two major Python libraries in the declarative visualisation space are
[HoloViews](http://holoviews.org/) and [Altair](https://altair-viz.github.io/).
The former (which has been around much longer) uses matplotlib or Bokeh under the hood,
which means it allows for the generation of static or interactive plots.
Since HoloViews doesn’t have support for geographic plots,
[GeoViews](http://geoviews.org/) has been created on top of it
(which incorporates cartopy and can handle Iris or xarray data arrays).

## Sub-discipline-specific libraries

So far we’ve considered libraries that do general,
broad-scale tasks like data input/output, common statistics, visualisation, etc.
Given their large user base,
these libraries are usually written and supported by large companies
(e.g. Anaconda supports Bokeh and HoloViews/Geoviews),
large institutions (e.g. the MetOffice supports Iris, cartopy and GeoViews)
or the wider PyData community (e.g. pandas, xarray).
Within each sub-discipline of atmosphere and ocean science,
individuals and research groups take these libraries
and apply them to their very specific data analysis tasks.
Increasingly, these individuals and groups
are formally packaging and releasing their code for use within their community.
For instance, Andrew Dawson (an atmospheric scientist at Oxford)
does a lot of EOF analysis and manipulation of wind data,
so he has released his [eofs](https://ajdawson.github.io/eofs/latest/)
and [windspharm](https://ajdawson.github.io/windspharm/latest/) libraries
(which are able to handle data arrays from NumPy, Iris or xarray).
Similarly, a group at the Atmospheric Radiation Measurement (ARM) Climate Research Facility
have released their Python ARM Radar Toolkit ([Py-ART](http://arm-doe.github.io/pyart/))
for analysing weather radar data,
and a [similar story](https://www.unidata.ucar.edu/blogs/news/entry/metpy_an_open_source_python)
is true for [MetPy](https://unidata.github.io/MetPy/latest/index.html).

> ## Coming soon
>
> In terms of new libraries that might be available soon,
> the [Pangeo](https://pangeo.io/) project is actively supporting and encouraging
> the development of more domain-specific geoscience packages. 
> It was also recently [announced](https://www.ncl.ucar.edu/Document/Pivot_to_Python/)
> that NCAR will adopt Python as their scripting language of choice
> for future development of analysis and visualisation tools,
> so expect to see many of your favourite [NCL](https://www.ncl.ucar.edu/) functions
> re-implemented as new Python libraries over the coming months/years.
{: .callout}

It would be impossible to list all the sub-discipline-specific libraries on this page,
but the [PyAOS community](http://pyaos.johnny-lin.com/) is an excellent resource
if you’re trying to find out what’s available in your area of research.

## Navigating the stack

All of the additional libraries discussed on this page
essentially exist to hide the complexity of the core libraries
(in software engineering this is known as abstraction).
Iris, for instance, was built to hide some of the complexity of netCDF4, NumPy and matplotlib.
GeoViews was built to hide some of the complexity of xarray/Iris, cartopy and Bokeh.
So if you want to start exploring your data, start at the top right of the stack
and move your way down and left as required.
If GeoViews doesn’t have quite the right functions for a particular plot that you want to create,
drop down a level and use some Iris and cartopy functions.
If Iris doesn’t have any functions for a statistical procedure that you want to apply,
go back down another level and use SciPy.
By starting at the top right and working your way back,
you’ll ensure that you never re-invent the wheel.
Nothing would be more heartbreaking than spending hours writing your own function (using netCDF4)
for extracting the metadata contained within a netCDF file, for instance,
only to find that Iris automatically keeps this information upon reading a file.
In this way, a solid working knowledge of the scientific Python stack
can save you a lot of time and effort.


