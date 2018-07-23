## Software check

### 1. Open the Bash Shell

*Linux*: Open the Terminal program via the applications menu.  The default shell is usually Bash.  If you aren't sure what yours is, type `echo $SHELL`.  If the shell listed is not bash, type `bash` and press Enter to access Bash.

*Mac*: Open the Applications Folder, and in Utilities select Terminal.

*Windows*: Open a terminal by running the Anaconda Prompt program from the Windows start menu. Type `conda install posix` (this only needs to be done once). Type `bash` to run the Bash Shell.

### 2. Check that Git is installed

At the Bash Shell, type `git --version`. You should see the version of your Git program listed. 

### 3. Check that Anaconda is installed

1. At the Bash Shell, type `python --version`. You should see the version of your Python program listed, with a reference to Anaconda: e.g. 
```
$ python --version
Python 3.6.5 :: Anaconda, Inc.
```
In other words, the default Python program on your laptop needs to the the Anaconda installation of Python.

2. In the Bash Shell, type `conda --version`. You should see the version of your conda program listed.

3. In the Bash Shell, type `jupyter notebook` to run Jupyter Notebook. After a few seconds, text should appear in your terminal and Jupyter Notebook should pop up in a browser window. You can close the browser window and press `CTRL+C` in the terminal to exit the program.

