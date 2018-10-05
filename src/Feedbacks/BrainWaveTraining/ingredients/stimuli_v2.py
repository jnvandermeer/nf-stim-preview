# -*- coding: utf-8 -*-






# 
#VIS_SCALING = X, X
#VIS_DEGREES = ...
# if you specify the win as 'deg' monitor, then all the sizes will become degrees ... so you can set/rescale..






#%% imports
# getting the window right:

import inspect, os
import sys
import traceback


from psychopy import visual, clock, data
import numpy as np
import random
import threading
import time
import copy
import re


# let's try using async to keep all things into the Main Thread.
import trollius as asyncio
from trollius import From

if __name__ == "__main__":
    from create_incremental_filename import create_incremental_filename
else:
    from Feedbacks.BrainWaveTraining.tools.create_incremental_filename import create_incremental_filename    



#%% He[per functions
def flatten(lst):
    new_lst = []
    flatten_helper(lst, new_lst)
    return new_lst
 
def flatten_helper(lst, new_lst):
    for element in lst:
        if isinstance(element, list):
            flatten_helper(element, new_lst)
        else:
            new_lst.append(element)




#%% Variables
G=dict()


G['EX_TINSTR']  = 2.0
G['EX_TPAUSE']  = 0.5
G['EX_TFB']     = 12.0     # we'd wish to have the subjects look long at this, right?
G['EX_TVSP']    = 0.4
G['EX_TMARK']   = 1.5
G['EX_TJITT']   = [0.8, 1.3]


G['EX_TESTNFNOISE'] = True  # for checkign whether everything works...
G['EX_TESTSIGNALTYPE'] = 'sin'  # or random
G['EX_TESTSIGNALPERIOD'] = 4  # seconds
G['EX_TESTSIGNALUPDATEINTERVAL'] = 0.05   # make sure it's not the same.

G['EX_GRAPHICSMODE'] = 'line'  # what kind of stimulus?
G['EX_INTERACTIONMODE'] = 'master'  # now it will calculate succes and failure itself based on passed-on parameters in G
                                 # also, it will listen to what kind of trial needs to be run depending on what's passed on.
                                 # slave will be that it's dependent on the signals coming in from the Master Computer.



G['EX_UPREGTEXT'] = 'regulate up'
G['EX_NOREGTEXT']= 'do not regulate'
G['EX_POINTS_REWARD'] = 10
G['EX_POINTS_PENALTY'] = -2
G['EX_STAIRCASEMANIPULATION'] = 'offset'


G['EX_NREST']=10
G['EX_NOBSERVE']=10
G['EX_NREGULATE']=30
G['EX_NTRANSFER']=10
G['EX_SCALING']=[0.75, 0.75]
G['EX_PATCHCOLOR']='green'

G['EX_SHOWCHECKORCROSS'] = True
G['EX_SHOWCHECKORCROSSTRANSFER'] = True

G['EX_SQUARESIZE'] = 0.25 # in case we have the square NF...

G['EX_THRLINEWIDTH']=2
G['EX_THERMOCLIMS']=['c4572e', '4fc42e']  # in hex format

G['EX_COLORGAP'] = 1  # the gap between colors when thr is passed. -- uses the colorcalculator


G['EX_PR_SLEEPTIME'] = 0.01 # 0.01  # how long do we 'sleep' in our main program threads? (screen update is ~0.0016 seconds)


# so these are NOW control parameters:
G['EX_TUNING_TYPE'] = 'thr'  # alternatives are 'linear', and maybe 'fancy'
G['EX_TUNING_PARAMS'] = [0.5, 0.0]  # linear requires a slope and offset. - eill not be used if it's not 'linear'
G['EX_WIN_CONDITION'] = 'time_above_thr'
G['EX_WIN_PARAMS'] = [0.25]  # 25 % of the time, it needs to be above the threshold...

G['EX_NUMBEROFSETS'] = 6  # how long (sets of 6) do we wish our experiment to have?? Determines also our staircases.
G['EX_MIXOFSETS'] = {'train':3, 'transfer':1, 'observe':1, 'rest':1}
G['EX_STAIRIDENTIFIER'] = '0001'  # needed to keep track of the staircases.
G['EX_XorV_RESET_POINTS'] = False  # at the start of the day --> this should be True.


G['MONITOR_PIXWIDTH']=1280
G['MONITOR_PIXHEIGHT']=1024
G['MONITOR_WIDTH']=40.  # width of screen
G['MONITOR_HEIGHT']=30.  # height of screen
G['MONITOR_DISTANCE']=70.  # distance to screen
G['MONITOR_GAMMA']=1.
G['MONITOR_FPS']=60.
G['MONITOR_USEDEGS']=False
G['MONITOR_DEGS_WIDTHBASE']=12
G['MONITOR_DEGS_HEIGHTBASE']=10
G['MONITOR_FLIPHORIZONTAL'] = False
G['MONITOR_FLIPVERTICAL'] = False
G['MONITOR_RECORDFRAMEINTERVALS'] = True  # for debugging..        
G['MONITOR_NSCREENS']=2
G['MONITOR_DISPLAYONSCREEN']=1
G['MONITOR_FULLSCR'] = False
G['MONITOR_ALLOWGUI'] = False




# control parameters for the NF Experiment, things that change due to programs or fcalls, etc.
CP=dict()
CP['nfsignalContainer'] = [0]
CP['thrContainer'] = [0.5]
CP['TJITT'] = [1]
CP['CURRENTPART'] = [None]
CP['instruction'] = 'arrowup'  # choose between 'arrowup' and 'donotreg'
CP['corr_incorr'] = [None]  # chooose between 'st_correct' and 'st_incorrect'
CP['TUNING_TYPE'] = G['EX_TUNING_TYPE']  # copy/paste into CP, to be (changed) later during the experiment...
CP['TUNING_PARAMS'] = G['EX_TUNING_PARAMS']  # same here -- but, it is a list.
CP['TrialType'] = [None]
CP['WIN_CONDITION'] = G['EX_WIN_CONDITION']
CP['WIN_PARAMS'] = G['EX_WIN_PARAMS'] 




#%%  getting the window

def init_window(G):
    win=visual.Window(size=(1400,900), fullscr=False, screen=0, allowGUI=True, winType='pyglet', waitBlanking=False)
    G['win']=win


#%% Generate the stimuli

