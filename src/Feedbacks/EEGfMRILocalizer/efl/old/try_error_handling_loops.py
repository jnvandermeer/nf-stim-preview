#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 23:05:47 2018

@author: johan
"""

import trollius as asyncio
from trollius import From
import traceback


@asyncio.coroutine
def run_division(a, b):
    while True:
        print  a / b
        yield From(asyncio.sleep(2))


def custom_exception_handler(loop, context):
    # first, handle with default handler
    # loop.default_exception_handler(context)

    pass
#    exception = context.get('exception')
#
#    if exception:
#    
#        print('hallo!')
#
#        tb = traceback.format_exc()
#        print tb
#        
#        with open('exception','w') as f:
#            f.write('hallo!!!')
#
#        
#        tb = traceback.format_exc()
#        print tb
#        #if isinstance(exception, ZeroDivisionError):
#        print(context)
#        print(exception)
#        # loop.stop()

loop = asyncio.get_event_loop()

# Set custom handler
loop.set_exception_handler(custom_exception_handler)

tasks = [asyncio.async(run_division(1, 0))]
loop.run_until_complete(asyncio.wait(tasks)) 
    
    