import tkinter
import os
import time
from Escenas import *
from ObjetosInventario import *
from ObjetosInteractivos import *

listaAcciones=[0,"mirar",1,"abrir",2,"cerrar",3,"empujar",4,"tirar",5,"encender",6,"apagar",7,"recoger",8,"usar",9,"ir"]
mostrarResultado=""
clearConsole = lambda: print('\n' * 500)

#Funciones CREAR OBJETOS Y ESCENAS
def CrearListaObjetos(value):

	if value == 1:
		archivo=open("ObjetosInventario.txt","r")
	if value == 2:
		archivo=open("ObjetosInteractivos.txt","r")

	lista1=archivo.readlines()
	lista2=[]

	var0=""
	var1=""
	var2=""
	var3=""
	var4=""
	var5=""

	index=0
	for linea in lista1:
		aux=True
		if index==5:
			var5=linea.strip()
			index=0
			lista2.append((int(var0),var1,var2,var3,var4,int(var5)))
			aux=False
		if index==4:
			var4=linea.strip()
			index = index + 1
		if index==3:
			var3=linea.strip()
			index = index + 1
		if index==2:
			var2=linea.strip()
			index = index + 1
		if index==1:
			var1=linea.strip()
			index = index + 1
		if index==0 and aux==True:
			var0=linea.strip()
			index = index + 1
	archivo.close()
	nuevaLista=[]

	if value==1:
		for elemento in lista2:
			nuevaLista.append(ObjetosInventario(elemento[0],elemento[1],elemento[2],elemento[3],elemento[4],elemento[5]))
	if value==2:
		for elemento in lista2:
			nuevaLista.append(ObjetosInteractivos(elemento[0],elemento[1],elemento[2],elemento[3],elemento[4],elemento[5]))

	for elemento in nuevaLista:
		if value==1:
			elemento.setTipoObjeto(1)
		if value==2:
			elemento.setTipoObjeto(2)

	return nuevaLista
def CrearEscenas():
	"""
	A partir de un .txt, creo una lista de tuplas que, posteriormente, convierto en lista de objetos de clase Escenas.
	"""
	archivo=open("Escenas.txt","r")
	lista1=archivo.read()
	lista2=[]
	
	var0=""
	var1=""
	var2=""
	var3=""
	index=0
	palabra=""
	for caracter in lista1:
		aux=True
		if index==3:
			if caracter == "#":
				index=0
				lista2.append((var0,var1,var2,var3))
				aux=False
				var0=""
				var1=""
				var2=""
				var3=""
			else:
				var3=var3+caracter
		if index==2:
			if caracter == "#":
				index = index + 1 
			else:
				var2=var2+caracter
		if index==1:
			if caracter == "#":
				index = index + 1 
			else:
				var1 = var1+caracter
		if index==0 and aux==True:
			if caracter == "#":
				index = index + 1  
			else:
				var0 = var0+caracter  

	archivo.close()

	nuevaLista=[]

	for elemento in lista2:
		nuevaLista.append(Escenas(elemento[0],elemento[1],elemento[2],elemento[3]))

	return nuevaLista	
#Funciones Escenas
def DescripcionEscena():
	global escenaActiva
	global listaEscenas
	global objInteractivo
	global objInventario

	print("                                          ",listaEscenas[escenaActiva].getName())
	print(listaEscenas[escenaActiva].getDescription())

	for elemento in objInteractivo:
		if elemento.getNumeroEscena() == escenaActiva:
			if elemento.getActivo():
				print(elemento.getDynamicText())

	for elemento in objInventario:
		if elemento.getNumeroEscenaDondeEstaActivo() == escenaActiva and elemento.getActivo():
			print(elemento.getDynamic1())
	print("\n")
	MostrarInteractivos()
	MostrarInventario()
def ActivarEscena(nroEscena,value):
	global listaEscenas
	listaEscenas[nroEscena].setSceneActive(value)
def HandlerEscenas():
	#(nro escena, nro escena NORTE, nro escena SUR, nro escena OESTE, nro escena ESTE)  --- se ingresa -1 si no se puede ir
	salidasPosibles=[(0,1,-1,-1,-1),(1,4,0,2,3),(2,-1,-1,-1,1),(3,-1,-1,1,-1),(4,-1,1,-1,-1)]
	return salidasPosibles