def make_stimuli(G, CP):
    win=G['win']
    

    
    # accomodate degrees, also, when we wish to use degrees:
    # take into account when making stimuli
    if G['MONITOR_USEDEGS'] is True:
        
        
        f_x = G['MONITOR_DEGS_WIDTHBASE']
        f_y = G['MONITOR_DEGS_HEIGHTBASE']
        
        G['EX_SCALING'][0] = f_x
        G['EX_SCALING'][1] = f_y
           
        
        G['f_x'] = f_x
        G['f_y'] = f_y


    SCALING=G['EX_SCALING']
    # print(SCALING)
    
    # another essential -- making sure we can load in the stimuli from wherever this file is located:
    currfile=inspect.getfile(inspect.currentframe()) # script filename (usually with path)
    currpath=os.path.dirname(os.path.abspath(currfile)) # script directory
    print(currfile)
    print(currpath)
    
    
    # making the dashed line -- for the stimulus, we can set autodraw optially to true for this one.
    def make_dashed(win, G, b, e, N, d):
        lines=[]
        b=(float(b[0]),float(b[1]))
        e=(float(e[0]),float(e[1]))
        # diff=(e[0]-b[0], e[1]-b[1])
        # print(diff/float(N)*d)
        # scaling:
        if b[0]==e[0]:
            scalingx=0
        else:
            scalingx = (e[0]-b[0]) / (e[0] - (e[0]-b[0])/float(N)*(1-d) - b[0])
        if b[1]==e[1]:
            scalingy=0
        else:
            scalingy = (e[1]-b[1]) / (e[1] - (e[1]-b[1])/float(N)*(1-d) - b[1])
    
            
        for i in range(N):
            #print('i='+str(i))
            #print(N)
            #print(float(1+i))
            xposb = b[0] + (e[0]-b[0])/float(N)*float(i)*scalingx
            yposb = b[1] + (e[1]-b[1])/float(N)*float(i)*scalingy
            xpose = xposb + (e[0]-b[0])/float(N)*d*scalingx
            ypose = yposb + (e[1]-b[1])/float(N)*d*scalingy
    
            #xpose = xposb+0.1
            # ypose = yposb+0.1
            # print([xposb, yposb, xpose, ypose])
            
            lines.append(visual.Line(win, start=(xposb, yposb), end=(xpose, ypose), lineWidth=G['EX_THRLINEWIDTH']))

            
        return lines
            
    # the dotted line:
    lines=make_dashed(win, G, (-1, 0), (1, 0), 20, 0.5)
    for l in lines:
        l.setWidth=G['EX_THRLINEWIDTH']

    
    # background
    background=visual.Rect(win, width=2, height=2,fillColor=[-0.1,-0.1,-0.1],lineWidth=0)
    
    # arrow up
    stimSize=0.25
    arrowPinch=1.75;
    arrowVert = [(-0.7071, -0.7071/arrowPinch), (0, -0.7071/arrowPinch),
                  (0, -1), (1, 0),
                  (0, 1),(0, 0.7071/arrowPinch), 
                  (-0.7071, 0.7071/arrowPinch)]
    arrowup = visual.ShapeStim(win, vertices=arrowVert, fillColor='white', 
                                 size=stimSize, ori=-90, lineColor='white', autoLog=False)
    
    # feedback 'cross' (blue)
    fa=.1;fb=1
    cfbVert = [(fa, fa),(fa, fb),(-fa, fb),(-fa, fa),(-fb, fa),(-fb, -fa),
                        (-fa, -fa),(-fa, -fb),(fa, -fb),(fa, -fa),(fb, -fa), (fb, fa)]
    cfb = visual.ShapeStim(win, vertices=cfbVert, fillColor='lightblue', 
                                 size=stimSize/7.5, ori=45, lineColor='blue', autoLog=False)
    
    # do-not-regulate arrow
    fa=0.25;fb=1
    donotregVert = [(fa, fa),(fa, fb),(-fa, fb),(-fa, fa),(-fb, fa),(-fb, -fa),
                        (-fa, -fa),(-fa, -fb),(fa, -fb),(fa, -fa),(fb, -fa), (fb, fa)]
    donotreg = visual.ShapeStim(win, vertices=donotregVert, fillColor='white', 
                                 size=stimSize, ori=45, lineColor='white', autoLog=False)
    
    
    # this emulates a NF trace...
    # import random
    
    ypos=[0.6+random.random()*0.2 for i in range(100)]
    times=[1+random.random()/4 for i in range(100)]
    tpos=[sum(times[:-i-1:-1]) for i in range(len(times))]
    
    tpos_max = max(tpos)
    xpos = [-1 + 2*t/tpos_max for t in tpos]
    
    nf_vertices = []
    for i, t in enumerate(ypos):
        nf_vertices.append((xpos[i], ypos[i]))
    
    nf_line = visual.ShapeStim(win, vertices=nf_vertices, closeShape=False, lineColor='lightblue')
    
    
    
    # might need alteration(s) here..
    # the vertices for 'correct':
    vert_correct=np.loadtxt(os.path.join(currpath, 'stim/vert_correct.txt'))
    st_correct_color='#5fd35f'
    st_correct = visual.ShapeStim(win, vertices=vert_correct, closeShape=True, size=stimSize, fillColor=st_correct_color, lineWidth =0, autoLog=False)
    
    vert_incorrect=np.loadtxt(os.path.join(currpath,'stim/vert_incorrect.txt'))
    st_incorrect_color='#e01000';
    st_incorrect = visual.ShapeStim(win, vertices=vert_incorrect, closeShape=True, size=stimSize, fillColor=st_incorrect_color, lineWidth =0, autoLog=False)
    
    st_txt_upregulate = visual.TextStim(win, text=G['EX_UPREGTEXT'],units='norm')
    st_txt_noregulate = visual.TextStim(win, text=G['EX_NOREGTEXT'],units='norm')  # we won't be scaling these
    
    
    
    items=[background, st_correct, st_incorrect, arrowup, donotreg, nf_line]
    for l in lines:
        items.append(l)
    items.append(cfb)
    
    
    # apply OUR scaling:
    for i in items:
        oldsize=i.size
        i.setSize((oldsize[0]*SCALING[0], oldsize[1]*SCALING[1]))



    # all stimuli (see above)
    st=dict()
    st['background'] = background
    st['st_correct'] = st_correct
    st['st_incorrect'] = st_incorrect
    st['arrowup'] = arrowup
    st['donotreg'] = donotreg
    st['nf_line'] = [nf_line]   # this is a complex shape.. changing all thetime
    st['cfb'] = cfb
    st['thrline'] = lines
    st['patches'] = []   # this will grow throoughout the experiment -- these are 'patches'...
    st['st_txt_upregulate']=st_txt_upregulate
    st['st_txt_noregulate']=st_txt_noregulate


    # set these for now, since we use these later on. Use control parameters to choose which one.
    st['instruction'] =  st[CP['instruction']]
    #st['corr_incorr'] =  st[CP['corr_incorr']]


    #
    #
    # Now, let us choose our second type of experiment -- using the (very basic) thermometer.
    #
    #

    
    thermo_lines=make_dashed(win, G, (-0.6, CP['thrContainer'][0]*G['EX_SCALING'][1]), (0.6, CP['thrContainer'][0]*G['EX_SCALING'][1]), 15, 0.5)
    
    
    thermo_thermometer = thermo_thermometer=visual.ShapeStim(win, lineWidth=1.5, lineColor='white', fillColor='green', vertices=[(-0.25, -1), (-0.25, 1), (0.25, 1), (0.25, -1)])
    thermo_thermometer_silent = visual.ShapeStim(win, lineWidth=1.5, lineColor='white', fillColor='grey', vertices=[(-0.25, -1), (-0.25, CP['thrContainer'][0]), (0.25, CP['thrContainer'][0]), (0.25, -1)])
    
    items=[thermo_thermometer, thermo_thermometer_silent] #, thermo_thermometer_silent]
    for l in thermo_lines:
        items.append(l)
    
    # scale it:
    for i in items:
        oldsize=i.size
        i.setSize((oldsize[0]*SCALING[0], oldsize[1]*SCALING[1]))   # this will already scale the lines!! So even if you (re-set) the start and stop, things are fine.
                                                                    # this is, indeed, supremely confusing!!! .. but naja.

    
    st['thermo_lines'] = thermo_lines
    st['thermo_thermometer'] = [thermo_thermometer]  # so we re-create for each instance
    st['thermo_thermometer_silent']= [thermo_thermometer_silent]


    #
    #
    # Now, let us choose our THIRD type of experiment -- using the (very basic) thermometer.
    #
    #

    square=visual.Rect(G['win'], width=G['EX_SQUARESIZE'], height=G['EX_SQUARESIZE'], fillColor=[-0.1,-0.1,-0.1], lineColor=[-0.1,-0.1,-0.1])
    square_silent = visual.Rect(G['win'], width=G['EX_SQUARESIZE'], height=G['EX_SQUARESIZE'], fillColor='grey', lineColor='black')
    
    if G['win'].units == 'norm':
        square_focus = visual.Rect(G['win'], width=G['EX_SQUARESIZE']/10. * G['win'].size[1] / float(G['win'].size[0]), height=G['EX_SQUARESIZE']/10., fillColor='black', lineWidth=0)
    else:
        square_focus = visual.Rect(G['win'], width=G['EX_SQUARESIZE']/10., height=G['EX_SQUARESIZE']/10., fillColor='black', lineWidth=0)
        
    
    
    # scale them, too...
    items=[square, square_silent,square_focus] #, thermo_thermometer_silent]
    # scale it:
    for i in items:
        oldsize=i.size
        i.setSize((oldsize[0]*SCALING[0], oldsize[1]*SCALING[1])) 
    

    # assign them...
    st['square']=square
    st['square_silent']=square_silent
    st['square_focus']=square_focus
    
    
    
    

    
    return st


