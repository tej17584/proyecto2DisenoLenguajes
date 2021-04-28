"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: main.py
Propósito: Este programa es el que lee los archivos
V 1.0
"""
# zona de import de librerías
from os import remove
from funciones import *
from pprint import pprint as pp
from posftixEvaluador import *
from tipoVar import *
from postFixTokens import *
from reader import *
from AFNDirecto import *
import pickle
import re
import os


# creamos las instancias de clases
instancia_reader = Reader()
instancia_funciones = funciones()
arrayEntradaP1 = []


def menu():

    os.system('cls')  # NOTA para windows tienes que cambiar clear por cls
    print("Selecciona una opción")
    print("\t1 - Iniciar lectura y creacion de scanner")
    print("\t9 - salir")


while True:
    # Mostramos el menu
    menu()

    # solicituamos una opción al usuario
    opcionMenu = input("Ingresa un valor... ")
    expresion = ""
    palabra = ""
    if opcionMenu == "1":

        expresion = ""
        palabra = "+5"
        # primero obtenemos los tokens finales
        tokensFinales = instancia_reader.getTokensFinales()
        llaveFinal = instancia_funciones.getLastTokenValueFromDict(
            tokensFinales)
        arrayValores = []
        for llave, valueforPostfix in tokensFinales.items():
            for numero, valornumero in valueforPostfix.items():
                arrayValores.append(valornumero)
            if(llaveFinal != llave):
                orEntreExpresiones = variableER_Enum(tipoVar.OR, ord("|"))
                arrayValores.append(orEntreExpresiones)
         # creamos una instancia nueva del posftix
        instancia_posftixTokens = ConversionPostfixTokens()
        posftix = instancia_posftixTokens.infixToPostfix(
            arrayValores)  # colocamos el valor del postfix
        # obtenemos el lenguaje
        lenguaje = instancia_funciones.getLanguage(posftix)
        # instanciamos el AFD directo
        objDirecto = AFNDIRECTO(posftix, lenguaje, palabra)
        objDirecto.generateAFNDIRECTO()
        # obtenemos el AFD final, el diccionario de siguientePos y los nodos de aceptacion
        dicionarioAFDFinal = objDirecto.getAFDDirecto()
        diccionarioSiguientePos = objDirecto.getdiccionarioSiguientePos()
        diccionarioEstadosAceptacion = objDirecto.getNodosAceptacion()
        #! hacemos DUMP de los tres files
        # primero el afd entero
        filename = 'dicionarioAFDFinal'
        outfile = open(filename, 'wb')
        pickle.dump(dicionarioAFDFinal, outfile)
        outfile.close()
        # ahora el de siguiente pos
        filename = 'diccionarioSiguientePos'
        outfile = open(filename, 'wb')
        pickle.dump(diccionarioSiguientePos, outfile)
        outfile.close()
        # finalmente el de estados de aceptacion
        filename = 'diccionarioEstadosAceptacion'
        outfile = open(filename, 'wb')
        pickle.dump(diccionarioEstadosAceptacion, outfile)
        outfile.close()
        # generamos el scanner.py
        input("Presiona ENTER para continuar")
    elif opcionMenu == "9":
        break
    else:
        print("")
        input("No has pulsado ninguna opción correcta...\npulsa ENTER para continuar")
