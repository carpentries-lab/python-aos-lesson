## Helper lesson check

Once you've installed the required software for the workshop (following the instructions given to participants)...

1. Clone this repository:

```
$ git clone https://github.com/carpentries-lab/python-aos-lesson.git
$ cd python-aos-lesson
```

2. Install the `jupyter`, `xarray` and `cmocean` libraries in a new conda environment called `pyaos-lesson`:

```
$ conda config --add channels conda-forge
$ conda create -n pyaos-lesson jupyter xarray cmocean
```

3. Activate the new environment by typing `source activate pyaos-lesson`. If that doesn't work, try `conda activate pyaos-lesson`.

4. Install the `cmdline-provenance` library: 

```
(pyaos-lesson) $ pip install cmdline-provenance
```

5. Run the final version of the script that participants will develop throughout the workshop:

```
(pyaos-lesson) $ python code/plot_precipitation_climatology_final.py data/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc DJF test.png
```

It should produce an image file (`test.png`) as well as a log of command line entries (`test.txt`).
