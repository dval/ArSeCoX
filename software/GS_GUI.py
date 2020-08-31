import tkinter as tk
from tkinter.ttk import *


root = tk.Tk()
root.title("Feet to Meters")

class Main_Window:
	"""docstring for MainWindow"""
	def __init__(self, main):
		self.main = main
		

'''
The Calculate Distance window is just an example of a simple  in-app app.
Each of the sub-windows/sub-apps has access to the global app variables, 
including window methods.
'''
class Sub_Distance:
	"""docstring for CalculateDistance"""
	def __init__(self, root):
		self.root = root

		self.mainframe = tk.Frame(self.root)
		self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W))
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)

		self.feet = tk.StringVar()
		self.meters = tk.StringVar()

		self.feet_entry = tk.Entry(self.mainframe, width=7, textvariable=self.feet)
		self.feet_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

		tk.Label(self.mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(tk.W, tk.E))
		tk.Button(self.mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=tk.W)

		tk.Label(self.mainframe, text="feet").grid(column=3, row=1, sticky=tk.W)
		tk.Label(self.mainframe, text="is equivalent to").grid(column=1, row=2, sticky=tk.E)
		tk.Label(self.mainframe, text="meters").grid(column=3, row=2, sticky=tk.W)


		self.feet_entry.focus()
		self.root.bind('<Return>', self.calculate)

		# We can run this to update window anytime after
		# all child widgets have been created.
		for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

	def calculate(self, *args):
		try:
			value = float(self.feet.get())
			self.meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
		except ValueError:
			pass
	

def BuildList(listBoxWidget, displayList):
	try:
		for li in displayList:
			listBoxWidget.insert(li[0], li[1])

	except ValueError:
		pass


def Proc_Menu(menubar, root):

	filemenu = tk.Menu(menubar, tearoff=0)
	filemenu.add_command(label="Select", command=create_select_window)
	filemenu.add_command(label="Save", command=create_conversion_window)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="File", menu=filemenu)
	#root.config(menu=menubar)

	editmenu = tk.Menu(menubar, tearoff=0)
	editmenu.add_command(label="Theme", command=create_select_window)
	editmenu.add_command(label="Settings", command=create_select_window)
	menubar.add_cascade(label="Edit", menu=editmenu)
	root.config(menu=menubar)

	helpmenu = tk.Menu(menubar, tearoff=0)
	helpmenu.add_command(label="User Manual", command=create_select_window)
	helpmenu.add_command(label="About", command=create_conversion_window)
	menubar.add_cascade(label="Help", menu=helpmenu)
	root.config(menu=menubar)


# Create Tkinter variables for globals
activeDevice = tk.StringVar(root)
# Dictionary with options
choices = { 'Pizza','Lasagne','Fries','Fish','Potatoe'}
activeDevice.set(next(iter(choices))) # set item as default option


def Sub_Device_Select():
	global root, activeDevice
	window = tk.Toplevel(root)

	'''
	#TODO: This will need to be implemented differently with 
	actual COM list.
	'''
	## 
	frame = tk.Frame(window)
	frame.grid(column=1, row=5, sticky=(tk.N))

	popupMenu = tk.OptionMenu(frame, activeDevice, activeDevice.get(), *choices)
	popupMenu.grid(row = 2, column =1)
	tk.Label(frame, text="Choose a dish").grid(row = 1, column = 1)

	cancelBtn = tk.Button(frame, text="Cancel", command=lambda:close_window(window))
	cancelBtn.grid(column=2, row=3, sticky=tk.W)
	# button with argument
	saveBtn = tk.Button(frame, text="Select", command=lambda:close_window(window))
	saveBtn.grid(column=4, row=3, sticky=tk.W)
	#


	# link function to change dropdown
	activeDevice.trace('w', change_dropdown)

	#window.protocol("WM_DELETE_WINDOW", on_closing)

def create_conversion_window():
	global root
	app = tk.Toplevel(root)
	CalculateDistance(app)



# on change dropdown value
def change_dropdown(*args):
	global activeDevice
	print( activeDevice.get() )

def close_window(window):
	window.destroy()

def on_closing():
	global root
	#root.destroy()

def select_device():
	global activeDevice
	print (activeDevice)

menubar = tk.Menu(root)
Proc_Menu(menubar, root)


root.mainloop()


'''
listbox = Listbox(frame, width=10, height=3)
listbox.grid(column=0, row=0, sticky=N)

scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.config(command=listbox.yview)
scrollbar.grid(column=1, row=0, sticky=(N, S, E))

# The child widgets are dynamic and can be updated
# anytime after creation.
newList = [ (1, "Jerry"), (2, "George"), (3, "Elaine"), (4, "Kramer"), (5, "Newman") ]
BuildList( listbox, newList )
'''

