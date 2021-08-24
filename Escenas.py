class Escenas:
	def __init__(self,number,name,description1,description2):
		self.number=number
		self.name=name
		self.sceneActive=True
		self.firstTime=True
		self.description1=description1
		self.description2=description2

	def getNumber(self):
		return int(self.number)

	def getName(self):
		return self.name

	def getDescription(self):
		return self.description1

	def getFirstTime(self):
		return self.firstTime

	def setNotFirstTime(self):
		self.firstTime=False

	def setNewDescription(self):
		self.description1 = self.description2
		self.sceneChanged = True

	def getSceneActive(self):
		return self.sceneActive

	def setSceneActive(self,value):
		self.sceneActive=value

	def getSceneChanged(self):
		return self.sceneChanged

	def print(self):
		print("number> ",self.number," name> ",self.name,"description1> ",self.description1,"description2> ",self.description2)