def PuedoIr(desde,hacia):
	global salidasEscenas
	global escenaActiva
	salida=False
	for elemento in salidasEscenas:
		if elemento[0] == desde:
			for subelemento in elemento:
				if hacia in elemento and hacia != elemento[0]:
					salida=True
	return salida

#Funciones Objetos
def ChequearObjetoExistente(nombreObjeto):
	#deberia hacer un return con el numero de objeto.
	global objInteractivo
	global objInventario
	global escenaActiva
	global mostrarResultado
	

	encontrado=False
	activado=False
	salida=False
	tipoObjeto=0
	nroObjeto=0

	for elemento in objInventario:
		if elemento.getNombre() == nombreObjeto:
			encontrado=True
			tipoObjeto=1
			nroObjeto=elemento.getNumero()

	for elemento in objInteractivo:
		if elemento.getNombre() == nombreObjeto:
			encontrado=True
			tipoObjeto=2
			nroObjeto=elemento.getNumero()

	if encontrado==True:
		activado=ChequearObjetoActivo(tipoObjeto,int(nroObjeto))
		if activado==True:
			salida=True
		else:
			if tipoObjeto == 1:
				mostrarResultado="El objeto no esta en tu inventario"
			elif (tipoObjeto == 2) and (escenaActiva == int(ObjetoEnEscenaCorrecta(nroObjeto))):
				mostrarResultado="El objeto no esta disponible."
			else:
				mostrarResultado="Aquí no hay nada que se llame así."
	else:
		mostrarResultado="El objeto no existe."
	return salida
def ChequearObjetoActivo(tipoObjeto,numeroObjeto):
	"""
	Con el tipo de objeto (1 o 2) y el numero, me fijo si el objeto existe o no y devuelvo booleano.
	"""
	global objInventario
	global objInteractivo
	global escenaActiva

	string=""
	if tipoObjeto == 1:
		if objInventario[int(numeroObjeto)].getActivo() == True:
			return True
		else:
			return False
	if tipoObjeto == 2:
		if objInteractivo[numeroObjeto].getActivo() and int(objInteractivo[numeroObjeto].getNumeroEscena()) == escenaActiva:
			return True
		else:
			return False
def ObjetoEnEscenaCorrecta(nroObjeto):
	global objInteractivo
	nroObjeto = int(nroObjeto)
	return objInteractivo[nroObjeto].getNumeroEscena()

#Funciones MENSAJE
def ConstruirMensaje(entrada):
	cantidadEntrada=DevolverCantidadEntrada(entrada)
	global ultimaEntrada
	global mostrarResultado

	if cantidadEntrada == 0:
		mostrarResultado="Tienes que escribir una acción."
	elif cantidadEntrada == 3:
		mostrarResultado="Te falta algo... o quizas te sobra."
	elif cantidadEntrada > 4:
		mostrarResultado="La frase es demasiado larga. Revisa que no haya errores."
	else:
		ArmarEntrada(entrada,cantidadEntrada)

def DevolverCantidadEntrada(entrada):
	contador=1
	if entrada == "":
		contador=0
	for caracter in entrada:
		if caracter == " ":
			contador = contador +1
	return contador	
def ArmarEntrada(entrada,cantidad):
	global mensaje
	global mostrarResultado
	m1=""
	m2=""
	m3=""
	m4=""
	contador=0
	if cantidad == 1:
		if entrada == "quit":
			mensaje[0]=entrada
		elif entrada == "ayuda" or entrada == "help":
			Ayuda()
		elif entrada == "acciones":
			MostrarAcciones()
		else:
			mostrarResultado="Tienes que construir una frase valida. Introduce ayuda para recibir tips."
	if cantidad == 2:
		for caracter in entrada:
			if caracter == " ":
				contador = contador + 1
			if contador == 0:
				m1 = m1 + caracter
			if contador == 1 and caracter != " ":
				m2 = m2 + caracter
		mensaje[0]=m1
		mensaje[1]=m2
	if cantidad == 4:
		for caracter in entrada:
			if caracter == " ":
				contador = contador + 1
			if contador == 0:
				m1 = m1 + caracter
			if contador == 1 and caracter != " ":
				m2 = m2 + caracter
			if contador == 2 and caracter != " ":
				m3 = m3 + caracter
			if contador == 3 and caracter != " ":
				m4 = m4 + caracter
		mensaje[0]=m1
		mensaje[1]=m2
		mensaje[2]=m3
		mensaje[3]=m4	
	if cantidad != 1:	
		ChequearPalabrasEnMensaje(cantidad)	
