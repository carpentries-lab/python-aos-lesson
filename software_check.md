## Software check

### 1. Open the Bash Shell

*Windows*: Open a terminal by running the program Git Bash from the Windows start menu.

*Mac*: Open the Applications Folder, and in Utilities select Terminal.

*Linux*: Open the Terminal program via the applications menu.  The default shell is usually Bash.  If you aren't sure what yours is, type `echo $SHELL`.  If the shell listed is not bash, type `bash` and press Enter to access Bash.

### 2. Check that Git is installed

In the terminal, type `git --version` to check that it is installed.  

### 3. Check that Anaconda is installed

1. In the terminal, type `python --version`. You should see the version of your Python program listed.

2. In the terminal, type `conda --version`. You should see the version of your conda program listed.

3. In the terminal, type `jupyter notebook` to run Jupyter Notebook. After a few seconds, text should appear in your terminal and Jupyter Notebook should pop up in a browser window. You can close the browser window and press `CTRL+C` in the terminal to exit the program.


*Windows*: If you receive an error message about python or conda not being found, try the following:

* Run the program Anaconda Prompt from the Windows start menu and enter the following to find the path of the Anaconda3 directory:
  ```
  where python
  ```
  The output should show a path similar to `C:\Users\Username\Anaconda3\python.exe`.

* Convert that path for use in the next step by doing the following:
   * Replace all instances of `\` with `/`
   * Replace `C:` with `/c`
   * Replace `python.exe` with `Scripts/activate`
        
   So, for example, if you got `C:\Users\Username\Anaconda3\python.exe` from the previous step, you will use `/c/Users/Username/Anaconda3/Scripts/activate` for the next step.

* Go back to the terminal and run the following command, replacing `[Anaconda path]` with the path you generated in the previous step. Please note that you can copy text into the terminal window by right clicking and then selecting "paste".
  ```
  echo  "source [Anaconda path]" >> ~/.profile && source ~/.profile
  ```
  then try typing `python --version` and `conda --version` again.

