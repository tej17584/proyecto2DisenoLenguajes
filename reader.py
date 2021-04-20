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
from posftixEvaluador import *


class Reader:
    """
    La clase Reader lee el file y lo guarda en una estructura de datos adecuada
    """

    def __init__(self) -> None:
        self.rutaFile = "ATGFilesExamples\C.atg"
        self.streamCompleto = ""
        self.dictArchivoEntrada = ""
        self.lineasArchivo = []
        self.lineasArchivoWithNumber = {}
        self.lineasPalabras = {}
        self.jsonFinal = {}  # diccionario final
        self.nombreCompilador = ""
        self.funciones = funciones()
        self.posftixEvaluador = Conversion()
        self.isChar = False
        self.isToken = False
        self.isKeyword = False
        self.readDocumentAndPoblateStream()
        self.readDocument()

    def readDocumentAndPoblateStream(self):
        """
        Lee el documento ENTERO y lo guarda en una variable,
        es un stream continuo y contiene como llave la linea
        """
        with open(self.rutaFile, "r", encoding='utf-8') as f:
            self.lineasArchivo = f.readlines()
        f.close()

        contador = 0
        for x in self.lineasArchivo:
            self.lineasArchivoWithNumber[(contador)] = x
            contador = contador+1
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

    def TokenMultiLinea(self, tokenEnorme, lineadelToken):
        newTokenValue = ""
        # obtenemos la linea del token general
        lineaTokenHeader = self.lineasPalabras["TOKENS"]
        line = self.lineasArchivoWithNumber[lineadelToken]
        line = line.rstrip("\n")  # eliminamos la linea
        line = line.replace(" ", "")  # quitamos el espacio en blanco
        lineaArray = line.split("=")
        newTokenValue = newTokenValue+lineaArray[1]
        varExit = True
        contadorInterno = lineadelToken+1
        while varExit:
            line = self.lineasArchivoWithNumber[contadorInterno]
            line = line.rstrip("\n")  # eliminamos la linea
            line = line.replace(" ", "")  # quitamos el espacio en blanco
            if(line[len(line)-1] == "."):
                newTokenValue = newTokenValue+line.replace(".", "")
                varExit = False
            else:
                newTokenValue = newTokenValue+line

            contadorInterno += 1
        return newTokenValue

    def replaceCharValues(self, charValue):
        acumulable = ""
        arrayNumeros = []
        if('..' in charValue):
            arrayCharsRango = charValue.split(' ')
            # encontramos los rangos
            for x in arrayCharsRango:
                if('CHR(' in x):
                    posicionInicialCHR = x.index('(')
                    posicionFInalCHR = x.index(')')
                    numeroChar = int(
                        x[int(posicionInicialCHR+1): int(posicionFInalCHR)])
                    arrayNumeros.append(numeroChar)
                    # reemplazamos los CHR de una vez
                    valorChar = chr(
                        int(x[int(posicionInicialCHR+1): int(posicionFInalCHR)]))
                    stringReplace = 'CHR(' +\
                        x[int(posicionInicialCHR+1):int(posicionFInalCHR)] +\
                        ')'
                    # print("")
                    charValue = charValue.replace(
                        stringReplace,  valorChar)

            for x in arrayCharsRango:
                if(x == ".."):
                    maximoValor = max(arrayNumeros)
                    minimoValor = min(arrayNumeros)
                    acumulador = ""
                    # Ya teniendo los rangos, iteramos
                    for valor in range(minimoValor+1, maximoValor):
                        acumulador += (chr(valor))
                    stringReplace = '..'
                    # print("")
                    charValue = charValue.replace(
                        stringReplace, acumulador)
        else:
            arrayChars = charValue.split(' ')
            for x in arrayChars:
                if('CHR(' in x):
                    posicionInicialCHR = x.index('(')
                    posicionFInalCHR = x.index(')')
                    valorChar = chr(
                        int(x[int(posicionInicialCHR+1): int(posicionFInalCHR)]))
                    stringReplace = 'CHR(' +\
                        x[int(posicionInicialCHR+1):int(posicionFInalCHR)] +\
                        ')'
                    # print("")
                    charValue = charValue.replace(
                        stringReplace, '"' + valorChar + '"')

        return charValue

    def readDocument(self):
        """
        Lee el documento de entrada linea por linea y va guardandolo en un diccionario, esa será la estructura.
        Luego, verifica en toda las lineas cual es la linea donde estan los tokens que nos interesan.
        """
        # Leemos las lineas donde estan las palabras especiales y guardamos el número  de linea.
        # Esto nos puede servir luego.
        count = 0
        for line in self.lineasArchivo:
            line = line.rstrip("\n")  # eliminamos la linea
            line = line.replace(" ", "")  # quitamos el espacio en blanco
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

        count2 = 0
        for line in self.lineasArchivo:
            line = line.rstrip("\n")  # eliminamos la linea
            line2 = line.replace(" ", "")  # quitamos el espacio en blanco
            # Dependiendo del tipo de valor, seteamos el valor de la booleana,
            # de esa forma iteramos
            if(line2 == "CHARACTERS" or line2 == "CHARACTER"):
                self.isChar = True
                self.isKeyword = False
                self.isToken = False
                # creamos la entrada de valor en el dict final
                self.jsonFinal["CHARACTERS"] = {}
            elif(line2 == "TOKENS" or line2 == "TOKEN"):
                self.isChar = False
                self.isKeyword = False
                self.isToken = True
                # creamos la entrada de valor en el dict final
                self.jsonFinal["TOKENS"] = {}
            elif(line2 == "KEYWORDS" or line2 == "KEYWORD"):
                self.isChar = False
                self.isKeyword = True
                self.isToken = False
                # creamos la entrada de valor en el dict final
                self.jsonFinal["KEYWORDS"] = {}
            elif(line2 == "PRODUCTIONS" or line2 == "PRAGMAS"):
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
                    charValue1 = charValue.replace(" ", "")
                    # removemos el punto del character
                    if(charValue1[len(charValue1)-1] == "."):
                        charValue1 = charValue1[0:len(charValue1)-1]
                    if(charValue[len(charValue)-1] == "."):
                        charValue = charValue[0:len(charValue)-1]
                    # extramos los valores unicos la
                    localEvaluador = Conversion()
                    arrayCharValue = localEvaluador.infixToPostfix(
                        charValue1)  # convertimos a posftix
                    arrayCharValue = arrayCharValue.split(' ')
                    # verificamos si existe más de un valor por sustituir
                    arrayCharacters = self.checkIfMoreCharExist(arrayCharValue)
                    for x in arrayCharacters:
                        x = x.replace('.', '')
                        # esta función retorna el valor del char a sustiuir y su contenido
                        charExists, array = self.checkIfCharExists(x)
                        if(charExists and len(x) > 0 and len(array) > 0):  # si existe
                            array = array.replace('.', '')
                            charValue1 = charValue1.replace(
                                x, array)  # reemplazamos el valor

                    # ? Ahora verificamos si tiene algún CHAR
                    if('CHR(' in charValue):
                        if('-' in charValue or '+' in charValue):
                            signoMas = False
                            signoMenos = False
                            splitporOperando = []
                            charASumador = []
                            if('+' in charValue):
                                signoMas = True
                                signoMenos = False
                            elif('-' in charValue):
                                signoMenos = True
                                signoMas = False
                            if(signoMas == True and signoMenos == False):
                                splitporOperando = charValue.split('+')
                            elif(signoMas == False and signoMenos == True):
                                splitporOperando = charValue.split('-')
                            charAOperar = ""
                            for x in splitporOperando:
                                if('CHR(' in x):
                                    charAOperar = x  # este el que nos interesa sustutuir
                            for y in splitporOperando:
                                if('CHR(' not in y):
                                    charASumador = y  # este char es el que SUMA
                            sustitucionTokens = self.replaceCharValues(
                                charAOperar)
                            localEvaluador2 = Conversion()
                            # reemplzamos valores
                            postfixCharValue = localEvaluador2.infixToPostfix(
                                charValue.replace(" ", ""))  # hacemos la expresion postfix
                            # hacemos split
                            postfixCharValue = postfixCharValue.split(' ')
                            contador = 0
                            for w in postfixCharValue:
                                if(w == charAOperar.replace(" ", "")):
                                    postfixCharValue[contador] = sustitucionTokens
                                elif(w == charASumador.replace(" ", "")):
                                    postfixCharValue[contador] = self.funciones.getBetweenComillaSandComillaDoble(
                                        w)
                                contador += 1
                             # operamos el postfix, para que nos lo retorne bien
                            operatedCharValue = localEvaluador2.operatePostFix(
                                postfixCharValue)
                            # si resulta que no es operable no actualizamos
                            if(operatedCharValue != "NO_OPERABLE"):
                                # operatedCharValue = operatedCharValue.replace(
                                #    '"', '')  # reemplazamos los '"' con vacíos
                                charValue1 = operatedCharValue  # igaualamos
                                charValue1 = charValue1  # agregamos
                        else:
                            sustitucionTokens = self.replaceCharValues(
                                charValue.replace(" ", ""))
                            charValue1 = sustitucionTokens
                        # verificamos si hay un símbolo de operar
                    if('+' in charValue1 or '-' in charValue1):
                        localEvaluador2 = Conversion()
                        charValue1 = charValue1.replace(" ", "")
                        postfixCharValue = localEvaluador2.infixToPostfix(
                            charValue1)  # hacemos la expresion postfix
                        # hacemos split
                        postfixCharValue = postfixCharValue.split(' ')
                        # operamos el postfix, para que nos lo retorne bien
                        operatedCharValue = localEvaluador2.operatePostFix(
                            postfixCharValue)
                        # si resulta que no es operable no actualizamos
                        if(operatedCharValue != "NO_OPERABLE"):
                            # operatedCharValue = operatedCharValue.replace(
                            #    '"', '')  # reemplazamos los '"' con vacíos
                            charValue1 = operatedCharValue  # igaualamos
                            charValue1 = charValue1  # agregamos

                    localDictChar[charName] = charValue1
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
                    # además de remover verificamos que no sea de doble línea
                    if(tokenValue[len(tokenValue)-1] == "."):
                        tokenValue = tokenValue[0:len(tokenValue)-1]
                        localTokenDict[tokenName] = tokenValue
                        self.jsonFinal["TOKENS"].update(localTokenDict)
                    else:  # si por el contrario no termina en punto iteramos
                        tokenValue = self.TokenMultiLinea(tokenValue, count2)
                        localTokenDict[tokenName] = tokenValue
                        self.jsonFinal["TOKENS"].update(localTokenDict)
            count2 += 1

            # ? -----------------------------------------FINALIZA TOKENS SECTION ----------------------------------------------------------------

         # Si incluso luego de todo esto no es aún set lo volvemos set
        for llave, valor in self.jsonFinal["CHARACTERS"].items():
            if(isinstance(valor, str)):
                valor = self.funciones.getBetweenComillaSandComillaDoble(
                    valor)
                self.jsonFinal["CHARACTERS"][llave] = set(valor)
        print(self.jsonFinal)
        """ for x, y in self.jsonFinal.items():
            for valor, pedazito in y.items():
                print(valor)
                print(f'Tipo de la llave {type(valor)}')
                print(pedazito)
                print(f'Tipo del valor {type(pedazito)}') """
        # print("Nombre compilador: "+self.nombreCompilador)
        # pp(self.lineasPalabras)


reader = Reader()
