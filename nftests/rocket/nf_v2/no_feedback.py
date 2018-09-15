#!/usr/bin/env NF_test

"""
This is the script for creating the rocket feedback for
NF experiment. This is a demo with a dummy variable for
calculating the speed of the rocket - this will be done
in future with the input from the EEG power spectrum
(e.g. theta band power)
"""

import pygame as pg
import random

## constants ##

WHITE = [255, 255, 255]
BLACK = [  0,   0,   0]
GREY  = [192, 192, 192]


def main():



	## Initialise ##
	pg.init()
	start_time = pg.time.get_ticks()
	done = False
	w, h = 1200, 900
	screen = pg.display.set_mode((w, h))
	screenrect = screen.get_rect()
	
	surface = pg.Surface((w, h), pg.SRCALPHA)	

	foreground=BLACK
	background=WHITE

	## Message ##
	
	def message(screen):
		text = "Prepare for liftoff!"
		font = pg.font.SysFont("liberationserif", 56)

		image = font.render(text, True, foreground)
        	rect = image.get_rect()
        	rect.center = screen.get_rect().center
	
		screen.fill(background)
		screen.blit(image, rect)
		pg.display.flip()
	
	## Cross ##
	
	def cross(scr, surf):
		c1 = pg.draw.line(surf, foreground, (w/4,5*h/6),
                        (3*w/4, h/6), 10)
        	c2 = pg.draw.line(surf, foreground, (3*w/4,5*h/6),
                        (w/4, h/5), 10)
		scr.fill(background)
		scr.blit(surf, (0, 0))
		pg.display.flip()
		
	
	## Rocket ##

	def rocket(scr, surf, srect):
		l1 = pg.draw.line(surf, [255,255,255], (w /3, 5*h/6),
			(2*w/3, 5*h/6), 4) #lower line
		l2 = pg.draw.line(surf, [255,255,255], (w /3, h/6),
			(2*w/3, h/6), 4) #upper line
		bg = pg.image.load('data/background.png').convert()
		rkt = pg.image.load('data/01_rocket.png').convert_alpha()
		pos = rkt.get_rect(center=srect.center)
		pos = pos.move(0, random.randint(-10,10)) #random variable here is a dummy for the input from EEG power band
                #draw bg, rocket and lines
		scr.blit(bg, (0, 0))
		scr.blit(surf, (0, 0))
		scr.blit(rkt, pos)
                pg.display.update()
                pg.time.delay(100)
                
                #collision detection
                if l1.colliderect(pos):
                        return #do something if hits bottom line
                if l2.colliderect(pos):
                        return #do something if hits top line



	## ~~~ Main ~~~ ##

	while 1:
		#initiate timer
		time = (pg.time.get_ticks() - start_time)/1000 #seconds
		
		## Display Message ##
		if time < 5:
			message(screen)
		
		## Cross ##
		if 5 <= time < 7:
			cross(screen, surface)
		
		## Blank Screen ##
		if 7 <= time < 9:
			screen.fill(background)
			pg.display.update()

		## Rocket Feedback ##
		if 9 <= time < 17:
			rocket(screen, surface, screenrect)

		## Final Screen ##
		if 17 <= time < 19:
			screen.fill(background)
			pg.display.update()
	
		## END ##
		if time >= 19:
			return	

		## Escape Feature ##
		for event in pg.event.get():
			if event.type in (pg.QUIT, pg.KEYDOWN):
				done = True
		

if __name__ == '__main__':
	main()
