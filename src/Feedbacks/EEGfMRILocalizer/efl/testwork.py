# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 10:47:52 2018

@author: User
"""


TVAR='bla'


G=dict()
G['bla']=1



def test1():
    print(TVAR)
    

def test2(G):
    print(TVAR)
    print(G['bla'])
    

test1()
test2(G)
