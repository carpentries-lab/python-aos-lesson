---
title: 'Python for Atmosphere and Ocean Scientists'
tags:
- python
- meteorology
- oceanography
authors:
- name: Damien B Irving
  orcid: 0000-0003-1258-5002
  affiliation: 1
affiliations:
- name: Commonwealth Scientific and Industrial Research Organisation (CSIRO)
  index: 1
date: 23 October 2018
bibliography: paper.bib
---

# Summary

Python is rapidly emerging as the programming language of choice for data analysis in the atmosphere and ocean sciences. By consulting online tutorials and help pages, most researchers in this community are able to pick up the basic syntax and programming constructs (e.g. loops, lists and conditionals). This self-taught knowledge is sufficient to get work done, but it often involves spending hours to do things that should take minutes, reinventing a lot of wheels, and a nagging uncertainty at the end of it all regarding the reliability and reproducibility of the results. To help address these issues, the [Python for Atmosphere and Ocean Scientists](https://carpentrieslab.github.io/python-aos-lesson/) educational materials cover a suite of programming and data management best practices that are not so easy to glean from a quick Google search.

The materials contain everything required to run a one-day workshop. This includes data files, software installation instructions and lesson plans (complete with exercises and solutions), which double as teaching notes for instructors and a reference for learners to refer back to. For those unable to attend a workshop, it is also possible work through the lessons independently. The skills covered in the lessons are presented in the context of a typical data analysis task: creating a command line program that plots the average rainfall for any given month, so that the output from two different global climate models can be compared visually. After giving an overview of the PyAOS stack (i.e. the ecosystem of libraries used in the atmosphere and ocean sciences) and the management of software environments using conda, the lessons introduce the basic Python commands required to create the plot. Those commands are then refactored to be more modular/reusable (using functions) before being transferred to a stand-alone script that can be executed from the command line. Changes to that script are then tracked using version control as further edits are made to implement common defensive programming strategies and to record the provenance of the input data files and output figures. Along the way, the basics of the Network Common Data Form (netCDF) file format and associated “climate and forecasting” metadata convention are introduced. The raster (or “gridded”) output from weather, climate and/or ocean models is almost universally archived using this format.

## Statement of need

The inspiration for the materials was the world-renowned Software Carpentry initiative [@Wilson2014]. In 2013, the author was involved in organising the first ever Software Carpentry workshops outside of Europe and North America, one of which was held alongside the annual conference of the Australian Meteorological and Oceanographic Society (AMOS) in Melbourne, Australia. He then trained up as a Software Carpentry instructor and taught workshops alongside the AMOS conference from 2014-2017, as well as other ad hoc workshops in various meteorology and oceanography departments. While these workshops were very popular and well received, there was clearly demand for a workshop designed specifically for atmosphere and ocean scientists. Instead of teaching generic skills in the hope that people would figure out how to apply them in their own context (i.e. in the context of netCDF files, the PyAOS stack, etc), such a workshop would teach programming [@Wilson2014a], data management and reproducible research [@Irving2016] skills in the atmosphere and ocean science context. This idea of discipline (or data-type) specific workshops was the driving force behind the establishment of the Data Carpentry initiative, so it was with their assistance that these materials were developed. The first pilot workshops were held in 2018 at the AMOS Conference in Sydney and at Woods Hole Oceanographic Institution in Massachusetts. The materials have since been formally endorsed and released for use by the wider Data Carpentry instructor community.

Carpentries workshops (i.e. Data Carpentry and Software Carpentry) are taught by volunteer instructors, trained in pedagogy [@Wilson2018], who focus on creating a motivating and engaging environment for learners. The one-day Python for Atmosphere and Ocean Scientists workshop is no different, and incorporates a number of teaching practices that make it effective and enjoyable. These include a code of conduct to ensure the workshop is welcoming, live coding by the instructor, peers teaching peers, continuous opportunity for feedback, collaborative note taking, a lesson design that avoids cognitive overload, regular challenges/quizzes and learners work in a familiar environment by using their own laptop [@Wilson2014]. Of course, the materials can also be adapted and used in other forums. The first few modules, for instance, are being used in a third year undergraduate subject at the University of Wollongong.

## Future directions

Going forward, it is hoped that these materials can be collaboratively updated and improved (at the associated [GitHub repository](https://github.com/carpentrieslab/python-aos-lesson)) by the atmosphere and ocean science community [@Devenyi2018]. Additional topics that could be covered include strategies and best practices for remapping data from one grid to another, processing very large data arrays (i.e. to reduce processing time and to avoid memory errors) and workflow management. These topics are especially relevant for the oceanography community, as ocean models tend to output large data arrays on complex grids.   

# References
