


# use frames to figure out the timings, so in the 'main' something like:


# figure out display Refresh Rate

# Visual
# use the VisualTimings --> obtain frame-by-frame the (numbered) contents of the Window, as far as Visual is concerned. 
#   The number coincideswith the elements created by VisualCreateStims, so they work in tandem
# use the VisualCreateStims --> obtain the window elements that will be drawn
# this solves the issue regarding Visual


# Audio
# use a function to return an object --> which is runnable as a Process.
# you input into this process the framenumber, and internally it'll determine whether audio should run or not (and which one).


# Go NoGo
# Like Visual, use a GoNogoTimings function to obtain a dict of which should run which frame
# Create the GoNogoCreateCases to populate this array with behaviors --> which will be considered within the main loop.
# Inside the main loop, python should ALSO:
#   - monitor the event.getKeys() to change the visual contents + record presses, etc.
#   - use the staircases to adjust the visual contents (timings) dpeending on behavior(s)



# within main loop:
# update Frame Number
# get visual contents according to frame number
# pass on the frame number Audio Process
# obtain behavior from Go NoGo Dict
# if behavior == Pre, fill with Pre
# if behavior == Jitt, fill with Jitt


# Control the flow according to 
# if behavior is not Go and prev behavior = Go:
    # if not keypressed --> error of Omission
    
# if behavior is not Stop and prev behavior = Stop,
# keypressed = 0
# FrameCounter = -1

# if behavior is not Stop and prev behavior = Stop,
# keypressed = 0
# FrameCounter = -1


# if behavior is Go && behavior prev trial is not Go:
#       FrameCounter = 0
#       Keypressed = 0
# else
#       FrameCounter += 1

# if behavior is Stop && behavior prev trial is not Stop:
#       FrameCounter = 0
#       Keypressed = 0
# else
#       FrameCounter += 1


# capturing keys:
# if behavior == Go or behavior == Stop
#   if event.getkeys()
        #keytpressed=1;
    
    



# some logic(s) over here: --> GO Stimulus:
#
# if behavior == Go & FrameCounter >= 0 & not KeyPressed
#       visual == Go
# else
#        visual == blank


# NOGO Stimulus
# if behavior == Stop & not keypressed
#   if FrameCounter < CurrentStopTime (lookup from init)
#       Normal Arrow
#   else
#       Red Arrow


# if behavior == Stop & Keypressed
#   keypressed = 1
#   visual == Fixation
#   LOG --> which frame, + which FrameCounter
#   LOG --> Error of Commission
#
