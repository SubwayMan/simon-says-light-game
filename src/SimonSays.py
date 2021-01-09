from gamebuttons import *
from fltk import *
import os
import random

#Please read the README.md. Unfortunately reading raw markdown is not always pleasant. :/ 
class Main(Fl_Double_Window):
    """The main class that handles main framework of program."""

    def __init__(self, w, h) -> None:
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
        #draw display
        self.scoredisp = scoredisplay((w//2)-45, 225, 85, 50)
        #set its default value to 0
        self.scoredisp.val(0)
        #make sure buttons cannot receive events while not playing
        self.plate.deactivate()
        self.end()
        self.show()
        
    def addseq(self) -> None:
        """function that adds to sequence."""
        self.seq += random.choice("RGBY")

    def playseq(self) -> None:
        """Plays a given string as a sequence of lights/sounds."""
        #prevent plate from getting events
        self.plate.deactivate()
        #iterate through color codes
        for i in range(len(self.seq)):
            #schedule light flash and light unflash
            Fl.repeat_timeout(0.7*i, self.plate.chcol, self.seq[i])
            Fl.repeat_timeout((0.7*i)+0.5, self.plate.off)
        #Schedules reactivation
        Fl.repeat_timeout(0.7*len(self.seq), self.plate.activate)
        #For idle loss condition
        Fl.repeat_timeout((0.7*len(self.seq))+5.0, self.stop)

    def stop(self, sec=2.0, t=True) -> None:
        """Function that ends game and any game related processes."""
        #flag for game loss
        if t:
            #check score vs highscore
            f = open("data.txt", "r").read()
            dat = f.split(":")
            if int(dat[1]) < self.score:
                #get name
                pl = fl_input("New highscore!", "Your Name Here")
                #exit if user cancels
                if not pl:
                    return None
                f = open("data.txt", "w")
                #store score
                f.write(pl+":"+str(self.score))
            #reenables leaderboard button after finishing
            self.lbbut.activate()

        #resets sequence and score
        self.seq = ""
        self.score = 0
        
        #remove stray plate off function
        Fl.remove_timeout(self.plate.off)
        #disable plate event handling
        self.plate.deactivate()
        #stop any music
        pygame.mixer.music.stop()
        #ask for an endflash
        self.plate.endflash(sec, t)
        #remove stray timeouts
        Fl.remove_timeout(self.stop)
        Fl.remove_timeout(self.turn)
        Fl.remove_timeout(self.plate.chcol)

    def leaderboard(self, w) -> None:
        """callback that displays highscore."""
        f = open("data.txt", "r").read().strip().split(":")[1]
        self.scoredisp.val(int(f))     

    def play_cb(self, w) -> None:
        """callback that starts rolling game into motion."""
        #prevent leaderboard access during game
        self.lbbut.deactivate()
        #enable buttons
        self.plate.activate()
        #kill any running procs as this function may have to overwrite other games
        self.stop(0.5, False)
        #schedule first turn
        Fl.repeat_timeout(2.0, self.turn)
        #reset display
        self.scoredisp.val(0)

    def turn(self) -> None:
        """Function for each turn, or after a correct sequence entry."""
        #current position reset
        self.current = 0
        #increase sequence and play it
        self.addseq()
        self.playseq()
        
 

    def signal(self, s) -> None:
        """Listener function that checks validity of input."""
        #lose if wrong button pressed
        if s != self.seq[self.current]:
            self.stop()
            return None

        #reset idle countdown
        Fl.remove_timeout(self.stop)
        Fl.repeat_timeout(5.0, self.stop)      
        #increase score
        self.score += 1
        self.scoredisp.val(self.score)
        #increase index of sequence of which to check
        self.current += 1

        #advance to next turn if sequence completed
        if self.current == len(self.seq):
            #prevent presses during wait for new sequence
            self.plate.deactivate()
            #remove idle timeout
            Fl.remove_timeout(self.stop)
            #schedule next turn
            Fl.repeat_timeout(1.0, self.turn)

#Running the program
win = Main(500, 500)
Fl.run()
