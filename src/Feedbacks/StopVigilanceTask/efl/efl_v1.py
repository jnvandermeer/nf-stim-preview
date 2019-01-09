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
    import sys
    import traceback

    
    import pyglet
    from psychopy import visual, clock, data, event, logging, sound, parallel
    import numpy as np
    
    # the assync stuff:
    import trollius as asyncio
    from trollius import From


#%% Some realy global variables

    LOGDIR='log'  # for if you want to change this...
    LOGFILEBASE='efl'  # how to call our logfile --> it adds a number each time
    IPADDRESS='localhost'  # port and ip to send codes towards to
    PORT=6000  
    BUTTONS = ['lctrl', 'rctrl']  # the button codes coming out of event.getStim()
    tooSoonTime=0.025  # if it's pressed before this time --> discard + error


#%% Initialize the Window
    win=visual.Window(size=(800,600), fullscr=False, allowGUI=True, winType='pyglet', waitBlanking=False)


    # since we're dealing with a couple of loops that are intermixed, and global variables are evil, at least
    # do this -- make a dict that contains all variables that are needed so that the intermixed loops all
    # require only ONE input argument, which helps me with the async stuff later on.
    
    # only use the G if it's going to be used later on in the gonogo, in the stop or in the visual.
    G=dict()



#%% Handle logging

    G['mainClock']=clock.Clock()


    
    # figure out if there's a log directory, if not --> make it:
    if not os.path.exists(LOGDIR):
        os.makedirs(LOGDIR)
    
    # figure out which files reside within this logfile directory:
    if len(os.listdir(LOGDIR)) == 0:
        logcounter=0
    else:
        # figure out biggest number:
        #logcounter = max([int(match.group(1)) 
        #for match in [re.match(LOGFILEBASE+'([0-9]*)'+'.log',item) 
        #for item in os.listdir(LOGDIR)]])
    
        # figure out biggest number:
        matches=[match for match in [re.match(LOGFILEBASE+'([0-9]*)'+'.log',item) for item in os.listdir(LOGDIR)]]
        newlist=[]
        for match in matches:
            if match is not None:
                newlist.append(match.group(1))
        logcounter = max([int(n) for n in newlist])
    
    
    
    # so make just another logfile on top of this one -- it'll be timestamped    
    logcounter += 1
    
    # this is the new logfile:
    newLogFile=os.path.join(LOGDIR, LOGFILEBASE+'%d.log' % logcounter)
    
    
    # open up a log:
    expLogger = logging.LogFile(newLogFile, logging.EXP) # the correct loglevel should be EXP!
    logging.setDefaultClock(mainClock)
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


    
    G['vstims']=dict()
    G['vstims']['V']=vstims
    G['vstims']['S']=sstims
    G['vstims']['eyesclosed']=eyesclosed

    G['vstims']['eyesclosed']=eyesclosed


#%% Send Markers To Everything: The Event Handler

