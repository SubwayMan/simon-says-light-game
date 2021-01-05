from gamebuttons import Simon_Button
from fltk import *
import os
import random
class Main(Fl_Double_Window):

    def __init__(self, w, h):
        
        Fl_Double_Window.__init__(self, w, h, "Simon Says")
        self.seq = ""
        self.spdir = os.path.join(os.getcwd(), "..", "assets")

        self.begin()
        self.plate = Simon_Button(0, 0, 250)
        self.center = Fl_Box(170, 170, 155, 155)
        self.center.box(FL_NO_BOX)
        self.startbut = Fl_Button((w//2)-25, 200, 50, 20)
        self.startbut.box(FL_NO_BOX)
        self.butbaseimg = Fl_PNG_Image(os.path.join(self.spdir, "button.png"))
        self.startbut.image(self.butbaseimg.copy(self.startbut.w(), self.startbut.h()))
        
        self.censpr = Fl_PNG_Image(os.path.join(self.spdir, "center.png"))
        self.center.image(self.censpr.copy(self.center.w(), self.center.h()))
        self.end()
        self.show()
        
    def addseq(self):
        self.seq += random.choice("RGBY")
    
    def playseq(self):

        self.plate.deactivate()
        for i in range(len(self.seq)):
            Fl.repeat_timeout(0.5*i, self.plate.chcol(self.seq[i]))

        Fl.repeat_timeout(0.5*len(self.seq), self.plate.activate)

win = Main(500, 500)
Fl.run()
