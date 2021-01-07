from gamebuttons import *
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
        
        self.censpr = Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], "center.png"))
        self.center.image(self.censpr.copy(self.center.w(), self.center.h()))

        self.startbut = redbutton((w//2)-28, 200, 50, 20, self.addseq)
        self.tempbut = redbutton((w//2)-28, 250, 50, 20, self.playseq)

        
        self.end()
        self.show()
        
    def addseq(self, w):
        self.seq += random.choice("RGBY")
        print(self.seq)

    def playseq(self, w):

        self.plate.deactivate()
        for i in range(len(self.seq)):
            Fl.repeat_timeout(0.5*i, self.plate.chcol, self.seq[i])
            Fl.repeat_timeout((0.5*i)+0.3, self.plate.off)
        Fl.repeat_timeout(0.5*len(self.seq), self.plate.activate)

win = Main(500, 500)
Fl.run()