#%% TUNING AND WINNING
    



def calculate_total_points(G):
    
    # think of a way to calculate the total # of points.
    # perhaps, we add in the transfer list, too.
    

    
    EX_POINTS_REWARD = G['EX_POINTS_REWARD']  #= 10
    EX_POINTS_PENALTY = G['EX_POINTS_PENALTY']  #= -2
    pass


    # use this to figure out total points...:
    if G['EX_SHOWCHECKORCROSSTRANSFER']:
        pass

    responses_train = G['staircases']['train'].otherData['list_up_till_now'][-1]
    responses_transfer = G['staircases']['transfer'].otherData['list_up_till_now'][-1]


    return 0



def tuning(CP, y):
    """ This function returns a tuned version of the input value, according to
    what is defined in the G(lobal) variable setup
    There should be a 'tuning type' and a 'tuning intensity'
    """
    
    # these can be set, too, by the BCI system, using control parameters...
    tuningType = CP['TUNING_TYPE']
    tuningParams = CP['TUNING_PARAMS']
    
    
    # if nothing matches -- just return y.
    yn = y
    
    
    if tuningType == 'linear':
        
        slope = tuningParams[0]
        offset = tuningParams[1]
        
        yn = y * slope + offset
    
    if tuningType == 'fancy':
        raise NotImplementedError


    #if tuningType == 'threshold':


    
    return yn




def check_win_condition(CP, times, ydata, thrdata):
    """ this function check whether you did well on a trial, as defined...
    with the CP (control parameters)
    
    There IS a smoothness assumption here. Things should go slower than:
        - EX_PR_SLEEPTIME
        - FPS of the Monitor
        progably at least twice as slow.
        
    If that's the case (likely, but if unattended could cause some bugs)
    then we can safely ignore the fact that some points are valued more than
    other points (since they are not evenly temporally spaced)
    .. for the purposes of whether things are above the THR
    .. and also for purposes of calculating an area-above-the-threshold
    """
    
    if len(times) != len(ydata):
        raise Exception('times is not equal in length to ydata : something went wrong in check_win_condition')
        
        
    winCondition = CP['WIN_CONDITION']
    winConditionParams = CP['WIN_PARAMS']
    
    # so we are NOT going to change the thr during the experiment.. or are we?
    # in case we do: we need another list of thr values, too.
    
    
    
    outcome = False
    outcomebool = 0
    
    if winCondition == 'time_above_thr':
        totTime = max(times) - min(times)
        
        fraction_above = winConditionParams[0]
        
        
        tot_time_above = 0.0
        for i, val in enumerate(ydata):
            if i == 0:
                pass  # do nothing here
            else:
                currtime = times[i]
                prevtime = times[i-1]
                
                currvalue = ydata[i]
                prevvalue = ydata[i-1]
                
                currthr = thrdata[i]
                prevthr = thrdata[i-1]

                # some artithmatics to figure out the intercept time:            
                if prevvalue < prevthr and currvalue > prevthr:
                    t_above = (1.0 - (prevthr - prevvalue) / (currvalue + prevthr - prevvalue - currthr)) * (currtime - prevtime)
                elif prevvalue > prevthr and currvalue < prevthr:
                    t_above = (prevthr - prevvalue) / (currvalue + prevthr - prevvalue - currthr) * (currtime - prevtime)
                elif prevvalue > prevthr and currvalue > currthr:
                    t_above = (currtime - prevtime)
                elif prevvalue < prevthr and currvalue < currthr:
                    t_above = 0.0
                    
                tot_time_above += t_above


        print('WIN CONDITION: tot_time_above = %f, tot_time = %f' % (tot_time_above, totTime))            
        print('WIN CONDITION: Fraction above = %f, Fraction needed = %f' % (tot_time_above / totTime, fraction_above))
        if tot_time_above / totTime > fraction_above:
            outcome = True
            outcomebool = 1
            # print('WIN CONDITION %s --> succeeded' % CP['WIN_CONDITION'])





    print('WIN CONDITION: %s --> %s' % (CP['WIN_CONDITION'], {0:'Failed', 1:'Succeeded'}[outcomebool]))





        
    return outcomebool





def init_staircases_steps(G):
    pass

    # the same initialization stuff, but now with (more regular) staircases.





def init_staircases_quest(G):
    
    # we won't optionalize this ... just go with it. 
    NUMBEROFSETS = G['EX_NUMBEROFSETS']
    MIX = G['EX_MIXOFSETS'] 
    STAIRIDENTIFIER = G['EX_STAIRIDENTIFIER']
    TUNINGTYPE = G['EX_TUNING_TYPE']
    
    
    if TUNINGTYPE == 'thr':
    
        startVal = 0.7
        startValSd = 0.25
        pThreshold = 0.82
        gamma = 0.5
        minVal = 0.0
        maxVal = 1.0


    elif TUNINGTYPE == 'linear':
        
        startVal = 1
        startValSd = 0.1
        pThreshold = 0.82
        gamma = 0.5
        minVal = 0.5
        maxVal = 1.5
        
    #nTrials = NUMBEROFSETS
    
    
    # some logic to figure out whether there is a previous staircase
    # see IF there is a number given: 1-1, or 0001. Then use the create
    # fname magic to check whether there is a logfile like that in there.
    # then if it's there -- load it (it's a .pkl).

    
    staircase_logfile_basename = 'log/staircases_quest_%s_%s.log' % (TUNINGTYPE, STAIRIDENTIFIER)
    file_to_check = create_incremental_filename(staircase_logfile_basename)
    
    if os.path.isfile(file_to_check):
        count = int(re.sub(r'(.*?)([0-9]*?)(\..+)',r'\2',file_to_check))
        current_file = re.sub(r'(.*?)([0-9]*?)(\..+)',r'\1%d\3',file_to_check) % count-1
    
        if os.path.isfile(current_file):
            
            print('Found previous Staircase information! : %s\n' % current_file)
            
            with open(current_file,'rb') as f:
                prev_staircases = f.read()
                

            list_up_till_now=dict()
            for key in prev_staircases.keys():
                list_up_till_now[key] = prev_staircases[key].otherData['list_up_till_now'][-1]  # pick the last one
            if G['EX_XorV_RESET_POINTS'] is True:
                list_up_till_now = {'train':[], 'transfer':[], 'observe':[], 'rest':[]}
                
                

    else:
        prev_staircases = {'train':None, 'transfer':None, 'observe':None, 'rest':None}   # any of the previous staircases                
        list_up_till_now = {'train':[], 'transfer':[], 'observe':[], 'rest':[]} 


    CP['list_up_till_now'] = list_up_till_now
    
    
    
    quest_staircase = dict()
    
    for qtype in ['train','transfer','observe','rest']:
        
        nTrials = NUMBEROFSETS * MIX[qtype]
        
        quest_staircase[qtype] = data.QuestHandler(
                startVal,
                startValSd,
                pThreshold=pThreshold, 
                gamma=gamma,
                nTrials=nTrials, 
                minVal=minVal, 
                maxVal=maxVal, 
                staircase=prev_staircases[qtype])
    
    
    # we try to get all of the responses up till now.
        quest_staircase[qtype].addOtherData('list_up_till_now',list_up_till_now[qtype])
    G['staircases'] = quest_staircase  
    #    while thisVal in staircase:
            
            # tune the curve with thisVal, if that's the thing
            # or alternatively, change the thr
            
            # do NF run
            
            # determine win condition
            # add it to Response
    #        staircase.addResponse
    
    





