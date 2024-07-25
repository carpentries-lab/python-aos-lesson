---
title: Instructor Notes
---

## Teaching notes

These materials are designed with the core [Carpentries teaching practices](https://carpentries.org/workshops/) in mind.
All of the episodes involve the instructor live coding
(in a Jupyter notebook, bash shell or text editor, depending on the lesson),
using these online notes as a guide
(it can be a good idea to print a copy of the notes to have next to you while live coding).
For most of the lessons, participants simply watch the live coding
and then get an opportunity to try the new concepts that are introduced by completing the challenges.
The only exception to this format are lessons on version control and GitHub,
where the participants are required to follow along with the instructor,
typing and executing every command as the instructor enters them on the screen.
This is done to reinforce the repetitive "add, commit, push" workflow in git.

## Downloads

At the beginning of the workshop,
participants are required to download a number of data files
(instructions at the [setup page](https://carpentries-lab.github.io/python-aos-lesson/setup.html)).
In the [first lesson](https://carpentries-lab.github.io/python-aos-lesson/01-conda/index.html),
they are then required to install some python libraries (`jupyter`, `xarray`, `cmocean`, etc).
Both these tasks can be problematic at venues with slow wifi,
so it is often a good idea to ask participants to download the data
and install the libraries prior to the workshop.

The large data lesson involves the analysis of a 45GB dataset.
Instructors can download the relevant data files from the
Earth System Grid Federation (ESGF) following the
[CMIP6 Guidance for Data Users](https://pcmdi.llnl.gov/CMIP6/Guide/dataUsers.html#3-accessing-model-output).
(Workshop participants do not need to download this data.)
Use the following search terms to locate the data at your nearest ESGF node:

- Source ID: CNRM-CM6-1-HR
- Experiment ID: historical
- Variant Label: r1i1p1f2
- Grid Label: gr
- Table ID: day
- Variable: pr

## Software and code

The [setup page](https://carpentries-lab.github.io/python-aos-lesson/setup.html)
gives details of the software installation instructions that can provided to participants.

You can also send the
[helper lesson check](https://github.com/carpentries-lab/python-aos-lesson/blob/gh-pages/helper_lesson_check.md)
to helpers prior to the workshop,
so that they can test that all the software and code is working correctly.


