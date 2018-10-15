---
layout: page
title: Setup
---

## Software

If your instructor hasn't sent you instructions on how to install the required software,
follow the [default Carpentries instructions](https://carpentries.github.io/workshop-template/#setup).
You need to install the bash shell, git, text editor and Python.

The `conda` command is not automatically available using Git Bash.
This means that Windows users cannot create and activate a conda environment from the bash shell,
which is an option in the [first lesson](https://carpentrieslab.github.io/python-aos-lesson/01-conda/index.html).

While this is not a big issue (the first lesson can be completed without creating a new environment),
Windows users who would like to be able create and activate conda environments from the bash shell
can do one of the following:

1. Update their Anaconda path so that `conda` is available using Git Bash
2. Access the bash shell from the Anaconda Prompt using the posix package


## Data

In preparation for this lesson,
you will need to download two Python scripts and four netCDF files and place them in a new folder/directory:

1. Make a new folder in your Desktop called `data-carpentry`.
2. Download [script_template.py][template_script] and [plot_precipitation_climatology.py][precip_script] and move them into that folder.
3. Make a new folder in your `data_carpentry` folder called `data`.
   Download the following files and place them in that folder:
   - [pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc][pr_access_file]
   - [pr_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_200101-200512.nc][pr_csiro_file]
   - [sftlf_fx_ACCESS1-3_historical_r0i0p0.nc][sftlf_access_file]
   - [sftlf_fx_CSIRO-Mk3-6-0_historical_r0i0p0.nc][sftlf_csiro_file]


[pr_access_file]: {{ "/data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc" | relative_url }}
[pr_csiro_file]: {{ "/data/pr_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_200101-200512.nc" | relative_url }}
[sftlf_access_file]: {{"/data/sftlf_fx_ACCESS1-3_historical_r0i0p0.nc" | relative_url }}
[sftlf_csiro_file]: {{ "/data/sftlf_fx_CSIRO-Mk3-6-0_historical_r0i0p0.nc" | relative_url }}
[template_script]: {{ "/code/script_template.py" | relative_url }}
[precip_script]: {{ "code/plot_precipitation_climatology.py" | relative_url }}
