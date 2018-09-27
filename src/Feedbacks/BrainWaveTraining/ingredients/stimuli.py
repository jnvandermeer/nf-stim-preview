# -*- coding: utf-8 -*-






# 
#VIS_SCALING = X, X
#VIS_DEGREES = ...
# if you specify the win as 'deg' monitor, then all the sizes will become degrees ... so you can set/rescale..






#%% imports
# getting the window right:

import inspect, os

from psychopy import visual, clock
import numpy as np
import random
import threading
import time
import copy




#%% He[per functions]
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
CP['corr_incorr'] = 'st_incorrect'  # chooose between 'st_correct' and 'st_incorrect'




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
    st['corr_incorr'] =  st[CP['corr_incorr']]


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
    ex['line']['train']['pause']                = ([],                                  TPAUSE,      [st['background']],                                                            [], [])
    ex['line']['train']['feedback']             = ([[pr['LineCalculations'], 'start']], TFB,         [st['background'], st['patches'], st['thrline'], st['nf_line'], st['cfb']],    ['bFB','btrain'], ['eFB','etrain'])
    ex['line']['train']['veryshortpause1']      = ([],                                  TVSP,        [st['background'], st['patches'], st['thrline'], st['nf_line'], st['cfb']],    [], [])
    ex['line']['train']['veryshortpause2']      = ([],                                  TVSP,        [st['background']],                                                            [], [])
    ex['line']['train']['mark']                 = ([],                                  TMARK,       [st['background'], st['corr_incorr']],                                         ['XorV','xorvtrain'], [])
    ex['line']['train']['jitterpause']          = ([[pr['pickRandomJitter'], 'call']],  CP['TJITT'], [st['background']],                                                            ['bISI','bisitrain'], ['eISI','eisitrain'])
    
    
    ex['line']['transfer']['sequence']          = ['instruction', 'pause', 'feedback', 'veryshortpause', 'mark', 'jitterpause' ]
    ex['line']['transfer']['instruction']       = ([],                                  TINSTR,      [st['background'], st['st_txt_upregulate']],                                   ['instruction','itransfer'], [])
    ex['line']['transfer']['pause']             = ([],                                  TPAUSE,      [st['background']],                                                            [], [])
    ex['line']['transfer']['feedback']          = ([[pr['LineCheck'], 'call']],         TFB,         [st['background'], st['thrline']],                                             ['bFB','btransfer'], ['eFB','etransfer'])
    ex['line']['transfer']['veryshortpause']    = ([],                                  TVSP,        [st['background']],                                                            [], [])
    ex['line']['transfer']['mark']              = ([],                                  TMARK,       [st['background'], st['corr_incorr']],                                         ['XorV''xorvtransfer'], [])
    ex['line']['transfer']['jitterpause']       = ([[pr['pickRandomJitter'], 'call']],  CP['TJITT'], [st['background']],                                                            ['bISI','bisitransfer'], ['eISI','eisitransfer'])
    
    
    ex['line']['observe']['sequence']           = ['instruction', 'pause', 'feedback', 'veryshortpause', 'jitterpause' ]
    ex['line']['observe']['instruction']        = ([],                                  TINSTR,      [st['background'], st['st_txt_noregulate']],                                   ['instruction','iobserve'], [])
    ex['line']['observe']['pause']              = ([],                                  TPAUSE,      [st['background']],                                                            [], [])
    ex['line']['observe']['feedback']           = ([[pr['LineCalculations'], 'start']], TFB,         [st['background'], st['patches'], st['thrline'], st['nf_line'], st['cfb']],    ['bFB','bobserve'], ['eFB','eobserve'])
    ex['line']['observe']['veryshortpause']     = ([],                                  TVSP,        [st['background'], st['patches'], st['thrline'], st['nf_line'], st['cfb']],    [], [])
    ex['line']['observe']['jitterpause']        = ([[pr['pickRandomJitter'], 'call']],  CP['TJITT'], [st['background']],                                                            ['bISI','bisiobserve'], ['eISI','eisiobserve'])

    
    ex['line']['rest']['sequence']              = ['instruction', 'pause', 'feedback', 'jitterpause' ]
    ex['line']['rest']['instruction']           = ([],                                  TINSTR,      [st['background'], st['st_txt_noregulate']],                                   ['instruction','irest'], [])
    ex['line']['rest']['pause']                 = ([],                                  TPAUSE,      [st['background']],                                                            [], [])
    ex['line']['rest']['feedback']              = ([[pr['LineCheck'], 'call']],         TFB,         [st['background'], st['thrline']],                                             ['bFB', 'brest'], ['eFB', 'erest'])
    ex['line']['rest']['jitterpause']           = ([[pr['pickRandomJitter'], 'call']],  CP['TJITT'], [st['background']],                                                            ['bISI','bisirest'],['eISI','eisirest'])



    # we will just set the only thing to be different, which is the feedback, mostly...
    # copy the entire thing and change only what's needed:
    ex['thermo']=dict()
    ex['thermo']['train']       = copy.copy(ex['line']['train'])
    ex['thermo']['transfer']    = copy.copy(ex['line']['transfer'])
    ex['thermo']['observe']     = copy.copy(ex['line']['observe'])
    ex['thermo']['rest']        = copy.copy(ex['line']['rest'])


    ex['thermo']['train']['feedback']           = ([[pr['ThermoCalculations'], 'start']], TFB,    [st['background'], st['thermo_lines'], st['thermo_thermometer']])
    ex['thermo']['train']['veryshortpause1']    = ([],                                    TVSP,   [st['background'], st['thermo_lines'], st['thermo_thermometer']])
    ex['thermo']['observe']['feedback']         = ([[pr['ThermoCalculations'], 'start']], TFB,    [st['background'], st['thermo_lines'], st['thermo_thermometer']])
    ex['thermo']['observe']['veryshortpause']   = ([],                                    TVSP,   [st['background'], st['thermo_lines'], st['thermo_thermometer']])

    ex['thermo']['transfer']['feedback']        = ([[pr['ThermoCheck'], 'call']],         TFB,    [st['background'], st['thermo_lines'], st['thermo_thermometer_silent']])
    ex['thermo']['rest']['feedback']            = ([[pr['ThermoCheck'], 'call']],         TFB,    [st['background'], st['thermo_lines'], st['thermo_thermometer_silent']])



    # and we will also implement here, the SQUARE.
    ex['square']=dict()
    ex['square']['train']       = copy.copy(ex['line']['train'])
    ex['square']['transfer']    = copy.copy(ex['line']['transfer'])
    ex['square']['observe']     = copy.copy(ex['line']['observe'])
    ex['square']['rest']        = copy.copy(ex['line']['rest'])


    ex['square']['train']['feedback']           = ([[pr['SquareCalculations'], 'start']], TFB,    [st['background'], st['square'], st['square_focus']])
    ex['square']['train']['veryshortpause1']    = ([],                                    TVSP,   [st['background'], st['square'], st['square_focus']])
    ex['square']['observe']['feedback']         = ([[pr['SquareCalculations'], 'start']], TFB,    [st['background'], st['square'], st['square_focus']])
    ex['square']['observe']['veryshortpause']   = ([],                                    TVSP,   [st['background'], st['square'], st['square_focus']])

    ex['square']['transfer']['feedback']        = ([],                                    TFB,    [st['background'], st['square_silent'], st['square_focus']])  # no need to further calibrate a grey square, like with line and thermo.
    ex['square']['rest']['feedback']            = ([],                                    TFB,    [st['background'], st['square_silent'], st['square_focus']])  # no need to further calibrate a grey square, like with line and thermo.




    # taking care of other stuff, like do-we-show feedback or not?
    for key in ex.keys():
        if G['EX_SHOWCHECKORCROSS'] is False:
            ex[key]['train']['sequence']             = ['instruction', 'pause', 'feedback', 'veryshortpause1', 'jitterpause' ]
            
        elif G['EX_SHOWCHECKORCROSSTRANSFER'] is False:
            ex[key]['transfer']['sequence']           = ['instruction', 'pause', 'feedback', 'jitterpause' ]
            


    

    return ex[G['EX_GRAPHICSMODE']]



