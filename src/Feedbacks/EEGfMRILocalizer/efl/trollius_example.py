# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 15:48:44 2018

@author: User
"""

import trollius as asyncio
from trollius import From


@asyncio.coroutine
def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print("Task %s: Compute factorial(%d)..." % (name, i))
        yield From(asyncio.sleep(1))
        f *= i
    print("Task %s completed! factorial(%d) is %d" % (name, number, f))

loop = asyncio.get_event_loop()
tasks = [
    asyncio.async(factorial("A", 8)),
    asyncio.async(factorial("B", 3)),
    asyncio.async(factorial("C", 4))]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()