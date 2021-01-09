from fltk import *
import os
import math
import random
import pygame
glob = {
    "SPRITEDIR": os.path.join(os.getcwd(), "..", "assets")
    }

class Simon_Button(Fl_Button):

    def __init__(self, x, y, rad, sfunc):

        self.rad = rad
        Fl_Button.__init__(self, x, y, rad*2, rad*2)
    #    self.spritedir = os.path.join(os.getcwd(), "..", "assets")
        self.box(FL_NO_BOX)
        self.down_box(FL_NO_BOX)
        self.sfunc = sfunc
        self.sprite = Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], "alloff.png"))
        self.image(self.sprite.copy(rad*2, rad*2))
        self.callback(self.b_cb)
        self.rad = rad
        pygame.mixer.init()
        self.col_to_mp3 = {
            "B": "sound1.wav",
            "Y": "sound2.wav",
            "G": "sound3.wav",
            "R": "sound4.wav"}
        self.clickval = None

 
    def handle(self, e):
        r = super().handle(e)

        if e == FL_PUSH:
            id = self.mcheck()
            if id:
                
                self.chcol(id)
                self.clickval = id
            
                return 1
        return r
    
    def mcheck(self) -> str:
        mx, my = Fl.event_x(), Fl.event_y()
        cx = mx - self.rad
        cy = my - self.rad
        crad = math.pi * math.pow(self.rad, 2)
        mdist = math.pow(cx, 2) + math.pow(cy, 2)


        if not 87 <= math.sqrt(mdist) < self.rad-30:
            return None
        if mx < self.rad-10 and my < self.rad-10:
            return "G"
        elif mx > self.rad+10 and my < self.rad-10:
            return "R"
        elif mx > self.rad+10 and my > self.rad+10:
            return "B"
        elif mx < self.rad-10 and my > self.rad+10:
            return "Y"
        else:
            return None


    def b_cb(self, w):
        if self.clickval:
                self.off()
                self.sfunc(self.clickval)
                self.clickval = None

    def chcol(self, c):

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
        pygame.mixer.music.load(os.path.join(glob["SPRITEDIR"], self.col_to_mp3[c]))
        pygame.mixer.music.play(-1)
        self.sprite = Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], pic))
        self.image(self.sprite.copy(self.rad*2, self.rad*2))
        self.parent().redraw()
        
    def off(self):

        self.image(Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], "alloff.png")).copy(self.rad*2, self.rad*2))
        self.parent().redraw()
        pygame.mixer.music.stop()
       

    def endflash(self, t, sflag):
        self.image(Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], "allon.png")).copy(self.rad*2, self.rad*2))
        self.parent().redraw()
        Fl.repeat_timeout(t, self.off)
        if sflag:
            pygame.mixer.music.load(os.path.join(glob["SPRITEDIR"], "failure.wav"))
            pygame.mixer.music.play(-1)

class redbutton(Fl_Button):

    def __init__(self, x, y, w, h, cb, label):
       
        Fl_Button.__init__(self, x, y, w, h)
        self.sprite = Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], "button.png"))
        self.lsprite = Fl_PNG_Image(os.path.join(glob["SPRITEDIR"], label))

        self.box(FL_NO_BOX)
        self.callback(cb)
        self.image(self.sprite.copy(self.w(), self.h()))

        self.labelbox = Fl_Box(x+((w//2)-(h//2)), y, h, h)
        self.labelbox.image(self.lsprite.copy(h, h))

class scoredisplay(Fl_Pack):

    def __init__(self, x, y, w, h):
        super.__init__(self, x, y, w, h)

        
if __name__ == "__main__":

    win = Fl_Double_Window(500, 500, "buttontest")
    win.begin()
    
    b = Simon_Button(0, 0, 250)
    win.end()
    win.show()
    Fl.run()