#%% now, make the workflow...
def init_programs(G, st, CP):
    # lst=[0]
    pr=dict()    
    
    class GenTestSignal(threading.Thread):
        '''
        This thread will generate a test-signal and put it into CP['nfsignalContainer']
        Options are Sin and random. Update-interval is in G['TESTSIGNALUPDATEINTERVAL']
        For purposes of testing.
        '''
        
        def __init__(self, G, st, CP):
            ''' start up a dummy signal'''
            super(GenTestSignal, self).__init__()
            
            self.lst=CP['nfsignalContainer']
            self.running=True
        
        def run(self):
            
            if G['EX_TESTSIGNALTYPE'] == 'random':
                while self.running is True:
                    signal = random.random()/2 + 0.25
                    
                    self.lst[0] = signal
                    
                    time.sleep(G['EX_TESTSIGNALUPDATEINTERVAL'])
                    
            elif G['EX_TESTSIGNALTYPE'] == 'sin':
                
                period = G['EX_TESTSIGNALPERIOD']
                from math import sin, pi
                
                cl=clock.Clock()
                
                while self.running is True:
                    signal = sin(cl.getTime() / float(period) * 2. * pi)
                    self.lst[0]=signal
                    time.sleep(G['EX_TESTSIGNALUPDATEINTERVAL'])
                
            
        def stop(self):
            self.running=False
    
    pr['GenTestSignal']=GenTestSignal
    


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
        
    pr['pickRandomJitter']=pickRandomJitter
    

    
        # this is a helper function for the other functions...
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
    pr['my_color_calculator']=my_color_calculator
        
    
    
    # we WILL start the thread to do this thing.
    class LineCalculations(threading.Thread):
        def __init__(self, G, st, CP):
            '''
            This will start up, for a period specified within the G, changes to the shapes for the LINESTIM type of NF
            '''
            
            super(LineCalculations, self).__init__()
            
            self.win = G['win']  # our window..
            self.tmax = G['EX_TFB']   # this is how long we should display the stimulus on screen.
            self.thrContainer = CP['thrContainer']  # this is the threshold -- probably also set by on_control_event...
            self.nfvalueContainer = CP['nfsignalContainer']  # so this will be set (hopefully) by the handle_control_event...
            self.scaling = G['EX_SCALING']  # to scale... implementation of pos to be done later..
            self.st = st  # this contains points to all the stimuli.
            self.patch_color = G['EX_PATCHCOLOR']
            self.hb, self.he = G['EX_THERMOCLIMS']
            self.colorgap = G['EX_COLORGAP']
            
            self._vert=[]
            
            # reset the NFLINE and PATCHES
            self.st['nf_line'][0] = visual.ShapeStim(self.win, vertices=[(0, 0)], closeShape=False, lineColor='lightblue', size=self.scaling, lineWidth=0)
            self.st['patches'][:] =[]
            # self.st['patches'] = []
            # print nfvalueContainer
            
            
        def run(self):
            ''' 1) (re-set) vertices of the line (i.e. add to them)
                2) update the position of the crosshair according to curvalue and time
                3) handle the patches, too.
            '''
    
    
            # print self.nfvalueContainer
            scaling=self.scaling
    
            # 'unpack' what we need"
            patches = self.st['patches']
            
            cfb = self.st['cfb']
            # print(cfb)
            thrline = self.st['thrline']  # set positions...
            for l in thrline:
                oldstart = l.start
                oldend = l.end
                l.start = (oldstart[0]  , self.thrContainer[0]) #* self.scaling[1])
                l.end = (oldend[0]      , self.thrContainer[0]) # * self.scaling[1])



            
            nf_line = self.st['nf_line']
            vertices=[]
            vertices.append( (-1, self.nfvalueContainer[0]) )
            replacement_line = visual.ShapeStim(self.win, vertices=vertices, closeShape=False, lineColor='lightblue', size=scaling)
            nf_line[0] = replacement_line
            # nf_line.pos = (0., 0.)
            
    
            # upkeep for those patches:
            patches[:]=[]  # clear all of them
            
            if self.nfvalueContainer[0] > self.thrContainer[0]:
                # make a new patch..
                
                patch_vert=[]
                ABOVE_PREV = True
                patch_vert.append((-1,  self.thrContainer[0]      ))
                patch_vert.append((-1,  self.nfvalueContainer[0]  ))
                patch_vert.append((-1,  self.thrContainer[0]      ))
    
                newpatch = visual.ShapeStim(self.win, vertices=patch_vert, fillColor=self.patch_color, lineWidth=0)
                patches.append(newpatch)
            else:
                ABOVE_PREV = False
            
            
            
            curtime=0
            curi=0
            cl=clock.Clock()  # yeah...well, we make a second clock. should not be too off in seconds.
            
            lastypos=0.
            while curtime < self.tmax:
                
                time.sleep(G['EX_PR_SLEEPTIME'])
                
                curtime=cl.getTime()
                curi += 1
                # patchi += 1
                thr=self.thrContainer[0]
                
                xpos = -1 + 2 * curtime / self.tmax
                ypos = self.nfvalueContainer[0]

                
                
                
                vertices.append((xpos, ypos))
                # nf_line.setVertices(vertices)  # ok, we did the line.. now on to:
                replacement_line = visual.ShapeStim(self.win, vertices=vertices, closeShape=False, lineColor='lightblue', size=scaling)
                nf_line[0] = replacement_line
                
                cfb.setPos((xpos * scaling[0], ypos * scaling[1]))  # ok, so that was the NF stimulus
                # print(cfb.pos)
                
                # if patchi>0:
                # now comes fun part -- i.e. the patches.

                if ypos > self.thrContainer[0]:
                    ABOVE=True
                    
                    if ABOVE_PREV is True:
                        # just add one vertex..

                        if ypos > lastypos:
                            ypos_for_color = ypos
                        rnew, gnew, bnew = my_color_calculator(self.hb, self.he, thr, self.colorgap, ypos_for_color, 1, -1)   
                        self.patch_color = (rnew, gnew, bnew)                        
                                
                        patch_vert.pop()
                        patch_vert.append((xpos, ypos))
                        patch_vert.append((xpos, thr))
    
                        
                        # pdb.set_trace()
                        replacement = visual.ShapeStim(self.win, vertices=patch_vert, fillColor=self.patch_color, size=self.scaling, lineWidth=0)
                        # current_patch.setVertices(patch_vert)
                        patches[-1] = replacement
                        
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
                        
    
                        
                        # patches.append(visual.ShapeStim(self.win, vertices=patch_vert, closeShape=True, fillColor=self.patch_color, lineWidth =0, autoLog=False))
                        # make a totally NEW patch
                        newpatch = visual.ShapeStim(self.win, vertices=patch_vert, fillColor=self.patch_color, size=self.scaling, lineWidth=0)
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
                        
                        replacement=visual.ShapeStim(self.win, vertices=patch_vert, fillColor=self.patch_color, size=self.scaling, lineWidth=0)
                        patches[-1] = replacement
    
                    
                ABOVE_PREV=ABOVE

                
            if G['EX_INTERACTIONMODE'] == 'master':
                pass  # call staircase calculator now, that will make things ready for the next (feedback) step.

                
    pr['LineCalculations']=LineCalculations
        
        

    def LineCheck(G, st, CP):
        ''' This should just re-draw the line according to whatps in CP['Threshold'][0]
        '''
        thrline = st['thrline']  # set positions...
        for l in thrline:
            oldstart = l.start
            oldend = l.end
            l.start = (oldstart[0]  , CP['thrContainer'][0]) #* self.scaling[1])
            l.end = (oldend[0]      , CP['thrContainer'][0]) # * self.scaling[1])
    pr['LineCheck'] = LineCheck

        






    # we WILL start the thread to do this thing.
    class ThermoCalculations(threading.Thread):
        def __init__(self, G, st, CP):
            '''
            This will start up, for a period specified within the G, changes to the shapes for the LINESTIM type of NF
            '''
            
            super(ThermoCalculations, self).__init__()
            
            self.win = G['win']  # our window..
            self.tmax = G['EX_TFB']   # this is how long we should display the stimulus on screen.
            self.thrContainer = CP['thrContainer']  # this is the threshold -- probably also set by on_control_event...
            self.nfsignalContainer = CP['nfsignalContainer']  # so this will be set (hopefully) by the handle_control_event...
            self.scaling = G['EX_SCALING']  # to scale... implementation of pos to be done later..
            self.st = st  # this contains points to all the stimuli.
            self.patch_color = G['EX_THERMOCLIMS']
            self.colorgap = G['EX_COLORGAP']
            


            self.hb, self.he = G['EX_THERMOCLIMS']
            
            



        def run(self):
            ''' 1) (re-set) vertices of the line (i.e. add to them)
                2) update the position of the crosshair according to curvalue and time
                3) handle the patches, too.
            '''
    
    
            # print self.nfvalueContainer
            thrline = self.st['thermo_lines']  # set positions...
            for l in thrline:
                oldstart = l.start
                oldend = l.end
                l.start = (oldstart[0]  , self.thrContainer[0]) #* self.scaling[1])
                l.end = (oldend[0]      , self.thrContainer[0]) # * self.scaling[1])
                # print(l.pos)
            # drawing comes later.
            
    
            scaling=self.scaling

            curtime=0
            
            cl=clock.Clock()  # yeah...well, we make a second clock. should not be too off in seconds.
            while curtime < self.tmax:
                
                time.sleep(G['EX_PR_SLEEPTIME'])
                
                curtime=cl.getTime()
                
                # so, what is the y pos?
                ypos = self.nfsignalContainer[0]

                rnew, gnew, bnew = my_color_calculator(self.hb, self.he, self.thrContainer[0], self.colorgap, ypos, 1, -1)                

                # then, what is the color?

                thermo_thermometer_container = self.st['thermo_thermometer']
                thermocolor = (rnew, gnew, bnew)
                thermovert = [(coord[0] * scaling[0], coord[1] * scaling[1]) for coord in [(-0.25, -1), (0.25, -1), (0.25, ypos), (-0.25, ypos)]]
                
                
                
                replacement_thermo = visual.ShapeStim(self.win, lineWidth=1.5, lineColor='white', fillColor=thermocolor, vertices=thermovert)
                thermo_thermometer_container[0] = replacement_thermo


            if G['EX_INTERACTIONMODE'] == 'master':
                pass  # call staircase calculator now, that will make things ready for the next (feedback) step.



    pr['ThermoCalculations']=ThermoCalculations
    

    def ThermoCheck(G, st, CP):
        ''' This should just re-draw the line according to whatps in CP['Threshold'][0]
        '''
        thrline = st['thermo_lines']  # set positions...
        for l in thrline:
            oldstart = l.start
            oldend = l.end
            l.start = (oldstart[0]  , CP['thrContainer'][0]) #* self.scaling[1])
            l.end = (oldend[0]      , CP['thrContainer'][0]) # * self.scaling[1])
    
    pr['ThermoCheck'] = ThermoCheck


    



    # we WILL start the thread to do this thing.
    class SquareCalculations(threading.Thread):
        def __init__(self, G, st, CP):
            '''
            This will start up, for a period specified within the G, changes to the shapes for the LINESTIM type of NF
            '''
            
            super(SquareCalculations, self).__init__()
            
            self.win = G['win']  # our window..
            self.tmax = G['EX_TFB']   # this is how long we should display the stimulus on screen.
            self.thrContainer = CP['thrContainer']  # this is the threshold -- probably also set by on_control_event...
            self.nfsignalContainer = CP['nfsignalContainer']  # so this will be set (hopefully) by the handle_control_event...
            self.st = st  # this contains points to all the stimuli.
            self.colorgap = G['EX_COLORGAP']
            self.hb, self.he = G['EX_THERMOCLIMS']



        def run(self):
            ''' check the current value of Y --> then, change the color --> done!
            '''

            curtime=0
            square_to_be_colorized = self.st['square']
            
            cl=clock.Clock()  # yeah...well, we make a second clock. should not be too off in seconds.
            while curtime < self.tmax:
                
                time.sleep(G['EX_PR_SLEEPTIME'])
                
                curtime=cl.getTime()

                
                # so, what is the y pos?
                ypos = self.nfsignalContainer[0]  #this changes due to the other thread...
                

                rnew, gnew, bnew = my_color_calculator(self.hb, self.he, self.thrContainer[0], self.colorgap, ypos, 1, -1)                
                square_to_be_colorized.setFillColor((rnew, gnew, bnew), colorSpace='rgb')
                square_to_be_colorized.setLineColor('black')
                # then, what is the color?

                # square_to_be_colorized.fillColor = (rnew, gnew, bnew)

            if G['EX_INTERACTIONMODE'] == 'master':
                pass  # call staircase calculator now, that will make things ready for the next (feedback) step.




    pr['SquareCalculations']=SquareCalculations



    
    
    
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