#%% Experimental Contruction, I
def define_experiment(G, st, pr, CP):
    
    
    # all different trial types
    ex=dict()
    ex['line']=dict()
    ex['line']['rest']=dict()
    ex['line']['observe']=dict()
    ex['line']['train']=dict()
    ex['line']['transfer']=dict()
    
    TINSTR=G['EX_TINSTR']  
    TPAUSE=G['EX_TPAUSE'] 
    TFB=G['EX_TFB']     
    TVSP=G['EX_TVSP']    
    TMARK=G['EX_TMARK']  
    # TJITT=G['TJITT']  
    
    
    
    # for each trial type, show what's going the be on the screen...
    ex['line']['train']['sequence']             = ['instruction', 'pause', 'feedback', 'veryshortpause1', 'veryshortpause2', 'mark', 'jitterpause' ]
    ex['line']['train']['instruction']          = ([],                                  TINSTR,      [st['background'], st['st_txt_upregulate']],                                   ['instruction','itrain'], [])
    ex['line']['train']['pause']                = ([pr['pickRandomJitter']],            TPAUSE,      [st['background']],                                                            [], [])
    ex['line']['train']['feedback']             = ([pr['LineCalculations']],            TFB,         [st['background'], st['patches'], st['thrline'], st['nf_line'], st['cfb']],    ['bFB','btrain'], ['eFB','etrain'])
    ex['line']['train']['veryshortpause1']      = ([],                                  TVSP,        [st['background'], st['patches'], st['thrline'], st['nf_line'], st['cfb']],    [], [])
    ex['line']['train']['veryshortpause2']      = ([],                                  TVSP,        [st['background']],                                                            [], [])
    ex['line']['train']['mark']                 = ([],                                  TMARK,       [st['background'], CP['corr_incorr']],                                         ['XorV','xorvtrain'], [])
    ex['line']['train']['jitterpause']          = ([],                                  CP['TJITT'], [st['background']],                                                            ['bISI','bisitrain'], ['eISI','eisitrain'])
    
    
    ex['line']['transfer']['sequence']          = ['instruction', 'pause', 'feedback', 'veryshortpause', 'mark', 'jitterpause' ]
    ex['line']['transfer']['instruction']       = ([],                                  TINSTR,      [st['background'], st['st_txt_upregulate']],                                   ['instruction','itransfer'], [])
    ex['line']['transfer']['pause']             = ([pr['pickRandomJitter']],            TPAUSE,      [st['background']],                                                            [], [])
    ex['line']['transfer']['feedback']          = ([pr['LineCalculations']],            TFB,         [st['background'], st['thrline']],                                             ['bFB','btransfer'], ['eFB','etransfer'])
    ex['line']['transfer']['veryshortpause']    = ([],                                  TVSP,        [st['background']],                                                            [], [])
    ex['line']['transfer']['mark']              = ([],                                  TMARK,       [st['background'], CP['corr_incorr']],                                         ['XorV''xorvtransfer'], [])
    ex['line']['transfer']['jitterpause']       = ([],                                  CP['TJITT'], [st['background']],                                                            ['bISI','bisitransfer'], ['eISI','eisitransfer'])
    
    
    ex['line']['observe']['sequence']           = ['instruction', 'pause', 'feedback', 'veryshortpause', 'jitterpause' ]
    ex['line']['observe']['instruction']        = ([],                                  TINSTR,      [st['background'], st['st_txt_noregulate']],                                   ['instruction','iobserve'], [])
    ex['line']['observe']['pause']              = ([pr['pickRandomJitter']],            TPAUSE,      [st['background']],                                                            [], [])
    ex['line']['observe']['feedback']           = ([pr['LineCalculations']],            TFB,         [st['background'], st['patches'], st['thrline'], st['nf_line'], st['cfb']],    ['bFB','bobserve'], ['eFB','eobserve'])
    ex['line']['observe']['veryshortpause']     = ([],                                  TVSP,        [st['background'], st['patches'], st['thrline'], st['nf_line'], st['cfb']],    [], [])
    ex['line']['observe']['jitterpause']        = ([],                                  CP['TJITT'], [st['background']],                                                            ['bISI','bisiobserve'], ['eISI','eisiobserve'])

    
    ex['line']['rest']['sequence']              = ['instruction', 'pause', 'feedback', 'jitterpause' ]
    ex['line']['rest']['instruction']           = ([],                                  TINSTR,      [st['background'], st['st_txt_noregulate']],                                   ['instruction','irest'], [])
    ex['line']['rest']['pause']                 = ([pr['pickRandomJitter']],            TPAUSE,      [st['background']],                                                            [], [])
    ex['line']['rest']['feedback']              = ([pr['LineCalculations']],            TFB,         [st['background'], st['thrline']],                                             ['bFB', 'brest'], ['eFB', 'erest'])
    ex['line']['rest']['jitterpause']           = ([],                                  CP['TJITT'], [st['background']],                                                            ['bISI','bisirest'],['eISI','eisirest'])



    # we will just set the only thing to be different, which is the feedback, mostly...
    # copy the entire thing and change only what's needed:
    ex['thermo']=dict()
    ex['thermo']['train']       = copy.copy(ex['line']['train'])
    ex['thermo']['transfer']    = copy.copy(ex['line']['transfer'])
    ex['thermo']['observe']     = copy.copy(ex['line']['observe'])
    ex['thermo']['rest']        = copy.copy(ex['line']['rest'])


    ex['thermo']['train']['feedback']           = ([pr['ThermoCalculations']],          TFB,    [st['background'], st['thermo_lines'], st['thermo_thermometer']],                 ['bFB','btrain'], ['eFB','etrain'])
    ex['thermo']['train']['veryshortpause1']    = ([],                                  TVSP,   [st['background'], st['thermo_lines'], st['thermo_thermometer']],                 [], [])
    ex['thermo']['observe']['feedback']         = ([pr['ThermoCalculations']],          TFB,    [st['background'], st['thermo_lines'], st['thermo_thermometer']],                 ['bFB','bobserve'], ['eFB','eobserve'])
    ex['thermo']['observe']['veryshortpause']   = ([],                                  TVSP,   [st['background'], st['thermo_lines'], st['thermo_thermometer']],                 [], [])

    ex['thermo']['transfer']['feedback']        = ([pr['ThermoCalculations']],          TFB,    [st['background'], st['thermo_lines'], st['thermo_thermometer_silent']],          ['bFB','btransfer'], ['eFB','etransfer'])
    ex['thermo']['rest']['feedback']            = ([pr['ThermoCalculations']],          TFB,    [st['background'], st['thermo_lines'], st['thermo_thermometer_silent']],          ['bFB', 'brest'], ['eFB', 'erest'])



    # and we will also implement here, the SQUARE.
    ex['square']=dict()
    ex['square']['train']       = copy.copy(ex['line']['train'])
    ex['square']['transfer']    = copy.copy(ex['line']['transfer'])
    ex['square']['observe']     = copy.copy(ex['line']['observe'])
    ex['square']['rest']        = copy.copy(ex['line']['rest'])


    ex['square']['train']['feedback']           = ([pr['SquareCalculations']],          TFB,    [st['background'], st['square'], st['square_focus']],                             ['bFB','btrain'], ['eFB','etrain'])
    ex['square']['train']['veryshortpause1']    = ([],                                  TVSP,   [st['background'], st['square'], st['square_focus']],                             [], [])
    ex['square']['observe']['feedback']         = ([pr['SquareCalculations']],          TFB,    [st['background'], st['square'], st['square_focus']],                             ['bFB','bobserve'], ['eFB','eobserve'])
    ex['square']['observe']['veryshortpause']   = ([],                                  TVSP,   [st['background'], st['square'], st['square_focus']],                             [], [])

    ex['square']['transfer']['feedback']        = ([pr['SquareCalculations']],          TFB,    [st['background'], st['square_silent'], st['square_focus']],                      ['bFB','btransfer'], ['eFB','etransfer'])  # no need to further calibrate a grey square, like with line and thermo.
    ex['square']['rest']['feedback']            = ([pr['SquareCalculations']],          TFB,    [st['background'], st['square_silent'], st['square_focus']],                      ['bFB', 'brest'], ['eFB', 'erest'])  # no need to further calibrate a grey square, like with line and thermo.



    # taking care of other stuff, like do-we-show feedback or not?
    for key in ex.keys():
        if G['EX_SHOWCHECKORCROSS'] is False:
            ex[key]['train']['sequence']             = ['instruction', 'pause', 'feedback', 'veryshortpause1', 'jitterpause' ]
            
        elif G['EX_SHOWCHECKORCROSSTRANSFER'] is False:
            ex[key]['transfer']['sequence']           = ['instruction', 'pause', 'feedback', 'jitterpause' ]
            


    

    return ex[G['EX_GRAPHICSMODE']]



