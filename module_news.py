from tkinter import *
import requests
import json
import traceback
import feedparser
from PIL import Image, ImageTk
import datetime


country_code = 'us'
city_code = 'lb'


class News(Frame):
	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, *args, **kwargs)
		self.config(bg='black')
		self.title = 'News'
		self.newsLbl = Label(self, text=self.title, font=('Helvetica', 28), fg="white", bg="black")
		self.newsLbl.pack(side=TOP, anchor=W)
		self.headlinesContainer = Frame(self, bg="black")
		self.headlinesContainer.pack(side=TOP)
		self.get_localheadlines()
		
	def get_headlines(self):
		try:
			for widget in self.headlinesContainer.winfo_children():
				widget.destroy()
			headlines_url = "https://news.google.com/?hl=en-%s&gl=%s&ceid=%s:en&output=rss" % (country_code,country_code,country_code)
			feed = feedparser.parse(headlines_url)
			for post in feed.entries[0:3]:
				#print(post)
				#print(post.title)
				headline = NewsHeadline(self.headlinesContainer, post.title)
				headline.pack(side=TOP, anchor=W)
		except Exception as e:
			traceback.print_exc()
			return "Error: %s. Cannot get news." % e
		self.after(600000, self.get_headlines)
		
	def get_localheadlines(self):
		try:
			# remove all children
			for widget in self.headlinesContainer.winfo_children():
				widget.destroy()
			if city_code == None:
				localnews_url = "No news to Display"
			else:
				localnews_url = "https://news.google.com/news?cf=all&hl=en&pz=1&ned=us&q=long+beach+california&output=rss"
			feed1 = feedparser.parse(localnews_url)
			for post in feed1.entries[0:3]:
				print(post.title)
				headline = NewsHeadline(self.headlinesContainer, post.title)
				headline.pack(side=TOP, anchor=W)
		except Exception as e:
			traceback.print_exc()
			return "Error: %s. Cannot get news." % e
		self.after(600000, self.get_headlines)

class NewsHeadline(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=event_name, font=('Helvetica', 18), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=N)