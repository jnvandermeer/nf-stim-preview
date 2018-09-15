#!/usr/bin/env python

""" Copyright (c) 2010 Torsten Schmits

This file is part of the pyff framework. pyff is free software;
you can redistribute it and/or modify it under the terms of the GNU General
Public License version 2, as published by the Free Software Foundation.

pyff is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA  02111-1307  USA

"""

import logging

from Feedbacks.RSVPSpeller.control import Control

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    c = Control()
    c.on_init()
    c.on_play()