#%% The PROGRAMS

@asyncio.coroutine
def GenTestSignal(G, st, CP):
    '''
    This thread will generate a test-signal and put it into CP['nfsignalContainer']
    Options are Sin and random. Update-interval is in G['TESTSIGNALUPDATEINTERVAL']
    For purposes of testing.
    '''

    # print('debug: GenTestSignal is Started!')
    
    G['GenTestSignalRunning'] = True
    
    lst=CP['nfsignalContainer']

    
    if G['EX_TESTSIGNALTYPE'] == 'random':
        while G['GenTestSignalRunning'] is True:
            signal = random.random()/2 + 0.25
            
            lst[0] = signal
            
            yield From(asyncio.sleep(G['EX_TESTSIGNALUPDATEINTERVAL']))
            # time.sleep(G['EX_TESTSIGNALUPDATEINTERVAL'])
            
    elif G['EX_TESTSIGNALTYPE'] == 'sin':
        
        period = G['EX_TESTSIGNALPERIOD']
        from math import sin, pi
        
        cl=clock.Clock()
        
        while G['GenTestSignalRunning'] is True:
            signal = sin(cl.getTime() / float(period) * 2. * pi)
            lst[0]=signal
            yield From(asyncio.sleep(G['EX_TESTSIGNALUPDATEINTERVAL']))




@asyncio.coroutine
def pickRandomJitter(G, st, CP):
    '''
    This function will pick a value between G['TJITT'][0] and G['TJITT'][1]
    And has been implemented to add the jitter time between triaks
    '''
    
    e=G['EX_TJITT'][1]
    b=G['EX_TJITT'][0]
    t = random.random() * (e-b) + b
    
    CP['TJITT'][0] = t  # well, the memory olcation points to a list and this is the constant. the contents of the list changes.
                        # so we mimick the functionality of a pointer.
                        
    yield From(asyncio.sleep(0))
                        

    



# this is a helper function for the other functions... this is a completely standalong function
def my_color_calculator(hb, he, thr, gap, y, ymax, ymin):
    
    ''' input: hex values begin and ending, threshold, gap and the current value
        we create a new y-value and look-up the color for that
        This might make the 'gap' noticable
        And necessiates subjects that aren't colorblind, for our purposes...
        since it's just a helper function, we won't put it into pr.
    '''
    
    # convert to -1 <--> +1
    rb = int(hb[0:2], 16) / 128. - 1;
    re = int(he[0:2], 16) / 128. - 1;
    gb = int(hb[2:4], 16) / 128. - 1;
    ge = int(he[2:4], 16) / 128. - 1;
    bb = int(hb[4:6], 16) / 128. - 1;
    be = int(he[4:6], 16) / 128. - 1;
    
    
    # first re-scale y and thr to be within ymax and ymin.
    
    ry = 2 * (float(y) - ymin) / (float(ymax) - ymin) - 1
    rthr = 2 * (float(thr) - ymin) / (float(ymax) - ymin) - 1
    rgap = gap / (float(ymax) - ymin)

    ##         
    #rymax = 1.
    #rymin = -1.
    cthr = 0    # we set cthr to 0 because this will perform rescaling in a way to make everything
                # ABOVE thr more green, and everything BELOW thr more RED. we cam cjamge back to (normal) thr, too...
                # then we can also increase color gap.
    
    if ry > rthr:
        rynew = 1 - (1 - ry) * (1 - cthr - rgap/2.) / (1 - rthr)
    elif ry <= rthr:
        rynew = (ry + 1) * (cthr - rgap/2. +1) / (rthr +1) - 1

    # print([ry, rynew])

    if rynew > 1.:
        rynew = 1.
    elif rynew < -1.:
        rynew = -1.

    rnew = rb + (re - rb) * (rynew + 1) / 2.
    gnew = gb + (ge - gb) * (rynew + 1) / 2.
    bnew = bb + (be - bb) * (rynew + 1) / 2.
    
    return (rnew, gnew, bnew)
    # now we can pick the color.        




