#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 14:21:18 2018

@author: johan
"""

from psychopy import visual, clock, data, event, logging, sound, monitors


def init_screen(G):
    MONITOR_WIDTH=G['v']['MONITOR_WIDTH']
    MONITOR_DISTANCE=G['v']['MONITOR_DISTANCE']
    MONITOR_PIXWIDTH=G['v']['MONITOR_PIXWIDTH']
    MONITOR_PIXHEIGHT=G['v']['MONITOR_PIXHEIGHT']
    MONITOR_NSCREENS=G['v']['MONITOR_NSCREENS']
    MONITOR_USEDEGS=G['v']['MONITOR_USEDEGS']
    MONITOR_DISPLAYONSCREEN=G['v']['MONITOR_DISPLAYONSCREEN']
    MONITOR_FLIPHORIZONTAL=G['v']['MONITOR_FLIPHORIZONTAL']
    MONITOR_FLIPHORIZONTAL=G['v']['MONITOR_FLIPHORIZONTAL']
    RECORDFRAMEINTERVALS=G['v']['MONITOR_RECORDFRAMEINTERVALS']
    MONITOR_FULLSCR=G['v']['MONITOR_FULLSCR']
    MONITOR_ALLOWGUI=G['v']['MONITOR_ALLOWGUI']
    MONITOR_FPS=G['v']['MONITOR_FPS']
    
    mon = monitors.Monitor('current', width=MONITOR_WIDTH, distance=MONITOR_DISTANCE, gamma=None)
    # mon.setDistance(MONITOR_DISTANCE)  # in CM
    # mon.setWidth(MONITOR_WIDTH)  # in cm?
    mon.setSizePix((MONITOR_PIXWIDTH,MONITOR_PIXHEIGHT))  # an INT?
    
    # in win definition, monitor=mon
    # in shapes definition; setSize((x, y), units='deg')  ## then use that...
    #
    #	SCREEN_SIZE = (1440,900)        
    #	win0 = visual.Window(SCREEN_SIZE, monitor='Monitor_00', screen=0, fullscr=False, allowGUI=True,winType='pyglet')
    #        win1 = visual.Window(SCREEN_SIZE, monitor='Monitor_01', screen=1, fullscr=False, allowGUI=True,winType='pyglet')
    #        win2 = visual.Window(SCREEN_SIZE, monitor='Monitor_02', screen=2, fullscr=False, allowGUI=True,winType='pyglet')
    #
    #        # the TRICK == to then close win1.
    #        # win0 is (always?) the window which is where the main Desktop UI resides
    #        self.win=win0
    #        win1.close()
    #        win2.close()
    #        print('PsychoPy initialized')
    
    
    tmpwin=[]
    for i in range(MONITOR_NSCREENS):
        
        if MONITOR_USEDEGS is True:
            tmpwin.append(visual.Window(size=(MONITOR_PIXWIDTH,MONITOR_PIXHEIGHT), fullscr=MONITOR_FULLSCR, screen=int(i+1), allowGUI=MONITOR_ALLOWGUI, winType='pyglet', waitBlanking=False, monitor=mon, units='deg', autoLog=False))
        else:
            tmpwin.append(visual.Window(size=(MONITOR_PIXWIDTH,MONITOR_PIXHEIGHT), fullscr=MONITOR_FULLSCR, screen=int(i+1), allowGUI=MONITOR_ALLOWGUI, winType='pyglet', waitBlanking=False))
        
    # we pick the screen.    
    win=tmpwin[MONITOR_DISPLAYONSCREEN-1]
    # and close off the other screens.
    for i in range(MONITOR_NSCREENS):
        if i != (MONITOR_DISPLAYONSCREEN-1):
            tmpwin[i].close()
    
    
    if MONITOR_FLIPHORIZONTAL is True and MONITOR_FLIPHORIZONTAL is False:
        win.viewScale = (-1, +1)
    if MONITOR_FLIPHORIZONTAL is False and MONITOR_FLIPHORIZONTAL is True:
        win.viewScale = (+1, -1)
    if MONITOR_FLIPHORIZONTAL is True and MONITOR_FLIPHORIZONTAL is True:
        win.viewScale = (-1, -1)
    # don't touch the False and False, since that's the default setting..
    
    
    win.recordFrameIntervals = RECORDFRAMEINTERVALS  # record frame intervals...
    FPS=MONITOR_FPS  # frames per second of your screen
    # access with: win.frameIntervals
    G['win']=win
    return(G)