def ChequearPalabrasEnMensaje(cantidad):
	global mensaje
	global listaAcciones

	if mensaje[0] not in listaAcciones:
		mostrarResultado="Esa accion no existe. Teclea de nuevo la frase y revisa la ortografia."
	else:
		if cantidad == 2 and DestinoAceptado(mensaje[1].lower()) == False:
			if ChequearObjetoExistente(mensaje[1]):
				SeleccionFuncionAcciones(mensaje[0])
				
		if cantidad == 2 and DestinoAceptado(mensaje[1].lower()):
			SeleccionFuncionAcciones(mensaje[0])

		if cantidad == 4:
			if ChequearObjetoExistente(mensaje[1]) and ChequearSilabas4Palabras():
				if ChequearCuartaPalabra():
					SeleccionFuncionAcciones(mensaje[0])
				else:
					mostrarResultado="No se puede usar",mensaje[1],"porque",mensaje[3], "no existe o no esta disponible."

def ChequearSilabas4Palabras():
	global mensaje
	global listaAcciones
	listaPreposiciones=("con","sobre","en","contra")

	resultado = False

	if mensaje[0] == "usar" and mensaje[2] in listaPreposiciones:
		resultado = True
	else:
		if mensaje[0] != "usar" and mensaje[2] in listaPreposiciones:
			mostrarResultado="Lee otra vez la ayuda (escribe ayuda). Las frases complejas solo funcionan con la acción USAR."
		elif mensaje[0] == "usar" and mensaje[2] not in listaPreposiciones:
			mostrarResultado="Lee otra vez la ayuda (escribe ayuda). La accion usar solo funciona con algunas preposiciones."
		else:
			mostrarResultado="No entiendo la frase. Escribela otra vez, revisa la ortografia o pide ayuda (escribe ayuda)."
	return resultado
def ChequearCuartaPalabra():
	global mensaje

	if ChequearObjetoExistente(mensaje[3]):
		return True
	else:
		return False

#Funciones ACCIONES
def SeleccionFuncionAcciones(accion):
	global mensaje
	global escenaActiva
	global listaEscenas
	global mostrarResultado

	if accion == "ir":
		destino=DefinirOrientacion(mensaje[1])		
		if destino != -1 and irOtraEscena(destino) and irOtraEscena(destino):
			escenaActiva=DefinirOrientacion(mensaje[1])
			mostrarResultado="Llegando..."
		else:
			mostrarResultado="Es imposible ir al " + mensaje[1]
	elif accion == "usar":
		UsarItemsConItems()
	else:
		DeterminadorAcciones()
def AccionPorDefecto(accion,tipoObjeto,objeto):
	"""
	Esta seria la funcion por defecto, es decir, si no es una accion "especial", viene acá y me tira un mensaje generico.
	Pero se llega a ésta función después de chequear que el objeto existe (es decir, está activo en escena/inventario)
	"""
	global listaAcciones
	global objInteractivo
	global objInventario
	global mostrarResultado

	if tipoObjeto==1:
		lista=objInventario
	if tipoObjeto==2:
		lista=objInteractivo

	#mirar
	if accion == 0:
		mostrarResultado=lista[objeto].getDescripcion()
	#abrir
	if accion == 1:
		mostrarResultado=lista[objeto].getNombre().capitalize() + " << No se puede abrir."
	#cerrar
	if accion == 2:
		mostrarResultado=lista[objeto].getNombre().capitalize() + " << No se puede cerrar."
	#empujar
	if accion == 3:
		mostrarResultado=lista[objeto].getNombre().capitalize() + " << No quiero empujar eso."
	#tirar
	if accion == 4:
		mostrarResultado=lista[objeto].getNombre().capitalize() + " << No puedo tirar de eso."
	#encender
	if accion == 5:
		mostrarResultado=lista[objeto].getNombre().capitalize() + " << Eso no se enciende."
	#apagar
	if accion == 6:
		mostrarResultado=lista[objeto].getNombre().capitalize() + " << ¿Como voy a apagar eso?"
	#recoger
	if accion == 7:
		mostrarResultado=lista[objeto].getNombre().capitalize() + " << No puedo recoger eso."
	#usar
	if accion == 8:
		mostrarResultado=lista[objeto].getNombre().capitalize() + " << Eso no se puede usar así."