# these are the visual evt codes that I conceived a while ago:
    
        
        
    MSGDICT={
            
            # Stop / Inhibit Response Codes
            'BeginGoL':1,
            'BeginGoR':2,
            'BeginStopL':3,
            'BeginStopR':4,
            
            'RespL':5,
            'RespR':6,

            'CorrectGoL':11,
            'CorrectGoR':12,
            'CorrectStopL':13,
            'CorrectStopR':14,
            'ErrorCommission':15,
            
            # don't expect too many of these:
            'ErrorOmission':21,
            'PressedTooSoon':22,
            'TooManyResponses':23,
            'WrongSideErrorCommission':24,
            'WrongSideGo':25,

            
    
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
        def __init__(self, 
                     messagedict,
                     clock, 
                     destip='127.0.0.1', 
                     destport=6500, 
                     LPTAddress=0x0378,
                     filename='log/triggerlog.log',
                     sendParallel=True, 
                     sendTcpIp=True, 
                     sendLogFile=True
                     ):
            '''
            we check parallel port, network port, and a file here (and we use the
            logger to do all of that log stuff)
            '''
            
            super(eventHandler, self).__init__()
            
            self.messagedict=messagedict
            self.clock=clock
            self.sendParallel=sendParallel
            self.sendTcpIp=sendTcpIp
            self.sendLogFile=sendLogFile
            self.destip=destip
            self.destport=destport
            
            
            # do we even have a parallel port?
            try:
                self._port=parallel.ParallelPort(LPTAddress)
                self._port.setData(0)  # this is the 'reset' to 0
                self._port_doreset=False  # once done we shouldn't do it..
                self._port_waitttime=0.005  # wait 5 msec after a trigger..
                
            except OSError:
                self._port=None
                self._port_doreset=False
                self._port_waitttime=None
                print('OS Does not seem to have a parallel port')
                # deactivate our parallel...
                self.sendParallel=False
                
            self._queue = multiprocessing.Queue()
            
            self._timequeue = multiprocessing.Queue()
            
            self._shutdown = multiprocessing.Event()
            
    
            
            # check whether there's another logfile - in log directory
            # make efl_triggers version of it, too.
            logdir=os.path.dirname(filename)
            logbasename, ext = os.path.splitext(os.path.basename(filename))
    
            
            # figure out if there's a log directory, if not --> make it:
            if not os.path.exists(logdir):
                os.makedirs(logdir)
            
            # figure out which files reside within this logfile directory:
            if len(os.listdir(logdir)) == 0:
                logcounter=0
            else:
                # figure out biggest number:
                matches=[match for match in [re.match(logbasename+'([0-9]*)'+ext,item) for item in os.listdir(logdir)]]
                newlist=[]
                for match in matches:
                    if match is not None:
                        newlist.append(match.group(1))
                logcounter = max([int(n) for n in newlist])
                        
                        
            
            # so make just another logfile on top of this one -- it'll be timestamped    
            logcounter += 1
            
            # this is the new logfile:
            newLogFile=os.path.join(logdir,logbasename+'%d'%logcounter + ext )
            
            
            # open up a log:
            self.expLogger = logging.LogFile(newLogFile, logging.EXP) # the correct loglevel should be EXP!
            
            
            
            # so that's the logfile -- open op the socet, too:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
            
            
            print(newLogFile)
    
    
        def send_message(self,message):
            '''
            it'll put the message into the queue, to be processed by 'run'
            '''
            self._queue.put(message)
            self._timequeue.put(self.clock.getTime())
            
            
        def run(self):
            '''
            This part runs - with a copy of memory upon its creation - in the separate process
            So it should just look at the queue, see if something's up, and send
            a trigger when it does.
            '''
            
            # do some while loop, checking for messages, and when one arrives -->
            # process it with both logfile (possibly) and with sending parallel
            # and also with.
            
            while not self._shutdown.is_set():
                while not self._queue.empty():
                    
                    
                    try:
                    
                        message =  self._queue.get()
                        senttime = self._timequeue.get()  # I want to check how long it takes to deal with the queue like this.
                        code_to_send=self.messagedict[message]
                    
                    except:
                        
                        print('That code doesn\'''t exist!')
                        break
                        
                    

                    
                    # print(message)
                    # print(code_to_send)
                    if self.sendParallel:
                        self._port.setData(code_to_send)
                        
                        # following code is to reset to 0 of the LPT code output, after X msec.
                        # only evaluate if the queue is empty == dealing with the latest marker.
                        if self._queue.empty():
                            lasttime=self.clock.getTime()
                            self._port_doreset=True
                            
                    
                    if self.sendTcpIp:
                        
                        print 
                        self.sock.sendto(unicode(code_to_send), (self.destip, self.destport))
                        
                    if self.sendLogFile:
                        
                        heretime=self.clock.getTime()
                        
                        print('code: %d\t time sent: %.6f time logged: %.6f, diff = %.6f' % (code_to_send, senttime, heretime, heretime-senttime))
                        
                        self.expLogger.write('%.6f\t%.6f\t%d\n' % (senttime, heretime, code_to_send))
                        
                        
                        # heretime2=self.clock.getTime()
                        
                        # print('code: %d\t time sent: %.6f time logged: %.6f, diff = %.6f' % (code_to_send, senttime, heretime2, heretime2-senttime))
                        
                        # print('writing stuff took: %.3f msec' % ((heretime2-heretime)*1000));

                     
                # this is onlyt true if port needs to be reset, otherwise leave as-is.
                if self.sendParallel and self._port_doreset:
                    # check the time - 10msec passed?
                    if (self.clock.getTime() - lasttime) > self._port_waitttime:
                        self._port.setData(0)
                        self._port_doreset=False
                        

            # close it off
            if self.sendParallel:
                self._port.setData(0)                        

                
                

        def shutdown(self):
            ''' 
            get rid of this process -- call join later on from the main process
            '''
            # also - send triggers via our network connection towards
            self._shutdown.set()
    
    
    
    
    # initualize it + make it findable by all subfucntions
    eh=eventHandler(
            MSGDICT,
            mainClock, 
            destip='127.0.0.1', 
            destport=6050, 
            LPTAddress=0x0378,
            filename='log/triggerlog.log',
            sendParallel=True, 
            sendTcpIp=True, 
            sendLogFile=True
            )
    
    eh.start()
    
    
    G['eh']=eh

    
#                     messagedict,
#                     clock, 
#                     ip='127.0.0.1', 
#                     port=6500, 
#                     LPTAddress=0x0378,
#                     filename='log/triggerlog.log',
#                     sendParallel=True, 
#                     sendTcpIp=True, 
#                     sendLogFile=True



#%% ASYNC I - The GoNogo handler
#
    
    G['S']=dict()
    G['S']['STOP']=1
    G['S']['GO']=0
    G['S']['BUTTONS'] = BUTTONS 
    
    
    # this is a list which basically acts as a pointer. From within functions 
    # we can change this as needed.
    G['S']['continueRoutine']=False # Container=[False]
    G['S']['goNogoStim'] = [None] # Container=[None]
    # nextfliptasks=[]
    G['S']['tooSoonTime'] = tooSoonTime
    
        
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
    G['S']['myMultiStairs'] = data.MultiStairHandler(stairType='simple', method='random', conditions=conditions, nTrials=40)
    
    
    # Obtain the Go Nogo Timing Parameters
    # for stop-signal task: read in the critucal timings from one of my 500 
    # OPTIMAL GLM Design specifications:
    tmp_rand_number = random.randint(1,501)
    #with open('efl/param_%d.txt' % (tmp_rand_number )) as f:
    #    matrix=[[float(s) for s in re.findall(r'-?\d+\.?\d*', line)] for line in f]
    with open('efl/tmpFile.txt','rb') as f:
        matrix=pickle.load(f)
    
    
    SSnumber, SSstopgo, ISIwaitTime, tmp1, tmp2, LeftOrRight = zip(*matrix)
    
    G['S']['SSnumber']=SSnumber
    G['S']['SSstopgo']=SSstopgo
    G['S']['ISIwaitTime']=ISIwaitTime
    G['S']['LeftOrRight']=LeftOrRight
    
    
    
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
            
    G['S']['correctResponseSides']=correctResponseSides
    G['S']['wrongResponseSides']=wrongResponseSides
        
    
    
    G['S']['nextFlipTasks'] = []
    
    # handle the new clock..., so put the function handle into the struct too.
    G['S']['clock'] = None # Container=[None]
    def new_clock(x):
        x['S']['clock'] = clock.Clock()
        x['S']['continueRoutine'] = True
    G['S']['makeNewClock'] = new_clock
    
    
    
    

#    
    
    
    
    # decorate this function...    
    @asyncio.coroutine
    def handle_gonogo(GLOBS):
        '''
        This contains the experimenal logic of the Stop Task. A lot of work
        went into constructing the stimuli. Stimuli parameters are loaded
        into variables in the code above. Runs 136 trials of Go-Nogo.
        This function is to be run within the asyncio loop.
        '''
     
        
        # we just need it here...
        STOP=1
        GO=0
        
        tooSoonTime = G['S']['tooSoonTime']  
        
        myMultiStairs = G['S']['myMultiStairs']
    
        # if the time it took tov respond is smaller than this time --> invalid.
        numberOfResponses=0
        
        
        G['S']['nextFLipTasks']=[]  # stuff winflupper needs to do later on..
        G['S']['clock']=[None]

        # set the visual contents here...
        # INITIAL SETTING
        G['S']['goNogoStim']=G['vstims']['S']['fix']

  
    
        # yeah, do all kinds of init here.
        for trialNumber in range(len(G['S']['SSstopgo'])):
    
    
            
            
            thisDirection=random.choice(('al','ar')) # obtain this from the file!!
            LorR = thisDirection[1].upper()

            thisTrialType = G['S']['SSstopgo'][trialNumber] # this is a 0 (GO) or 1 (STOP)
            thisTrialType = [GO, STOP][int(thisTrialType)]  # shady practices indeed -- so later on I cany say 'if this TrialType is GO:, etc'
            GorNG = ['Go', 'Stop'][int(thisTrialType)]


            thisISIWaitTime = G['S']['ISIwaitTime'][trialNumber]
            
            correctResponseSide = G['S']['correctResponseSides'][trialNumber]
            wrongResponseSide = G['S']['wrongResponseSides'][trialNumber]
            

            
            allResponses=[] 
            responded=False # subj responded?
            tooManyResponses=False
            trialHandled=False
            
            
            
            if taskType is STOP:
                # this should be called only 40 times, since there are 40 stop trials...
                thisSSD, thisCondition = myMultiStairs.next() # I defined the myMultiStairs above.
            
    
    
            # this code tells the loop to only continue when continueTroutine is not False
            # otherwise it'll just keep yielding.
            # let winflipper make new clock
            G['S']['continueRoutine']=False
            G['S']['nextFlipTasks'].append([G['S']['makeNewClock'], G]) # the makeNewClock automatically makes things continue
            while G['S']['continueRoutine'] is False:
                yield From(asyncio.sleep(0))
            cl=G['S']['clock'] # obtain the clock that was just made.
    
    
            # ok, we can proceed -- the clock has been set.
            G['S']['goNogoStim']=G['vstims']['S']['pre']
            while cl.getTime() < 0.5:
                yield From(asyncio.sleep(0))
        
        



        
            # obtain our next clock...
            # this code tells the loop to only continue when continueTroutine is not False
            # otherwise it'll just keep yielding.
            # let winflipper make new clock
            G['S']['continueRoutine']=False
            
            # make sure upon next window flow, we have a new clock set, and also - that marker is sent signalling the start of the new go/stop trial.
            G['S']['nextFlipTasks'].append([G['S']['makeNewClock'], G]) # the makeNewClock automatically makes things continue
            # send the trigger regarding the arrow, as soon as the windows flips
            G['S']['nextFlipTasks'].append([G['eh'].send_message, 
                                  ['Begin'+GorNG+LorR])
            while G['S']['continueRoutine'] is False:
                yield From(asyncio.sleep(0))
            cl=G['S']['clock'] # obtain the clock that was just made.
            
    
            # this is where we show the arrow + find out whether a key is pressed:
            G['S']['goNogoStim']=G['vstims']['S'][thisDirection]
            currentTime = 0.0
            while currentTime < 1.0:
                currentTime = cl.getTime()
                
                # set the stimulus to the proper direction (it's a choice, for now... -- but it's much much better to hard-code it)
                # make the arrow (+ circle)
    
                evs=event.getKeys(timeStamped=cl)
                if len(evs)>0:
                    buttonsPressed, timesPressed = zip(*evs)
                    # it's highly unlikely that two buttons are pressed in a signle
                    # frame, but control for that anyway.
                    allResponses.append((buttonsPressed[0], timesPressed[0]))
                    numberOfResponses += 1
                    # LOG this event... (i.e. send trigger)
                    
                    # handle event:


                # once a button is pressed -- display fixation point again.
                if len(allResponses) > 0 and not responded:
                    # 'clear' the visual window --> fixation cross, again:
                    G['S']['goNogoStim']=G['vstims']['S']['fix']
                    responded=True
                    
                    buttonPressed, RTime = allResponses[0]
                    
                    if RTime < tooSoonTime:
                        G['ev'].send_message('PressedTooSoon')
                    else:
                        if buttonsPressed[0] == BUTTONS[0]:
                            G['ev'].send_message('RespL')
                        elif buttonsPressed[0] == BUTTONS[1]:
                            G['ev'].send_message('RespR')


        
        
                # if it's a stop trial, then make arrow red after X time
                if thisTrialType is STOP and not responded:
                    if currentTime > thisSSD:
                        G['S']['goNogoStim']=G['vstims']['S'][thisDirection+'r']
    
            
                # here we wait...
                yield From(asyncio.sleep(0))

            #            # Stop / Inhibit Response Codes
            #            'BeginGoL':1,
            #            'BeginGoR':2,
            #            'BeginStopL':3,
            #            'BeginStopR':4,
            #            
            #            'RespL':5,
            #            'RespR':6,
            #
            #            'CorrectGoL':11,
            #            'CorrectGoR':12,
            #            'CorrectStopL':13,
            #            'CorrectStopR':14,
            #            'ErrorCommission':15,
            #            
            #            # don't expect too many of these:
            #            'ErrorOmission':21,
            #            'PressedTooSoon':22,
            #            'TooManyResponses':23,
            #            'WrongSideErrorCommission':24,
            #            'WrongSideGo':25,

            # so the loop is done -- let's figure out what kind of trial this was.
            # taking care of the button press itself, as soon as button is pressed:
            if not trialHandled and responded:

                trialHandled=True

                if len(allResponses) > 1:
                    trialOutcome = 'TooManyResponses'
                    if trialType is STOP:
                        myMultiStairs.addResponse(0)

                else:
                    if RTime < tooSoonTime:
                        trialOutcome = 'PressedTooSoon'
                        if trialType is STOP:
                            myMultiStairs.addResponse(0)
                    else:
                        if thisTrialType is STOP:
                            
                            if buttonPressed == correctResponseSide:
                                trialOutcome = 'ErrorCommission'
                                myMultiStairs.addResponse(0)
        
                            elif buttonPressed == wrongResponseSide:
                                trialOutcome = 'WrongSideErrorCommission'
                                myMultiStairs.addResponse(0)
                                
                            
                        elif thisTrialType is GO:
                            if buttonPressed == correctResponseSide:
                                trialOutcome = 'CorrectGo'+correctResponseSide

                                # not yet...
                            elif buttonPressed == wrongResponseSide:
                                trialOutcome = 'WrongSideGo'


        
                        # handle the 'response' if the button was NOT pressed:
            if not trialHandled and not responded:
                trialHandled = True

                if trialType is GO:
                    trialOutcome = 'ErrorOmission'
    
                if trialType is STOP:
                    trialOutcome = 'CorrectStop'+LorR
                    myMultiStairs.addResponse(1)
                    
            # so we send it out:
            G['ev'].send_message(trialOutcome)
            

    
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
            # logging.data('messa')
            logging.flush()

    
             # ok, we can proceed -- the clock has been set.
            goNogoStimContainer=sstims['fix']
            while cl.getTime() < thisISIWaitTime:
                yield From(asyncio.sleep(0))
            


        # the stop task should be finished now!
        # the visual task should also be finished around the same time.
        # so further stuff, we can do with basic instructions, wait times, etc
            


#%% ASYNC V - Handle the Audio!

# the audio stim list:
# audio_stim_list = [[10.,20.,'audio',['left','40']],[112.5,130.,'audio',['left','40']],[242.5,260.,'audio',['left','40']],[50.,60.,'audio',['left','55']],[195.,205.,'audio',['left','55']],[312.5,330.,'audio',['left','55']],[30.,40.,'audio',['right','40']],[147.5,165.,'audio',['right','40']],[277.5,295.,'audio',['right','40']],[77.5,95.,'audio',['right','55']],[175.,185.,'audio',['right','55']],[215.,225.,'audio',['right','55']]]

# make a more usable stim list:
    audio_stim_list = [
            [10.0, 20.0, 'aud_l40'],
            [112.5, 130.0, 'aud_l40'],
            [242.5, 260.0, 'aud_l40'],
            [50.0, 60.0, 'aud_l55'],
            [195.0, 205.0, 'aud_l55'],
            [312.5, 330.0, 'aud_l55'],
            [30.0, 40.0, 'aud_r40'],
            [147.5, 165.0, 'aud_r40'],
            [277.5, 295.0, 'aud_r40'],
            [77.5, 95.0, 'aud_r55'],
            [175.0, 185.0, 'aud_r55'],
            [215.0, 225.0, 'aud_r55']
            ]
    
    # load in the audio's timings, defined in seconds, so that later on, one could
    # input triggers into the EEG (or optionally -- send out triggers with the event handler)        
    
    # 40 Hz:
    timings40Hz=np.loadtxt('stims/audio_40_ts.txt');
    # 50 Hz:
    timings55Hz=np.loadtxt('stims/audio_55_ts.txt')
    
    # see also the figure_out_audio_timings.m file to further play with the audio's
    # waveforms.
    
    
    snd40hzL = sound.backend_pygame.SoundPygame(value='stims/audio_40Hz_L.wav',loops=0)
    snd40hzR = sound.backend_pygame.SoundPygame(value='stims/audio_40Hz_R.wav',loops=0)
    snd55hzL = sound.backend_pygame.SoundPygame(value='stims/audio_55Hz_L.wav',loops=0)
    snd55hzR = sound.backend_pygame.SoundPygame(value='stims/audio_55Hz_R.wav',loops=0)
    
    
    astims={
            'aud_l40':snd40hzL,
            'aud_r40':snd40hzR,
            'aud_l55':snd55hzL,
            'aud_r55':snd55hzR
            }
    
    
    # put these into the variable, too...
    G['astims']=astims
    G['A']['audio_stim_list']=audio_stim_list
    G['A']['timings40Hz']=timings40Hz
    G['A']['timings55Hz']=timings5Hz
    
    
    @asyncio.coroutine
    def handle_audio(G):
        '''
        this should handle the audio stimuli, using the async programming style.
        it starts a new clock and depending on timings, will start some audio
        samples, L or R, 40 or 55 Hz.
        '''
        
        audioClock=clock.Clock()
        playing=False
        withinAudioBlock=False
        prevWithinAudioBlock=False
        RunAudio=True
        
        
        currentTime=audioClock.getTime()
        while currentTime < 340.: #currentTime < 340.:
            
            # print('hello')
            # print(currentTime)
            
            if not playing:     # I can safely use this since only one audio is playing at a time.
    
                withinAudioBlock=False
                
                for item in audio_stim_list:
                    b, e, stim = item
                    if b < currentTime < e:
                        currentStim = stim
                        withinAudioBlock=True
                        astims[stim].play()
                        playDuration=astims[stim].getDuration()
                        playing=True
                        playClock=clock.Clock()
                        
                        print(stim)
                        logging.data(stim)
                        # eh.send_message(stim)
    
                        
            else:
                if playClock.getTime() > playDuration:  # figure out if something is playing 
                    playing=False
    
                    
            # try dealing with begin and ending markers:                    
            if withinAudioBlock and not prevWithinAudioBlock:
                messg=currentStim.replace('_','_b')
                print(messg)
                logging.data(messg)
                # eh.send_message(stim)
                prevWithinAudioBlock=True
                
            elif prevWithinAudioBlock and not withinAudioBlock:
                messg=currentStim.replace('_','_e')
                print(messg)
                logging.data(messg)
                # eh.send_message(stim)
                prevWithinAudioBlock=False
                
            
            # this will stop this loop, probably:
            currentTime=audioClock.getTime()
            #if currentTime > 340.:
            #    print('Stopping!')
            #    RunAudio=False
            
            yield From(asyncio.sleep(0))  # pass control to someone else, while this guy sleeps a bit.
            



#%% ASYNC II - The Visual handler
## set up the functions to be used in the end for asyncing through the loops:
# load the vis table somewhere here - big mem space (.csv?)
    
    
    # Visual Helpers
    nextfliptasks=[]
    stimulusContents=[]
    
    def makeNewClock():
        clockContainer.append(clock.Clock())
        continueRoutineContainer[0]=True
    


    
    # load in the table that tells me all the stop signal stuff (.csv?)
    #% Frame-by-frame checkerboard List
    # load in the frame-list of the visual stimuli: i.e. saying when things should
    # be used:
    ASYNC_SLEEPTIME = 1/60.*0.75        
    
    
    with open('efl/fd.pkl','rb') as f:
        fd=pickle.load(f)
        
    
    with open('efl/complete_fd_list.pkl','rb') as f:
        complete_fd_list=pickle.load(f)
    
    #    with open('efl/fd_with_markers.pkl','rb') as f:
    #        fd_with_markers=pickle.load(f)
        
    with open('efl/fd_with_markers_II.pkl','rb') as f:
        fd_with_markers=pickle.load(f)
    
    
            
            
     
    
    
    
    @asyncio.coroutine
    def handle_visual():
        '''
        This flips the window, draws the stuff to be drawn, and calls
        functions to be called from the stop task. It is supposed to be
        run in the asyncio loop.
        '''
        
        # logging.console.setLevel(logging.DEBUG)
        mainClock=mainClockContainer[0]
        frameCounter=0
        previousShapes=[]
        mainCurrentTime=0
        totFrames=len(fd_with_markers)
    
        # visualClock=clock.Clock()
        # this will run the entire length of the visual...
        # within this time, the stop signal task will (hopefully) finish.
        # OR... we can also just use a counter.
        while frameCounter < totFrames:
        
        
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
            if goNogoStimContainer[0] is not None:
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
        

    

            
            
    

#%% ASYNC III - The Main Event Loop
            
    @asyncio.coroutine
    def test_it():
        cl=clock.Clock()
        # while cl.getTime() < 1: #i in range(1000):e
        runit=True
        while runit:
            print cl.getTime()
            yield From(asyncio.sleep(0))
        
            if cl.getTime() > 1:
                runit=False
            if cl.getTime() > 0.5:
                #pass
                print(1/0)
        
    
    @asyncio.coroutine
    def handle_exception(f, G, loop):
        print f
        print loop
        try:
            yield From(f(G))
        except Exception:
            # print debug information
            print('---------------')
            print('---------------')
            print('ERROR OCCURRED:')
            print(sys.exc_info()[1])
            traceback.print_tb(sys.exc_info()[2])
    
            pending = asyncio.Task.all_tasks()
            for task in pending:
                task.cancel()
                # Now we should await task to execute it's cancellation.
                # Cancelled task raises asyncio.CancelledError that we can suppress:
                #with suppress(asyncio.CancelledError):
                #    loop.run_until_complete(task)        
            loop.stop()  # stops the loop, gives an error for that, too.
    
    
    
    def run_main_loop(G):    
        '''
        This runs the stopingibition/visual/audio part of the paradigm using
        asyncio-replacement trollius. Before and after, we can still present
        other stimuli.
        '''
        
        
        # something like this:
        mainClock=clock.Clock()
        mainClockContainer[0]=mainClock # put it into my list, that double-serves
                                        # as a pointer
        
        
        
        loop=asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        #tasks = [
        #    asyncio.async(handleVisual()),
        #    asyncio.async(handleGonogo()),
        #    asyncio.async(handleEscape()),
        #    ]
        tasks_dbg = [
                asyncio.async(handle_exception(test_it,G,loop)),
                asyncio.async(handle_exception(handle_audio,G,loop)),
                asyncio.async(handle_exception(handle_visual,G,loop))
                #asyncio.async(handle_exception(handle_visual,loop)),
                #asyncio.async(handle_exception(handle_gonogo,loop))
                ]
        
        
        tasks = [
                asyncio.async(test_it(G)),
                asyncio.async(handle_audio(G))
                ]
        
        # so to debug, just run tasks_dbg instead of tasks.
        loop.run_until_complete(asyncio.wait(tasks_dbg))   
        loop.close()

    




#%% MAIN -- hope things work
    if __name__=="__main__":
        # do the stuff.
        run_main_loop()
    
        
        
        
        





#%% The Rest
#    @asyncio.coroutine
#    def handle_exception_test_it():
#        try:
#            yield From(test_it())
#        except Exception:
#            
#            #print(sys.last_type)
#            #traceback.print_tb(sys.last_traceback)
#            #print("exception consumed")
#            # print('hallo!')
#            # print(traceback)
#            print(sys.exc_info()[1])
#            traceback.print_tb(sys.exc_info()[2])
#            # etype, evalue, etraceback = sys.exec_info()
#            # traceback.format_exc()
#            # print(traceback.fortmat_exec(etraceback))
#            
#    @asyncio.coroutine
#    def handle_exception_handle_audio():
#        try:
#            yield From(handle_audio())
#        except Exception:
#            
#            #print(sys.last_type)
#            #traceback.print_tb(sys.last_traceback)
#            #print("exception consumed")
#            # print('hallo!')
#            # print(traceback)
#            print(sys.exc_info()[1])
#            traceback.print_tb(sys.exc_info()[2])
#            
#            # etype, evalue, etraceback = sys.exec_info()
#            # traceback.format_exc()
#            # print(traceback.fortmat_exec(etraceback))
#            
#            
#    # we debug by CHAINING coroutines. Very very clear, yes. But it's necessity for now.
#    # would be nice to enable this feature in a nicer way for someone like me.
        
        
        

#%% Getting Input

# see: http://easygui.sourceforge.net/tutorial.html#enterbox
# variable = easygui.enterbox('hello','title','text')



# OR -- use psychopy's functions:
# expName = 'loc_v1'  # from the Builder filename that created this script
# expInfo = {'participant':'', 'session':'001'}
# dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
#
# access via expInfo['participant'], etc.


#%% Gonogo Thoughts
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
        
        
#%% Starcase usage -- use the starcase to loop over the stop trials:
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
        
        
#%%

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
        
        
#