#%% Run Trial Function
    
def runTrial(trialType, G, st, CP, ex):

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
        
        
        CP['CURRENTPART'][0] = part
        programs, tdur, stims, messages_start, messages_stop = ex[trialType][part]
        
        for message in messages_start:
            G['win'].callOnFlip(G['eh'].send_message,message)    

        if isinstance(tdur,list):  # in case we have set t using CP (control parameter)
            tdur=tdur[0]

        # start the program, if any:
        for pitem in programs:
            prhandle, instr = pitem
            
            if instr == 'start':
                # it's a thread -- stop it
                instance=prhandle(G, st, CP)
                instance.start()
            elif instr == 'stop':
                # it's a thread -- stop it, if it hasn't already.
                instance.stop()
                instance.join()
            elif instr == 'call':
                # it's a function -- just call it
                prhandle(G, st, CP)                    
                

    
        G['cl'].reset()
        while G['cl'].getTime() < tdur:
            for i, stim in enumerate(stims):
                
                if isinstance(stim, list):  # specifically for the patches..
                    #print(stim)
                    for p in stim:
                        p.draw()
                else:
                    stim.draw()
            G['win'].flip()  # here we send the message !!
            
        # now that the window flipping is done -- send 'end' markers directoy.
        for message in messages_stop:
            G['eh'].send_message(message)
        



#%% The Main
            
if __name__ == "__main__":

    

    
    class dummy_logger():
        def send_message(self, m):
            print(m)
    
    G['eh']=dummy_logger()
    

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
    

    
    if visual.globalVars.currWindow:
        visual.globalVars.currWindow.close()
    
    # our clock..
    G['cl']=clock.Clock()
    

    # G is global parameters...
    # CP is 'Control Parameters', i.e. for which-trial-next, etc.

    G['EX_GRAPHICSMODE'] = 'line'

    init_window(G)
    st=make_stimuli(G, CP)
    pr=init_programs(G, st, CP)
    ex=define_experiment(G, st, pr, CP)  # pr is passed to define_experiment, but then we won't need...
    
    
    if G['EX_TESTNFNOISE'] is True:
        nfsignalContainer=[0]
        nfsignal_gen=pr['GenTestSignal'](G, st, CP)  # this changes the nfsignal continuously...
        nfsignal_gen.start()
    

    for t_i in my_trial_sequence:
        trialType = my_trial_definitions[t_i]
        print(trialType)
        runTrial(trialType, G, st, CP, ex)  # this can be one 'tick'.
                                            # when things are run in full, call the 'close'. or 'endroutine'??




# check the grant..