@asyncio.coroutine    
def LineCalculations(G, st, CP):
    '''
    This will start up, for a period specified within the G, changes to the shapes for the LINESTIM type of NF
    '''
    
    win = G['win']  # our window..
    tmax = G['EX_TFB']   # this is how long we should display the stimulus on screen.
    thrContainer = CP['thrContainer']  # this is the threshold -- probably also set by on_control_event...
    nfvalueContainer = CP['nfsignalContainer']  # so this will be set (hopefully) by the handle_control_event...
    scaling = G['EX_SCALING']  # to scale... implementation of pos to be done later..
    st = st  # this contains points to all the stimuli.
    patch_color = G['EX_PATCHCOLOR']
    hb, he = G['EX_THERMOCLIMS']
    colorgap = G['EX_COLORGAP']

    cfb = st['cfb']  # this is the shape of the FB itself.
    thrline = st['thrline']  # set positions...            
    # reset the NFLINE and PATCHES
    
    nf_line = st['nf_line'][0]        # this is a shapestim
    patches = st['patches']           # this is a list of shapestims
    
    trialtype = CP['TrialType'][0]
    this_staircase = G['staircases'][trialtype]    
    # obtain next response from staircase
    nextTuningVal = this_staircase.next()
    # check if the tuning type is THR --> change THR
    if CP['TUNING_TYPE'] == 'thr':
        CP['thrContainer'][0] = nextTuningVal
    
    
    # should work...
    thr=thrContainer[0]
    # ypos_for_color=nfvalueContainer[0]
    ypos_for_color=tuning(CP, nfvalueContainer[0])
    
    nf_line.setVertices((0, 0)) # this should reset it without this being re-initialized again/
    # self.st['nf_line'][0] = visual.ShapeStim(self.win, vertices=[(0, 0)], closeShape=False, lineColor='lightblue', size=self.scaling, lineWidth=0)
    patches[:]=[]  # empty this list
    # self.st['patches'] = []
    

    # deal with the thresh-line:
    for l in thrline:
        oldstart = l.start
        oldend = l.end
        l.start = (oldstart[0]  , thrContainer[0]) 
        l.end = (oldend[0]      , thrContainer[0]) 


    # deal with the NF line:
    vertices=[]
    vertices.append( (-1, ypos_for_color) )
    nf_line.setVertices(vertices)


    
    if ypos_for_color > thrContainer[0]:
        # make a new patch..

        rnew, gnew, bnew = my_color_calculator(hb, he, thr, colorgap, ypos_for_color, 1, -1)   
        patch_color = (rnew, gnew, bnew)    
        
        patch_vert=[]
        ABOVE_PREV = True
        patch_vert.append((-1,  thrContainer[0]      ))
        patch_vert.append((-1+0.0001,  ypos_for_color  ))
        patch_vert.append((-1+0.0001,  thrContainer[0]      ))

        newpatch = visual.ShapeStim(win, vertices=patch_vert, fillColor=patch_color, size=scaling, lineWidth=0)
        patches.append(newpatch)
    else:
        ABOVE_PREV = False
    
    
    tlist=[]  # needed to calculate the win condition
    ylist=[]  # this too -- needed to calculate the win condition
    thrlist=[]  # yes, this too. To be ultra-flexible.
    curtime=0
    curi=0
    cl=clock.Clock()  # yeah...well, we make a second clock. should not be too off in seconds.
    
    lastypos=0.
    while curtime < tmax:
        
        # time.sleep(G['EX_PR_SLEEPTIME'])
        
        curtime=cl.getTime()
        curi += 1
        # patchi += 1
        thr=thrContainer[0]  # might've changed in the meantime?
        
        xpos = -1 + 2 * curtime / tmax
        #ypos = nfvalueContainer[0]
        ypos = tuning(CP, nfvalueContainer[0])

        tlist.append(curtime)
        ylist.append(ypos)
        thrlist.append(thr)
        
        
        vertices.append((xpos, ypos))
        # nf_line.setVertices(vertices)  # ok, we did the line.. now on to:
        nf_line.setVertices(vertices)
        
        # replacement_line = visual.ShapeStim(self.win, vertices=vertices, closeShape=False, lineColor='lightblue', size=scaling)
        # nf_line[0] = replacement_line
        
        cfb.setPos((xpos * scaling[0], ypos * scaling[1]))  # ok, so that was the NF stimulus
        # print(cfb.pos)
        
        # if patchi>0:
        # now comes fun part -- i.e. the patches.

        if ypos > thrContainer[0]:
            ABOVE=True
            
            if ABOVE_PREV is True:
                # just add one vertex..

                if ypos > lastypos:
                    ypos_for_color = ypos
                rnew, gnew, bnew = my_color_calculator(hb, he, thr, colorgap, ypos_for_color, 1, -1)   
                patch_color = (rnew, gnew, bnew)                        
                        
                patch_vert.pop()
                patch_vert.append((xpos, ypos))
                patch_vert.append((xpos, thr))

                thispatch = patches[-1]
                thispatch.setVertices(patch_vert)
                thispatch.setFillColor(patch_color, colorSpace='rgb')
                # pdb.set_trace()
                # replacement = visual.ShapeStim(self.win, vertices=patch_vert, fillColor=self.patch_color, size=self.scaling, lineWidth=0)
                # current_patch.setVertices(patch_vert)
                # patches[-1] = replacement
                
                lastypos=ypos
            
            else:
                
                patch_vert=[]
                old_xpos = vertices[-2][0]
                old_ypos = vertices[-2][1]
                
                xbegin = old_xpos + (xpos-old_xpos) * (ypos-thr) / (ypos - old_ypos + 1)
                ybegin = thr
                
                patch_vert.append((xbegin, ybegin))  # we just will close off this patch, then..
                patch_vert.append((xpos, ypos))
                patch_vert.append((xpos, thr))
                
                rnew, gnew, bnew = my_color_calculator(hb, he, thr, colorgap, ypos_for_color, 1, -1)  
                patch_color=(rnew, gnew, bnew)
                
                # patches.append(visual.ShapeStim(self.win, vertices=patch_vert, closeShape=True, fillColor=self.patch_color, lineWidth =0, autoLog=False))
                # make a totally NEW patch
                newpatch = visual.ShapeStim(win, vertices=patch_vert, fillColor=patch_color, size=scaling, lineWidth=0)
                patches.append(newpatch)
                # so, this is the first one... so we need the xpos of the previous...
            
        else:
            ABOVE = False
            #patches.append(visual.ShapeStim(self.win, vertices=patch_vert, closeShape=True, size=stimSize, fillColor=self.patch_color, lineWidth =0, autoLog=False))

            if ABOVE_PREV is False:
                pass 
            else:
                
                old_xpos = vertices[-2][0]
                old_ypos = vertices[-2][1]

                xend = old_xpos + (xpos-old_xpos) * (old_ypos - thr) / (old_ypos - ypos)
                yend = thr
                
                patch_vert.pop()
                patch_vert.append((xend, yend))
                
                thispatch = patches[-1]
                thispatch.setVertices(patch_vert)

            
        ABOVE_PREV=ABOVE
        
        yield From(asyncio.sleep(G['EX_PR_SLEEPTIME']))


    is_won = check_win_condition(CP, tlist, ylist, thrlist)
    this_staircase.addResponse(1-is_won)
    this_staircase.otherData['list_up_till_now'][-1].append(is_won)
    
    tot_points = calculate_total_points(G)
    
    if is_won == 1:
        CP['corr_incorr'][0] = st['st_correct']
        print('should draw the st_correct now!!!')
    else:
        CP['corr_incorr'][0] = st['st_incorrect']
    
    
    if G['EX_INTERACTIONMODE'] == 'master':
        pass  # call staircase calculator now, that will make things ready for the next (feedback) step.



        
    
@asyncio.coroutine    
def LineCheck(G, st, CP):
    ''' This should just re-draw the line according to whatps in CP['Threshold'][0]
    '''
    thrline = st['thrline']  # set positions...
    for l in thrline:
        oldstart = l.start
        oldend = l.end
        l.start = (oldstart[0]  , CP['thrContainer'][0]) #* self.scaling[1])
        l.end = (oldend[0]      , CP['thrContainer'][0]) # * self.scaling[1])

    yield From(asyncio.sleep(0))






