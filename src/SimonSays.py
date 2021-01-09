from gamebuttons import *
from fltk import *
import os
import random
class Main(Fl_Double_Window):

    def __init__(self, w, h):
        
        Fl_Double_Window.__init__(self, w, h, "Simon Says")
        self.seq = ""
        self.spdir = os.path.join(os.getcwd(), "..", "assets")
        self.score = 0
        self.current = 0

        self.begin()
        self.plate = Simon_Button(0, 0, 250, self.signal)
        self.add(self.plate)
        self.center = Fl_Box(170, 170, 155, 155)
        self.center.box(FL_NO_BOX)
        
        self.censpr = Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], "center.png"))
        self.center.image(self.censpr.copy(self.center.w(), self.center.h()))

        self.startbut = redbutton((w//2)-33, 190, 60, 24, self.play_cb, "play.png")
        self.lbbut = redbutton((w//2)-33, 285, 60, 24, self.leaderboard, "leaderboard.png")
        
        self.plate.deactivate()
        self.end()
        self.show()
        
    def addseq(self):
        self.seq += random.choice("RGBY")
        print(self.seq)

    def playseq(self):

        self.plate.deactivate()
        for i in range(len(self.seq)):
            Fl.repeat_timeout(0.5*i, self.plate.chcol, self.seq[i])
            Fl.repeat_timeout((0.5*i)+0.3, self.plate.off)
        Fl.repeat_timeout(0.5*len(self.seq), self.plate.activate)

    def stop(self):
        self.seq = ""
        self.score = 0
        self.plate.deactivate()
        self.plate.endflash()
        Fl.remove_timeout(self.stop)
        Fl.remove_timeout(self.turn)

    def leaderboard(self, w):
        pass

    def play_cb(self, w):
        self.plate.activate()
        self.stop()
        Fl.repeat_timeout(2.0, self.turn)

    def turn(self):

        self.score += 1
        self.addseq()
        self.playseq()
        Fl.repeat_timeout(5.0, self.stop)
 

    def signal(self, s):

        if s != self.seq[self.current]:
            self.stop()
            Fl.remove_timeout(self.stop)
        self.current += 1
        if self.current == len(self.seq):
            Fl.remove_timeout(self.stop)
            Fl.repeat_timeout(1.0, self.turn)
            self.current = 0
        else:
            Fl.repeat_timeout(5.0, self.stop)


win = Main(500, 500)
Fl.run()
