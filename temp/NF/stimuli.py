# -*- coding: utf-8 -*-



#%% window..
# getting the window right:
from psychopy import visual
import numpy as np
# getting the window
win=visual.Window(size=(1400,900), fullscr=False, screen=0, allowGUI=True, winType='pyglet', waitBlanking=False)


#%% Generate the stimuli

# making the dashed line -- for the stimulus, we can set autodraw optially to true for this one.
def make_dashed(win, b, e, N, d):
    lines=[]
    b=(float(b[0]),float(b[1]))
    e=(float(e[0]),float(e[1]))
    # diff=(e[0]-b[0], e[1]-b[1])
    # print(diff/float(N)*d)
    # scaling:
    if b[0]==0 and e[0]==0:
        scalingx=0
    else:
        scalingx = (e[0]-b[0]) / (e[0] - (e[0]-b[0])/float(N)*(1-d) - b[0])
    if b[1]==0 and e[1]==0:
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
        
        lines.append(visual.Line(win, start=(xposb, yposb), end=(xpose, ypose)))
    return lines
        
# the dotted line:
lines=make_dashed(win, (-1, 0), (1, 0), 20, 0.5)


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
import random

ypos=[0.6+random.random()*0.2 for i in range(100)]
times=[1+random.random()/4 for i in range(100)]
tpos=[sum(times[:-i-1:-1]) for i in range(len(times))]

tpos_max = max(tpos)
xpos = [-1 + 2*t/tpos_max for t in tpos]

nf_vertices = []
for i, t in enumerate(ypos):
    nf_vertices.append((xpos[i], ypos[i]))

nf_line = visual.ShapeStim(win, vertices=nf_vertices, closeShape=False, lineColor='lightblue')



# the vertices for 'correct':
vert_correct=np.loadtxt('stim/vert_correct.txt')
st_correct_color='#5fd35f'
st_correct = visual.ShapeStim(win, vertices=vert_correct, closeShape=True, size=stimSize, fillColor=st_correct_color, lineWidth =0, autoLog=False)

vert_incorrect=np.loadtxt('stim/vert_incorrect.txt')
st_incorrect_color='#eb2c00';
st_incorrect = visual.ShapeStim(win, vertices=vert_incorrect, closeShape=True, size=stimSize, fillColor=st_incorrect_color, lineWidth =0, autoLog=False)






items=[background, st_correct, st_incorrect, arrowup, donotreg, nf_line]
for l in lines:
    items.append(l)
items.append(cfb)
    




# scale it:
for i in items:
    oldsize=i.size
    i.setSize((oldsize[0]*0.5, oldsize[1]*0.5))

# draw..
for i in items:
    i.draw()
win.flip()    
    


#%% now, make the workflow...
