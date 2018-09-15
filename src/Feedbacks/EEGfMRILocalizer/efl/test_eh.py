# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 20:45:57 2018

@author: User
"""

import psychopy
import eventhandler
from psychopy import clock

if __name__ == "__main__":
    eh=eventhandler.eventHandler({'a':1,'b':2},clock.Clock())

    eh.start()

    eh.send_message('a')
