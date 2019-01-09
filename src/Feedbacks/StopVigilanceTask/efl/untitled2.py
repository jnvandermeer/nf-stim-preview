# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 21:04:15 2018

@author: User
"""

import eventhandler
from psychopy import clock
import time



def start_event_handler():

    
    print('hallo!')
    
    eh=eventhandler.eventHandler({'a':1,'b':2},clock.Clock())
    
    print(eh.is_alive())
    
    print('hallo!')
    eh.start()
    print(eh.is_alive())
    
    for i in range(10):
        eh.send_message('a')
        print(eh.is_alive())
        time.sleep(0.5)
    eh.shutdown()
    
    return eh
    
    
    