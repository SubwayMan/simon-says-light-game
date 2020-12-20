from fltk import *
import os
import math

class Simon_Button(Fl_Button):

    def __init__(self, x, y, rad, spr):

        Fl_Button.__init__(self, x, y, rad, rad)
        self.box(FL_OVAL_BOX)
        self.sprite = spr
        self.down_box(FL_OVAL_BOX)
        self.callback(click_cb)
        self.rad = rad

    def click_cb(self, n):

        cx = Fl.event_x() - self.rad
        cy = Fl.event_y() - self.rad
        crad = math.pi * math.pow(self.rad, 2)
        mdist = math.pow(cx, 2) + math.pow(cy, 2)
        if math.sqrt(mdist) > self.rad:
            return None
        




