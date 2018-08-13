## Helper software check

1. Install the software for the workshop (i.e. Bash Shell, Git, Anaconda) by following the [setup instructions](https://damienirving.github.io/2018-08-15-whoi/#setup) at the workshop website

2. Check that the software is installed correctly by following the [participant software check](https://github.com/data-lessons/python-aos-lesson/blob/gh-pages/participant_software_check.md)

3. Clone this repository:

```
$ git clone https://github.com/data-lessons/python-aos-lesson.git
$ cd python-aos-lesson
```

4. Install the `jupyter`, `iris` and `cmocean` libraries in a new conda environment called `pyaos-lesson`:

```
$ conda config --add channels conda-forge
$ conda create -n pyaos-lesson jupyter iris cmocean
```

5. Activate the new environment by typing `source activate pyaos-lesson`. If that doesn't work, try `conda activate pyaos-lesson`.

6. Install the `cmdline-provenance` library: 

```
(pyaos-lesson) $ pip install cmdline-provenance
```

7. Run the final version of the script that participants will develop throughout the workshop:

```
(pyaos-lesson) $ python code/plot_precipitation_climatology_final.py data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc Jan test.png
```

It should produce an image file (`test.png`) as well as a log of command line entries (`test.txt`).
