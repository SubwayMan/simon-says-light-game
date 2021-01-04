from fltk import *
import os
import math
import random

class Simon_Button(Fl_Button):

    def __init__(self, x, y, rad):

        self.rad = rad
        Fl_Button.__init__(self, x, y, rad*2, rad*2)
        self.spritedir = os.path.join(os.getcwd(), "..", "assets")
        self.box(FL_NO_BOX)
        self.down_box(FL_NO_BOX)
        self.sprite = Fl_PNG_Image(os.path.join(self.spritedir, "alloff.png"))
        self.image(self.sprite.copy(rad*2, rad*2))
        
        self.callback(self.click_cb)
        self.rad = rad

    def click_cb(self, n):

        mx, my = Fl.event_x(), Fl.event_y()
        cx = mx - self.rad
        cy = my - self.rad
        crad = math.pi * math.pow(self.rad, 2)
        mdist = math.pow(cx, 2) + math.pow(cy, 2)
        if not 87 <= math.sqrt(mdist) < self.rad-30:
            print("exit")
            return None

        if mx < self.rad-10 and my < self.rad-10:
            self.chcol("G")
        elif mx > self.rad+10 and my < self.rad-10:
            self.chcol("R")
        elif mx > self.rad+10 and my > self.rad+10:
            self.chcol("B")
        elif mx < self.rad-10 and my > self.rad+10:
            self.chcol("Y")
        else:
            return None
        
        self.deactivate()
        Fl.repeat_timeout(0.5, self.activate())
        
    def chcol(self, c):
        
        if c == "R":
            pic = "redlight.png"
        elif c == "B":
            pic = "bluelight.png"
        elif c == "Y":
            pic = "yellight.png"
        elif c == "G":
            pic = "greenlight.png"
        self.sprite = Fl_PNG_Image(c)
        self.image(self.sprite.copy(self.rad*2, self.rad*2))
        self.redraw()
        Fl.repeat_timeout(0.5, self.image(Fl_PNG_Image(os.path.join(self.spritedir, "alloff.png"))))
        
        

    

if __name__ == "__main__":

    win = Fl_Double_Window(500, 500, "buttontest")
    win.begin()
    
    b = Simon_Button(0, 0, 250)
    win.end()
    win.show()
    Fl.run()



