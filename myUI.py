## import Statements ##
import Tkinter as tk
import qGen
import time
import random
import os


## Class definition ##
class myUI(tk.Frame):
	## class variables to keep track of current question, player's answer and whethen user has responded'##
	myEntry = None
	equationText=None
	uResp=False

	# to keep track of overall progress and also timeout
	myScore = None
	myTimer = None
	myCoins = None

	#happy and sad zebras
	zup=None
	zdn=None
	zbtn=None

	#buttons to start and stop/ reset
	bstart=None
	breset=None
	playing=False # to toggle with bstart
	reset=False
	
	#help text 
	lhelp=None
	
	#let's see if we can find the zebras. if they can't be found, ignore the button with zebra
	useImages=False

	msg_praise=["Well done","Great job","Awesome","Brilliant","Genius!!","The best"]
	msg_insult=["Doh","Really!","That sucked","Blah Blah","Are you sure?", "Oh brother!"]

	## set up labels and buttons. ##
	def __init__(self, root, *args, **kwargs):

		## create frame. ##
		tk.Frame.__init__(self, root, bg="black", *args, **kwargs)

		## title label ##
		myTitleLabel = tk.Label(self, text = "All Zebra ...", fg="red", font=("Helvetica",26))
		myTitleLabel.grid(row =0, column = 0, columnspan=4)

		## equation text label ##
		self.equationText = tk.Label(self, text = "", fg="white",  bg="black", font=("Helvetica",22))
		self.equationText.grid(row = 1, column = 0, columnspan = 4)

		## user Entry ##
		self.myEntry = tk.Entry(self)
		self.myEntry.grid(row = 2, column = 0, columnspan = 2)
		self.myEntry.bind('<Return>',self.goReturn)

		## Timer Label ##
		self.myTmx = tk.Label(self, text = "Tmx: ", fg="red",  bg="black", font=("Helvetica",32))
		self.myTimer = tk.Label(self, text = "T", fg="red",  bg="black", font=("Helvetica",32))
		self.myTmx.grid(row = 3, column = 0)
		self.myTimer.grid(row = 3, column = 1)

		## Score Label ##
		self.myScx = tk.Label(self, text = "Score: ", fg="blue",  bg="black", font=("Helvetica",32))
		self.myScx.grid(row = 3, column = 2)
		self.myScore = tk.Label(self, text = "0", fg="blue",  bg="black", font=("Helvetica",32))
		self.myScore.grid(row = 3, column = 3)

		## gold Coins Label:
		self.myCoins = tk.Label(self, text = "Gold Coins: ", fg = "gold",  bg="black", font=('Helvetica', 32))
		self.myCoins.grid(row = 5, column = 2, columnspan = 2)

		## msg label
		self.myMsg=tk.Label(self, text = "Give it a go", fg = "white",  bg="black", font=('Helvetica', 24))
		self.myMsg.grid(row = 6, column = 0, columnspan = 4)

		## zebra button
		if os.path.exists("zup.png") and os.path.exists("zdn.png"):
			self.useImages=True
			self.zup=tk.PhotoImage(file="zup.png")
			self.zdn=tk.PhotoImage(file="zdn.png")
			self.zbtn=tk.Button(self,image=self.zup)
			self.zbtn.grid(row=7,column=0,columnspan=4)
		
		##start and stop/reset
		self.bstart=tk.Button(self,text="START",command=self.do_bstart)
		self.breset=tk.Button(self,text="RESET",command=self.do_breset)
		self.bstart.grid(row=8,column=0,columnspan=2)
		self.breset.grid(row=8,column=2,columnspan=2)
		##help label
		htxt="""
		Hit START to play.
		5 correct answers for a Gold Coin.
		8-4 = 4
		4-8 = -4
		8/7 = 1
		7/8 = 0
		Have fun.....
		"""
		self.lhelp=tk.Label(self,text=htxt)
		self.lhelp.grid(row=9,column=0,columnspan=4)

		## place everything ##
		self.grid(row=0,column=0)

	## Check user Answer with correct answer. ##
	## Accepts the current actual answer to the question being displayed, then
	## compares with user input
	def checkAnswer(self, realAns):
		myAnswer = str(self.myEntry.get())
		self.myEntry.delete(0,tk.END)
		if myAnswer == str(realAns):
			self.setZebra(True)
			return True
		else:
			self.setZebra(False)
			return False

	def setZebra(self,mode):
		if self.useImages==True:
			if mode==True:
				self.zbtn.configure(image=self.zup)
			elif mode==False:
				self.zbtn.configure(image=self.zdn)

	## on Return key Clicked action. ##
	def goReturn(self,event):
		self.uResp=True

	## change to a new question. ##
	def setQuestion(self,txt):
		self.equationText.configure(text = txt)

	## set game messages to encourage player
	def setmsg(self,mode):
		if mode=="insult":
			tmp=self.msg_insult[random.randint(0,len(self.msg_insult)-1)]
			self.myMsg.configure(text=tmp)
		elif mode=="fmore":
			self.myMsg.configure(text="Only 4 more for Gold.")
		elif mode=="praise":
			tmp=self.msg_praise[random.randint(0,len(self.msg_praise)-1)]
			self.myMsg.configure(text=tmp)

	def do_bstart(self):
		if self.playing==False:
			self.playing=True
			self.bstart.configure(text="PAUSE")
		else:
			self.playing=False
			self.bstart.configure(text="START")

	def do_breset(self):
			self.reset=True
			
