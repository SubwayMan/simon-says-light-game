from gamebuttons import Simon_Button
from fltk import *
import os

class Main(Fl_Double_Window):

	def __init__(self, w, h):
		Fl_Double_Window.__init__(self, w, h, "Simon Says")
		self.begin()
		self.plate = Simon_Button(0, 0, 250)
		self.center = Fl_Box(170, 170, 155, 155)
		self.center.box(FL_NO_BOX)
		self.spdir = os.path.join(os.getcwd(), "..", "assets")
		self.censpr = Fl_PNG_Image(os.path.join(self.spdir, "center.png"))
		self.center.image(self.censpr.copy(self.center.w(), self.center.h()))
		self.end()
		self.show()

win = Main(500, 500)
Fl.run()
