

# in * is also: from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
# visual, sound, core, data, event and logging are the crucial ones.

import random
import pickle
from psychopy import clock, event, data, logging

from FeedbackBase.MostBasicPsychopyFeedback import MostBasicPsychopyFeedback


# some helpers:
# from Feedbacks.EEGfMRILocalizer.efl import eventhandler
# from Feedbacks.EEGfMRILocalizer.efl import visualHelper

# the actual experiment:
# from Feedbacks.EEGfMRILocalizer.efl.efl_v11 import * # point to another (maybe more common) library - that I'll copy/paste later on from.

from Feedbacks.BrainWaveTraining_II.tools.create_incremental_filename import create_incremental_filename
from Feedbacks.BrainWaveTraining_II.tools.init_screen import init_screen
from Feedbacks.BrainWaveTraining_II.tools.init_eventcodes import init_eventcodes
from Feedbacks.BrainWaveTraining_II.tools.start_eh import start_eh

from Feedbacks.BrainWaveTraining_II.ingredients.stimuli_v2 import make_stimuli
from Feedbacks.BrainWaveTraining_II.ingredients.stimuli_v2 import init_programs
from Feedbacks.BrainWaveTraining_II.ingredients.stimuli_v2 import define_experiment
from Feedbacks.BrainWaveTraining_II.ingredients.stimuli_v2 import init_staircases_quest
from Feedbacks.BrainWaveTraining_II.ingredients.stimuli_v2 import init_staircases_steps



from Feedbacks.BrainWaveTraining_II.ingredients.stimuli_v2 import runTrial
from Feedbacks.BrainWaveTraining_II.ingredients.stimuli_v2 import flatten





# let's try using async to keep all things into the Main Thread.
import trollius as asyncio
from trollius import From
from Feedbacks.BrainWaveTraining_II.ingredients.stimuli_v2 import handle_exception_pr
from Feedbacks.BrainWaveTraining_II.ingredients.stimuli_v2 import handle_exception


# get the pause screen!
from Feedbacks.EEGfMRILocalizer.efl.efl_v11 import wait_for_key
# we use the Dirty Programming Method (*) to import all of psychopy's utlilities and tricks

# we need this additional line - this is how we import psychopy -- why we need to write this multiple times?
# "The downside of having to write a couple import statements per module does not outweigh the potential problems
# introduced by trying to get around writing them." (PEP20).


