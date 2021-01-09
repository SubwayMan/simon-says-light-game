from fltk import *
import os
import math
import random
import pygame
#global variable to yank from assets directory
glob = {
    "SPRITEDIR": os.path.join(os.getcwd(), "..", "assets")
    }

class Simon_Button(Fl_Button):
    """The button class. Handles its own event parsing and sound 
    handling and sends information to the main class."""

    def __init__(self, x, y, rad, sfunc) -> None:
        """Initialize object"""
        #Due to circular nature, takes radius argument to construct self.
        self.rad = rad
        Fl_Button.__init__(self, x, y, rad*2, rad*2)
        #Transparent edges
        self.box(FL_NO_BOX)
        #receives listener function from main
        self.sfunc = sfunc
        #sprite handling
        self.sprite = Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], "alloff.png"))
        self.image(self.sprite.copy(rad*2, rad*2))
        #set callback
        self.callback(self.b_cb)
        #initialize music
        pygame.mixer.init()
        #maps button return values to specific files
        self.col_to_mp3 = {
            "B": "sound1.wav",
            "Y": "sound2.wav",
            "G": "sound3.wav",
            "R": "sound4.wav"}
        #stores current color
        self.clickval = None
        #dictionary that maps key ascii to color characters
        self.keyshort = dict((ord(a), b) for a, b in zip("qwsa", "GRBY"))
 
    def handle(self, e) -> int:
        """Event handler that registers push 
        events and keyboard shortcuts."""
        r = super().handle(e)
        #button press
        if e == FL_PUSH:
            #check hitboxes
            id = self.mcheck()
            #runs if check successful
            if id:
                #color change, store color
                self.chcol(id)
                self.clickval = id
                return 1
        #check key release events
        if e == FL_KEYUP:
            #key release function would do same thing as mouse release, so link to callback for simplicity
            self.do_callback()
            return 1
        #check if any of the shortcut keys are currently held
        for k in self.keyshort:
            if Fl.get_key(k):
                #color change and store color
                id = self.keyshort[k]
                self.chcol(id)
                self.clickval = id
                return 1
        return r        
    
    def mcheck(self) -> str:
        """This is the function that manages the 
        button hitboxes. TL;DR: Math here."""
        #get mouse position and store distance from origin point
        mx, my = Fl.event_x(), Fl.event_y()
        cx = mx - self.rad
        cy = my - self.rad

        #pythag to get absolute distance
        mdist = math.pow(cx, 2) + math.pow(cy, 2)

        #check bounds for distance from origin to create donut-shaped hitbox
        if not 87 <= math.sqrt(mdist) < self.rad-30:
            return None
        #overlay square hitboxes on top for each individual subbutton
        if mx < self.rad-10 and my < self.rad-10:
            #convention here is to return the color character
            return "G"
        elif mx > self.rad+10 and my < self.rad-10:
            return "R"
        elif mx > self.rad+10 and my > self.rad+10:
            return "B"
        elif mx < self.rad-10 and my > self.rad+10:
            return "Y"
        else:
            #this is basically the black strip in between each button, which we don't want
            return None


    def b_cb(self, w) -> None:
        """Button/key release callback. Responsible for sending stored value to event listener."""
        #only executes if there is a stored value. 
        if self.clickval:
            #turn self off
            self.off()
            #send stored color value to main class
            self.sfunc(self.clickval)
            #remove stored color value
            self.clickval = None

    def chcol(self, c) -> None:
        """Color changer class, which also controls sound."""

        #maps color char to image
        if c == "R":
            pic = "redlight.png"
        elif c == "B":
            pic = "bluelight.png"
        elif c == "Y":
            pic = "yellight.png"
        elif c == "G":
            pic = "greenlight.png"
        else:
            return None
        #play music and loop
        pygame.mixer.music.load(os.path.join(glob["SPRITEDIR"], self.col_to_mp3[c]))
        pygame.mixer.music.play(-1)
        #set sprite and ask the main window to redraw
        #does not call own redraw method directly due to layering issues
        self.sprite = Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], pic))
        self.image(self.sprite.copy(self.rad*2, self.rad*2))
        self.parent().redraw()
        
    def off(self) -> None:
        """Basic process terminator. 
        Turns lights off and stops music."""

        #what it says in the docstring
        self.image(Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], "alloff.png")).copy(self.rad*2, self.rad*2))
        self.parent().redraw()
        pygame.mixer.music.stop()
       

    def endflash(self, t, sflag) -> None:
        """Simple method that flashes all lights for t seconds. 
        Accepts special parameters for game end."""
        
        #Turn all lights on
        self.image(Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], "allon.png")).copy(self.rad*2, self.rad*2))
        self.parent().redraw()
        #schedule self to be turned off
        Fl.repeat_timeout(t, self.off)
        #only play failure music at game end
        if sflag:
            pygame.mixer.music.load(os.path.join(glob["SPRITEDIR"], "failure.wav"))
            pygame.mixer.music.play(-1)

class redbutton(Fl_Button):
    """A snazzy red button class that can also accept an image label."""
    def __init__(self, x, y, w, h, cb, label) -> None:
        """Initialize"""

        Fl_Button.__init__(self, x, y, w, h)
        #sprite
        self.sprite = Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], "button.png"))
        #labelsprite
        self.lsprite = Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], label))

        #prevents opaque backdrop
        self.box(FL_NO_BOX)
        #event handle - allows passing of a function into constructor
        self.callback(cb)
        #set image
        self.image(self.sprite.copy(self.w(), self.h()))
        #create label
        self.labelbox = Fl_Box(x+((w//2)-(h//2)), y, h, h)
        self.labelbox.image(self.lsprite.copy(h, h))

class scoredisplay(Fl_Pack):
    """A short and simple class for the triple-digit LCD display."""
    def __init__(self, x, y, w, h) -> None:
        """Initialize"""
        Fl_Pack.__init__(self, x, y, w, h)
        #Horizontal
        self.type(1)
        self.begin()
        #list to store digits
        self.nums = []
        #create box for each digit 
        for i in range(3):
            digit = Fl_Box(i*(w//3), 0, w//3, h)
            digit.box(FL_FLAT_BOX)
            digit.color(FL_BLACK)
            self.nums.append(digit)
        self.end()

    def val(self, n) -> None:
        """Changes and displays stored value."""
        #limit digits to 3
        n = min(999, n)
        #justify right with 0s and zip each digit with corresponding space in display
        for d, space in zip(str(n).zfill(3), self.nums):
            #set image
            im = Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], (d+".png")))
            space.image(im.copy(space.w(), space.h()))
        self.redraw()
        
if __name__ == "__main__":
    #defunct testing function. Main file for this program is TylerChen.py.
    win = Fl_Double_Window(500, 500, "buttontest")
    win.begin()
    
    b = Simon_Button(0, 0, 250)
    win.end()
    win.show()
    Fl.run()



