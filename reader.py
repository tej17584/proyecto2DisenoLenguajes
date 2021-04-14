"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: reader.py
Propósito: Este programa tiene como propósito leer el archivo con extension .ATG
V 1.0
"""

# ! Zona de imports
from funciones import funciones
from pprint import pprint as pp
from Evaluador import *


class Reader:
    """
    La clase Reader lee el file y lo guarda en una estructura de datos adecuada
    """

    def __init__(self) -> None:
        self.streamCompleto = ""
        self.dictArchivoEntrada = ""
        self.lineasArchivo = []
        self.lineasPalabras = {}
        self.jsonFinal = {}  # diccionario final
        self.nombreCompilador = ""
        self.funciones = funciones()
        self.evaluador = Conversion()
        self.isChar = False
        self.isToken = False
        self.isKeyword = False
        # self.readDocumentAndPoblateStream()
        self.readDocument()

    def readDocumentAndPoblateStream(self):
        """
        Lee el documento ENTERO y lo guarda en una variable, es un stream continuo
        """
        with open('ATGFilesExamples\ejemploProyecto.atg', 'r') as f:
            self.streamCompleto = f.read().replace('\n', '')
        f.close()

        #print("Stream completo ", self.streamCompleto)

    def checkIfCharExists(self, character):

        for llave, valor in self.jsonFinal.items():
            for x, y in valor.items():
                for valorCaracter in character:
                    if(x == valorCaracter and llave == "CHARACTERS"):
                        return True, y, valorCaracter

        return False, [], ""

    def readDocument(self):
        """
        Lee el documento de entrada linea por linea y va guardandolo en un diccionario, esa será la estructura.
        Luego, verifica en toda las lineas cual es la linea donde estan los tokens que nos interesan.
        """
        with open('ATGFilesExamples\ejemploProyecto.atg', "r") as f:
            self.lineasArchivo = f.readlines()
        f.close()

        # Leemos las lineas donde estan las palabras especiales y guardamos el número  de linea.
        # Esto nos puede servir luego.
        count = 0
        for line in self.lineasArchivo:
            line = line.rstrip("\n")  # eliminamos la linea
            if "COMPILER" in line:
                self.nombreCompilador = self.funciones.removerPalabraSingle(
                    line, "COMPILER")
                self.lineasPalabras["COMPILER"] = count
            if line == "CHARACTERS" or line == "CHARACTER":
                self.lineasPalabras[line] = count
            if line == "TOKENS" or line == "TOKEN":
                self.lineasPalabras[line] = count
            if line == "KEYWORDS" or line == "KEYWORD":
                self.lineasPalabras[line] = count
            if ("END" in line) and (self.funciones.removerPalabraSingle(line, "END") == ((self.nombreCompilador+"."))
                                    or self.funciones.removerPalabraSingle(line, "END") == ((self.nombreCompilador))):
                self.lineasPalabras["END"] = count
            if line == "PRODUCTIONS" or line == "PRODUCTION":
                self.lineasPalabras[line] = count
            count += 1

        for line in self.lineasArchivo:
            line = line.rstrip("\n")  # eliminamos la linea
            line = line.replace(" ", "")  # quitamos el espacio en blanco
            # Dependiendo del tipo de valor, seteamos el valor de la booleana,
            # de esa forma iteramos
            if(line == "CHARACTERS" or line == "CHARACTER"):
                self.isChar = True
                self.isKeyword = False
                self.isToken = False
                # creamos la entrada de valor en el dict final
                self.jsonFinal["CHARACTERS"] = {}
            elif(line == "TOKENS" or line == "TOKEN"):
                self.isChar = False
                self.isKeyword = False
                self.isToken = True
                # creamos la entrada de valor en el dict final
                self.jsonFinal["TOKENS"] = {}
            elif(line == "KEYWORDS" or line == "KEYWORD"):
                self.isChar = False
                self.isKeyword = True
                self.isToken = False
                # creamos la entrada de valor en el dict final
                self.jsonFinal["KEYWORDS"] = {}

            if(self.isChar):
                # hacemos split con el '=', esto es un ARRAY
                charSplit = line.split("=")
                if(type(charSplit) != None and len(charSplit) > 1 and charSplit[0] != "CHARACTERS"):
                    localDictChar = {}
                    charName = str(charSplit[0].replace(" ", ""))
                    charValue = charSplit[1]
                    # extramos los valores unicos la
                    localEvaluador = Conversion()
                    arrayCharValue = localEvaluador.infixToPostfix(charValue)
                    arrayCharValue = arrayCharValue.split(' ')
                    charExists, array, valorCaracter = self.checkIfCharExists(
                        arrayCharValue)
                    if(charExists and len(valorCaracter) > 0 and len(array) > 0):
                        array = array.replace('.', '')
                        charValue = charValue.replace(valorCaracter, array)
                        localDictChar[charName] = charValue
                        self.jsonFinal["CHARACTERS"].update(localDictChar)

                    # verificamos si existe
                    if('+' in charValue):
                        localEvaluador2 = Conversion()
                        charValue2 = charValue.replace('.', "")
                        postfixCharValue = localEvaluador2.infixToPostfix(
                            charValue2)
                        postfixCharValue = postfixCharValue.split(' ')
                        operatedCharValue = localEvaluador2.operatePostFix(
                            postfixCharValue)
                        charValue = self.funciones.sortString(
                            operatedCharValue)
                        # print(charValue)
                        localDictChar[charName] = charValue
                        self.jsonFinal["CHARACTERS"].update(localDictChar)

                    localDictChar[charName] = charValue
                    self.jsonFinal["CHARACTERS"].update(localDictChar)

        pp(self.jsonFinal)
        #print("Nombre compilador: "+self.nombreCompilador)
        # pp(self.lineasPalabras)


reader = Reader()
