from gamebuttons import *
from fltk import *
import os
import random

#Please read the README.md. Unfortunately reading raw markdown is not always pleasant. :/ 
class Main(Fl_Double_Window):
    """The main class that handles main framework of program."""

    def __init__(self, w, h):
        """Initialize"""

        Fl_Double_Window.__init__(self, w, h, "Simon Says")
        #current colorsequence, score, colorsequence index
        self.seq = ""
        self.score = 0
        self.current = 0

        self.begin()
        #background
        self.bg = Fl_Box(0, 0, w, h)
        self.bg.box(FL_FLAT_BOX)
        self.bg.color(FL_DARK2)
        #buttons and game center 
        self.plate = Simon_Button(0, 0, 250, self.signal)
        self.center = Fl_Box(170, 170, 155, 155)
        self.center.box(FL_NO_BOX)
        
        #set the sprite for the middle
        self.censpr = Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], "center.png"))
        self.center.image(self.censpr.copy(self.center.w(), self.center.h()))

        #create red buttons
        self.startbut = redbutton((w//2)-33, 190, 60, 24, self.play_cb, "play.png")
        self.lbbut = redbutton((w//2)-33, 285, 60, 24, self.leaderboard, "leaderboard.png")
        
        #draw a white border around the display
        self.wborder = Fl_Box((w//2)-47, 223, 89, 54)
        self.wborder.box(FL_FLAT_BOX)
        self.wborder.color(FL_WHITE)
        self.scoredisp = scoredisplay((w//2)-45, 225, 85, 50)
        self.scoredisp.val(0)
        self.plate.deactivate()
        self.end()
        self.show()
        
    def addseq(self):
        self.seq += random.choice("RGBY")

    def playseq(self):

        self.current = 0
        self.plate.deactivate()
        for i in range(len(self.seq)):
            Fl.repeat_timeout(0.7*i, self.plate.chcol, self.seq[i])
            Fl.repeat_timeout((0.7*i)+0.5, self.plate.off)
        Fl.repeat_timeout(0.7*len(self.seq), self.plate.activate)
        Fl.repeat_timeout((0.7*len(self.seq))+5.0, self.stop)

    def stop(self, sec=2.0, t=True):

        if t:
            f = open("data.txt", "r").read()
            dat = f.split(":")
            if int(dat[1]) < self.score:
                pl = fl_input("New highscore!", "Your Name Here")
                f = open("data.txt", "w")
                f.write(pl+":"+str(self.score))

            self.lbbut.activate()

        self.seq = ""
        self.score = 0
        
        
        Fl.remove_timeout(self.plate.off)
        self.plate.deactivate()
        pygame.mixer.music.stop()
        self.plate.endflash(sec, t)
        
        Fl.remove_timeout(self.stop)
        Fl.remove_timeout(self.turn)
        Fl.remove_timeout(self.plate.chcol)

    def leaderboard(self, w):
        f = open("data.txt", "r").read().strip().split(":")[1]
        self.scoredisp.val(int(f))     

    def play_cb(self, w):

        self.lbbut.deactivate()
        self.scoredisp.val(self.score)
        self.plate.activate()
        self.stop(0.5, False)
        Fl.repeat_timeout(2.0, self.turn)
        self.scoredisp.val(0)

    def turn(self):

        self.current = 0
        self.addseq()
        self.playseq()
        
 

    def signal(self, s):
        print(s)
        if s != self.seq[self.current]:
            Fl.remove_timeout(self.stop)
            self.stop()
            return None

        Fl.remove_timeout(self.stop)
        Fl.repeat_timeout(5.0, self.stop)      
        self.score += 1
        self.scoredisp.val(self.score)
        self.current += 1

        if self.current == len(self.seq):
            self.plate.deactivate()
            Fl.remove_timeout(self.stop)
            Fl.repeat_timeout(1.0, self.turn)
            self.current = 0


win = Main(500, 500)
Fl.run()
