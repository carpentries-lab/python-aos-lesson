## Helper software check

1. Install and open the Bash Shell, following the setup instructions at the [workshop website](https://damienirving.github.io/2018-08-15-whoi/)

2. Clone this repository

```
$ git clone https://github.com/data-lessons/python-aos-lesson.git
$ cd python-aos-lesson
```

3. Install the `jupyter`, `iris` and `cmocean` libraries following the [software installation](https://data-lessons.github.io/python-aos-lesson/01-conda/index.html) lesson

4. Install the `cmdline-provenance` library 

```
$ pip install cmdline-provenance
```

5. Run the final version of the script that participants will develop throughout the workshop:

```
$ python code/plot_precipitation_climatology_final.py data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc Jan test.png
```

It should produce an image file (`test.png`) as well as a log of command line entries (`test.txt`).
