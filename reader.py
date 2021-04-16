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
        self.rutaFile = "ATGFilesExamples\C.atg"
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
        self.readDocumentAndPoblateStream()
        self.readDocument()

    def readDocumentAndPoblateStream(self):
        """
        Lee el documento ENTERO y lo guarda en una variable, es un stream continuo
        """
        with open(self.rutaFile, 'r', encoding='utf-8') as f:
            self.streamCompleto = f.read().replace('\n', '')
        f.close()

        # print("Stream completo ", self.streamCompleto)

    def checkIfCharExists(self, character):

        for llave, valor in self.jsonFinal.items():
            for x, y in valor.items():
                if(x == character and llave == "CHARACTERS"):
                    return True, y

        return False, []

    def checkIfMoreCharExist(self, character):
        arrayLocal = []
        for llave, valor in self.jsonFinal.items():
            for x, y in valor.items():
                for valorCaracter in character:
                    if(x == valorCaracter.replace(".", "") and llave == "CHARACTERS"):
                        arrayLocal.append(valorCaracter)

        return arrayLocal

    def readDocument(self):
        """
        Lee el documento de entrada linea por linea y va guardandolo en un diccionario, esa será la estructura.
        Luego, verifica en toda las lineas cual es la linea donde estan los tokens que nos interesan.
        """
        with open(self.rutaFile, "r", encoding='utf-8') as f:
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
            elif(line == "PRODUCTIONS" or line == "PRAGMAS"):
                self.isChar = False
                self.isKeyword = False
                self.isToken = False

            #!----------------------------------------- CHARACTERES SECTIONS---------------------------------------------------
            if((self.isChar == True) and (self.isKeyword == False) and (self.isToken == False)):
                # hacemos split con el '=', esto es un ARRAY
                charSplit = line.split("=")
                if(type(charSplit) != None and len(charSplit) > 1 and charSplit[0] != "CHARACTERS"):
                    localDictChar = {}
                    charName = str(charSplit[0].replace(" ", ""))
                    charValue = charSplit[1]
                    # removemos el punto del character
                    if(charValue[len(charValue)-1] == "."):
                        charValue = charValue[0:len(charValue)-1]
                    # extramos los valores unicos la
                    localEvaluador = Conversion()
                    arrayCharValue = localEvaluador.infixToPostfix(
                        charValue)  # convertimos a posftix
                    arrayCharValue = arrayCharValue.split(' ')
                    # verificamos si existe más de un valor por sustituir
                    arrayCharacters = self.checkIfMoreCharExist(arrayCharValue)
                    for x in arrayCharacters:
                        x = x.replace('.', '')
                        # esta función retorna el valor del char a sustiuir y su contenido
                        charExists, array = self.checkIfCharExists(x)
                        if(charExists and len(x) > 0 and len(array) > 0):  # si existe
                            array = array.replace('.', '')
                            charValue = charValue.replace(
                                x, array)  # reemplazamos el valor
                            # actualizamos el diccionario
                            localDictChar[charName] = charValue
                            self.jsonFinal["CHARACTERS"].update(localDictChar)

                    # verificamos si hay un símbolo de operar
                    if('+' in charValue or '-' in charValue):
                        localEvaluador2 = Conversion()
                        charValue2 = charValue.replace(
                            '.', "")  # reemplazamos los puntos
                        postfixCharValue = localEvaluador2.infixToPostfix(
                            charValue2)  # hacemos la expresion postfix
                        # hacemos split
                        postfixCharValue = postfixCharValue.split(' ')
                        # operamos el postfix, para que nos lo retorne bien
                        operatedCharValue = localEvaluador2.operatePostFix(
                            postfixCharValue)
                        # si resulta que no es operable no actualizamos
                        if(operatedCharValue != "NO_OPERABLE"):
                            operatedCharValue = operatedCharValue.replace(
                                '"', '')  # reemplazamos los '"' con vacíos
                            charValue = operatedCharValue  # igaualamos
                            charValue = '"'+charValue+'"'  # agregamos
                            # print(charValue)
                            # actualizamos diccionarios
                            localDictChar[charName] = charValue
                            self.jsonFinal["CHARACTERS"].update(localDictChar)

                    localDictChar[charName] = charValue
                    self.jsonFinal["CHARACTERS"].update(localDictChar)
        #!----------------------------------------- FINALIZA CHARACTERES SECTIONS---------------------------------------------------
        # ? -----------------------------------------KEYWORDS SECTION ----------------------------------------------------------------
            # leemos las keywords
            elif((self.isChar == False) and (self.isKeyword == True) and (self.isToken == False)):
                # hacemos split con el '=', esto es un ARRAY
                keywordSplit = line.split("=")
                if(type(keywordSplit) != None and len(keywordSplit) > 1 and keywordSplit[0] != "KEYWORDS"):
                    localDictKeyWord = {}
                    keyName = str(keywordSplit[0].replace(" ", ""))
                    keyValue = keywordSplit[1]
                    # removemos el punto del character
                    if(keyValue[len(keyValue)-1] == "."):
                        keyValue = keyValue[0:len(keyValue)-1]
                    localDictKeyWord[keyName] = keyValue
                    self.jsonFinal["KEYWORDS"].update(localDictKeyWord)

        # ? -----------------------------------------FINALIZA KEYWORDS SECTION ----------------------------------------------------------------
        # ? -----------------------------------------TOKENS SECTION ----------------------------------------------------------------
            # leemos las tokens
            elif((self.isChar == False) and (self.isKeyword == False) and (self.isToken == True)):
                # hacemos split con el '=', esto es un ARRAY
                tokenSplit = line.split("=")
                if(type(tokenSplit) != None and len(tokenSplit) > 1 and tokenSplit[0] != "TOKENS"):
                    localTokenDict = {}
                    tokenName = str(tokenSplit[0].replace(" ", ""))
                    tokenValue = tokenSplit[1]
                    # removemos el punto del character
                    if(tokenValue[len(tokenValue)-1] == "."):
                        tokenValue = tokenValue[0:len(tokenValue)-1]
                    localTokenDict[tokenName] = tokenValue
                    self.jsonFinal["TOKENS"].update(localTokenDict)

        # ? -----------------------------------------FINALIZA TOKENS SECTION ----------------------------------------------------------------

        pp(self.jsonFinal)
        # print("Nombre compilador: "+self.nombreCompilador)
        # pp(self.lineasPalabras)


reader = Reader()