def AccionEspecial(escena,accion,tipoObjeto,objeto):
	global listaAcciones
	global objInteractivo
	global objInventario
	global mostrarResultado
	global listaEscenas

	if tipoObjeto==1:
		lista=objInventario
	if tipoObjeto==2:
		lista=objInteractivo

	#ESCENA 0 - BOSQUE
	if escena == 0:
		if accion == 7:
			if tipoObjeto == 2 and objeto == 4:
				mostrarResultado="Parecen ser pesadas y no tiene sentido ir cargando con ellas."
		if accion==9:
			if tipoObjeto==2 and objeto == 2:
				mostrarResultado="CAMINO HACIA LA SALIDA"
			if tipoObjeto == 2 and objeto == 5:
				mostrarResultado="No tiene sentido. La ruta esta abandonada y quiero saber que está pasando"

	#ESCENA 1 - PUERTAS LABORATORIO
	if escena == 1:
		if accion == 1:
			if tipoObjeto == 2 and objeto == 14: 
				#tengo que chequear que la electricidad este funcionando 
				if listaVerbose[0] == True:
					mostrarResultado="El porton ya esta abierto"
				else:
					if listaVerbose[7]: #el ojo ya fue usado en el panel
						mostrarResultado="Lo logre. El porton se ha abierto. Ya puedo ingresar al laboratorio."
						listaEscenas[4].setSceneActive(True)
					else:
						mostrarResultado="El porton tiene que abrirse con algun tipo de mecanismo de seguridad cercano."
			if tipoObjeto == 2 and objeto == 5:
				mostrarResultado="Están muy altas y no llego. Además, creo que me sería imposible abrirlas."
			if tipoObjeto == 2 and objeto == 4:
				mostrarResultado="El panel no esta hecho para abrirse. Podria estropearlo."
		if accion == 3:
			if tipoObjeto == 2 and objeto == 6: 
				#tengo que chequear accion1
				if listaVerbose[1] == True:
					if listaVerbose[2] == False:
						mostrarResultado="Forcejeo." + "\n" + "Erratico, se tira contra mi. Luchamos." + "\n" + "Mueve la mandíbula de arriba hacia abajo, buscando mi piel." + "\n" + "Jadeando, logro sacar fuerza de lo más profundo de mi ser. Lo empujo contra la pared y su cabeza da con la palanca. Lo que quedaba de el ahora no es mas que una viscosidad. Sobre la palanca, ha quedado uno de sus ojos intactos."
						AccionesVerbose(2,True)
						objInventario[5].setActivo(True)
						objInteractivo[6].setDynamicTextNew()
					else:
						mostrarResultado="No tiene sentido, ya no puede hacer ningun tipo de dano."
			if tipoObjeto == 2 and objeto == 8:
				mostrarResultado="La parte visible esta incrustada en la pared. Es imposible lograr que se mueva."
			if tipoObjeto == 2 and objeto == 14:
				mostrarResultado="Debe pesar una tonelada. No voy a malgastar fuerza."				
		if accion == 4:
			if tipoObjeto == 2 and objeto == 6:
				mostrarResultado="Prefiero no hacerlo."
		if accion == 7:
			if tipoObjeto == 1 and objeto == 5:
				if objInventario[5].getRecogido() == False and objInventario[5].getActivo():
					mostrarResultado="Pensar en eso me da nauseas, pero me puede servir. Presiento que nunca me olvidare de esto."
					objInventario[5].setRecogido(True) #para que me aparezca en el inventario
					objInventario[5].setChangeDynamic()
			if tipoObjeto == 2 and objeto == 8:
				mostrarResultado="No puedo. No quiero. No tiene sentido. En resumen... no."

	#ESCENA - 2 ----------- Garita
	if escena == 2:
		if accion == 1:
			if tipoObjeto == 2 and objeto == 9:
				if listaVerbose[3]:
					mostrarResultado="Ya esta abierta. Y no hay nada interesante."
				else:
					mostrarResultado="Imposible abrirla solo con mis manos."
		if accion == 2:
			if tipoObjeto == 2 and objeto == 9:
				if listaVerbose[3]:
					mostrarResultado="Un verdadaro sinsentido."
				else:
					mostrarResultado="Ya esta cerrada. Cerrar lo cerrado es total y absolutamente imposible. Al menos para mi."
		if accion == 3:
			if tipoObjeto == 2 and objeto == 10:
				if listaVerbose[4]:
					mostrarResultado="No pienso acercarme. Es peligroso."
				else:
					mostrarResultado="No puedo llegar hasta alli. La fisica me lo impide."
		if accion == 5:
			if tipoObjeto == 2 and objeto == 11:
				if listaVerbose[5]:
					if listaVerbose[6]:
						mostrarResultado="Ya esta funcionando correctamente. Tengo que darme prisa."
					else:	
						mostrarResultado="Excelente. Ahora todo el perimetro tiene electricidad... al menos por un tiempo."
						#listaVerbose[6]=True
						objInteractivo[4].setDynamicTextNew()
						AccionesVerbose(6,True)
				else:
					mostrarResultado="Hasta que el cableado no este completo, no puedo hacer nada."
		if accion == 6:
			if tipoObjeto == 2 and objeto == 11:
				if listaVerbose[6]:
					mostrarResultado="No tiene sentido apagarlo ahora."
				else:
					mostrarResultado="Esta apagado..."
		if accion == 7:
			if tipoObjeto == 1 and objeto == 4:
				mostrarResultado="Una vieja palanca. Ahora no solo es vieja, tambien es mia."
				objInventario[4].setRecogido(True)
				objInventario[4].setChangeDynamic()
			if tipoObjeto == 2 and objeto == 13:
				mostrarResultado="Deberia darme cuenta que es imposible coger eso."

	#ESCENA - 3 ----------- Perimetro
	if escena == 3:
		if accion == 1:
			if tipoObjeto == 2 and objeto == 21:
				mostrarResultado="No es momento de ponerse a leer, pero si lo fuera, no elegiria jamas algo asi."
		if accion == 7:
			if tipoObjeto == 1 and objeto == 0:
				mostrarResultado="Ya la tengo en mi poder. Es pequeña y de metal."
				objInventario[0].setRecogido(True)
				objInventario[0].setChangeDynamic()
			if tipoObjeto == 1 and objeto == 2:
				mostrarResultado="Son unos buenos y resistenes cables de colores."
				objInventario[2].setRecogido(True)
				objInventario[2].setChangeDynamic()
			if tipoObjeto == 1 and objeto == 1:
				mostrarResultado="Perfecto. Es un cuchillo normal. Nunca esta mal tener uno... por si acaso."
				objInventario[1].setRecogido(True)
				objInventario[1].setChangeDynamic()
			if tipoObjeto == 2 and objeto == 15:
				mostrarResultado="Todavia no estoy en una situacion en donde eso sea algo posible o razonable... todavia.	"
			if tipoObjeto == 2 and objeto == 16:
				mostrarResultado="Son escombros. Que sentido tiene llevarlos conmigo? Donde los llevaria? Es ridiculo."
			if tipoObjeto == 2 and objeto == 18:
				mostrarResultado="No es una mala idea. Pero es pesado y necesitaria cortar un pedazo. No creo que tenga utilidad en mi situacion."
			if tipoObjeto == 2 and objeto == 20:
				mostrarResultado="Eso es algo muy sadico. La carne no se recoge. Ni se come."
			if tipoObjeto == 2 and objeto == 21:
				mostrarResultado="En otro momento de mi vida, podria haber sido una opcion. Ahora es solo una idea absurda."
