---
title: "Data provenance"
teaching: 25
exercises: 15
questions:
- "How can keep track of my data processing steps?"
objectives:
- "Automate the process of recording the history of what was entered at the command line to produce a given data file or image."
- "Write (and import) modules that contain commonly used code to avoid duplication."
keypoints:
- "It is possible (in only a few lines of code) to record the provenance of a given data file or image."
- "Write (and import) modules to avoid code duplication."
---

We've now successfully created a command line program - `plot_precipitation_climatology.py` -
that calculates and plots the precipitation climatology for a given month.
The last step is to capture the provenance of that plot.
In other words, we need a record of all the data processing steps
that were taken from the intial download of the data files to the end result
(i.e. the .png image).

The simplest way to do this is to follow the lead of the
[NCO](http://nco.sourceforge.net/)
and [CDO](https://code.mpimet.mpg.de/projects/cdo) command line tools,
which insert a record of what was executed at the command line
into the history attribute of the output netCDF file.

~~~
import iris
iris.FUTURE.netcdf_promote = True

access_pr_file = 'data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc'
cube = iris.load_cube(access_pr_file, 'precipitation_flux')
previous_history = cube.attributes['history']

print(previous_history)
~~~
{: .language-python}

~~~
Fri Dec  8 10:05:47 2017: ncatted -O -a history,pr,d,, pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc
Fri Dec 01 07:59:16 2017: cdo seldate,2001-01-01,2005-12-31 /g/data/ua6/DRSv2/CMIP5/ACCESS1-3/historical/mon/atmos/r1i1p1/pr/latest/pr_Amon_ACCESS1-3_historical_r1i1p1_185001-200512.nc pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc
CMIP5 compliant file produced from raw ACCESS model output using the ACCESS Post-Processor and CMOR2. 2012-02-08T06:45:54Z CMOR rewrote data to comply with CF standards and CMIP5 requirements. Fri Apr 13 09:55:30 2012: forcing attribute modified to correct value Fri Apr 13 12:13:10 2012: updated version number to v20120413. Fri Apr 13 12:29:34 2012: corrected model_id from ACCESS1-3 to ACCESS1.3
~~~
{: .output}

If we want to create our own entry for the history attribute, we'll need to be able to create a:

* Time stamp  
* Record of what was entered at the command line in order to execute `plot_precipitation_climatology.py`  
* Method of indicating which verion of the script was run (i.e. because the script is in our git repository)  

## Time stamp

A library called `datetime` can be used to find out the time and date right now:

~~~
import datetime
 
time_stamp = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
print(time_stamp)
~~~
{: .language-python}

~~~
Fri Dec 08 14:05:17 2017
~~~
{: .output}

The `strftime` function can be used to customise the appearance of a datetime object;
in this case we've made it look just like the other time stamps in our data file.

## Command line record

The `sys.argv` function, which the `argparse` library is built on top of,
contains all the arguments entered by the user at the command line:

~~~
import sys
print(sys.argv)
~~~
{: .language-python}

~~~
['/Applications/anaconda/envs/pyaos-lesson/lib/python3.6/site-packages/ipykernel_launcher.py', '-f', '/Users/irv033/Library/Jupyter/runtime/kernel-7183ce41-9fd9-4d30-9e46-a0d16bc9bd5e.json']
~~~
{: .output}

In launching this IPython notebook,
you can see that a command line program called `ipykernel_launcher.py` was run.
To join all these list elements up,
we can use the join function that belongs to Python strings:

~~~
args = " ".join(sys.argv)
print(args)
~~~
{: .language-python}

~~~
/Applications/anaconda/envs/pyaos-lesson/lib/python3.6/site-packages/ipykernel_launcher.py -f /Users/irv033/Library/Jupyter/runtime/kernel-7183ce41-9fd9-4d30-9e46-a0d16bc9bd5e.json
~~~
{: .output}

While this list of arguments is very useful,
it doesn't tell us which Python installation was used to execute those arguments.
The `sys` library can help us out here too:

~~~
exe = sys.executable
print(exe)
~~~
{: .language-python}

~~~
/Applications/anaconda/envs/pyaos-lesson/bin/python
~~~
{: .output}

## Git hash

In the lesson on version control using git
we learned that each commit is associated with a unique 40-character identifier
known as a hash.
We can use the git Python library to get the hash associated with the script.

~~~
import git
import os
     
repo_dir = '/Users/dirving/Desktop/data-carpentry'        
git_hash = git.Repo(repo_dir).heads[0].commit
print(git_hash)
~~~
{: .language-python}

~~~
588f96dcab5c78d10b4c994eb3ca67955c882697
~~~
{: .output}

## Putting it all together

We can now put all this together into a function that generates our history record.

~~~
def get_history_record(repo_dir):
    """Create a new history record."""

    time_stamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    exe = sys.executable
    args = " ".join(sys.argv)
    git_hash = git.Repo(repo_dir).heads[0].commit

    entry = """%s: %s %s (Git hash: %s)""" %(time_stamp, exe, args, str(git_hash)[0:7])
    
    return entry
~~~
{: .language-python}

~~~
new_history = get_history_record('/Users/dirving/Desktop/data-carpentry')
print(new_history)
~~~
{: .language-python}

~~~
2017-12-08T14:05:34: /Applications/anaconda/envs/pyaos-lesson/bin/python /Applications/anaconda/envs/pyaos-lesson/lib/python3.6/site-packages/ipykernel_launcher.py -f /Users/dirving/Library/Jupyter/runtime/kernel-7183ce41-9fd9-4d30-9e46-a0d16bc9bd5e.json (Git hash: 588f96d)
~~~
{: .output}

This can be combined with the previous history to compile a record that goes all the way back to when we obtained the original data file.

~~~
complete_history = '%s \n %s' %(new_history, previous_history)
print(complete_history)
~~~
{: .language-python}

~~~
2017-12-08T14:05:34: /Applications/anaconda/envs/pyaos-lesson/bin/python /Applications/anaconda/envs/pyaos-lesson/lib/python3.6/site-packages/ipykernel_launcher.py -f /Users/dirving/Library/Jupyter/runtime/kernel-7183ce41-9fd9-4d30-9e46-a0d16bc9bd5e.json (Git hash: 588f96d) 
 Fri Dec  8 10:05:47 2017: ncatted -O -a history,pr,d,, pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc
Fri Dec 01 07:59:16 2017: cdo seldate,2001-01-01,2005-12-31 /g/data/ua6/DRSv2/CMIP5/ACCESS1-3/historical/mon/atmos/r1i1p1/pr/latest/pr_Amon_ACCESS1-3_historical_r1i1p1_185001-200512.nc pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc
CMIP5 compliant file produced from raw ACCESS model output using the ACCESS Post-Processor and CMOR2. 2012-02-08T06:45:54Z CMOR rewrote data to comply with CF standards and CMIP5 requirements. Fri Apr 13 09:55:30 2012: forcing attribute modified to correct value Fri Apr 13 12:13:10 2012: updated version number to v20120413. Fri Apr 13 12:29:34 2012: corrected model_id from ACCESS1-3 to ACCESS1.3
~~~
{: .output}

(Noting that in real example of this process in action,
the new history would refer to what was entered at the command line to run
`plot_precipitation_climatology.py`,
as opposed to running `ipykernel_launcher.py` to run a notebook.)

## Writing your own modules

We could place this new `get_history_record()` function directly into the
`plot_precipitation_climatology.py` script, but there's a good chance
we'll want to use it in many scripts that we write into the future.
In the functions lesson
we discussed all the reasons why code duplication is a bad thing,
and it's the same principle here.
The solution is to place the `get_history_record()` function
in a separate script full of functions (which is called a module)
that we use regularly across many scripts.

(A slight modification has been added to `get_history_record()`
so that the `repo_dir` isn't hard wired into the code.
Instead, the script defines `repo_dir` as the current working directory,
which is assumed to be the top of the directory tree in the git repository,
as that's the input information required by `git.Repo`.)

> ## Accessing the command line from a Jupyter notebook
>
> When using IPython,
> any input line beginning with a `!` character is passed verbatim
> (minus the `!`, of course) to the underlying operating system.
> For example, typing `!ls` will run `ls` in the current directory.
>
{: .callout}

~~~
!cat provenance.py
~~~
{: .language-python}

~~~
"""
A collection of commonly used functions for data provenance

"""

import sys
import datetime
import git
import os


def get_history_record():
    """Create a new history record."""

    time_stamp = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    exe = sys.executable
    args = " ".join(sys.argv)
    
    repo_dir = os.getcwd()
    try:
        git_hash = git.Repo(repo_dir).heads[0].commit
    except git.exc.InvalidGitRepositoryError:
        print('To record the git hash, must run script from top of directory tree in git repo')
        git_hash = 'unknown'
        
    entry = """%s: %s %s (Git hash: %s)""" %(time_stamp, exe, args, str(git_hash)[0:7])
    
    return entry
~~~
{: .language-python}

We can then import that module and use it in all of our scripts.

~~~
import provenance
~~~
{: .language-python}

The first line of a module file is similar to the first line of a function
- if you enter a string, it will be picked up by the help generator.

~~~
help(provenance)
~~~
{: .language-python}

~~~
Help on module provenance:

NAME
    provenance - A collection of commonly used functions for data provenance

FUNCTIONS
    get_history_record(repo_dir)
        Create a new history record.

FILE
    /Users/dirving/Desktop/data-carpentry/provenance.py
~~~
{: .output}

> ## Data provenance
>
> Take (i.e. cut and paste to create a new file) the `provenance.py` script shown above
> and save it in your `data-carpentry` directory.
> 
> Now import the new provenance module into your `plot_precipitation_climatology.py` 
> script and use it to record the complete history of the output figure.
>
> Things to consider:
>
> * For command line programs that output a netCDF file,
>   the history record is typically added to the global history attribute.
>   In this case the output is a .png file, so it will be necessary to have 
>   `plot_precipitation_climatology.py` output a .txt file
>   that contains the history information
>   (it's usually easiest for this metadata file
>   to have exactly the same name as the figure file,
>   just with a .txt instead of .png file extension)
> * Do you need to record the history of the land surface fraction file,
>   or just the precipitation file?
>
> Don't forget to commit your changes to git and push to GitHub.
>
> > ## Solution
> > 
> > Make the following additions to `plot_precipitation_climatology.py`
> > (code omitted from this abbreviated version of the script is denoted `...`):
> > 
> > ~~~
> > ...
> >
> > import provenance
> > 
> > ...
> >
> > def write_metadata(outfile, previous_history):
> >     """Write the history record to file."""
> >    
> >     new_history = provenance.get_history_record()
> >     complete_history = '%s \n %s' %(new_history, previous_history)
> >    
> >     fname, extension = outfile.split('.')
> >     metadata_file = open(fname+'.txt', 'w')
> >     metadata_file.write(complete_history) 
> >     metadata_file.close()
> > 
> > ...
> >
> > def main(inargs):
> >     """Run the program."""
> >
> >     cube = read_data(inargs.infile, inargs.month)  
> > 
> >     ...
> >
> >     plt.savefig(inargs.outfile)
> >     write_metadata(inargs.outfile, cube.attributes['history']) 
> > 
> > ...
> > 
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}