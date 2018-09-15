#!/usr/bin/env python2 (obviously)
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 15:25:56 2018

@author: johan
"""

#%% COMMENTS
''' So the thing is to deconstruct the bigger problem into a lot of solutions 
for much smaller problems. This is especially true, for the EFL with
visual, auditory and stop-inhibition (staircased) components that operate
interleaved

There's no way one could do this with builder, but (hopefully) with coder
and some help from asyncio, things could work.
'''



#%% Importing Statements
# importing statements:
import re
import random
import os
import pickle
import socket

import pyglet
from psychopy import visual, clock, data, event, logging, sound
import numpy as np

# the assync stuff:
import trollius as asyncio
from trollius import From


#%% Getting Input

# see: http://easygui.sourceforge.net/tutorial.html#enterbox
# variable = easygui.enterbox('hello','title','text')



# OR -- use psychopy's functions:
# expName = 'loc_v1'  # from the Builder filename that created this script
# expInfo = {'participant':'', 'session':'001'}
# dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
#
# access via expInfo['participant'], etc.


#%% Initialize the Window
win=visual.Window(size=(800,600), fullscr=False, allowGUI=True, winType='pyglet', waitBlanking=False)


#%% Frame-by-frame checkerboard List
# load in the frame-list of the visual stimuli: i.e. saying when things should
# be used:
with open('efl/fd.pkl','rb') as f:
    fd=pickle.load(f)
    

with open('efl/complete_fd_list.pkl','rb') as f:
    complete_fd_list=pickle.load(f)

#    with open('efl/fd_with_markers.pkl','rb') as f:
#        fd_with_markers=pickle.load(f)
    
with open('efl/fd_with_markers_II.pkl','rb') as f:
    fd_with_markers=pickle.load(f)



#%% Handle logging

LOGDIR='log'
LOGFILEBASE='efl'

# figure out if there's a log directory, if not --> make it:
if not os.path.exists(LOGDIR):
    os.makedirs(LOGDIR)

# figure out which files reside within this logfile directory:
if len(os.listdir(LOGDIR)) == 0:
    logcounter=0
else:
    # figure out biggest number:
    logcounter = max([int(match.group(1)) 
    for match in [re.match(LOGFILEBASE+'([0-9]*)'+'.log',item) 
    for item in os.listdir(LOGDIR)]])

# so make just another logfile on top of this one -- it'll be timestamped    
logcounter += 1

# this is the new logfile:
newLogFile=os.path.join(LOGDIR, LOGFILEBASE+'%d.log' % logcounter)


# open up a log:
expLogger = logging.LogFile(newLogFile, logging.EXP) # the correct loglevel should be EXP!
# this ensures that all kinds of Exp thingies are written. DATA, WARNING and ERROR are higher
# but INFO and DEBUG won't be used.
# this is actually useful.


# so -- write stuff away with logging.data('blabla'); logging;flush()
# then -- logging.data('message') --> will give timestamped stuff
# logging.flush() --> to ACTUALLY WRITE it to the file!

# many (!!) of the stimuli also create a logging trigger, but you'd need to flush it
# in order to write it as-you-go
# otherwise it'll only happen at the end of the experiment
# and if there is an error of some sort --> bad luck, if you relied on loggin
# for your experimental logfile data crawlers, you just lost EVERYTHING.



#%% Define Visual and GoNogo Stimuli
# make the dicts of visual and stop-inhibition stimuli:
# build a dict of visuals:
vstims=dict()
sstims=dict()
radialFreq=6
angleFreq=6
checkerSize=1.5
cicleSize=checkerSize/12*2
stimSize=checkerSize/12*1.5

AUTOLOGIT = True


checkr=visual.RadialStim(win, tex='sqrXsqr', ori=0, size=checkerSize, 
                     visibleWedge=(0, 181),
                     angularCycles=angleFreq, radialCycles=radialFreq, autoLog=AUTOLOGIT)


checkrf=visual.RadialStim(win, tex='sqrXsqr', ori=-90, size=checkerSize, 
                     visibleWedge=(90, 271),
                     angularCycles=angleFreq, radialCycles=radialFreq, autoLog=AUTOLOGIT)

checkl=visual.RadialStim(win, tex='sqrXsqr', ori=0, size=1.5, 
                     visibleWedge=(180, 360),
                     angularCycles=angleFreq, radialCycles=radialFreq, autoLog=AUTOLOGIT)


checklf=visual.RadialStim(win, tex='sqrXsqr', ori=90, size=1.5, 
                     visibleWedge=(90, 271),
                     angularCycles=angleFreq, radialCycles=radialFreq, autoLog=AUTOLOGIT)

circ=visual.Circle(win, radius=cicleSize, fillColor=[0,0,0], lineColor=[0, 0, 0], autoLog=AUTOLOGIT)

fa=.1;fb=1
fixationVert = [(fa, fa),(fa, fb),(-fa, fb),(-fa, fa),(-fb, fa),(-fb, -fa),
                (-fa, -fa),(-fa, -fb),(fa, -fb),(fa, -fa),(fb, -fa), (fb, fa)]
fixation = visual.ShapeStim(win, vertices=fixationVert, fillColor='red', 
                         size=.025, ori=0, lineColor='red', autoLog=AUTOLOGIT)


vstims['r']=[checkr, circ, fixation]
vstims['rf']=[checkrf, circ, fixation]
vstims['l']=[checkl, circ, fixation]
vstims['lf']=[checklf, circ, fixation]


stimcirc1=visual.Circle(win, radius=stimSize, fillColor=[1, 1, 1], lineColor=[1, 1, 1], autoLog=AUTOLOGIT)
stimcirc2=visual.Circle(win, radius=stimSize/1.5*1.37, fillColor=[0, 0, 0], lineColor=[1, 1, 1], autoLog=AUTOLOGIT)


#al=visual.ImageStim(win, image=u'stims/arrow.png')

arrowPinch=1.75;
arrowVert = [(-0.7071, -0.7071/arrowPinch), (0, -0.7071/arrowPinch),
              (0, -1), (1, 0),
              (0, 1),(0, 0.7071/arrowPinch), 
              (-0.7071, 0.7071/arrowPinch)]

arrowl = visual.ShapeStim(win, vertices=arrowVert, fillColor='white', 
                         size=.095, ori=180, lineColor='white', autoLog=AUTOLOGIT)

arrowr = visual.ShapeStim(win, vertices=arrowVert, fillColor='white', 
                         size=.095, ori=0, lineColor='white', autoLog=AUTOLOGIT)

arrowlr = visual.ShapeStim(win, vertices=arrowVert, fillColor='darkred', 
                         size=.095, ori=180, lineColor='darkred', autoLog=AUTOLOGIT)

arrowrr = visual.ShapeStim(win, vertices=arrowVert, fillColor='darkred', 
                         size=.095, ori=0, lineColor='darkred', autoLog=AUTOLOGIT)


sstims['pre']=[stimcirc1, stimcirc2, fixation]
sstims['fix']=[fixation]

sstims['al']=[stimcirc1, stimcirc2, arrowl]
sstims['ar']=[stimcirc1, stimcirc2, arrowr]
sstims['alr']=[stimcirc1, stimcirc2, arrowlr]
sstims['arr']=[stimcirc1, stimcirc2, arrowrr]




# the eyes closed stimulus:
eyesclosed = visual.TextStim(win, '\t\tEyes Closed\n\n20 seconds, do not count!',
                      color=(1, 1, 1), colorSpace='rgb', autoLog=AUTOLOGIT)




#%% Obtain the Go Nogo Timing Parameters
# for stop-signal task: read in the critucal timings from one of my 500 
# OPTIMAL GLM Design specifications:
tmp_rand_number = random.randint(1,501)
with open('efl/param_%d.txt' % (tmp_rand_number )) as f:
    matrix=[[float(s) for s in re.findall(r'-?\d+\.?\d*', line)] for line in f]
SSnumber, SSstopgo, ISIwaitTime, tmp1, tmp2, LeftOrRight = zip(*matrix)

#
STOP=1
GO=0
#
BUTTONS = ['lctrl', 'rctrl']

# a rather convoluted way of dealing with this on late Friday with beer in sight:
correctResponseSides=[]
wrongResponseSides=[]
for side in LeftOrRight:
    if side == 'left':
        correctResponseSides.append(BUTTONS[0])
        wrongResponseSides.append(BUTTONS[1])
    elif side == 'right':
        correctResponseSides.append(BUTTONS[1])
        wrongResponseSides.append(BUTTONS[0])
        


#%% Initialize the Staircase

    
# set up the staircase handler according specifications in Aron & Poldrack, 2009
# ""Cortical and Subcortical Contributions to Stop Signal Response Inhibition: 
# Role of the Subthalamic Nucleus""
# 
conditions = [
    {'label':'staircase1', 'startVal':100, 'stepSizes':50, 'nTrials':10, 'nUp':1, 'nDown':1, 'applyInitialRule':False, 'stepType':'lin'},
    {'label':'staircase2', 'startVal':150, 'stepSizes':50, 'nTrials':10, 'nUp':1, 'nDown':1, 'applyInitialRule':False, 'stepType':'lin'},
    {'label':'staircase3', 'startVal':200, 'stepSizes':50, 'nTrials':10, 'nUp':1, 'nDown':1, 'applyInitialRule':False, 'stepType':'lin'},
    {'label':'staircase4', 'startVal':250, 'stepSizes':50, 'nTrials':10, 'nUp':1, 'nDown':1, 'applyInitialRule':False, 'stepType':'lin'}
]
myMultiStairs = data.MultiStairHandler(stairType='simple', method='random', conditions=conditions, nTrials=40)

# usage -- use the starcase to loop over the stop trials:
# myMultiStair.next()
# myMultiStair.addResponse(1)
#
# getting intensities (for later to average over):
#
# myMultiStair.staircases[3].intensities
#    for thisIntensity, thisCondition in myMultiStairs:
#        print(thisIntensity)
#        print(thisCondition)
#        myMultiStairs.addResponse(random.choice([0,1]))

#%% Visual Helpers
nextfliptasks=[]
stimulusContents=[]

def makeNewClock():
    clockContainer.append(clock.Clock())
    continueRoutineContainer[0]=True
    


#%% ASYNC I - The GoNogo handler
#
#
# SS Logic:
#
#
# vis contents is a list that's accessible by the function
# if the function changes its contents, then other functions will be able to
# read in those contents, too.
# I let the functions talk to each other using ... what?

# visContents is a list from handleGoNogo that contains the stuff to be drawn 
# GoNogo's end
# nexFlipTasks is a list/.. or a dict of stuff with function names and arguments
# that handleVisual should call using win.
    
#
#class GoNogo(object):
#    def __init__(self, SSnumber, SSstopgo, myMultiStairs, myVisualContents,nextFlipTasks, newClock, continueRoutine):
#        self.SSnumber=SSnumber
#        self.SSstopgo=SSstopgo
#        self.myMultiStairs=myMultiStairs
#        self.myVisualContents=myVisualContents
#        self.nextFlipTasks=nextFlipTasks
#        self.newClock=newClock
#        self.continueRoutine=continueRoutine
#        
# after some sleep, my brain might be able to conceive of how I could make this with a Object Oriented programming
# in the event loop in any case I should definitely use some kind of function that yields.
# or can I also make coroutine objects?
# and.. how to implement this, then?    
    

# this is a list which basically acts as a pointer. From within functions 
# we can change this as needed.
continueRoutineContainer=[False]
# decorate this function...    
@asyncio.coroutine
def handle_gonogo(nextFlipTasks, myClocks, continueRoutineContainer, goNogoStimContainer, eventHandler):
    '''
    This contains the experimenal logic of the Stop Task. A lot of work
    went into constructing the stimuli. Stimuli parameters are loaded
    into variables in the code above. Runs 136 trials of Go-Nogo.
    This function is to be run within the asyncio loop.
    '''
 

    # if the time it took to respond is smaller than this time --> invalid.
    tooSoonTime=0.025
    allResponses=[] 
    numberOfResponses=0
    # set the visual contents here...
    # INITIAL SETTING
    goNogoStimContainer=sstims['fix']


    # yeah, do all kinds of init here.
    for trialNumber in range(SStopgo):

        
        thisDirection=random.choice(('al','ar')) # obtain this from the file!!
        thisTrialType = SStopgo[trialNumber] # this is a 0 (GO) or 1 (STOP)
        thisISIWaitTime = ISIwaitTime[trialNumber]
        
        correctResponseSide = correctResponseSides[trialNumber]
        wrongResponseSide = wrongResponseSides[trialNumber]
        
        responded=False # subj responded?
        tooManyResponses=False
        trialHandled=False
        triggerSentGo=False
        
        
        
        
        # figure out these:
            # BGoL
            # BGoR
            # BStopL
            # BStopR
        
        
        if taskType is STOP:
            # this should be called only 40 times, since there are 40 stop trials...
            thisSSD, thisCondition = myMultiStairs.next() # I defined the myMultiStairs above.
        



        # this code tells the loop to only continue when continueTroutine is not False
        # otherwise it'll just keep yielding.
        # let winflipper make new clock
        continueRoutineContainer[0]=False
        nextfliptasks.append([makeNewClock]) # the makeNewClock automatically makes things continue
        while continueRoutineContainer[0] is False:
            yield From(asyncio.sleep(0))
        cl=clockContainer[0] # obtain the clock that was just made.


        # ok, we can proceed -- the clock has been set.
        while cl.getTime() < 0.5:
            goNogoStimContainer[0]=sstims['pre']
            yield From(asyncio.sleep(0))
    
    
    
    
    
        # obtain our next clock...
        # this code tells the loop to only continue when continueTroutine is not False
        # otherwise it'll just keep yielding.
        # let winflipper make new clock
        continueRoutineContainer[0]=False
        nextfliptasks.append([makeNewClock]) # the makeNewClock automatically makes things continue
        # send the trigger regarding the arrow, as soon as the windows flips
        nextfliptasks.append([eventHandler.handle, 
                              ['BGo','BStop'][thisTrialType] 
                              + {BUTTONS[0]:'L',BUTTONS[1]:'R'}[correctResponseSide]])
        while continueRoutineContainer[0] is False:
            yield From(asyncio.sleep(0))
        cl=clockContainer[0] # obtain the clock that was just made.
        


        
        currentTime = 0.0
        while currentTime < 1.0:
            currentTime = cl.getTime()
            
            # set the stimulus to the proper direction (it's a choice, for now... -- but it's much much better to hard-code it)
            # make the arrow (+ circle)
            vStimContainer[0]=sstims[thisDirection]

            evs=event.getKeys(timeStamped=cl)
            if len(evs)>0:
                buttonsPressed, timesPressed = zip(*evs)
                # it's highly unlikely that two buttons are pressed in a signle
                # frame, but control for that anyway.
                allResponses.append((buttonsPressed[0], timesPressed[0]))
                numberOfResponses += 1
                # LOG this event... (i.e. send trigger)
                
                # handle event:
                if buttonsPressed[0] == BUTTONS[0]:
                    send_event('RR')
                elif buttonsPressed[0] == BUTTONS[1]:
                    send_event('RL')
                    
                    
                

                
            # once a button is pressed -- display fixation point again.
            if len(allResponses) > 0 and not responded:
                # 'clear' the visual window --> fixation cross, again:
                goNogoStimContainer=sstims['fix']
                responded=True
    
            # if it's a stop trial, then make arrow red after X time
            if thisTrialType is STOP and not responded:
                if currentTime > thisSSD:
                    goNogoStimContainer=sstims[thisDirection+'r']

        
            # taking care of the button press itself, as soon as button is pressed:
            if not trialHandled and buttonpressed:
                RTime = allResponses[0][1]
                buttonPressed = allResponses[0][0]
        
                if RTime < tooSoonTime:
                    trialOutcome = 'PressedTooSoon'
                    trialHandled = True
                    myMultiStairs.addResponse(0)
                else:
                    if trialType is STOP:
                        
                        if buttonPressed == correctResponseSide:
                            trialOutcome = 'ErrorCommission'
                            trialHandled = True
                            # ...aaand... of course, add the response to the Staircase Handler.
                            myMultiStairs.addResponse(0)
    
                        elif buttonPressed == wrongResponseSide:
                            trialOutcome = 'WrongSideErrorCommission'
                            trialHandled = True
                            myMultiStairs.addResponse(0)
                            
                        
                    elif trialType is GO:
                        if buttonPressed == correctResponseSide:
                            trialOutcome = 'Go'+correctResponseSide
                            trialHandled = True
                            triggerSentGo = False
                            # not yet...
                        elif buttonPressed == wrongResponseSide:
                            trialOutcome = 'WrongSideGo'
                            trialHandled = True
                            myMultiStairs.addResponse(0)
                        
                # something happened --> so send an event!
                eventHandler.handle(trialOutcome)
                
        
            # here we wait...
            yield From(asyncio.sleep(0))
    
        
        # AFTER 1.0 seconds we should be here... out of the while loop:            
        # handle the 'response' if the button was NOT pressed:
        if not trialHandled and not buttonpressed:
            if trialType is GO:
                trialOutcome = 'ErrorOmission'
                trialHandled = True
                myMultiStairs.addResponse(0)

            if trialType is STOP:
                trialOutcome = 'Stop'+correctResponseSide
                trialHandled = True
                 # ...aaand... of course, add the response to the Staircase Handler.
                myMultiStairs.addResponse(1)
                
                
        # only when 1 button was pressed, and trialoutcome = 'Go'                
        if numberOfResponses > 1:
            tooManyResponses = True
                
        if trialOutcome == 'Go'+correctResponseSide and not triggerSentGo:
            if numberOfResponses == 1:
                myMultiStairs.addResponse(1)
            else:
                myMultiStairs.addResponse(0)
            triggerSentGo=True
            
            
            
        

        # obtain our next clock...
        # this code tells the loop to only continue when continueTroutine is not False
        # otherwise it'll just keep yielding.
        # let winflipper make new clock
        continueRoutineContainer[0]=False
        nextfliptasks.append([makeNewClock]) # the makeNewClock automatically makes things continue
        while continueRoutineContainer[0] is False:
            yield From(asyncio.sleep(0))
        cl=clockContainer[0] # obtain the clock that was just made.



        # this is a nice place to save it to logfile: before the 
        # send a report about the STOP trial, write a nice line:
        logging.data('messa')
        logging.flush()

         # ok, we can proceed -- the clock has been set.
        while cl.getTime() < thisISIWaitTime:
            goNogoStimContainer=sstims['fix']
            yield From(asyncio.sleep(0))
        


        # the stop task should be finished now!
        # the visual task should also be finished around the same time.
        # so further stuff, we can do with basic instructions, wait times, etc
            


#%% ASYNC V - Handle the Audio!

# the audio stim list:
audio_stim_list = [[10.,20.,'audio',['left','40']],[112.5,130.,'audio',['left','40']],[242.5,260.,'audio',['left','40']],[50.,60.,'audio',['left','55']],[195.,205.,'audio',['left','55']],[312.5,330.,'audio',['left','55']],[30.,40.,'audio',['right','40']],[147.5,165.,'audio',['right','40']],[277.5,295.,'audio',['right','40']],[77.5,95.,'audio',['right','55']],[175.,185.,'audio',['right','55']],[215.,225.,'audio',['right','55']]]
        

snd = sound.backend_pygame.SoundPygame(value='stims/audio_40Hz_L.wav',loops=4)


#%% ASYNC II - The Visual handler
## set up the functions to be used in the end for asyncing through the loops:
# load the vis table somewhere here - big mem space (.csv?)



# load in the table that tells me all the stop signal stuff (.csv?)



# init the window..

# draw all the stimuli for both vis and stop already (and store them)

# load in the audio

# curr frame = 0
# coroutine:

# this tells the asyncIO to sleep this function for a little while, allowing other routines to do their thing.
# after this time (which is 0.8 * the time to flip the screen), continue here
# python will then pause until the previous screen flip is done
# before it calls the current screen flip (and hopefully yields control of the
# interpreter to the user again, allowing processing of the Go-Nogo and auditory. )
        
        
MARKER_VISUAL=1;        
ASYNC_SLEEPTIME = 1/60.*0.75

@asyncio.coroutine
def handle_visual(win):
    '''
    This flips the window, draws the stuff to be drawn, and calls
    functions to be called from the stop task. It is supposed to be
    run in the asyncio loop.
    '''
    
    
    mainClock=clock.Clock() # our main clock...
    frameCounter=0
    previousShapes=[]
    mainCurrentTime=0

    
    # this will run the entire length of the visual...
    # within this time, the stop signal task will (hopefully) finish.
    # OR... we can also just use a counter.
    while mainCurrentTime < 340. :
    
    
    
    
        # the workflow
        # 1) Prepare everything + draw
        # 2) Prepare markers
        # 3) win.flip() + the callOnFlip routines to be done.
    
        
        # all the visual stuff:
        frameIndex, visContents, markers = fd_with_markers[frameCounter]
        frameCounter += 1
        # deal with the visuals -- using vstims which should be accessible
        # we get the list...
        # create the shapes to be drawn using list comprehension
        if len(visContents) > 0:
            shapes=[stim for stim in vstims[ind] for ind in visContents]
        else:
            shapes=[]


        
        
        # add the gonogo stimuli to them:
        for stim in goNogoStimContainer[0]:
            shapes.append(goNogoStims)
        
        
        
        
        # draw them on our little canvas.
        for shape in shapes:
            shape.draw()
        

        
        # prepare the calls for the next iteration, including marlers;
        # deal with visual markers
        if len(markers) > 0:
            for marker in markers:
                win.callOnFlip(eventHandler.handle,marker)
        
        
        for task in nextfliptasks:
            if len(task)==1:
                win.callOnFlip(task)
            elif len(task)==2:
                win.callOnFlip(task, args)



        # we flip the screen here - this will take ~ 16.66667 msec.
        win.flip()
        
        
        
        
        # sleep for a little while:
        yield From(asyncio.sleep(ASYNC_SLEEPTIME))
        
        
        
        # do for loop for TIME (I suppose)
        
        # check vis table + draw stimuli
        # if there's an event - send to sync
        
        # check stimulus for stop + draw stimuli
        
        # pass on current time for audio presentation (this is another process)
        
        # AWAIT (!) -- to flip the window
    

#%% ASYNC IV - If someone presses the 'Escape' Key:
        


    

#%% LOGGING & TRIGGERS Handle our logging & triggers

# these are the visual evt codes that I conceived a while ago:



#    visual_evt_codes={'left':{'8':87,'13':137},'right':{'8':88,'13':138}}
#    
#    # these are markers for the frequency analysis
#    visual_evt_codes_begin={'left':{'8':83,'13':133},'right':{'8':84,'13':134}}
#    visual_evt_codes_end={'left':{'8':85,'13':135},'right':{'8':86,'13':136}}
#    
#    # these are the thread starts - which conveniently also denotify what your visual segments
#    # should BE - in case you wish to reconstruct the visual ERP
#    global visual_evt_codes_beginvisthread
#    visual_evt_codes_beginvisthread={'left':{'8':81,'13':131},'right':{'8':82,'13':132}}
#    
#    
#    
#    
#    
#    
#    audio_evt_codes={'left':{'40':41,'55':51},'right':{'40':42,'55':52}}
#    audio_evt_codes_begin={'left':{'40':43,'55':53},'right':{'40':44,'55':54}}
#    audio_evt_codes_end={'left':{'40':45,'55':55},'right':{'40':46,'55':56}}
#    
#    
#    txt_evt_codes = {'normal':100, 'oddball':101}
        

# define a dict with ev codes and numerals that need to be sent out:
        



MSGDICT={
        
        # Stop / Inhibit Response Codes
        'BeginGoL':1,
        'BeginGoR':2,
        'BeginStopL':3,
        'BeginStopR':4,
        
        'RespL':5,
        'RespR':6,

        'PressedTooSoon':30,
        'ErrorCommission':31,
        'WrongSideErrorCommission':32,
        'CorrectGoL':11,
        'CorrectGoR':12,
        'WrongSideGo':33,
        'ErrorOmission':34,
        'CorrectStopL':13,
        'CorrectStopR':14,

        # visual SSVEP checkerboard codes (8 and 13 Hz)
        #
        # when the contrast inverts, for SSVEP deconvolution
        'vis_l8':81,
        'vis_r8':82,
        'vis_l13':131,
        'vis_r13':132,

        # begin and end markers (for EEG frequency analysis), 8Hz and 13Hz
        'vis_bl8':83,
        'vis_br8':84,
        'vis_el8':85,
        'vis_er8':86,
 
        'vis_bl13':133,
        'vis_br13':134,
        'vis_el13':135,
        'vis_er13':136,

        # audio SSVEP codes (40 Hz and 55 Hz)
        #
        # when audio sample starts -- one audio sample contains 32 
        'aud_l40':41,
        'aud_r40':42,
        'aud_l55':51,
        'aud_r55':52,

        'aud_bl40':43,
        'aud_br40':44,
        'aud_el40':45,
        'aud_er40':46,
 
        'aud_bl55':53,
        'aud_br55':54,
        'aud_el55':55,
        'aud_er55':56
            
        }        
        


import multiprocessing
class eventHandler(multiprocessing.Process):
    def __init__(self, ip, port, clock, filename='log/triggerlog.log',
                 sendParallel=True, sendTcpIp=True, sendLogFile=False):
        '''
        we check parallel port, network port, and a file here (and we use the
        logger to do all of that log stuff)
        '''
        
        self.clock=clock
        self.sendParallel=sendParallel
        self.sendTcpIp=sendTcpIp
        self.sendLogFile=sendLogFile
        
        
        
        super(eventHandler, self).__init__()
        # do we even have a parallel port?
        try:
            port=parallel.ParallelPort()
        except OSError:
            print('OS Does not seem to have a parallel port')
            
        self._queue = multiprocessing.Queue()
        

        
        # check whether there's another logfile - in log directory
        # make efl_triggers version of it, too.
        logdir=os.path.dirname(filename)
        logbasename, ext = os.path.splitext(os.path.basename(fn))

        
        # figure out if there's a log directory, if not --> make it:
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        
        # figure out which files reside within this logfile directory:
        if len(os.listdir(logdir)) == 0:
            logcounter=0
        else:
            # figure out biggest number:
            logcounter = max([int(match.group(1)) 
            for match in [re.match(logbasename+'([0-9]*)'+ext,item) 
            for item in os.listdir(logdir)]])
        
        # so make just another logfile on top of this one -- it'll be timestamped    
        logcounter += 1
        
        # this is the new logfile:
        newLogFile=os.path.join(logdir,logbasename+'%d' + ext % logcounter)
        
        
        # open up a log:
        expLogger = logging.LogFile(newLogFile, logging.EXP) # the correct loglevel should be EXP!
        
        
        
        # so that's the logfile -- open op the socet, too:
        
        
        
        
        
        


    def send_message(self,message):
        '''
        it'll put the message into the queue, to be processed by 'run'
        '''
        self._queue.put(message)
        
        
    def run(self):
        
        
        # do some while loop, checking for messages, and when one arrives -->
        # process it with both logfile (possibly) and with sending parallel
        # and also with.
        
        while not self._queue.empty():
            
            message =  self._queue.get()
            code_to_send=MSGDICT[message]

            if self.sendParallel:
                pass
            
            if self.sendTcpIp=sendTcpIp:
                pass

            if self.sendLogFile=sendLogFile:
                expLogger.write('%.6f\t%d\n' % (cl.getTime() code_to_send))
                
                
        
        # so - figure out whether we're in Windows or in Linux world
        
        # if windows, get parallel port
        
        # I guess things should be general enough, right?
        
        
        
        # also - send triggers via our network connection towards
        
        
        
    

#%% ASYNC III - The Main Event Loop
def run_main_loop():    
    '''
    This runs the stopingibition/visual/audio part of the paradigm using
    asyncio-replacement trollius. Before and after, we can still present
    other stimuli.
    '''
    
    
# something like this:
    
    
    # initialuze the eventHandler
    ev = eventHandler()
    ev.start()
    
    
    
    
    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.async(handleVisual()),
        asyncio.async(handleGonogo()),
        asyncio.async(handleEscape()),
        ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
        
    




#%% MAIN -- hope things work
    if __name__=="__main__":
        # do the stuff.
    
    
        