# we WILL start the thread to do this thing.
@asyncio.coroutine    
def ThermoCalculations(G, st, CP):
    '''
    This will start up, for a period specified within the G, changes to the shapes for the LINESTIM type of NF
    '''
    
    win = G['win']  # our window..
    tmax = G['EX_TFB']   # this is how long we should display the stimulus on screen.
    thrContainer = CP['thrContainer']  # this is the threshold -- probably also set by on_control_event...
    nfsignalContainer = CP['nfsignalContainer']  # so this will be set (hopefully) by the handle_control_event...
    scaling = G['EX_SCALING']  # to scale... implementation of pos to be done later..
    st = st  # this contains points to all the stimuli.
    patch_color = G['EX_THERMOCLIMS']
    colorgap = G['EX_COLORGAP']


    hb, he = G['EX_THERMOCLIMS']


    trialtype = CP['TrialType'][0]
    
    this_staircase = G['staircases'][trialtype]    
    # obtain next response from staircase
    nextTuningVal = this_staircase.next()
    # check if the tuning type is THR --> change THR
    if CP['TUNING_TYPE'] == 'thr':
        CP['thrContainer'][0] = nextTuningVal
    
    


    ''' 1) (re-set) vertices of the line (i.e. add to them)
        2) update the position of the crosshair according to curvalue and time
        3) handle the patches, too.
    '''


    # print self.nfvalueContainer
    thrline = st['thermo_lines']  # set positions...
    for l in thrline:
        oldstart = l.start
        oldend = l.end
        l.start = (oldstart[0]  , thrContainer[0]) #* self.scaling[1])
        l.end = (oldend[0]      , thrContainer[0]) # * self.scaling[1])
        # print(l.pos)
    # drawing comes later.
    
    #ypos = nfsignalContainer[0]
    #rnew, gnew, bnew = my_color_calculator(hb, he, thrContainer[0], colorgap, ypos, 1, -1); thermocolor = (rnew, gnew, bnew)
    #thermovert = [(-0.25, -1), (0.25, -1), (0.25, ypos), (-0.25, ypos)]
    #thermo_thermometer = st['thermo_thermometer'][0]
    #thermo_thermometer.setVertices(thermovert)
    #thermo_thermometer.setFillColor(thermocolor, colorSpace='rgb')

    scaling=scaling

    curtime=0
    
    
    tlist=[]  # needed to calculate the win condition
    ylist=[]  # this too -- needed to calculate the win condition
    thrlist=[]
    
    
    cl=clock.Clock()  # yeah...well, we make a second clock. should not be too off in seconds.
    while curtime < tmax:
        
        # time.sleep(G['EX_PR_SLEEPTIME'])
        
        curtime=cl.getTime()
        
        # so, what is the y pos?
        ypos = tuning(CP, nfsignalContainer[0])
        
        tlist.append(curtime)
        ylist.append(ypos)
        thrlist.append(thrContainer[0])

        rnew, gnew, bnew = my_color_calculator(hb, he, thrContainer[0], colorgap, ypos, 1, -1)                

        # then, what is the color?

        thermo_thermometer = st['thermo_thermometer'][0]
        thermocolor = (rnew, gnew, bnew)
        # thermovert = [(coord[0] * scaling[0], coord[1] * scaling[1]) for coord in [(-0.25, -1), (0.25, -1), (0.25, ypos), (-0.25, ypos)]]
        # I already scaled them!!
        thermovert = [(-0.25, -1), (0.25, -1), (0.25, ypos), (-0.25, ypos)]
        
        thermo_thermometer.setVertices(thermovert)
        thermo_thermometer.setFillColor(thermocolor, colorSpace='rgb')
        
        #replacement_thermo = visual.ShapeStim(self.win, lineWidth=1.5, lineColor='white', fillColor=thermocolor, vertices=thermovert)
        #thermo_thermometer_container[0] = replacement_thermo
        yield From(asyncio.sleep(G['EX_PR_SLEEPTIME']))
        # print(thermo_thermometer)
        
        


    is_won = check_win_condition(CP, tlist, ylist, thrlist)
    this_staircase.addResponse(1-is_won)
    this_staircase.otherData['list_up_till_now'][-1].append(is_won)
    
    tot_points = calculate_total_points(G)
    
    if is_won == 1:
        CP['corr_incorr'][0] = st['st_correct']
        print('should draw the st_correct now!!!')
    else:
        CP['corr_incorr'][0] = st['st_incorrect']
    
        
    
    if G['EX_INTERACTIONMODE'] == 'master':
        pass  # call staircase calculator now, that will make things ready for the next (feedback) step.




@asyncio.coroutine    
def ThermoCheck(G, st, CP):
    ''' This should just re-draw the line according to whatps in CP['Threshold'][0]
    '''
    thrline = st['thermo_lines']  # set positions...
    for l in thrline:
        oldstart = l.start
        oldend = l.end
        l.start = (oldstart[0]  , CP['thrContainer'][0]) #* self.scaling[1])
        l.end = (oldend[0]      , CP['thrContainer'][0]) # * self.scaling[1])


    yield From(asyncio.sleep(0))






# we WILL start the thread to do this thing.
@asyncio.coroutine
def SquareCalculations(G, st, CP):
    '''
    This will start up, for a period specified within the G, changes to the shapes for the LINESTIM type of NF
    '''
    
    
    print('debug: SquareCalculations has been started!')
    win = G['win']  # our window..
    tmax = G['EX_TFB']   # this is how long we should display the stimulus on screen.
    thrContainer = CP['thrContainer']  # this is the threshold -- probably also set by on_control_event...
    nfsignalContainer = CP['nfsignalContainer']  # so this will be set (hopefully) by the handle_control_event...
    st = st  # this contains points to all the stimuli.
    colorgap = G['EX_COLORGAP']
    hb, he = G['EX_THERMOCLIMS']
    
    trialtype = CP['TrialType'][0]
    this_staircase = G['staircases'][trialtype]




    # obtain next response from staircase
    nextTuningVal = this_staircase.next()
    # check if the tuning type is THR --> change THR
    if CP['TUNING_TYPE'] == 'thr':
        CP['thrContainer'][0] = nextTuningVal
    



    curtime=0
    square_to_be_colorized = st['square']
    
    tlist=[]  # needed to calculate the win condition
    ylist=[]  # this too -- needed to calculate the win condition
    thrlist=[]
    
    cl=clock.Clock()  # yeah...well, we make a second clock. should not be too off in seconds.
    while curtime < tmax:
        
        #time.sleep(G['EX_PR_SLEEPTIME'])
        
        curtime=cl.getTime()


        # so, what is the y pos?
        ypos = tuning(CP, nfsignalContainer[0])  #this changes due to the other thread...


        tlist.append(curtime)
        ylist.append(ypos)        
        thrlist.append(thrContainer[0])

        rnew, gnew, bnew = my_color_calculator(hb, he, thrContainer[0], colorgap, ypos, 1, -1)                
        square_to_be_colorized.setFillColor((rnew, gnew, bnew), colorSpace='rgb')
        square_to_be_colorized.setLineColor('black')
        
        
        yield From(asyncio.sleep(G['EX_PR_SLEEPTIME']))
        # then, what is the color?

        # square_to_be_colorized.fillColor = (rnew, gnew, bnew)
        



    is_won = check_win_condition(CP, tlist, ylist, thrlist)
    this_staircase.addResponse(1-is_won)
    
    tot_points = calculate_total_points(G)  # the staircases are also in G...
    
    this_staircase.otherData['list_up_till_now'][-1].append(is_won)
    
    # add some logic to figure out what the total score is!
    # this_staircase.otherData['list_up_till_now'][-1]
    
    if is_won == 1:
        CP['corr_incorr'][0] = st['st_correct']
        print('should draw the st_correct now!!!')
    else:
        CP['corr_incorr'][0] = st['st_incorrect']
    
    
    #    list_up_till_now.append(is_won)
    #    this_staircase.addOtherData(list_up_till_now)
    # prep the next corr/incorr stimulus:
    

    if G['EX_INTERACTIONMODE'] == 'master':
        pass  # call staircase calculator now, that will make things ready for the next (feedback) step.







