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