#wunderlist https://medium.com/wunderlist-engineering/talk-to-wunderlist-in-python-8c456a1ba821
#for the current version run "pip install wunderpy2"

from tkinter import *
from PIL import Image, ImageTk
import wunderpy2
import json


CLIENT_ID = ""
CLIENT_SECRET = ""
ACCESS_TOKEN = ""

api = wunderpy2.WunderApi()
client = api.get_client(ACCESS_TOKEN, CLIENT_ID)
#get lists
lists = client.get_lists()
#get the id based on the name
listName = "SmartMirror"
listID = 0
list = json.loads(json.dumps(lists))
#print("{0:10} {1:45}".format("ID","Title"))
for lst in lists:
	#print("{0:10} {1:45}".format(lst["id"], lst["title"]))
	if listName == lst["title"]:
		listID = lst["id"]
		print ("Found match")

class Wunderlist(Frame):
	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, *args, **kwargs)
		self.add_icon()
		self.title='To Do List'
		self.wunderlistLbl = Label(self, text=self.title, font=('Helvetica',28), fg="white", bg="black")
		self.wunderlistLbl.pack(side = TOP, anchor=W, fill=BOTH, expand = YES)
		self.wunderlistEventContainer = Frame(self, bg='black')
		self.wunderlistEventContainer.pack(side=TOP, fill=BOTH, expand = YES)
		self.get_task()
	
	def get_task(self):
		#setup calendar api
		print("Getting Tasks...")
		try:
			tasks = client.get_tasks(listID)
			parsedTask = json.loads(json.dumps(tasks))
			for task in parsedTask:
				print(task["title"])
				taskDes_label = Label(self.wunderlistEventContainer, text=task["title"],font=('Helvetica',14),fg="white",bg="black")
				taskDes_label.pack(fill=BOTH, expand = YES)
			#print(parsed_task[1]["title"])
			#print(parsed_tsk)	
			
					
				
		except Exception as e:
			traceback.print_exc()
			return "Error getting task"
		self.after(600000, self.get_task)
	
	def add_icon(self):
		image = Image.open("assets/Calendar.png")
		image = image.resize((50,50), Image.ANTIALIAS)
		image = image.convert('RGB')
		photo = ImageTk.PhotoImage(image)
		
		self.iconLbl = Label(self, bg='black', image=photo)
		self.iconLbl.image = photo
		self.iconLbl.pack(side=LEFT, anchor=N, fill=BOTH, expand = YES)
