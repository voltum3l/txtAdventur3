#Importante entender que debería activarlos a todos por defecto y tener una funcion que "desactive" algunos en particular.

class ObjetosInteractivos:
	def __init__(self,numero,nombre,descripcion,dynamicText1,dynamicText2,numeroEscena):
		self.numero = numero
		self.nombre = nombre
		self.descripcion = descripcion
		self.dynamicText1 = dynamicText1
		self.dynamicText2 = dynamicText2
		self.tipoObjeto = 0
		self.activo = True
		self.numeroEscena = numeroEscena

	def getNumero(self):
		return self.numero

	def getNombre(self):
		return self.nombre

	def getDescripcion(self):
		return self.descripcion

	def getDynamicText(self):
		return self.dynamicText1

	def getNumeroEscena(self):
		return int(self.numeroEscena)

	def setDynamicTextNew(self):
		self.dynamicText1 = self.dynamicText2

	def getActivo(self):
		return self.activo

	def setTipoObjeto(self,value):
		self.tipoObjeto=value

	def setActivo(self,value):
		self.activo=value

	################################
	def print(self):
		print ("numero> ",self.numero,"nombre> ",self.nombre,"descripcion> ",self.descripcion,"dyn1> ",self.dynamicText1,"dyn2> ",self.dynamicText2,"tipoObjeto> ",self.tipoObjeto,"activo> ",self.activo,"escena> ",self.numeroEscena)
