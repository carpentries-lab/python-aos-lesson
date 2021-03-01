---
layout: lesson
---

Python is rapidly emerging as the programming language of choice for data analysis
in the atmosphere and ocean sciences.
By consulting online tutorials and help pages,
most researchers in this community are able to pick up the basic syntax and programming constructs
(e.g. loops, lists and conditionals).
This self-taught knowledge is sufficient to get work done,
but it often involves spending hours to do things that should take minutes,
reinventing a lot of wheels,
and a nagging uncertainty at the end of it all
regarding the reliability and reproducibility of the results.
To help address these issues,
these Data Carpentry lessons cover a suite of programming and data management best practices
that aren’t so easy to glean from a quick Google search. 

The skills covered in the lessons are taught in the context of a typical data analysis task:
creating a command line program that plots the precipitation climatology for any given month,
so that two different CMIP6 models (ACCESS-CM2 and ACCESS-ESM1-5) can be compared visually.


> ## raster vs vector data
>
> These lessons work with raster or “gridded” data that are stored as a uniform grid of values using the netCDF file format.
> This is the most common data format and file type in the atmosphere and ocean sciences; 
> essentially all output from weather, climate and ocean models is gridded data stored as a series of netCDF files.
> 
> The other data type that atmosphere and ocean scientists tend to work with is geospatial vector data.
> In contrast to gridded raster data,
> these vector data are composed of discrete geometric locations (i.e. x, y values)
> that define the shape of a spatial point, line or polygon.
> They are not stored using the netCDF file format and are not covered in these lessons.
> [Data Carpentry](http://www.datacarpentry.org/lessons/) have separate lessons on working with geospatial vector data.
>
{: .callout}

> ## Prerequisites
>
> Participants must have some familiarity with Python and the Unix shell.
> They don't need to be highly proficient,
> but a basic understanding of Python syntax,
> beginner-level programming constructs (e.g. loops and conditionals)
> and filesystem navigation using the shell
> (e.g. the `ls` and `cd` commands) is required. 
>
{: .prereq}

> ## Citation
>
> To cite these lessons, please refer to the following paper:
>
> Irving D (2019). [Python for atmosphere and ocean scientists](https://jose.theoj.org/papers/10.21105/jose.00037).
> *Journal of Open Source Education*. 2(11), 37. doi:10.21105/jose.00037
> 
{: .prereq}
