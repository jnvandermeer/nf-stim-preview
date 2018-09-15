import random
import sys
import math
import random
import os
import time


# in * is also: from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
# visual, sound, core, data, event and logging are the crucial ones.
import pygame
import psychopy
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging # I guess this is the best way?

# we use the Dirty Programming Method (*) to import all of psychopy's utlilities and tricks
from FeedbackBase.PsychopyFeedback import PsychopyFeedback
# we need this additional line - this is how we import psychopy -- why we need to write this multiple times?
# "The downside of having to write a couple import statements per module does not outweigh the potential problems
# introduced by trying to get around writing them." (PEP20).


class NFBasicThermometer(PsychopyFeedback):
    
    # constants to be used throughout the DEFs.
    # TRIGGER VALUES FOR THE PARALLEL PORT (MARKERS)
    START_EXP, END_EXP = 252, 253
    COUNTDOWN_START = 0
    START_TRIAL_ANIMATION = 36

    # anything you write in INIT, in terms of variables, will/can be sent and changed...
    def init(self):
        PsychopyFeedback.init(self)
        self.caption="Neurofeedback Thermometer"
        self.color=[0, 0, 0]
        self.fontheight=200
        self.NFPos=0.5

    # this is called BEFORE the main experiment (i.e. before 'play')
    def pre_mainloop(self):
        
        PsychopyFeedback.pre_mainloop(self)
        
        # so.. now you should have self.win, which is the window -- draw stuff on that, etc.
        # THIS ... is where we could 'draw' all kinds of stuff onto the window.
        # we COULD also, define a 'text output' window placed somewhere else, right?
        msg=visual.TextStim(self.win, text="Hallo!!")

        # this will define all of the stuff we're going to use later on. So it's fine if this is big.

        self.upperThr = visual.Rect(win=self.win, name='upperThr', width=0.25, height=0.02, \
                              ori=0, pos=(0, 0.5),\
                              lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb', \
                              fillColor=[1,1,1], fillColorSpace='rgb',\
                              opacity=1, depth=0.0, interpolate=True)

        self.lowerThr = visual.Rect(win=self.win, name='lowerThr', width=0.25, height=0.02,\
                              ori=0, pos=(0, -0.5),\
                              lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',\
                              fillColor=[1,1,1], fillColorSpace='rgb',\
                              opacity=1, depth=0.0, interpolate=True)

        self.levelBar = visual.Rect(win=self.win, name='levelBar', width=0.20, height=0.04,\
                              ori=0, pos=(0, -0),\
                              lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',\
                              fillColor=[1,1,1], fillColorSpace='rgb',\
                              opacity=1, depth=0.0, interpolate=True)

        # NFPos = -0.5 # -0.25
        self.draw_nf_stimulus(self.NFPos)
        self.win.flip()
        
        # i want it to stop here so I can debug?
        #import pdb
        # pdb.set_trace()

    # this is called AFTER main loop...
    def post_mainloop(self):
        PsychopyFeedback.post_mainloop(self)

    # this always gets called, even paused.. -- UNTIL self.on_stop() is called. this will exit the main loop.
    # a 'tick' == ONE passage through the main loop (which is a 'while True' loop, basically...)
    def tick(self):

        # let's see if we can change the parameter within this tick

        countdowntimer = psychopy.clock.CountdownTimer()
        countdowntimer.add(60)
        while countdowntimer.getTime() > 0:
            self.draw_nf_stimulus(self.NFPos)
            self.win.flip()

        self.on_stop()

    # this gets called ONLY -- while on play mode
    def play_tick(self):
        pass
    
    # this gets called ONLY -- while on pause mode
    def pause_tick(self):
        pass
    
    # one could define several other tick methods for different kinds of behaviours.
    
    
    # this function WILL get called whenever I send over a 'control' event -- which is..
    # f.e. the NF data (whatever variable it is!)
    def on_control_event(self, data):
        self.logger.debug("on_control_event: %s" % str(data))
        self.NFPos = data["data"]

        # this function WILL get called whenever I do anything like 'play','pause','quit', etc.
        # and this ALSO can contain some data (for example some init data...)
        # def on_interaction_event(self, data):
        #    print(data)
        #    pass

        # make sure to do some calculation
        # expect a value between -1 and +1 -- and adjust position of the stimulus accordingly.
        # so we either have a bar or a rocket or an image floating upwards or downwards -- make sure it works.



    # make a separate function to draw the NF stimulus, IF REQUESTED
    def draw_nf_stimulus(self, NFPos):

        # the total amount of space (using normalized units in psychopy) -- not taking into account the objects
        # themselves, and being mindful of that position is relative to the CENTER of an object.
        totalspace = self.upperThr.pos[1] - self.upperThr.height / 2. \
                     - (self.lowerThr.pos[1] + self.lowerThr.height / 2.) \
                     - self.levelBar.height


        if NFPos > 1 or NFPos < 1:
            Exception('error: NFPos should be between or equal to -1 and +1!')

        # calculate.. -- NFPos should be -1<=X<=1 --> THEN -- at what fraction of the totalspace should stim be?
        frac = (NFPos + 1.0) / 2.0  # this makes it between 0 and 1.

        # then - set levelBar to a new position == frac * totalspace + half of size of the bar...
        # because the height of an object is relative to the MIDDLE of that object...
        newypos = frac * totalspace + self.lowerThr.pos[1] + self.lowerThr.height/2.0 + self.levelBar.height/2.0

        self.levelBar.setPos((self.levelBar.pos[0], newypos))

        self.upperThr.draw()
        self.lowerThr.draw()
        self.levelBar.draw()
