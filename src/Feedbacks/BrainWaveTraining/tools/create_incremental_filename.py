#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 09:49:52 2018

@author: johan
"""
import inspect
import os
import glob



def getCallsite():
    """Return a string representing where the function was called from in the form 'filename:linenumber'"""
    _, filename, linenumber, _, _, _ = inspect.stack()[2]
    pathname = os.path.abspath(filename)
    # print(dir(filename))
    return pathname

    



def create_incremental_filename(filename):
    ''' this function allows you to come up with a logdir and a logname, and it will
    create a directory for you if it doen't exist. And if it does, it'll look into 
    it and figure out if there are any files there already mathcing your description
    and if there are, it'll come up with a new filename with a new counter
    ... so this is useful to never over-write an existing (log) filename
    '''

    
    # print(self.clock.getTime())
    # check whether there's another logfile - in log directory
    # make efl_triggers version of it, too.
    logdir=os.path.dirname(filename)  # the logdir you want!
    
    caller_full_path_and_file = getCallsite()
    caller_justpath = os.path.dirname(caller_full_path_and_file)
    
    
    logdir = os.path.join(caller_justpath, logdir)
    
    
    # if __name__ != "__main__":
    #     logdir = os.path.join(os.path.dirname(os.path.realpath(__file__)),logdir)

    # this function is called by some other function, 

    
    logbasename, ext = os.path.splitext(os.path.basename(filename))

   
    # figure out if there's a log directory, if not --> make it:
    if not os.path.exists(logdir):
        print('logdir does not exist -- making one!')
        os.makedirs(logdir)
    
    # figure out which files reside within this logfile directory:
    if len(glob.glob(logdir + os.sep + logbasename + "*" + ext)) == 0:
        logcounter=0
    else:
        # figure out biggest number:
        matches=[match for match in [re.match(logbasename+'([0-9]*)'+ext,item) for item in os.listdir(logdir)]]
        newlist=[]
        for match in matches:
            if match is not None:
                newlist.append(match.group(1))
        logcounter = max([int(n) for n in newlist])
                
                
    
    # so make just another logfile on top of this one -- it'll be timestamped    
    logcounter += 1
    
    # this is the new logfile:
    newLogFile=os.path.join(logdir,logbasename+'%d'%logcounter + ext )
    
    # print(self.newLogFile)
    
    # print('logfile for markers: %s\n ' % self.newLogFile)
    return newLogFile
    # open up a log: