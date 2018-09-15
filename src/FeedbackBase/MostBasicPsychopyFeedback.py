#from __future__ import absolute_import, division

from MainloopFeedback import MainloopFeedback
# from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
# from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
#                                 STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
# import numpy as np  # whole numpy lib is available, prepend 'np.'
# from numpy import (sin, cos, tan, log, log10, pi, average,
#                    sqrt, std, deg2rad, rad2deg, linspace, asarray)
# from numpy.random import random, randint, normal, shuffle
#import os  # handy system and path functions
#import sys  # to get file system encoding
#import time

# import os
# import pdb

# import pygame

# from sys import platform
# from os.path import expanduser
# homeDir=expanduser("~")

#import Xlib
#import Xlib.display



class MostBasicPsychopyFeedback(MainloopFeedback):
    def init(self):
        pass
        # take care of all of my logging, plz?
        # logFile = logging.LogFile('LastRun'+'.log', level=logging.EXP, filemode='w')
        # logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file
        
        # rather convoluted way to write stuff to home directory in an OS-independent fasion, right?
        # but it'd be normal to have this level of abstraction -- this is the 'baggage' of different conventions
        # and learned habits that must be unlearned
        # centralLog = logging.LogFile(os.path.join(homeDir, "psychopyExps.log"), level=logging.WARNING, filemode= 'a')
        
        
        
    def pre_mainloop(self):
        pass
        # self.init_psychopy() # call the init for psychopy...
        

        
    def post_mainloop(self):
        pass
        # self.quit_psychopy()
        

        
    def pause_tick(self):
        pass


    def play_tick(self):
        pass

        
    def tick(self):
        pass
        # do stuff depending on the Pygame Event Queue
        
        
        
    def init_psychopy(self):
        pass
        #display = Xlib.display.Display(':0')

        #number_displays = display.screen_count()  # output: 1

        # screen setup
        #SCREEN_SIZE = (1920,1080)                 # screen res, my screens are identical 
	# SCREEN_SIZE = (1440,900)        
	# win0 = visual.Window(SCREEN_SIZE, monitor='Monitor_00', screen=0, fullscr=False, allowGUI=True,winType='pyglet')
        # win1 = visual.Window(SCREEN_SIZE, monitor='Monitor_01', screen=1, fullscr=False, allowGUI=True,winType='pyglet')
        # win2 = visual.Window(SCREEN_SIZE, monitor='Monitor_02', screen=2, fullscr=False, allowGUI=True,winType='pyglet')

        # the TRICK == to then close win1.
        # win0 is (always?) the window which is where the main Desktop UI resides
        # self.win=win0
        # win1.close()
        # win2.close()
        # print('PsychoPy initialized')
        
        # we could also define a file for output... which would be better in case psychopy would be closed before
        # the experiment would end.
        
        
    def quit_psychopy(self):
        pass
        # self.win.close() -- yes, thanks, I will do this inside the main experiment.
        # core.quit() # core has been imported into the 'class' namespace, right?
        # do stuff like write the file(s), etc...
           
