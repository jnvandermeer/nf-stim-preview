#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 14:27:56 2018

@author: johan
"""



def init_eventcodes(G):
    MSGDICT={
            
            # general
            'instruction':1,

            'bFB':2,
            'eFB':3,
            
            'XorV':4,
            
            'bISI':5,
            'eISI':6,

            # specific for the trial type
            'irest':11,
            'brest':12,
            'erest':13,
            'bisirest':14,
            'eisirest':15,

            'iobserve':21,
            'bobserve':22,
            'eobserve':23,
            'bisiobserve':25,
            'eisiobserve':26,

            'itrain':31,
            'btrain':32,
            'etrain':33,
            'xorvtrain':34,
            'bisitrain':35,
            'eisitrain':36,
            
            'itransfer':41,
            'btransfer':42,
            'etransfer':43,
            'xorvtransfer':44,
            'bisitransfer':45,
            'eisitransfer':46,
            
            
            'recv_nfsignal':101,
            'recv_thr':102,
            'recv_corr_incorr':103,
            
            
    }        
            
            
    
        
    LOG_PATHFILE_EVENT=G['v']['LOG_PATHFILE_EVENT']
    
    # LOG_PATHFILE_EVENT = create_incremental_filename(LOG_PATHFILE_EVENT)
    # another check...
    #if __name__ != "__main__":
    #    EVENT_TRIGLOG = os.path.join(os.path.dirname(os.path.realpath(__file__)),EVENT_TRIGLOG)
    
    # required fields..
    G['evcodes']=MSGDICT
    
    # this too...
    G['LOG_PATHFILE_EVENT']=LOG_PATHFILE_EVENT
    
    
    
    # we can also start up the event handler, and give the pointer to that in G['eh'], and then return it, right?
    
    
    
    
    
    
    return(G)