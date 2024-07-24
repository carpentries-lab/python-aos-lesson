---
title: Setup
---

## Data

In preparation for these lessons,
you will need to download the following two Python scripts and four netCDF files
and place them in a new folder/directory:

1. Make a new folder in your Desktop called `data-carpentry`.
2. Download [script\_template.py][template\_script] and [plot\_precipitation\_climatology.py][precip\_script] and move them into that folder.
3. Make a new folder in your `data_carpentry` folder called `data`.
  Download the following files and place them in that folder:
  - [pr\_Amon\_ACCESS-CM2\_historical\_r1i1p1f1\_gn\_201001-201412.nc][pr\_access-cm\_file]
  - [pr\_Amon\_ACCESS-ESM1-5\_historical\_r1i1p1f1\_gn\_201001-201412.nc][pr\_access-esm\_file]
  - [sftlf\_fx\_ACCESS-CM2\_historical\_r1i1p1f1\_gn.nc][sftlf\_access-cm\_file]
  - [sftlf\_fx\_ACCESS-ESM1-5\_historical\_r1i1p1f1\_gn.nc][sftlf\_access-esm\_file]

## Software installation

In order to complete the lessons,
you will need access to the following:

- The bash shell (the Z-shell is also fine, which is default on new Macs)
- A text editor
- Git
- Anaconda (which is a Python distribution)

If you don't already have these installed,
please follow The Carpentries [software installation instructions](https://carpentries.github.io/workshop-template/#setup).
(You do not need to install R, which is also listed at that site.)

:::::::::::::::::::::::::::::::::::::::::  callout

## Troubeshooting

If you have any trouble with software installation,
The Carpentries maintain a list of common issues on their
[Configuration Problems and Solutions wiki page](https://github.com/carpentries/workshop-template/wiki/Configuration-Problems-and-Solutions).

::::::::::::::::::::::::::::::::::::::::::::::::::

Your workshop instructor may also ask that you install the python packages introduced in the
[first lesson](https://carpentries-lab.github.io/python-aos-lesson/01-conda/index.html)
ahead of time.
You can do this via the command line or by using the Anaconda Navigator:

:::::::::::::::  solution

## Installation of python packages: via the command line

(Windows users may need to open the Anaconda Prompt program
and run `conda init bash` to make conda available at the Bash Shell.)

**Step 1**

Add the conda-forge channel:

```bash
$ conda config --add channels conda-forge
```

**Option 1 for Step 2 (recommended if you're new to using Anaconda)**

Install the packages in the base conda environment:

```bash
$ conda install xarray dask netCDF4 cartopy cmocean cmdline_provenance
```

**Option 2 for Step 2**

Create a new environment called `pyaos-lesson` and install the packages there:

```bash
$ conda create -n pyaos-lesson jupyter xarray dask netCDF4 cartopy cmocean cmdline_provenance
```

You can activate this new environment as follows:

```bash
$ conda activate pyaos-lesson
```

(Or `source activate pyaos-lesson` if that doesn't work.)

Type `conda deactivate` to exit that environment.


:::::::::::::::::::::::::

:::::::::::::::  solution

## Installation of python packages: via the Anaconda Navigator

Once you've opened the Anaconda Navigator program
(which can be found at the start menu on Windows),
head to the "Environments" tab.

You can install the packages into the "base" environment
(recommended if you're new to Anaconda)
OR create a new environment called `pyaos-lesson`
by clicking the "create" button at the bottom of the environment
list before doing the following:

**Step 1**

Add the `conda-forge` channel.
![](fig/01-navigator-conda-forge.png){alt='Anaconda Navigator add conda-forge'}

**Step 2**

Install the `xarray`, `dask`, `netCDF4`, `cartopy`, `cmocean` and `cmdline_provenance`
packages one-by-one (click "apply" to install once selected).
If you've created a new environment,
you'll need to install `jupyter` too.
![](fig/01-navigator-xarray.png){alt='Anaconda Navigator install xarray'}


:::::::::::::::::::::::::

## Software check

To check that everything is installed correctly, follow the instructions below.

**Bash Shell**

- *Linux*: Open the Terminal program via the applications menu. The default shell is usually Bash. If you aren't sure what yours is, type `echo $SHELL`. If the shell listed is not bash, type `bash` and press Enter to access Bash.
- *Mac*: Open the Applications Folder, and in Utilities select Terminal.
- *Windows*: Open the Git Bash program via the Windows start menu.

**Git**

- At the Bash Shell, type `git --version`. You should see the version of your Git program listed.

**Anaconda**

- At the Bash Shell, type `python --version`. You should see the version of your Python program listed, with a reference to Anaconda (i.e. the default Python program on your laptop needs to be the Anaconda installation of Python).

[pr\_access-cm\_file]: {{"/data/pr\_Amon\_ACCESS-CM2\_historical\_r1i1p1f1\_gn\_201001-201412.nc" | relative\_url}}
[pr\_access-esm\_file]: {{"/data/pr\_Amon\_ACCESS-ESM1-5\_historical\_r1i1p1f1\_gn\_201001-201412.nc" | relative\_url}}
[sftlf\_access-cm\_file]: {{"/data/sftlf\_fx\_ACCESS-CM2\_historical\_r1i1p1f1\_gn.nc" | relative\_url }}
[sftlf\_access-esm\_file]: {{"/data/sftlf\_fx\_ACCESS-ESM1-5\_historical\_r1i1p1f1\_gn.nc" | relative\_url}}
[template\_script]: {{"/code/script\_template.py" | relative\_url}}
[precip\_script]: {{"code/plot\_precipitation\_climatology.py" | relative\_url}}