## set up variables. ##
root = tk.Tk()
root.geometry("500x600")
root.title("All Zebra")
root.configure(bg="black")
myMw = myUI(root)
myqGen = qGen.qGen()
cStatus="askq" # we will be changing between asking a question and waiting for user response/ time out
cAnswer=None
cTimeout=0
cTsta=0
cTend=0
cScore = 0
goldCoins = 0
cTspeed = 5 # this is to speed up the game if the player is good

## While the game is running, do this: ## endless loop
while True:
	## update labels and root. ##
	myMw.myTimer.configure(text=str(int(cTimeout)))
	myMw.myScore.configure(text=str(cScore))
	myMw.myCoins.configure(text="Gold Coins: "+str(goldCoins)+" .")
	root.update()
	
	if myMw.reset==True:
		cScore=0
		cTimeout=0
		goldCoins=0
		myMw.reset=False
	
	if myMw.playing: # don't run through unless player is playing
	
		
		## Check if the current status is to ask a question ##
		if cStatus == "askq":
			## if it is, then ask and start the timer counting ##
			cTsta=time.time()
			myquestion = myqGen.generate()
			myMw.setQuestion(myquestion[0])
			cAnswer = myquestion[1]
			cStatus = "wait"
			myMw.myEntry.focus()
		## set the status to wait and wait until the user responds. ##
		elif cStatus == "wait":
			cTimeout=time.time()-cTsta
			## if uresp then check the answer ##
			if myMw.uResp == True:
				myMw.uResp = False## set uresp to false ##
				## if ans correct - incr score, reset counter, status to askq ##
				if myMw.checkAnswer(cAnswer):
					if cScore==0:
						myMw.setmsg("fmore")
					else:
						myMw.setmsg("praise")

					cScore += 1
					cStatus = "askq"
					## else - decr score, reset counter, status to askq ##
				else:
					cScore -= 1
					cStatus = "askq"
					myMw.setmsg("insult")

				if cScore >= 5:
					goldCoins = goldCoins+1
					cScore=0
					cTspeed-=0.25 #this makes the timeout shorter, so player has to play faster

			## if not uresp, ##
			else:
				## if timeout, then decrement score and change status to askq ##
				if cTimeout > cTspeed:
					cScore -= 1
					cTimeout = 0
					cStatus = "askq"


		## go to next round. ##
