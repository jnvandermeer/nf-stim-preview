#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 18:14:19 2018

@author: johan
"""

import copy

def convert_to_fd_vis(FPS=60, VIS_SHOWOPPOSITE=False, VIS_checkerSpeedMultiplier=1.0):
    ''' 
    Convert the list of times into the frame-dict telling which frame should display what
    So it is a list of stuff; 
    1st value = the frame
    2nd value = the contents (l, lf, r or rf)
    3rd value = the marker(s) to be sent out later on -- defined in efl_v3.py
    '''

    complete_fd_list=[]

    visl=['l','lf']
    visr=['r','rf']
    
    runr8=False
    runr13=False
    runl8=False
    runl13=False
    flipr=False
    flipl=False
    trunr8=0
    trunr13=0
    trunl8=0
    trunl13=0
    viscontents=[]
    m_startstop=''
    
    
    
    
    vis_stim_list = [[17.5,35.,'video',['left','8']],[135.,145.,'video',['left','8']],[280.,290.,'video',['left','8']],[87.5,105.,'video',['left','13']],[217.5,235.,'video',['left','13']],[320.,330.,'video',['left','13']],[52.5,70.,'video',['right','8']],[155.,165.,'video',['right','8']],[300.,310.,'video',['right','8']],[115.,125.,'video',['right','13']],[182.5,200.,'video',['right','13']],[252.5,270.,'video',['right','13']]]
    vis_times={'8':[x * 1./VIS_checkerSpeedMultiplier for x in [0.111, 0.253,0.373,0.475, 0.600]],'13':[x * 1./VIS_checkerSpeedMultiplier for x in [0.078,0.151,0.214,0.300,0.376,0.442,0.525,0.600]]}
    # there are 4 possible visual stims that can be drawn -- L, LF, R and RF

    TOTFRAMES=int(340/(1./FPS));
    
    fd=[]
    for i in range(TOTFRAMES):
        
        
        if runr8:
            if trunr8 > ttimer8:
                evcode2='r8'
                flipr=True
                if len(htrunr8)>0:
                    ttimer8=htrunr8.pop(0)
                else:
                    runr8=False
            trunr8+=1./FPS



        if runr13:
            if trunr13 > ttimer13:
                evcode2='r13'
                flipr=True
                if len(htrunr13)>0:
                    ttimer13=htrunr13.pop(0)
                else:
                    runr13=False
            trunr13+=1./FPS



        if runl8:
            if trunl8 > ttimel8:
                evcode2='l8'
                flipl=True
                if len(htrunl8)>0:
                    ttimel8=htrunl8.pop(0)
                else:
                    runl8=False
            trunl8+=1./FPS   
         

        if runl13:
            if trunl13 > ttimel13:
                evcode2='l13'
                flipl=True
                if len(htrunl13)>0:
                    ttimel13=htrunl13.pop(0)
                else:
                    runl13=False
            trunl13+=1./FPS
            
        if not runl8 or not runl13 or not runr8 or not runl13:
            real_ev_code=''
            
      
        # reset the timings -- we need it
        if not runr8 and trunr8>0:
            trunr8=0
            
        if not runr13 and trunr13>0:
            trunr13=0
            
        if not runl8 and trunl8>0:
            trunl8=0
            
        if not runl13 and trunl13>0:
            trunl13=0
            
        
        
        ftime=i*(1.0/FPS)
        # print(vis_stim_list)
        for item in vis_stim_list:
            (tstart, tstop, modality, (lr, frequency)) = item

            if ftime > tstart and ftime < tstop:
                if lr is 'right' and frequency is '8':
                    if not runr8:
                        runr8=True
                        trunr8=0
                        htrunr8=copy.deepcopy(vis_times['8'])
                        ttimer8=htrunr8.pop(0)
                        evcode='r8'

                if lr is 'right' and frequency is '13':
                    if not runr13:
                        runr13=True
                        trunr13=0
                        htrunr13=copy.deepcopy(vis_times['13'])
                        ttimer13=htrunr13.pop(0)
                        evcode='r13'

                if lr is 'left' and frequency is '8':
                    if not runl8:
                        runl8=True
                        trunl8=0
                        htrunl8=copy.deepcopy(vis_times['8'])
                        ttimel8=htrunl8.pop(0)
                        evcode='l8'

                if lr is 'left' and frequency is '13':
                    if not runl13:
                        runl13=True
                        trunl13=0
                        htrunl13=copy.deepcopy(vis_times['13'])
                        ttimel13=htrunl13.pop(0)
                        evcode='l13'



        oldviscontents=viscontents
        
        viscontents=[]
        if runl8 or runl13:
            viscontents.append(visl[0])
            if VIS_SHOWOPPOSITE is True:
                viscontents.append(visr[0])


        if runr8 or runr13:
            if VIS_SHOWOPPOSITE is True:
                viscontents.append(visl[0])
            viscontents.append(visr[0])


        evcode=''
        if viscontents != oldviscontents:
            if runr8:
                evcode='r8'
            elif runr13:
                evcode='r13'
            elif runl8:
                evcode='l8'
            elif runl13:
                evcode='l13'
            
        # print([i, viscontents, runr8, runr13, runl8, runl13, trunr8, trunr13, trunl8, trunl13, flipr, flipl, evcode])

        complete_fd_list.append([i, viscontents, runr8, runr13, runl8, runl13, trunr8, trunr13, trunl8, trunl13, flipr, flipl, evcode])
        fd.append(viscontents)
       
        if flipl:
            visl=visl[::-1]
            flipl=False

        if flipr:
            visr=visr[::-1]
            flipr=False


    
    #print(len(fd))
    #print(len(complete_fd_list))





    

    prev=[];
    started=False
    begun=False
    bigmat=[]
    for i, stims in enumerate(fd):
        
        marker=''
        if len(stims) != len(prev):
            signal=True
            
            if not begun:
                begun=True
                mtype=complete_fd_list[i][-1];
                marker='b'+mtype
            else:
                begun=False
                marker='e'+mtype
           
            # print(signal)
            # print(marker)
            
            prev=stims
            
        markerlist=[]
        if len(complete_fd_list[i][-1]) > 0:
            markerlist.append(complete_fd_list[i][-1])
        if len(marker) > 0:
            markerlist.append(marker)
            
        # now -- write em!
        bigmat.append([i, stims, markerlist])

        

    return bigmat


if __name__ == '__main__':
    l=convert_to_fd_vis(FPS=60, VIS_SHOWOPPOSITE=True)