def DeterminadorAcciones():
	global listaAcciones
	global objInteractivo
	global objInventario
	global escenaActiva
	global mensaje
	global mostrarResultado

	ubicacionEnListaDeAccion=listaAcciones.index(mensaje[0])-1
	accion=listaAcciones[ubicacionEnListaDeAccion]
	tipoObjeto,objeto=DevolverTipoYNumeroObjeto(mensaje[1])
	especial=False

	if tipoObjeto==1:
		lista=objInteractivo
	if tipoObjeto==2:
		lista=objInteractivo

	if escenaActiva == 0:
		if accion == 7:
			if tipoObjeto == 2 and objeto == 4:
				mostrarResultado="Parecen ser pesadas y no tiene sentido ir cargando con ellas."
	#ESCENA 1 - PUERTAS LABORATORIO
	if escenaActiva == 1:
		if accion == 1:
			if tipoObjeto == 2 and objeto == 14: 
				especial = True
			if tipoObjeto == 2 and objeto == 5:
				especial = True
			if tipoObjeto == 2 and objeto == 4:
				especial = True
		if accion == 3:
			if tipoObjeto == 2 and objeto == 6: 
				especial = True
			if tipoObjeto == 2 and objeto == 8:
				especial = True
			if tipoObjeto == 2 and objeto == 14:
				especial = True					
		if accion == 4:
			if tipoObjeto == 2 and objeto == 6:
				especial = True
		if accion == 7:
			if tipoObjeto == 1 and objeto == 5:
				especial = True
			if tipoObjeto == 2 and objeto == 8:
				especial = True

	#ESCENA - 2 ----------- Garita
	if escenaActiva == 2:
		if accion == 1:
			if tipoObjeto == 2 and objeto == 9:
				especial = True
		if accion == 2:
			if tipoObjeto == 2 and objeto == 9:
				especial = True
		if accion == 3:
			if tipoObjeto == 2 and objeto == 10:
				especial = True
		if accion == 5:
			if tipoObjeto == 2 and objeto == 11:
				especial = True
		if accion == 6:
			if tipoObjeto == 2 and objeto == 11:
				especial = True
		if accion == 7:
			if tipoObjeto == 1 and objeto == 4:
				especial = True
			if tipoObjeto == 2 and objeto == 13:
				especial = True

	#ESCENA - 3 ----------- Perimetro
	if escenaActiva == 3:
		if accion == 1:
			if tipoObjeto == 2 and objeto == 21:
				especial = True
		if accion == 7:
			if tipoObjeto == 1 and objeto == 0:
				especial = True
			if tipoObjeto == 1 and objeto == 2:
				especial = True
			if tipoObjeto == 1 and objeto == 1:
				especial = True
			if tipoObjeto == 2 and objeto == 15:
				especial = True
			if tipoObjeto == 2 and objeto == 16:
				especial = True
			if tipoObjeto == 2 and objeto == 18:
				especial = True
			if tipoObjeto == 2 and objeto == 20:
				especial = True
			if tipoObjeto == 2 and objeto == 21:
				especial = True
	if especial==True:
		AccionEspecial(escenaActiva,accion,tipoObjeto,objeto)
	else:
		AccionPorDefecto(accion,tipoObjeto,objeto)