def init_programs(G, st, CP):
    # lst=[0]
    pr=dict()    

    pr['LineCalculations']=LineCalculations
    pr['ThermoCalculations']=ThermoCalculations
    pr['SquareCalculations']=SquareCalculations
    
    pr['ThermoCheck'] = ThermoCheck
    pr['LineCheck'] = LineCheck
    pr['GenTestSignal']=GenTestSignal

    pr['pickRandomJitter']=pickRandomJitter

    
    return pr
# the thr function will:ThermoCalculations

# a) determine whether things move upwards...
# b) add patchstim, maybe, to the list of things to draw on the screen
# c) figure out whether to draw a succes//failure
# d) convert the condition specified from the NF Control computer to parameters here, so they guve identical resuls....


# where does the NF control end, and the NF stim begin? That's kind of a boundary regions, right?


# rest trials - no FB



# observe trials - no FB


# regulation trials - definite FB


# transfer trials -- yes/no FB?





# show whether it's going to be up or no regulation


# show (or don't show) the EEG..


# show the summary (V or X)

#%% Machinery



# a special exception handler coroutine that'll kill our main loop if something
# happens

@asyncio.coroutine
def handle_exception_pr(f, G, st, CP, loop):
    #print f
    #print loop
    try:
        yield From(f(G, st, CP))
    except Exception:
        # print debug information
        print('---------------')
        print('---------------')
        print('ERROR OCCURRED:')
        print(sys.exc_info()[1])
        traceback.print_tb(sys.exc_info()[2])

        # G['eh'].shutdown()
        # G['eh'].join()
        # G['win'].close()
        # logging.flush()
        # loop.stop()
        
        #import os
        #import signal

        #os.kill(os.getpid(),signal.SIGINT)


        pending = asyncio.Task.all_tasks()
        for task in pending:
            task.cancel()
            # Now we should await task to execute it's cancellation.
            # Cancelled task raises asyncio.CancelledError that we can suppress:
            #with suppress(asyncio.CancelledError):
            #    loop.run_until_complete(task)        
        loop.stop()  # stops the loop, gives an error for that, too.



    


@asyncio.coroutine
def handle_exception(f, trialType, G, st, CP, ex, loop):
    #print f
    #print loop
    try:
        yield From(f(trialType, G, st, CP, ex, loop))
    except Exception:
        # print debug information
        print('---------------')
        print('---------------')
        print('ERROR OCCURRED:')
        print(sys.exc_info()[1])
        traceback.print_tb(sys.exc_info()[2])

        # G['eh'].shutdown()
        # G['eh'].join()
        # G['win'].close()
        # logging.flush()


        pending = asyncio.Task.all_tasks()
        for task in pending:
            task.cancel()
            # Now we should await task to execute it's cancellation.
            # Cancelled task raises asyncio.CancelledError that we can suppress:
            #with suppress(asyncio.CancelledError):
            #    loop.run_until_complete(task)        
        loop.stop()  # stops the loop, gives an error for that, too.


    
@asyncio.coroutine
def runTrial(trialType, G, st, CP, ex, loop):

    print('---->' + trialType)
    # print(trialType)
    # print(CP['TJITT'][0])
    #win = G['win']
    #st = G['st']
    #SCALING = G['scaling']
    #PATCHCOLOR = G['patchcolor']
    # the structure of the experiment is already within the data sctructure, and I make use of that.
    for part in ex[trialType]['sequence']:
        
        # so depending on trialType and part, we can figure out which code to send.
        # and thus, here we 'prime' win to call_on_flip our event handler, just like before.
        # so, what IS the message?
        # general
        
        CP['TrialType'][0] = trialType

        CP['CURRENTPART'][0] = part
        programs, tdur, stims, messages_start, messages_stop = ex[trialType][part]
        
        if part == 'jitterpause':
            print('Jitter Time: %f' % CP['TJITT'][0])
        
        for message in messages_start:
            G['win'].callOnFlip(G['eh'].send_message,message)    

        if isinstance(tdur,list):  # in case we have set t using CP (control parameter)
            tdur=tdur[0]

        # start the program or programs, if there are any, using ASYNC!!
        for pitem in programs:
            # yield From(asyncio.async(handle_exception_pr(pitem, G, st, CP, loop)))
            loop.create_task(handle_exception_pr(pitem, G, st, CP, loop))
            yield From(asyncio.sleep(0))
    
        # print('debug: ' + part + 'start')    
        G['cl'].reset()
        while G['cl'].getTime() < tdur:
            yield From(asyncio.sleep(0))
            for i, stim in enumerate(stims):
                if isinstance(stim, list):  # specifically for the patches..
                    #print(stim)
                    for p in stim:
                        p.draw()
                else:
                    stim.draw()
            G['win'].flip()  # here we send the message !!
            yield From(asyncio.sleep(0))
            
        # now that the window flipping is done -- send 'end' markers directoy.
        for message in messages_stop:
            G['eh'].send_message(message)
            
        # print('debug: ' + part + 'stop')            
    # print('trial ended!')
        



def run_main_program(G, st, CP, ex, pr):
    '''
    This runs the stopingibition/visual/audio part of the paradigm using
    asyncio-replacement trollius. Before and after, we can still present
    other stimuli.
    '''
    
    
    # something like this:
    # mainClock=clock.Clock()
    # mainClockContainer[0]=mainClock # put it into my list, that double-serves
    # as a pointer
    

    
    
    # add the signal generator (if requested):
    
    
    
    #tasks = [
    #    asyncio.async(handleVisual()),
    #    asyncio.async(handleGonogo()),
    #    asyncio.async(handleEscape()),
    #    ]
    #    tasks_dbg = [
    #            # asyncio.async(handle_exception(test_it,G,loop)),
    #            asyncio.async(handle_exception(runTrial,trialType, G, st, CP, ex, loop))
    #            
    #            ]
    #    
    #    
    #    tasks = [
    #            # asyncio.async(test_it(G)),
    #            # asyncio.async(handle_audio(G))
    #            ]
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
                                
    my_trial_sequence = flatten(trialopts[0:5])  # we do 5 of them.
    my_trial_definitions = {1:'train', 2:'transfer', 3:'observe', 4:'rest'}
    
    
        
    loop=asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    
    if G['EX_TESTNFNOISE'] is True:
        loop.create_task(pr['GenTestSignal'](G, st, CP))

    
    # so to debug, just run tasks_dbg instead of tasks.
    for t_i in my_trial_sequence:
        trialType = my_trial_definitions[t_i]
        # print(trialType)
        # trialType, G, st, CP, ex, loop
        loop.run_until_complete(asyncio.wait([asyncio.async(handle_exception(runTrial,trialType, G, st, CP, ex, loop))]))   
    
    
    # give it another second:
    


#%% The Main
            
if __name__ == "__main__":

    

    # define our dummy logger:    
    class dummy_logger():
        def send_message(self, m):
            pass
            # print(m)
    
    G['eh']=dummy_logger()
    
    

    # close the window, if it was open:
    if visual.globalVars.currWindow:
        visual.globalVars.currWindow.close()
    
    # our clock..
    G['cl']=clock.Clock()
    

    # G is global parameters...
    # CP is 'Control Parameters', i.e. for which-trial-next, etc.

    G['EX_GRAPHICSMODE'] = 'line'

    init_window(G)
    init_staircases_quest(G)
    st=make_stimuli(G, CP)
    pr=init_programs(G, st, CP)
    ex=define_experiment(G, st, pr, CP)  # pr is passed to define_experiment, but then we won't need...
    
    
    
    run_main_program(G, st, CP, ex, pr)




