Neurofeedback in Python
=======================

This is the stimulus environment (**nf-stim**)


It is a combination of stimulus audio/visual components (from psychopy) and real-time functionality to change them in real-time (pyff). Trollius (python 2.7's asyncio) is used to run things concurrently.


| Pyff| Psychopy  |
|----------|------|
| start/stop experiments | visual stimuli |
| remote control from another computer | auditory stimuli |
| send data to experiment in RT | keyboard/button interface |
| | logging to logfile |
| |use extra/dual screens |


A typical workflow exists of, when it comes to stimulus computer:

Enter the src directory and start FeedbackController:

    ```bash
    conda activate st
    cd nf-stim/src
    python FeedbackController.py
    ```
At this stage you can either 
 - start up experiments from the GUI, this will just run an experiment without feedback
  - or use the real-time computer to start up an experiment and send data in real-time (see the nf-rtime environment)


Installation
------------

Pyff is a rather old package, so won't work with the most up-to-date version of pyqt. Also it is coded in Python = 2.7, and it'd take serious effort to try to convert to python 3. In addition, Psychopy is (as of yet) coded in python 2.7. The use of a conda environment guarantees that the packages will run as intended on any system. In addition, it's rather easy to make a shortcut to start things up.

The way to install this stimulus presentation is:

1. Install Git
2. Install Conda
3. Clone the nf-stim environment
4. Use Conda to set up the correct environment `conda env create -f environment.yml` (there are different yml files for windows and linux!)
5. (optional) Make a shortcut to the desktop to easily quick-start the FeedbackController
















