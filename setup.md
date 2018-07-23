---
layout: page
title: Setup
root: .
---

## Software

If your instructor hasn't sent you instructions on how to install the required software,
follow the default Software Carpentry instructions on their
[workshop website template](https://swcarpentry.github.io/workshop-template/).
You need to install the bash shell, git, text editor and Python.

To check that everything installed correctly,
complete the [Software Check](https://github.com/data-lessons/python-aos-lesson/blob/gh-pages/participant_software_check.md).


## Data

In preparation for this lesson,
you will need to download four netCDF files and place them in the specified folder:

1. Make a new folder in your Desktop called `data-carpentry`.
2. Download [script_template.py][template_script] and move it into that folder.
3. Make a new folder in your `data_carpentry` folder called `data`.
   Download the following files and place them in that folder:
   - [pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc][pr_access_file]
   - [pr_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_200101-200512.nc][pr_csiro_file]
   - [sftlf_fx_ACCESS1-3_historical_r0i0p0.nc][sftlf_access_file]
   - [sftlf_fx_CSIRO-Mk3-6-0_historical_r0i0p0.nc][sftlf_csiro_file]
4. To get started, go into the `data-carpentry` folder from the Unix shell with:

~~~
$ cd
$ cd Desktop/data-carpentry
~~~
{: .language-bash}

## Environment

The lesson on [software installation using conda](https://data-lessons.github.io/python-aos-lesson/01-conda/index.html)
explains how to install the required Python libraries
([iris](http://scitools.org.uk/iris/), [jupyter](https://jupyter.org/) and [cmocean](http://matplotlib.org/cmocean/))
using either the command line, Anaconda Prompt (on Windows) or Anaconda Navigator.



[pr_access_file]: {{ page.root }}/data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc
[pr_csiro_file]: {{ page.root }}/data/pr_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_200101-200512.nc
[sftlf_access_file]: {{ page.root }}/data/sftlf_fx_ACCESS1-3_historical_r0i0p0.nc
[sftlf_csiro_file]: {{ page.root }}/data/sftlf_fx_CSIRO-Mk3-6-0_historical_r0i0p0.nc
[template_script]: {{ page.root }}/code/script_template.py
