# Software check

The workshop website has instructions on how to install the required software
(Bash Shell, Git and Anaconda) on your laptop:  
https://damienirving.github.io/2018-08-15-whoi/#setup

To check that everything is installed correctly, please follow the instructions below.

### 1. Bash Shell

*Linux*: Open the Terminal program via the applications menu.  The default shell is usually Bash.  If you aren't sure what yours is, type `echo $SHELL`.  If the shell listed is not bash, type `bash` and press Enter to access Bash.

*Mac*: Open the Applications Folder, and in Utilities select Terminal.

*Windows*: Open a terminal by running the Anaconda Prompt program from the Windows start menu. Type `conda install posix` (this only needs to be done once). Type `bash` to run the Bash Shell.

### 2. Git

At the Bash Shell, type `git --version`. You should see the version of your Git program listed. 

### 3. Anaconda

1. At the Bash Shell, type `python --version`. You should see the version of your Python program listed, with a reference to Anaconda: e.g. 
```
$ python --version
Python 3.6.5 :: Anaconda, Inc.
```
In other words, the default Python program on your laptop needs to the the Anaconda installation of Python.

2. In the Bash Shell, type `conda --version`. You should see the version of your conda program listed.


# Pre-workshop downloads

At the beginning of a typical workshop,
participants download a number of data files and Python libraries.

This can be problematic at venues with slow wifi,
so your workshop organiser may ask you to follow the instructions below
to download these items in advance
(i.e. preferrably from a fast, wired internet connection).

### 1. Data download

Download the workshop data files by following the "Data" instructions at the following page:  
https://data-lessons.github.io/python-aos-lesson/setup.html

### 2. Python libraries

Install the `jupyter`, `iris` and `cmocean` libraries in a new conda environment called `pyaos-lesson`:

```
$ conda config --add channels conda-forge
$ conda create -n pyaos-lesson jupyter iris cmocean
```

Enter "y" to proceed when asked.

Depending on the speed of your internet connection,
the download of these libraries can take anywhere between 1 and 20 minutes.

During the workshop you will learn about what conda environments are and how to use them.
