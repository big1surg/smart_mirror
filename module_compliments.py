from tkinter import *
import random
import datetime

class Compliments(Frame):
	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, bg='black')
		#initalize compliment
		self.compliment = 'Beautiful'
		self.complimentLbl = Label(self, text = self.compliment, font=('Gentium Book Basic', 48), fg="white", bg="black")
		self.complimentLbl.pack(side=TOP, anchor = N)
		self.changeCompliment()
		
	def changeCompliment(self):
		print("changing compliment")
		listOfCompliments=['Good day','Its a good day','Smile =)','Mirror mirror...','Its nice today','I think Im in love!','Youre da best!','high five!','Beautiful']
		x=random.randint(0,8)
		now=datetime.datetime.now()
		if now.hour%12==0:
			self.complimentLbl.config(text=listOfCompliments[x])
		self.complimentLbl.after(600000,self.changeCompliment)