def AccionesVerbose(numeroAccion,valor):
	global listaVerbose
	#accion 0 - Electricidad PORTON en funcionamiento	
	#accion 1 - Zombie en escena PORTON
	#accion 2 - Zombie abatido en escena PORTON
	#accion 3 - Garita abierta
	#accion 4 - Guardia despierto
	#accion 5 - Cables en generador
	#accion 6 - Generador encendido
	#accion 7 - Panel Encendido
	#accion 8 -
	listaVerbose[numeroAccion]=valor
def UsarItemsConItems():
	global escenaActiva
	global listaVerbose
	global objInteractivo
	global objInventario
	global listaEscenas
	global mostrarResultado

	mensajePorDefecto="No tiene sentido usar eso asi."
	print("Recogido> ",objInventario[0].getRecogido())
	print("msj[1]> ",mensaje[1])
	print("msj[3]> ",mensaje[3])
	if escenaActiva == 1:
		if mensaje[1] == "llave" and mensaje[3] == "porton":
			if objInventario[0].getRecogido():
				mostrarResultado="La llave es demasiado pequena, de una puerta normal. El porton se abre con un mecanismo especial. Nada de llaves."
		elif mensaje[1] == "ojo" and mensaje[3] == "panel":
			if objInventario[5].getRecogido() and listaVerbose[6]:
				AccionesVerbose(7,True)
				objInventario[5].setRecogido(False)
				objInteractivo[14].setDynamicTextNew()
				mostrarResultado="Presiono el ojo contra el panel y una luz verde aparece por debajo del porton. Ya puedo abrirlo."
			else:
				mostrarResultado="El panel no tiene electridad. Tengo que encender el generador."
		else:
			mostrarResultado=mensajePorDefecto

	if escenaActiva == 2:
		if mensaje[1] == "cables" and mensaje[3] == "generador":
			mostrarResultado="Excelente. Encajaron a la perfeccion. Ahora tengo que encenderlo."
			objInventario[2].setActivo(False)
			objInventario[2].setRecogido(False)
			AccionesVerbose(5,True)
			objInteractivo[11].setDynamicTextNew()
			#listaVerbose[5]=True
		if mensaje[1] == "cuchillo" and mensaje[3] == "guardia":
			if listaVerbose[4]:
				print("No puedo acercarme tanto... y en caso que pudiera, este cuchillo es un triste e inutil recuerdo de un arma. No puedo atacar al guardia con esto, necesito algo mas largo y poderoso.")
			else:
				print("Este es un cuchillo que ya ha gastado todo su potencial de ataque. Ahora es poco mas que un adorno.")			
		elif mensaje[1] == "llave" and mensaje[3] == "garita":
			mostrarResultado="Hecho. La garita esta abierta. La llave ya no me va a servir. Pero... el guardia. Se mueve. Esta vivo... o algo asi. Me tiene rodeado, no puedo escapar."
			AccionesVerbose(3,True)
			AccionesVerbose(4,True)
			#listaVerbose[3]=True
			#listaVerbose[4]=True
			objInventario[0].setActivo(False)
			objInventario[0].setRecogido(False)
			objInteractivo[9].setDynamicTextNew()
			objInteractivo[10].setDynamicTextNew()
			listaEscenas[1].setSceneActive(False)
		elif mensaje[1] == "palanca" and mensaje[3] == "guardia":
			if listaVerbose[4]:
				mostrarResultado="La palanca se ha roto contra su cabeza. El guardia esta aturdido y puedo escapar. Ya puedo salir de aqui."
				objInventario[4].setRecogido(False)
				objInventario[4].setActivo(False)
				objInteractivo[10].setActivo(False)
				listaEscenas[1].setSceneActive(True)
				objInteractivo[6].setActivo(True)
				AccionesVerbose(1,True)
			else:
				mostrarResultado="Pegarle con una palanca a un cuerpo inerte. No... no llegue a ese punto de locura. Todavia."
		else:
			mostrarResultado = mensajePorDefecto

