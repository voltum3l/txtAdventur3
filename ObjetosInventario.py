class ObjetosInventario:
	def __init__(self,numero,nombre,descripcion,dynamic1,dynamic2,activadoEnEscena):
		self.numero = numero
		self.nombre = nombre
		self.descripcion = descripcion
		self.dynamic1 = dynamic1
		self.dynamic2 = dynamic2
		self.tipoObjeto = 0
		self.activo = True
		self.activadoEnEscena = activadoEnEscena
		self.recogido = False

	def getNumero(self):
		return int(self.numero)

	def getNombre(self):
		return self.nombre

	def getDescripcion(self):
		return self.descripcion

	def getDynamic1(self):
		return self.dynamic1

	def getActivo(self):
		return self.activo

	def setChangeDynamic(self):
		self.dynamic1 = self.dynamic2

	def setActivo(self,value):
		self.activo=value
	def getNumeroEscenaDondeEstaActivo(self):
		return self.activadoEnEscena

	def setTipoObjeto(self,value):
		self.tipoObjeto=value

	def getRecogido(self):
		return self.recogido

	def setRecogido(self,value):
		self.recogido = value


	################################
	def print(self):
		print ("numero> ",self.numero,"nombre> ",self.nombre,"descripcion> ",self.descripcion,"tipoObjeto> ",self.tipoObjeto,"activo> ",self.activo,"desc1> ",self.dynamic1,"desc2> ",self.dynamic2,"activado en escena> ",self.activadoEnEscena)

