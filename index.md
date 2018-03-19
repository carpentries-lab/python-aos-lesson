---
layout: lesson
root: .
permalink: index.html  # Is the only page that don't follow the partner /:path/index.html
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
this one day Data Carpentry workshop covers a suite of programming and data management best practices
that aren’t so easy to glean from a quick Google search. 

> ## raster vs vector data
>
> These lessons work with raster or “gridded” data that are stored as a grid of values using the netCDF file format.
> This is the most common data format and file type in the atmosphere and ocean sciences 
> (e.g. essentially all output from weather, climate and ocean models is stored in this format),
> however there are a significant number of atmosphere and ocean scientists working with vector data.
> In contrast to raster data, these vector data are composed of discrete geometric locations (x, y values) known as vertices
> that define the “shape” of a spatial point, line or polygon.
> They are not stored using the netCDF file format.
> [Data Carpentry](http://www.datacarpentry.org/lessons/) have separate lessons on working with geospatial vector data.
>
{: .callout}

> ## Prerequisites
>
> Participants must already be using Python for their data analysis.
> They don't need to be highly proficient,
> but a strong familiarity with Python syntax and basic constructs
> such as loops, lists and conditionals (i.e. if statements) is required. 
>
> Participants should also read
> [this post](https://drclimate.wordpress.com/2016/10/04/the-weatherclimate-python-stack/)
> prior to the workshop,
> to familiarise themselves with the most commonly used Python libraries
> in the atmosphere and ocean sciences and how they relate to one another.
>
{: .prereq}
