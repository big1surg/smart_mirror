from __future__ import print_function
from tkinter import *
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from PIL import Image, ImageTk
import datetime

calendarBirthday=''
calendarPrimary ='primary'
calendarGames =''
calendarBills =''
calendarNames = ['Primary', 'Bills','Games','Birthdays']
arrayOfCalendars = [calendarPrimary, calendarBills, calendarGames, calendarBirthday]
#array of number of items, they should match the above, this is amt of items pulled from that specific calendar
arrayOfCalendarItems = [3,2,2,1]

class Calendar(Frame):
	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, *args, **kwargs)
		self.add_icon()
		self.title='Calendar Events'
		self.calendarLbl = Label(self, text=self.title, font=('Helvetica',28), fg="white", bg="black")
		self.calendarLbl.pack(side = TOP, anchor=W, fill=BOTH, expand = YES)
		self.calendarEventContainer = Frame(self, bg='black')
		self.calendarEventContainer.pack(side=TOP, fill=BOTH, expand = YES)
		self.get_events()
	
	def get_events(self):
		#setup calendar api
		SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
		store = file.Storage('credentials.json')
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets('client_secret.json',SCOPES)
			creds = tools.run_flow(flow, store)
		service = build('calendar', 'v3', http=creds.authorize(Http()))
		try:
			for widget in self.calendarEventContainer.winfo_children():
				widget.destroy();
			now = datetime.datetime.utcnow().isoformat()+'Z'
			
			#array of calendars
			listOfEvents = []
			calendarCount = 0
			for calendar in arrayOfCalendars:
				events_result = service.events().list(calendarId=arrayOfCalendars[calendarCount],timeMin=now, maxResults=arrayOfCalendarItems[calendarCount], singleEvents=True, orderBy='startTime').execute()
				events = events_result.get('items', [])
				listOfEvents.append(events)
				calendarCount= calendarCount+1
			
			eventsCount=0
			for events in listOfEvents:
				calendarName_label = Label(self.calendarEventContainer, text=calendarNames[eventsCount],font=('Helvetica',12),fg="yellow",bg="black")
				calendarName_label.pack(fill=BOTH, expand = YES)
				for event in events:
					startDate = event['start'].get('dateTime',event['start'].get('date'))
					start =  startDate.split("-")
					dateDay = start[2].split("T")
					event_label = Label(self.calendarEventContainer, text=start[1]+"/"+dateDay[0]+" "+event['summary'],font=('Helvetica',14),fg="white",bg="black")
					event_label.pack(fill=BOTH, expand = YES)
				eventsCount=eventsCount+1
					
				
		except Exception as e:
			traceback.print_exc()
			return "Error getting calendar"
		self.after(600000, self.get_events)
	
	def add_icon(self):
		image = Image.open("assets/Calendar.png")
		image = image.resize((50,50), Image.ANTIALIAS)
		image = image.convert('RGB')
		photo = ImageTk.PhotoImage(image)
		
		self.iconLbl = Label(self, bg='black', image=photo)
		self.iconLbl.image = photo
		self.iconLbl.pack(side=LEFT, anchor=N, fill=BOTH, expand = YES)
		