def irOtraEscena(hacia):
	global listaEscenas
	global escenaActiva
	salir=False
	if listaEscenas[hacia].getSceneActive() and hacia != -1:
		if PuedoIr(escenaActiva,hacia):
			salir = True
	return salir
def DefinirOrientacion(orientacion):
	global salidasEscenas
	global escenaActiva

	orientacion=orientacion.lower()
	salida = -1
	if orientacion == "norte":
		salida=salidasEscenas[escenaActiva][1]
	if orientacion == "sur":
		salida=salidasEscenas[escenaActiva][2]
	if orientacion == "oeste":
		salida=salidasEscenas[escenaActiva][3]
	if orientacion == "este":
		salida=salidasEscenas[escenaActiva][4]
	return salida

#Funciones VARIAS
def Introduccion():
	print("¿Donde estoy?")
	time.sleep(1)
	print("¿Que ha pasado aqui?")
	time.sleep(1)
	print("Huelo sangre. Oh Dios, es mia.")
	time.sleep(1)
	print("Alguien me ha traido aqui.")
	time.sleep(1)
	print("Tengo que saber que ha pasado.")
	time.sleep(3)
	clearConsole
def MostrarAcciones():
	print("Las acciones disponibles son:")
	print("Mirar  		   --->  mirar <objeto>")
	print("Abrir/Cerrar    ---> abrir <objeto>")
	print("Tirar/Empujar   ---> tirar <objeto>")
	print("Encender/Apagar ---> apagar <objeto>")
	print("Ir              ---> ir norte/sur/oeste/este")
	print("Usar            ---> usar <item> en/sobre/con <objeto>")
	print("")
	print("Presiona <ENTER> para continuar")
	input()
	clearConsole()
def Ayuda():
	print("Este es un juego en donde hay que ingresar los comandos por teclado.")
	print("La sintaxis es importante. Observa ingresar de forma correcta los comandos y los objetos.")
	print("Para saber las acciones disponibles:")
	print("Escribe 'acciones' en la linea de comando.")
	print("Presiona <ENTER> para continuar")
	input()
	clearConsole()
