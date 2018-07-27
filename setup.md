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
you will need to download two Python scripts and four netCDF files and place them in a new folder/directory:

1. Make a new folder in your Desktop called `data-carpentry`.
2. Download [script_template.py][template_script] and [plot_precipitation_climatology.py][precip_script] and move them into that folder.
3. Make a new folder in your `data_carpentry` folder called `data`.
   Download the following files and place them in that folder:
   - [pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc][pr_access_file]
   - [pr_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_200101-200512.nc][pr_csiro_file]
   - [sftlf_fx_ACCESS1-3_historical_r0i0p0.nc][sftlf_access_file]
   - [sftlf_fx_CSIRO-Mk3-6-0_historical_r0i0p0.nc][sftlf_csiro_file]


[pr_access_file]: {{ page.root }}/data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc
[pr_csiro_file]: {{ page.root }}/data/pr_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_200101-200512.nc
[sftlf_access_file]: {{ page.root }}/data/sftlf_fx_ACCESS1-3_historical_r0i0p0.nc
[sftlf_csiro_file]: {{ page.root }}/data/sftlf_fx_CSIRO-Mk3-6-0_historical_r0i0p0.nc
[template_script]: {{ page.root }}/code/script_template.py
[precip_script]: {{ page.root }}/code/plot_precipitation_climatology.py