class BrainWaveTraining_II(MostBasicPsychopyFeedback):
    
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
        
        self.STARTKEYS=['return','t']           # handy for the fmri
        
        self.EX_THRLINEWIDTH = 2
        self.EX_COLORGAP = 1
        self.EX_TVSP = 0.4
        self.EX_TPAUSE = 0.5
        self.EX_NREGULATE = 30
        self.EX_NTRANSFER = 10
        
        self.EX_SHOWCHECKORCROSS = True
        self.EX_SHOWCHECKORCROSSTRANSFER = True
        self.EX_SHOWPOINTS = True
        
        self.EX_SQUARESIZE = 0.25
        self.EX_UPREGTEXT = 'regulate up'
        self.EX_TESTSIGNALUPDATEINTERVAL = 0.01
        self.EX_NREST = 10
        self.EX_SCALING = [0.75, 0.75]          # scaling for X and Y
        self.EX_INTERACTIONMODE = 'master'      # the stimulus does already quite a lot
        self.EX_NOBSERVE = 10
        self.EX_NOREGTEXT = 'do not regulate'
        self.EX_TINSTR = 2.0
        self.EX_THERMOCLIMS = ['c4572e', '4fc42e']
        self.EX_GRAPHICSMODE = 'line'
        self.EX_STAIRCASEMANIPULATION = 'offset'
        self.EX_POINTS_PENALTY = -2
        self.EX_TESTSIGNALPERIOD = 4
        self.EX_TMARK = 1.5
        self.EX_TESTNFNOISE = True
        self.EX_PATCHCOLOR = 'green'
        self.EX_TJITT = [0.8, 1.3]
        self.EX_TFB = 12.0
        self.EX_POINTS_REWARD = 10
        self.EX_PR_SLEEPTIME = 0.01
        self.EX_TESTSIGNALTYPE = 'sin'
        self.EX_BUTTONS = ['lctrl', 'rctrl']  # the button codes coming out of event.getStim()
        self.EX_INSTR = 'Upregulate: Focus on moving upwards / more green'    
        self.EX_RUNS = 5 # how many runs-of-6?
        self.EX_EV_IGNORE_KEYS = ['5','t']

        self.EX_SND_LOWESTTONE = 27
        self.EX_SND_HIGHESTTONE = 48
        self.EX_EMG_THERMOWIDTH = 0.075
        self.EX_EMG_THERMOHEIGHT = 0.2
        self.EX_EMG_THERMOEDGE = 0.05
        self.EX_TXT_COUNTER = [0]

        # so these are NOW control parameters:
        self.EX_TUNING_TYPE = 'thr'  # alternatives are 'linear', and maybe 'fancy'
        self.EX_TUNING_PARAMS = [1.0, 0.0]  # linear requires a slope and offset. - eill not be used if it's not 'linear'
        self.EX_WIN_CONDITION = 'time_above_thr'
        self.EX_WIN_PARAMS = [0.25]  # 25 % of the time, it needs to be above the threshold...
        self.EX_NUMBEROFSETS = 6  # how long (sets of 6) do we wish our experiment to have?? Determines also our staircases.
        self.EX_MIXOFSETS = {'train':3, 'transfer':1, 'observe':1, 'rest':1}
        self.EX_STAIRIDENTIFIER = '0001'  # needed to keep track of the staircases.
        self.EX_XorV_RESET_POINTS = False  # at the start of the day --> this should be True.
        
        
        
        self.LOG_PATHFILE='log/bwt.log'  # for if you want to change this...
        self.LOG_PATHFILE_EVENT='log/evsbwt.log'  # for if you want to change this...
                
        # take care of our monitor-screen-display...
        self.MONITOR_PIXWIDTH=1280
        self.MONITOR_PIXHEIGHT=1024
        self.MONITOR_WIDTH=40.  # width of screen
        self.MONITOR_HEIGHT=30.  # height of screen
        self.MONITOR_DISTANCE=70.  # distance to screen
        self.MONITOR_GAMMA=1.
        self.MONITOR_FPS=60.
        self.MONITOR_USEDEGS=True
        self.MONITOR_DEGS_WIDTHBASE=12
        self.MONITOR_DEGS_HEIGHTBASE=10
        self.MONITOR_FLIPHORIZONTAL = False
        self.MONITOR_FLIPVERTICAL = False
        self.MONITOR_RECORDFRAMEINTERVALS = True  # for debugging..        
        self.MONITOR_NSCREENS=2
        self.MONITOR_DISPLAYONSCREEN=1
        self.MONITOR_FULLSCR = False
        self.MONITOR_ALLOWGUI = False
        
        self.SND_LOWESTTONE = 27
        self.SND_HIGHESTTONE = 48

        # self.LOG_FILEBASE='efl'  # how to call our logfile --> it adds a number each time
        # self.IPADDRESS='localhost'  # port and ip to send codes towards to
        # self.PORT=6050  # which port is nice?  

        # self.tooSoonTime=0.0  # if it's pressed before this time --> discard + error


        
        self.EVENT_LPT_TRIGGER_WAIT=0.005  # how long are the LPT port pulses?        
        self.EVENT_destip='127.0.0.1'
        self.EVENT_destport=6050
        self.EVENT_LPTAddress=0x0378
        self.EVENT_LPTTrigWaitTime=0.005
        self.EVENT_TRIGLOG='log/triggerlog.log'
        self.EVENT_sendParallel=True
        self.EVENT_sendTcpIp=True
        self.EVENT_sendLogFile=True
        self.EVENT_printToTerminal=True
        self.EVENT_printToTerminalAllowed=[0, 255]  # only allow the stops, which are < 40.
        

        
        
        # Control Parameters
        CP=dict()
        CP['nfsignalContainer'] = [0]
        CP['thrContainer'] = [0.5]
        CP['TJITT'] = [1]
        CP['CURRENTPART'] = [None]
        CP['instruction'] = 'arrowup'  # choose between 'arrowup' and 'donotreg'
        CP['corr_incorr'] = [None]  # chooose between 'st_correct' and 'st_incorrect'
        CP['TUNING_TYPE'] = self.EX_TUNING_TYPE # ']  # copy/paste into CP, to be (changed) later during the experiment...
        CP['TUNING_PARAMS'] = self.EX_TUNING_PARAMS #']  # same here -- but, it is a list.
        CP['TrialType'] = [None]
        CP['WIN_CONDITION'] = self.EX_WIN_CONDITION
        CP['WIN_PARAMS'] = self.EX_WIN_PARAMS
        CP['EX_TXT_COUNTER'] = self.EX_TXT_COUNTER

        CP['hitError'] = []
        CP['hit'] = []
        CP['emgThrContainer'] = [None]
        CP['emgContainer'] = [None]

        self.CP = CP
        
        
        #        self.DO_VISUAL = True
        #        self.DO_AUDIO = True
        #        self.DO_GNG = True#
        #        self.GNGSPEED = 1.0
         #       self.GNG_ARROWGOESRED = True
         #       self.GNG_ARROWGOESRED_DELAY = 0.25
         #       self.AUDIOTONE_ERROR_COMMISSION = False
         #       self.AUDIOTONE_STOP = False
         #       self.VIS_SHOWOPPOSITE = False
         #       self.VIS_radialFreq=6
         #       self.VIS_angleFreq=6
         #       self.VIS_checkerSize=1.5
         #       self.VIS_checkerSpeedMultiplier=1.0
         #       self.EYESCLOSED_TIME=25.
        
        


        
        
        
        
        

    # this is called BEFORE the main experiment (i.e. before 'play')
    def pre_mainloop(self):
        
        MostBasicPsychopyFeedback.pre_mainloop(self)
        
        
        # do the trick -- SAVE all of those things! --> and put it in settings.pkl.
        v=dict()

        v['caption']                        = self.caption
        v['color']                          = self.color
        v['fontheight']                     = self.fontheight
        
        v['STARTKEYS']                      = self.STARTKEYS
        
        v['EX_THRLINEWIDTH']                = self.EX_THRLINEWIDTH
        v['EX_COLORGAP']                    = self.EX_COLORGAP
        v['EX_TVSP']                        = self.EX_TVSP
        v['EX_TPAUSE']                      = self.EX_TPAUSE
        v['EX_NREGULATE']                   = self.EX_NREGULATE
        v['EX_NTRANSFER']                   = self.EX_NTRANSFER
        
        v['EX_SHOWCHECKORCROSS']            = self.EX_SHOWCHECKORCROSS
        v['EX_SHOWCHECKORCROSSTRANSFER']    = self.EX_SHOWCHECKORCROSSTRANSFER
        v['EX_SHOWPOINTS']                  = self.EX_SHOWPOINTS

        v['EX_SQUARESIZE']                  = self.EX_SQUARESIZE
        v['EX_UPREGTEXT']                   = self.EX_UPREGTEXT
        v['EX_TESTSIGNALUPDATEINTERVAL']    = self.EX_TESTSIGNALUPDATEINTERVAL
        v['EX_NREST']                       = self.EX_NREST
        v['EX_SCALING']                     = self.EX_SCALING
        v['EX_INTERACTIONMODE']             = self.EX_INTERACTIONMODE
        v['EX_NOBSERVE']                    = self.EX_NOBSERVE
        v['EX_NOREGTEXT']                   = self.EX_NOREGTEXT
        v['EX_TINSTR']                      = self.EX_TINSTR
        v['EX_THERMOCLIMS']                 = self.EX_THERMOCLIMS
        v['EX_GRAPHICSMODE']                = self.EX_GRAPHICSMODE

        v['EX_STAIRCASEMANIPULATION']       = self.EX_STAIRCASEMANIPULATION
        v['EX_POINTS_PENALTY']              = self.EX_POINTS_PENALTY
        v['EX_TESTSIGNALPERIOD']            = self.EX_TESTSIGNALPERIOD
        v['EX_TMARK']                       = self.EX_TMARK
        v['EX_TESTNFNOISE']                 = self.EX_TESTNFNOISE
        v['EX_PATCHCOLOR']                  = self.EX_PATCHCOLOR
        v['EX_TJITT']                       = self.EX_TJITT
        v['EX_TFB']                         = self.EX_TFB
        v['EX_POINTS_REWARD']               = self.EX_POINTS_REWARD
        v['EX_PR_SLEEPTIME']                = self.EX_PR_SLEEPTIME
        v['EX_TESTSIGNALTYPE']              = self.EX_TESTSIGNALTYPE
        v['EX_BUTTONS']                     = self.EX_BUTTONS
        v['EX_INSTR']                       = self.EX_INSTR
        v['EX_RUNS']                        = self.EX_RUNS


        v['EX_SND_LOWESTTONE']              = self.EX_SND_LOWESTTONE
        v['EX_SND_HIGHESTTONE']             = self.EX_SND_HIGHESTTONE

        v['EX_EMG_THERMOWIDTH']             = self.EX_EMG_THERMOWIDTH
        v['EX_EMG_THERMOHEIGHT']            = self.EX_EMG_THERMOHEIGHT
        v['EX_EMG_THERMOEDGE']              = self.EX_EMG_THERMOEDGE

        v['EX_TXT_COUNTER']                 = self.EX_TXT_COUNTER



        v['MONITOR_PIXWIDTH']               = self.MONITOR_PIXWIDTH
        v['MONITOR_PIXHEIGHT']              = self.MONITOR_PIXHEIGHT
        v['MONITOR_WIDTH']                  = self.MONITOR_WIDTH
        v['MONITOR_HEIGHT']                 = self.MONITOR_HEIGHT
        v['MONITOR_DISTANCE']               = self.MONITOR_DISTANCE
        v['MONITOR_GAMMA']                  = self.MONITOR_GAMMA
        v['MONITOR_FPS']                    = self.MONITOR_FPS
        v['MONITOR_USEDEGS']                = self.MONITOR_USEDEGS
        v['MONITOR_DEGS_WIDTHBASE']         = self.MONITOR_DEGS_WIDTHBASE
        v['MONITOR_DEGS_HEIGHTBASE']        = self.MONITOR_DEGS_HEIGHTBASE
        v['MONITOR_FLIPHORIZONTAL']         = self.MONITOR_FLIPHORIZONTAL
        v['MONITOR_FLIPVERTICAL']           = self.MONITOR_FLIPVERTICAL
        v['MONITOR_RECORDFRAMEINTERVALS']   = self.MONITOR_RECORDFRAMEINTERVALS
        v['MONITOR_NSCREENS']               = self.MONITOR_NSCREENS
        v['MONITOR_DISPLAYONSCREEN']        = self.MONITOR_DISPLAYONSCREEN
        v['MONITOR_FULLSCR']                = self.MONITOR_FULLSCR
        v['MONITOR_ALLOWGUI']               = self.MONITOR_ALLOWGUI

        v['LOG_PATHFILE']                   = self.LOG_PATHFILE
        v['LOG_PATHFILE_EVENT']             = self.LOG_PATHFILE_EVENT

        v['EVENT_LPT_TRIGGER_WAIT']         = self.EVENT_LPT_TRIGGER_WAIT
        v['EVENT_destip']                   = self.EVENT_destip
        v['EVENT_destport']                 = self.EVENT_destport
        v['EVENT_LPTAddress']               = self.EVENT_LPTAddress
        v['EVENT_LPTTrigWaitTime']          = self.EVENT_LPTTrigWaitTime
        v['EVENT_TRIGLOG']                  = self.EVENT_TRIGLOG
        v['EVENT_sendParallel']             = self.EVENT_sendParallel
        v['EVENT_sendTcpIp']                = self.EVENT_sendTcpIp
        v['EVENT_sendLogFile']              = self.EVENT_sendLogFile
        v['EVENT_printToTerminal']          = self.EVENT_printToTerminal
        v['EVENT_printToTerminalAllowed']   = self.EVENT_printToTerminalAllowed
        

        
                # so these are NOW control parameters:
        v['EX_TUNING_TYPE']                 = self.EX_TUNING_TYPE # = 'thr'  # alternatives are 'linear', and maybe 'fancy'
        v['EX_TUNING_PARAMS']               = self.EX_TUNING_PARAMS # = [1.0, 0.0]  # linear requires a slope and offset. - eill not be used if it's not 'linear'
        v['EX_WIN_CONDITION']               = self.EX_WIN_CONDITION # = 'time_above_thr'
        v['EX_WIN_PARAMS']                  = self.EX_WIN_PARAMS # = [0.25]  # 25 % of the time, it needs to be above the threshold...
        v['EX_NUMBEROFSETS']                = self.EX_NUMBEROFSETS # = 6  # how long (sets of 6) do we wish our experiment to have?? Determines also our staircases.
        v['EX_MIXOFSETS']                   = self.EX_MIXOFSETS # = {'train':3, 'transfer':1, 'observe':1, 'rest':1}
        v['EX_STAIRIDENTIFIER']             = self.EX_STAIRIDENTIFIER # = '0001'  # needed to keep track of the staircases.
        v['EX_XorV_RESET_POINTS']           = self.EX_XorV_RESET_POINTS # = False  # at the start of the day --> this should be True.



        # use the Cpntrol Parameters:
        CP=self.CP # control parameters...

        # create G, put it into self too..
        G=dict()
        G['v']=v
        self.G = G
        
        
        # we need this in order to continue working as if we're doing it using the normal (test) script...
        for key in G['v']:
            G[key]=G['v'][key] # this is actually superfluous. But removing it might possibly break things.
            
        
        
        # the main clock
        mainClock=clock.Clock()
        G['mainClock']=mainClock
        

        # screen/monitor...
        G=init_screen(G)  # we need to do this


        # logging...
        logging.setDefaultClock(G['mainClock'])
        newLogFile = create_incremental_filename(G['v']['LOG_PATHFILE'])
        expLogger = logging.LogFile(newLogFile, logging.EXP) # the correct loglevel should be EXP!
        print(expLogger)
        logging.LogFile(newLogFile, logging.EXP) # the correct loglevel should be EXP!
        print('made new logfile: ' + newLogFile)
        for key in G['v'].keys():
            logging.data("{key}: {value}".format(key=key, value=G['v'][key]))
        logging.flush()
        G['logging']=logging  # put into the G, which is in self
        
        # event handler...
        G=init_eventcodes(G)  # and this??
        G=start_eh(G)

        init_staircases_quest(G)
        st=make_stimuli(G, CP)
        pr=init_programs(G, st, CP)

        ex=define_experiment(G, st, pr, CP)  # pr is passed to define_experiment, but then we won't need...
    
        
        self.st=st
        self.ex=ex
      
        
        # take care of the randomization(s)...
        trialopts=[]
        
        trialopts.append([1,1,2,1,3,4])
        trialopts.append([1,1,2,1,4,3])
        trialopts.append([1,1,2,3,1,4])
        trialopts.append([1,1,2,4,1,3])
        trialopts.append([1,1,3,1,2,4])
        trialopts.append([1,1,3,1,4,2])
        trialopts.append([1,1,3,2,1,4])
        trialopts.append([1,1,3,4,1,2])
        trialopts.append([1,1,4,1,3,2])
        trialopts.append([1,1,4,1,2,3])
        trialopts.append([1,1,4,3,1,2])
        trialopts.append([1,1,4,2,1,3])
        trialopts.append([1,2,1,4,1,3])
        trialopts.append([1,2,1,3,1,4])
        trialopts.append([1,3,1,4,1,2])
        trialopts.append([1,3,1,2,1,4])
        trialopts.append([1,4,1,2,1,3])
        trialopts.append([1,4,1,3,1,2])
        
        random.shuffle(trialopts)
        random.shuffle(trialopts)
        random.shuffle(trialopts)   # 3 time shuffle, for good luck :-)
                                    # computational anathema and heretic!
        
        my_trial_sequence = flatten(trialopts[0:G['v']['EX_RUNS']])  # we do 5 of them.
        my_trial_definitions = {1:'train', 2:'transfer', 3:'observe', 4:'rest'}
        
        # so to debug, just run tasks_dbg instead of tasks.
        for t_i in my_trial_sequence:
                self.runlist = iter([my_trial_definitions[i] for i in my_trial_sequence])
    
        
        # the ev loop we're going to be using..
        loop=asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.loop=loop
        
        
        if G['EX_TESTNFNOISE'] is True:
            self.loop.create_task(pr['GenTestSignal'](G, st, CP))

        logging.flush()
        G['logging']=logging
        
        G['cl']=clock.Clock()   # init the trial-by-trial clock here and put into G...
        
        
        

    # this is called AFTER main loop...
    def post_mainloop(self):
        MostBasicPsychopyFeedback.post_mainloop(self)
        
        self.G['eh'].shutdown()
        self.G['eh'].join()
        self.G['logging'].flush()
        self.G['win'].close()


        # save the staircases:
        staircases = self.G['staircases']
        staircase_file_name_to_save = self.G['file_to_check']
        
        print('saving staircases in: %s' % staircase_file_name_to_save)
        with open(staircase_file_name_to_save,'wb') as f:
            pickle.dump(staircases, f)
        print('saving done');

    # this always gets called, even paused.. -- UNTIL self.on_stop() is called. this will exit the main loop.
    # a 'tick' == ONE passage through the main loop (which is a 'while True' loop, basically...)
    
    # since tick will be called repeatedly, this is fine.
    def tick(self):

        # getting in the variables:
        G=self.G
        ex=self.ex
        st=self.st
        CP=self.CP
        loop=self.loop
        # from efl.efl_v6 import *
        # put everything here, which is in from __name__ == "__main__"
        # so this is one 'tick', but that's OK - one tick is all we need from pyff.
        # print(st['st_correct'].pos)
        # print(st['st_incorrect'].pos)

        try:
            
            trialType=self.runlist.next()
            print(trialType)
            print(CP['TJITT'][0])
            # trialType, G, st, CP, ex, loop
            self.loop.run_until_complete(asyncio.wait([asyncio.async(handle_exception(runTrial,trialType, G, st, CP, ex, loop))]))   
            
            G['logging'].flush()
            
            
        except StopIteration:
            # stop the experiment when the iterable is ready.
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
        print('I Resumed Play!')
        # probably, play and pause don't do anything.. right?
        pass
    
    # this gets called ONLY -- while on pause mode
    def pause_tick(self):
        print('paused!')
        wait_for_key(self.G)  # so, call self.G
        
        # I could here put up a screen asking to press 'play', from EFL?
        
        
        
        # pass
    
    # one could define several other tick methods for different kinds of behaviours.
    
    
    # this function WILL get called whenever I send over a 'control' event -- which is..
    # f.e. the NF data (whatever variable it is!)
    def on_control_event(self, data):
        #self.logger.debug("on_control_event: %s" % str(data))
        #self.NFPos = data["data"]
        # but we can change properties of the data --> so can draw stff!
        
        for key in data.keys():
            self.CP[key] = data[key]
            if key == 'nfsignalContainer':
                self.G['eh'].send_message('recv_nfsignal')
            elif key == 'corr_incorr:':
                self.G['eh'].send_message('recv_thr')
            elif key == 'thrContainer':
                self.G['eh'].send_message('recv_corr_incorr')

        
        #CP['nfsignalContainer'] = [0]
        #CP['thrContainer'] = [0.5]
        #CP['TJITT'] = [1]
        #CP['CURRENTPART'] = [None]
        #CP['instruction'] = 'arrowup'  # choose between 'arrowup' and 'donotreg'
        #CP['corr_incorr'] = 'st_incorrect'  # chooose between 'st_correct' and 'st_incorrect'        
        

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