def DevolverTipoYNumeroObjeto(nombre):
	global objInventario
	global objInteractivo
	encontrado = False
	tipo=0
	numero=5000

	for elemento in objInventario:
		if elemento.getNombre() == nombre:
			encontrado=True
			tipo=1
			numero=int(elemento.getNumero())

	if encontrado==False:
		for elemento in objInteractivo:
			if elemento.getNombre() == nombre:
				encontrado=True
				tipo=2
				numero=int(elemento.getNumero())
	return tipo,numero
def DestinoAceptado(mensaje):
	if mensaje=="norte" or mensaje=="sur" or mensaje=="oeste" or mensaje=="este":
		return True
	else:
		return False
def DesactivarObjetos():
	#Desactivar zombie, ojo.

	global objInteractivo
	global objInventario
	listaInteractivosADesactivar=[6,7]
	listaInventarioADesactivar=[5]

	for elemento in listaInteractivosADesactivar:
		objInteractivo[elemento].setActivo(False)

	for elemento in listaInventarioADesactivar:
		objInventario[elemento].setActivo(False)
def DesactivarEscenas():
	global listaEscenas
	#Desactivar escena 4
	listaEscenasADesactivar=[4]

	for elemento in listaEscenasADesactivar:
		listaEscenas[elemento].setSceneActive(False)
def MostrarInventario():
	global objInventario
	global escenaActiva
	inventario=""

	for elemento in objInventario:
		if elemento.getRecogido():
			inventario = inventario + " -" + elemento.getNombre().capitalize()
	if inventario != "":
		print("Inventario|    ",inventario)
	else:
		print("Inventario|   <vacio>")
def MostrarInteractivos():
	global objInteractivo
	global objInventario
	global escenaActiva
	interactivos=""

	for elemento in objInteractivo:
		if elemento.getActivo() and escenaActiva == elemento.getNumeroEscena():
			interactivos = interactivos + " -" + elemento.getNombre().capitalize()

	for elemento in objInventario:
		if elemento.getActivo() and escenaActiva == elemento.getNumeroEscenaDondeEstaActivo() and elemento.getRecogido() == False:
			interactivos = interactivos + " -" + elemento.getNombre().capitalize()

	print("Objetos En Escena <<<" + interactivos + " >>>")
def MostrarSalidas():
	global escenaActiva
	global salidasEscenas

	mensaje = "Destinos: |"
	salidasPosibles=salidasEscenas[escenaActiva]
	if salidasPosibles[1] != -1 and irOtraEscena(DefinirOrientacion("norte")):
		mensaje = mensaje + " Norte |"
	if salidasPosibles[2] != -1 and irOtraEscena(DefinirOrientacion("sur")):
		mensaje = mensaje + " Sur |"
	if salidasPosibles[3] != -1 and irOtraEscena(DefinirOrientacion("oeste")):
		mensaje = mensaje + " Oeste |"
	if salidasPosibles[4] != -1 and irOtraEscena(DefinirOrientacion("este")):
		mensaje = mensaje + " Este |"

	print(mensaje)



objInventario=CrearListaObjetos(1)
objInteractivo=CrearListaObjetos(2)
listaEscenas=CrearEscenas()
escenaActiva=0
salidasEscenas=HandlerEscenas()
#el total de elementos de lista verbose tiene que finiquitarse cuando se sepan todas las acciones que va a requerir el juego.
listaVerbose=[False,False,False,False,False,False,False,False,False,False,False,False,False,False]

mensaje=["","","",""]
ultimaEntrada=" "
entrada =""

##PREPARACION PRE GAME
DesactivarObjetos()
DesactivarEscenas()


Introduccion()


while mensaje[0] != "quit":
	if escenaActiva==4:
		break;
	clearConsole()
	ConstruirMensaje(entrada)
	ultimaEntrada=entrada.upper()
	print("                                                                                         Ultimo Comando>>",ultimaEntrada)
	DescripcionEscena()
	print("\n",mostrarResultado,"\n")
	MostrarSalidas()
	print("\n")
	entrada=input(">>> ")


clearConsole()
print("Esto fue una demo.")
print("Algun dia, con suerte, estara terminado el proyecto.")
print("                                       voltum3l")









