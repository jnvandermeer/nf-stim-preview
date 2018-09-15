#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 15:30:15 2018

@author: johan
"""

from psychopy import visual
vstims=dict()
sstims=dict()
radialFreq=6
angleFreq=6
checkerSize=1.5
cicleSize=checkerSize/12*2
stimSize=checkerSize/12*1.5


checkr=visual.RadialStim(win, tex='sqrXsqr', ori=0, size=checkerSize, 
                     visibleWedge=(0, 181),
                     angularCycles=angleFreq, radialCycles=radialFreq)


checkrf=visual.RadialStim(win, tex='sqrXsqr', ori=-90, size=checkerSize, 
                     visibleWedge=(90, 271),
                     angularCycles=angleFreq, radialCycles=radialFreq)


checkl=visual.RadialStim(win, tex='sqrXsqr', ori=0, size=1.5, 
                     visibleWedge=(180, 360),
                     angularCycles=angleFreq, radialCycles=radialFreq)


checklf=visual.RadialStim(win, tex='sqrXsqr', ori=90, size=1.5, 
                     visibleWedge=(90, 271),
                     angularCycles=angleFreq, radialCycles=radialFreq)

circ=visual.Circle(win, radius=cicleSize, fillColor=[0,0,0], lineColor=[0, 0, 0])

fa=.1;fb=1
fixationVert = [(fa, fa),(fa, fb),(-fa, fb),(-fa, fa),(-fb, fa),(-fb, -fa),
                (-fa, -fa),(-fa, -fb),(fa, -fb),(fa, -fa),(fb, -fa), (fb, fa)]
fixation = visual.ShapeStim(win, vertices=fixationVert, fillColor='red', 
                         size=.025, ori=0, lineColor='red')


vstims['r']=[checkr, circ, fixation]
vstims['rf']=[checkrf, circ, fixation]
vstims['l']=[checkl, circ, fixation]
vstims['lf']=[checklf, circ, fixation]


stimcirc1=visual.Circle(win, radius=stimSize, fillColor=[1, 1, 1], lineColor=[1, 1, 1])
stimcirc2=visual.Circle(win, radius=stimSize/1.5*1.37, fillColor=[0, 0, 0], lineColor=[1, 1, 1])


#al=visual.ImageStim(win, image=u'stims/arrow.png')

arrowPinch=1.75;
arrowVert = [(-0.7071, -0.7071/arrowPinch), (0, -0.7071/arrowPinch),
              (0, -1), (1, 0),
              (0, 1),(0, 0.7071/arrowPinch), 
              (-0.7071, 0.7071/arrowPinch)]

arrowl = visual.ShapeStim(win, vertices=arrowVert, fillColor='white', 
                         size=.095, ori=180, lineColor='white')

arrowr = visual.ShapeStim(win, vertices=arrowVert, fillColor='white', 
                         size=.095, ori=0, lineColor='white')

arrowlr = visual.ShapeStim(win, vertices=arrowVert, fillColor='darkred', 
                         size=.095, ori=180, lineColor='darkred')

arrowrr = visual.ShapeStim(win, vertices=arrowVert, fillColor='darkred', 
                         size=.095, ori=0, lineColor='darkred')


sstims['pre']=[stimcirc1, stimcirc2, fixation]
sstims['fix']=[fixation]

sstims['al']=[stimcirc1, stimcirc2, arrowl]
sstims['ar']=[stimcirc1, stimcirc2, arrowr]
sstims['alr']=[stimcirc1, stimcirc2, arrowlr]
sstims['arr']=[stimcirc1, stimcirc2, arrowrr]

