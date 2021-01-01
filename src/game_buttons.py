from fltk import *
import os
import math
import random

class Simon_Button(Fl_Button):

    def __init__(self, x, y, rad):

        Fl_Button.__init__(self, x, y, rad*2, rad*2)
        self.spritedir = os.path.join(os.getcwd(), "..", "assets")
        self.box(FL_NO_BOX)
        self.down_box(FL_NO_BOX)
        self.sprite = Fl_PNG_Image(os.path.join(self.spritedir, "alloff.png"))
        self.image(self.sprite.copy(rad*2, rad*2))
        
        self.callback(self.click_cb)
        self.rad = rad

    def click_cb(self, n):

        cx = Fl.event_x() - self.rad
        cy = Fl.event_y() - self.rad
        print(cx, cy)
        crad = math.pi * math.pow(self.rad, 2)
        mdist = math.pow(cx, 2) + math.pow(cy, 2)
        print(math.sqrt(mdist))
        if math.sqrt(mdist) > self.rad:
            print("exit")
            return None
        


if __name__ == "__main__":

    win = Fl_Window(500, 500, "buttontest")
    win.begin()
    
    b = Simon_Button(0, 0, 250)
    win.end()
    win.show()
    Fl.run()



