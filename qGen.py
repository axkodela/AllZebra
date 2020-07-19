## import Statements ##
import random

## Class Definition ##
class qGen:
	## num 1 ##
	op1 = 0
	## num 2 ##
	op2 = 0
	## list of operators. ##
	ops = ["add", "sub", "mul", "div"]

	## init Method ##
	def __init__(self):
		pass

	## Generates a math question. ##
	def generate(self):
		self.op1 = random.randint(1,10)
		self.op2 = random.randint(1,10)
		eqt = ""
		eqr = 0
		opsindex = random.randint(0,len(self.ops)-1)
		currop = self.ops[opsindex]

		## goes through the operators list and does the appropriate math. ##
		if currop == "add":
			eqt = str(self.op1) + " + " + str(self.op2) + " =  ______ "
			eqr=self.op1 + self.op2
		elif currop == "sub":
			eqt = str(self.op1) + " - " + str(self.op2) + " =  ______ "
			eqr=self.op1 - self.op2
		elif currop == "mul":
			eqt = str(self.op1) + " * " + str(self.op2) + " =  ______ "
			eqr=self.op1 * self.op2
		elif currop == "div":
			eqt = str(self.op1) + " / " + str(self.op2) + " =  ______ "
			eqr=self.op1 / self.op2

		## Returns the question and the answer as a list. ##
		return [eqt, eqr]
