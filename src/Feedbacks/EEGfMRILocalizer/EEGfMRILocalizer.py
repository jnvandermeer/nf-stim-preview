import random
import sys
import math
import random
import os
import time
import pickle


# in * is also: from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
# visual, sound, core, data, event and logging are the crucial ones.
import pygame
import psychopy
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging # I guess this is the best way?


# some helpers:
from Feedbacks.EEGfMRILocalizer.efl import eventhandler
from Feedbacks.EEGfMRILocalizer.efl import visualHelper

# the actual experiment:
from Feedbacks.EEGfMRILocalizer.efl.efl_v11 import * 



# we use the Dirty Programming Method (*) to import all of psychopy's utlilities and tricks
from FeedbackBase.MostBasicPsychopyFeedback import MostBasicPsychopyFeedback
# we need this additional line - this is how we import psychopy -- why we need to write this multiple times?
# "The downside of having to write a couple import statements per module does not outweigh the potential problems
# introduced by trying to get around writing them." (PEP20).


class EEGfMRILocalizer(MostBasicPsychopyFeedback):
    
    # constants to be used throughout the DEFs.
    # TRIGGER VALUES FOR THE PARALLEL PORT (MARKERS)
    START_EXP, END_EXP = 252, 253
    COUNTDOWN_START = 0
    START_TRIAL_ANIMATION = 36

    # anything you write in INIT, in terms of variables, will/can be sent and changed...
    def init(self):
        MostBasicPsychopyFeedback.init(self)
        self.caption="EEG - fMRI Localizer"
        self.color=[0, 0, 0]
        self.fontheight=200
        
        self.STARTKEYS=['return','t']
        self.MONITOR_PIXWIDTH=1280
        self.MONITOR_PIXHEIGHT=1024
        self.MONITOR_WIDTH=40.  # width of screen
        self.MONITOR_HEIGHT=30.  # height of screen
        self.MONITOR_DISTANCE=70.  # distance to screen
        self.MONITOR_GAMMA=1.
        self.MONITOR_FPS=60.
        self.MONITOR_USEDEGS=True
        self.MONITOR_DEGS_WIDTHBASE=30
        self.MONITOR_DEGS_HEIGHTBASE=25
        self.MONITOR_FLIPHORIZONTAL = False
        self.MONITOR_FLIPVERTICAL = False
        
        self.MONITOR_NSCREENS=2
        self.MONITOR_DISPLAYONSCREEN=1
        self.MONITOR_FULLSCR = False
        self.MONITOR_ALLOWGUI = False
        
        self.LOGDIR='log'  # for if you want to change this...
        self.LOGFILEBASE='efl'  # how to call our logfile --> it adds a number each time
        self.IPADDRESS='localhost'  # port and ip to send codes towards to
        self.PORT=6050  # which port is nice?  
        self.BUTTONS = ['lctrl', 'rctrl']  # the button codes coming out of event.getStim()
        self.tooSoonTime=0.0  # if it's pressed before this time --> discard + error
        self.LPT_TRIGGER_WAIT=0.005  # how long are the LPT port pulses?
        self.RECORDFRAMEINTERVALS = True  # for debugging..
        self.DO_VISUAL = True
        self.DO_AUDIO = True
        self.DO_GNG = True
        self.GNGSPEED = 1.0
        self.GNG_ARROWGOESRED = True
        self.GNG_ARROWGOESRED_DELAY = 0.25
        self.AUDIOTONE_ERROR_COMMISSION = False
        self.AUDIOTONE_STOP = False
        self.VIS_SHOWOPPOSITE = False
        self.VIS_radialFreq=6
        self.VIS_angleFreq=6
        self.VIS_checkerSize=1.5
        self.VIS_checkerSpeedMultiplier=1.0
        self.EYESCLOSED_TIME=25.
        
        
        self.EVENT_destip='127.0.0.1'
        self.EVENT_destport=6050
        self.EVENT_LPTAddress=0x0378
        self.EVENT_LPTTrigWaitTime=0.005
        self.EVENT_TRIGLOG='log/triggerlog.log'
        self.EVENT_sendParallel=True
        self.EVENT_sendTcpIp=True
        self.EVENT_sendLogFile=True
        self.EVENT_printToTerminal=True
        self.EVENT_printToTerminalAllowed=[0, 40]  # only allow the stops, which are < 40.
        
        self.INSTR='Remember, respond as FAST as you can once you see the arrow.\n\n'+'However, if you hear a beep, your task is to STOP yourself '+'from pressing.\n\n'+'Stopping and Going are equally important.'

        
        
        
        
        

    # this is called BEFORE the main experiment (i.e. before 'play')
    def pre_mainloop(self):
        
        MostBasicPsychopyFeedback.pre_mainloop(self)
        
        
        # do the trick -- SAVE all of those things! --> and put it in settings.pkl.
        v=dict()
        v['STARTKEYS']                      =self.STARTKEYS
        v['MONITOR_PIXWIDTH']               =self.MONITOR_PIXWIDTH
        v['MONITOR_PIXHEIGHT']              =self.MONITOR_PIXHEIGHT
        v['MONITOR_WIDTH']                  =self.MONITOR_WIDTH  # width of screen
        v['MONITOR_HEIGHT']                 =self.MONITOR_HEIGHT  # height of screen
        v['MONITOR_DISTANCE']               =self.MONITOR_DISTANCE  # distance to screen
        v['MONITOR_GAMMA']                  =self.MONITOR_GAMMA
        v['MONITOR_FPS']                    =self.MONITOR_FPS
        v['MONITOR_USEDEGS']                =self.MONITOR_USEDEGS
        v['MONITOR_DEGS_WIDTHBASE']         =self.MONITOR_DEGS_WIDTHBASE
        v['MONITOR_DEGS_HEIGHTBASE']        =self.MONITOR_DEGS_HEIGHTBASE
        v['MONITOR_FLIPHORIZONTAL']         =self.MONITOR_FLIPHORIZONTAL
        v['MONITOR_FLIPVERTICAL']           =self.MONITOR_FLIPVERTICAL
        
        v['MONITOR_NSCREENS']               =self.MONITOR_NSCREENS
        v['MONITOR_DISPLAYONSCREEN']        =self.MONITOR_DISPLAYONSCREEN
        v['MONITOR_FULLSCR']                =self.MONITOR_FULLSCR
        v['MONITOR_ALLOWGUI']               =self.MONITOR_ALLOWGUI
            
        v['LOGDIR']                         =self.LOGDIR  # for if you want to change this...
        v['LOGFILEBASE']                    =self.LOGFILEBASE  # how to call our logfile --> it adds a number each time
        v['IPADDRESS']                      =self.IPADDRESS  # port and ip to send codes towards to
        v['PORT']                           =self.PORT  # which port is nice?  
        v['BUTTONS']                        =self.BUTTONS  # the button codes coming out of event.getStim()
        v['tooSoonTime']                    =self.tooSoonTime  # if it's pressed before this time --> discard + error
        v['LPT_TRIGGER_WAIT']               =self.LPT_TRIGGER_WAIT  # how long are the LPT port pulses?
        v['RECORDFRAMEINTERVALS']           =self.RECORDFRAMEINTERVALS  # for debugging..
        v['DO_VISUAL']                      =self.DO_VISUAL
        v['DO_AUDIO']                       =self.DO_AUDIO
        v['DO_GNG']                         =self.DO_GNG
        v['GNGSPEED']                       =self.GNGSPEED
        v['GNG_ARROWGOESRED']               =self.GNG_ARROWGOESRED
        v['GNG_ARROWGOESRED_DELAY']         =self.GNG_ARROWGOESRED_DELAY
        v['AUDIOTONE_ERROR_COMMISSION']     =self.AUDIOTONE_ERROR_COMMISSION
        v['AUDIOTONE_STOP']                 =self.AUDIOTONE_STOP
        v['VIS_SHOWOPPOSITE']               =self.VIS_SHOWOPPOSITE
        v['VIS_radialFreq']                 =self.VIS_radialFreq
        v['VIS_angleFreq']                  =self.VIS_angleFreq
        v['VIS_checkerSize']                =self.VIS_checkerSize
        v['VIS_checkerSpeedMultiplier']     =self.VIS_checkerSpeedMultiplier
        v['EYESCLOSED_TIME']                =self.EYESCLOSED_TIME
        
        v['EVENT_destip']                   =self.EVENT_destip
        v['EVENT_destport']                 =self.EVENT_destport
        v['EVENT_LPTAddress']               =self.EVENT_LPTAddress
        v['EVENT_LPTTrigWaitTime']          =self.EVENT_LPTTrigWaitTime
        v['EVENT_TRIGLOG']                  =self.EVENT_TRIGLOG
        v['EVENT_sendParallel']             =self.EVENT_sendParallel
        v['EVENT_sendTcpIp']                =self.EVENT_sendTcpIp
        v['EVENT_sendLogFile']              =self.EVENT_sendLogFile
        v['EVENT_printToTerminal']          =self.EVENT_printToTerminal
        v['EVENT_printToTerminalAllowed']   =self.EVENT_printToTerminalAllowed  # only allow the stops, which are < 40.
        
        v['INSTR']                          =self.INSTR



        G=dict()
        G['v']=v
        #
        # global variable with references to desired memory locations is easier to pass around.
        mainClock=clock.Clock()
        G['mainClock']=mainClock
        
        self.G=G  # try this..
        
        
        # doing all of the init stuff:
        G=init_screen(G)
        G=init_logfile(G)
        G=init_stimuli(G)
        G=init_eventcodes(G)
        
        G=init_gng(G)
        
        G=init_reset_clock(G)
        
        G=init_audio(G)
        G=init_visual(G)
        
        G=start_ev(G)
        
        # load in the settings file that is near THIS script!
        # the settings will also be written in the logfile
        # come to think of it -- probably this isn't necessary either.
        # settings and constants can be put into a file liek that, right?
        # --> test
        # OK, not if you're evaluating based on those constants like I try to do here!
        # so save/load to settings file seems to be the way to go.
        #settingsfile=os.path.join(os.path.dirname(os.path.realpath(__file__)),'settings.pkl')
        #with open(settingsfile,'wb') as f:
        #    pickle.dump(v, f)
        #    time.sleep(0.5)
        
        # we now just need to pass it on to G.
        
        
        # remove from the main script copy/paste all of those __init__ variables, so things will look better.
        # so it's in directory efl, and called "efl_v6.py"

        # import efl.efl_v6

    
        # now -- 
        
        
        #        # so.. now you should have self.win, which is the window -- draw stuff on that, etc.
        #        # THIS ... is where we could 'draw' all kinds of stuff onto the window.
        #        # we COULD also, define a 'text output' window placed somewhere else, right?
        #        msg=visual.TextStim(self.win, text="Hallo!!")
        #
        #        # this will define all of the stuff we're going to use later on. So it's fine if this is big.
        #
        #        self.upperThr = visual.Rect(win=self.win, name='upperThr', width=0.25, height=0.02, \
        #                              ori=0, pos=(0, 0.5),\
        #                              lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb', \
        #                              fillColor=[1,1,1], fillColorSpace='rgb',\
        #                              opacity=1, depth=0.0, interpolate=True)
        #
        #        self.lowerThr = visual.Rect(win=self.win, name='lowerThr', width=0.25, height=0.02,\
        #                              ori=0, pos=(0, -0.5),\
        #                              lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',\
        #                              fillColor=[1,1,1], fillColorSpace='rgb',\
        #                              opacity=1, depth=0.0, interpolate=True)
        #
        #        self.levelBar = visual.Rect(win=self.win, name='levelBar', width=0.20, height=0.04,\
        #                              ori=0, pos=(0, -0),\
        #                              lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',\
        #                              fillColor=[1,1,1], fillColorSpace='rgb',\
        #                              opacity=1, depth=0.0, interpolate=True)
        #
        #        # NFPos = -0.5 # -0.25
        #        self.draw_nf_stimulus(self.NFPos)
        #        self.win.flip()
        #        
        # i want it to stop here so I can debug?
        #import pdb
        # pdb.set_trace()

    # this is called AFTER main loop...
    def post_mainloop(self):
        MostBasicPsychopyFeedback.post_mainloop(self)

    # this always gets called, even paused.. -- UNTIL self.on_stop() is called. this will exit the main loop.
    # a 'tick' == ONE passage through the main loop (which is a 'while True' loop, basically...)
    def tick(self):

        # getting in the variables:
        G=self.G
        # from efl.efl_v6 import *
        # put everything here, which is in from __name__ == "__main__"
        # so this is one 'tick', but that's OK - one tick is all we need from pyff.
        
        try:
            
            wait_for_key(G)
            test_buttons(G)
            instr_screen0(G)
            eo_stim(G)
            ec_stim(G)
            logging.flush()

            
            test_buttons(G)
            instr_screen(G)
            logging.flush()
            
            # print(G['eh'].is_alive())
            # print('----><----')
            # G['eh'].send_message('boe!')
            # print('----><----')
            run_main_loop(G)
            logging.flush()
        
            eo_stim(G)
            ec_stim(G)
            end_task(G)
            logging.flush()
            
            
            # close window here.
            G['win'].close()
            logging.flush()
            
            
        except KeyboardInterrupt:
            G['eh'].shutdown()
            G['eh'].join()
            G['win'].close()
            logging.flush()


        # once done, stop the FB with this:
        # so we can re-start it, right?
        self.on_stop()
        
        # here, we should call the main script 'efl'.
        
        # let's see if we can change the parameter within this tick

        #        countdowntimer = psychopy.clock.CountdownTimer()
        #        countdowntimer.add(60)
        #        while countdowntimer.getTime() > 0:
        #            self.draw_nf_stimulus(self.NFPos)
        #            self.win.flip()
        #
        #        self.on_stop()

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
        pass
        #self.logger.debug("on_control_event: %s" % str(data))
        #self.NFPos = data["data"]
        # but we can change properties of the data --> so can draw stff!
        

        # this function WILL get called whenever I do anything like 'play','pause','quit', etc.
        # and this ALSO can contain some data (for example some init data...)
        # def on_interaction_event(self, data):
        #    print(data)
        #    pass

        # make sure to do some calculation
        # expect a value between -1 and +1 -- and adjust position of the stimulus accordingly.
        # so we either have a bar or a rocket or an image floating upwards or downwards -- make sure it works.



        #    # make a separate function to draw the NF stimulus, IF REQUESTED
        #    def draw_nf_stimulus(self, NFPos):
        #
        #        # the total amount of space (using normalized units in psychopy) -- not taking into account the objects
        #        # themselves, and being mindful of that position is relative to the CENTER of an object.
        #        totalspace = self.upperThr.pos[1] - self.upperThr.height / 2. \
        #                     - (self.lowerThr.pos[1] + self.lowerThr.height / 2.) \
        #                     - self.levelBar.height
        #
        #
        #        if NFPos > 1 or NFPos < 1:
        #            Exception('error: NFPos should be between or equal to -1 and +1!')
        #
        #        # calculate.. -- NFPos should be -1<=X<=1 --> THEN -- at what fraction of the totalspace should stim be?
        #        frac = (NFPos + 1.0) / 2.0  # this makes it between 0 and 1.
        #
        #        # then - set levelBar to a new position == frac * totalspace + half of size of the bar...
        #        # because the height of an object is relative to the MIDDLE of that object...
        #        newypos = frac * totalspace + self.lowerThr.pos[1] + self.lowerThr.height/2.0 + self.levelBar.height/2.0
        #
        #        self.levelBar.setPos((self.levelBar.pos[0], newypos))
        #
        #        self.upperThr.draw()
        #        self.lowerThr.draw()
        #        self.levelBar.draw()
