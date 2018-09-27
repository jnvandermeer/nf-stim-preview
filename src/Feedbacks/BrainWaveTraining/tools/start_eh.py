#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 14:27:56 2018

@author: johan
"""

import socket
import time
import multiprocessing
import os
# import glob
# import re

from psychopy import clock, parallel

from Feedbacks.BrainWaveTraining.tools.create_incremental_filename import create_incremental_filename

# from Feedbacks.BrainWaveTraining.tools.eventhandler import eventhandler


def start_eh(G):
    
    
    EVENT_destip=G['v']['EVENT_destip']
    EVENT_destport=G['v']['EVENT_destport']
    EVENT_LPTTrigWaitTime=G['v']['EVENT_LPTTrigWaitTime']
    EVENT_sendParallel=G['v']['EVENT_sendParallel']
    EVENT_sendTcpIp=G['v']['EVENT_sendTcpIp']
    EVENT_LPTAddress=G['v']['EVENT_LPTAddress']
    EVENT_sendLogFile=G['v']['EVENT_sendLogFile']
    EVENT_printToTerminal=G['v']['EVENT_printToTerminal']
    EVENT_printToTerminalAllowed=G['v']['EVENT_printToTerminalAllowed']
    
    mainClock=G['mainClock']
    MSGDICT=G['evcodes']
    LOG_PATHFILE_EVENT=G['v']['LOG_PATHFILE_EVENT']
    print('----')
    print(MSGDICT)
    print('EVENT_sendParallel is: ' + str(EVENT_sendParallel))
    print('----')
    
    eh=eventHandler(
        mainClock, 
        messagedict=MSGDICT,
        destip=EVENT_destip,
        destport=EVENT_destport,
        LPTAddress=EVENT_LPTAddress,
        LPTTriggerWaiting=EVENT_LPTTrigWaitTime,
        filename=LOG_PATHFILE_EVENT,
        sendParallel=EVENT_sendParallel, 
        sendTcpIp=EVENT_sendTcpIp, 
        sendLogFile=EVENT_sendLogFile,
        printToTerminal=EVENT_printToTerminal,
        printToTerminalAllowed=EVENT_printToTerminalAllowed  # only allow the stops, which are < 40.
        )

    

    print('----><----')
    print(eh)
    eh.start()
    # time.sleep(10)
    #print('<---><----')
    # eh.send_message('aud_l55')
    print('<---><----')
    print(eh)
    
    # return eh
    G['eh']=eh
    return(G)
    
    
    
    
    
    

class eventHandler(multiprocessing.Process):
    def __init__(self, 
                 clock, 
                 messagedict={},
                 destip='127.0.0.1', 
                 destport=6500, 
                 LPTAddress=0x0378,
                 LPTTriggerWaiting=0.005,
                 filename='log/triggerlog.log',
                 sendParallel=True, 
                 sendTcpIp=True, 
                 sendLogFile=True,
                 printToTerminal=True,
                 printToTerminalAllowed=[0, 256]
                 ):
        '''
        we check parallel port, network port, and a file here (and we use the
        logger to do all of that log stuff)
        '''
        
        super(eventHandler, self).__init__()
        
        self.messagedict=messagedict
        self.clock=clock
        self.sendParallel=sendParallel
        self.sendTcpIp=sendTcpIp
        self.sendLogFile=sendLogFile
        self.destip=destip
        self.destport=destport
        self.LPTAddress=LPTAddress
        self.LPTTriggerWaiting=float(LPTTriggerWaiting)
        self.printToTerminal=printToTerminal
        self.printToTerminalAllowed=range(printToTerminalAllowed[0], printToTerminalAllowed[1])

        
            
        self._queue = multiprocessing.Queue()
        
        self._timequeue = multiprocessing.Queue()
        
        self._shutdown = multiprocessing.Event()
        

        # try the dirty trick to put both logs in the same place.
        filename = os.path.join('..', filename)
        
        self.newLogFile = create_incremental_filename(filename)
        
        # print(self.newLogFile)
        
        print('logfile for markers: %s\n ' % self.newLogFile)
        # open up a log:
        # self.expLogger = logging.LogFile(newLogFile, logging.EXP) # the correct loglevel should be EXP!
        
        # time.sleep(10)
        


    def send_message(self,message):
        '''
        it'll put the message into the queue, to be processed by 'run'
        '''
        self._queue.put(message)
        self._timequeue.put(self.clock.getTime())
        
        
    def run(self):
        '''
        This part runs - with a copy of memory upon its creation - in the separate process
        So it should just look at the queue, see if something's up, and send
        a trigger when it does.
        '''
        
        # do some while loop, checking for messages, and when one arrives -->
        # process it with both logfile (possibly) and with sending parallel
        # and also with.
        
        print('___->' + __name__)
        
        print(self.clock.getTime())
                # do we even have a parallel port?

        #print('---------')
        #print('---------')
        #print('AT START OF RUN')
        #print('---------')
        #print('---------')
                

        print(self.LPTAddress)
                
        try:
            self._port=parallel.ParallelPort(self.LPTAddress)
            self._port.setData(0)  # this is the 'reset' to 0
            self._port_doreset=False  # once done we shouldn't do it..
            self._port_waitttime=0.005  # wait 5 msec after a trigger..
            
        except OSError:
            self._port=None
            self._port_doreset=False
            self._port_waitttime=None
            print('OS Does not seem to have a parallel port')
            # deactivate our parallel...
            self.sendParallel=False
        

        # so that's the logfile -- open op the socet, too:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         
        
        to_be_lpted=[]  # we start off empty here.
        to_be_written=[]  # for sending it to a file.
        to_be_written_messages=[]
        lpt_decay_clock=clock.Clock()
        code_sending_in_progress=False
        send_last_one=False
        
        
        
        if self.sendLogFile:
            expLogger = open(self.newLogFile,'w')  # , logging.EXP)
            print('Opened: %s\n' % expLogger)

        
        while not self._shutdown.is_set():
            
            time.sleep(0.0005) # take it easy on the CPU
            
            while not self._queue.empty():
                
                
                try:

                    
                    message =  self._queue.get()
                    senttime = self._timequeue.get()  # I want to check how long it takes to deal with the queue like this.
                    code_to_send=self.messagedict[message]
                    
                
                except:
                    
                    print('That code doesn\'''t exist: %s\n' % message)
                    break
                    
                
                # print(message)
                # print(code_to_send)
                if self.sendParallel:
                    
                    # put em into our to-be-sent-by-lpt list:
                    
                    to_be_lpted.append(code_to_send)
                    # self._port.setData(code_to_send)
                    
                    # following code is to reset to 0 of the LPT code output, after X msec.
                    # only evaluate if the queue is empty == dealing with the latest marker.
                    #if self._queue.empty():
                    #    lasttime=self.clock.getTime()
                    #    self._port_doreset=True
                        
                
                if self.sendTcpIp:
                    
                    # this is ultra-fast -- so no need to deal with this later.
                    self.sock.sendto(unicode(code_to_send), (self.destip, self.destport))

                    
                if self.sendLogFile:
                    
                    # might be slow - better make sure all codes are sent first
                    to_be_written.append(code_to_send)
                    to_be_written_messages.append(message)

                    
                    
            # heretime2=self.clock.getTime()
            # print('code: %d\t time sent: %.6f time logged: %.6f, diff = %.6f' % (code_to_send, senttime, heretime2, heretime2-senttime))
            # print('writing stuff took: %.3f msec' % ((heretime2-heretime)*1000));
            if self.sendParallel:   # avoid jamming up and missing triggers -- at the cost of making sure some temporal inaccuracy.
                                    # IF not too many codes to send out, things should work out. 
                if  not code_sending_in_progress and len(to_be_lpted) > 0:
                    tmpcode=to_be_lpted.pop(0)
                    self._port.setData(tmpcode)
                    lpt_decay_clock.reset()   # reset the clock...    
                    code_sending_in_progress=True
                    if len(to_be_lpted) == 0:  # after popping, see if we need to send the mast one.
                        send_last_one = True  # so send the last one (as 0)


                if not code_sending_in_progress and send_last_one:
                    self._port.setData(0)
                    lpt_decay_clock.reset()   # reset the clock...    
                    send_last_one=False
                    code_sending_in_progress=True

                if code_sending_in_progress and lpt_decay_clock.getTime() > self.LPTTriggerWaiting:
                    code_sending_in_progress=False  # so we can move on to the next code.
                    
                 
            if self.sendLogFile:
                
                if len(to_be_written) > 0:
                    # print(to_be_written)
                    wtmpcode = to_be_written.pop(0)
                    wtmpcode_message = to_be_written_messages.pop(0)
                
                    heretime=self.clock.getTime()

                    # simplified logfile for data analysis:
                    simplestr = '%.6f\t%.6f\t%.6f\t%d\n' % (senttime, heretime, heretime-senttime, wtmpcode)
                    expLogger.write(simplestr)
                    
                    # a more in-depth log of what was going on:
                    # logging.data(mystr)  # and write it to the psychopy main logifles, too.
      
                    if self.printToTerminal:
                        if wtmpcode in self.printToTerminalAllowed:
                            mystr = 'code: %d, message was: %s\ttime sent: %.6f time logged: %.6f, diff = %.6f' % (wtmpcode, wtmpcode_message, senttime, heretime, heretime-senttime)
                            print(mystr)
                    


                    
        #            # this is onlyt true if port needs to be reset, otherwise leave as-is.
        #            if self.sendParallel and self._port_doreset:
        #                # check the time - 10msec passed?
        #                if (self.clock.getTime() - lasttime) > self._port_waitttime:
        #                    self._port.setData(0)
        #                    self._port_doreset=False

        # at the end of the while loop, we have set the shutdown event - so do it.                    
        if self.sendLogFile:
            # give our system a little bit of time to actually write the file:
            time.sleep(1)
            expLogger.close()
            print('Closed: %s\n' % expLogger)

            
            

    def shutdown(self):
        ''' 
        get rid of this process -- call join later on from the main process
        '''
        # also - send triggers via our network connection towards
        if not self._shutdown.is_set():
            self._shutdown.set()
        else:
            print('already shut down!')
            

    # time.slee       
            
if __name__ == "__main__":
    
    # to test whether the LPT sends -- and it does!
    d={'a':1, 'b':2, 'c':101}
    cl=clock.Clock()
    
    
    cl=clock.Clock()
    eh=eventHandler(d,cl)   

    # time.sleep(0.5)
    
    print(cl.getTime())
    
    print('hallo!!!')
    
    ev=eventHandler(d,cl)
    # time.sleep(10)
    ev.start()
    print('event hander started')
    
    for x in range(10):
        ev.send_message('a')
        ev.send_message('b')
        ev.send_message('c')
        time.sleep(0.5)

    ev.shutdown()
    
    ev.join()
    
    print('done')