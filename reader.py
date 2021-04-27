"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: reader.py
Propósito: Este programa tiene como propósito leer el archivo con extension .ATG
V 1.0
"""

# ! Zona de imports
from os import remove
from funciones import funciones
from pprint import pprint as pp
from posftixEvaluador import *
from tipoVar import *
import re


class Reader:
    """
    La clase Reader lee el file y lo guarda en una estructura de datos adecuada
    """

    def __init__(self) -> None:
        self.rutaFile = "ATGFilesExamples\HexNumberP.ATG"
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
        self.isEXCET = False
        self.acumuladorExcept = ""  # el acumulador para saber que hay que exceptuar
        self.boolComillasPunto = False
        self.bannedPositionsString = []  # estas son las posiciones banneadas de stirngs
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

    def getTokensFinales(self):
        """
        REtorna los tokens
        """
        return self.jsonFinal["TOKENS"]

    def getCharactersFinales(self):
        """
        REtorna los characters
        """
        return self.jsonFinal["CHARACTERS"]

    def getKeywordsFinales(self):
        """
        REtorna los KEYWORDS
        """
        return self.jsonFinal["KEYWORDS"]

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
        # line = line.replace(" ", "")  # quitamos el espacio en blanco
        lineaArray = line.split("=")
        newTokenValue = newTokenValue+lineaArray[1]
        varExit = True
        contadorInterno = lineadelToken+1
        while varExit:
            line = self.lineasArchivoWithNumber[contadorInterno]
            line = line.rstrip("\n")  # eliminamos la linea
            # line = line.replace(" ", "")  # quitamos el espacio en blanco
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
                    if(valorChar == '"'):
                        charValue = charValue.replace(
                            stringReplace, valorChar)
                    else:
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
                            if(isinstance(array, str)):
                                array = array.replace('.', '')
                                charValue1 = charValue1.replace(
                                    x, array)  # reemplazamos el valor
                            elif(isinstance(array, set)):
                                setString = self.funciones.fromSetToSTring(
                                    array)
                                setString = setString.replace('.', '')
                                charValue1 = charValue1.replace(
                                    x, setString)  # reemplazamos el valor
                    for x in arrayCharacters:
                        x = x.replace('.', '')
                        # esta función retorna el valor del char a sustiuir y su contenido
                        charExists, array = self.checkIfCharExists(x)
                        if(charExists and len(x) > 0 and len(array) > 0):  # si existe
                            if(isinstance(array, str)):
                                array = array.replace('.', '')
                                charValue = charValue.replace(
                                    x, array)  # reemplazamos el valor
                            elif(isinstance(array, set)):
                                setString = self.funciones.fromSetToSTring(
                                    array)
                                setString = setString.replace('.', '')
                                charValue = charValue.replace(
                                    x, setString)  # reemplazamos el valor
                    #! verificamos si hay un .. en el character
                    if('..' in charValue1 and ('CHR(' not in charValue1)):
                        charValue1Modificado = self.funciones.getRangeFromLetters(
                            charValue1)
                        charValue1 = charValue1Modificado
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
                                    # este char es el que SUMA
                                    charASumador.append(y.replace(" ", ""))
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
                                    postfixCharValue[contador] = self.funciones.getBetweenComillaSandComillaDoble(
                                        sustitucionTokens.replace(" ", ""))
                                elif(w in charASumador):
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
                        if("'+'" in charValue1 or "'-'" in charValue1):
                            arrayPartido = charValue.split(' ')
                            postfixCharValue = localEvaluador2.infixToPostfix(
                                arrayPartido)  # hacemos la expresion postfix
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
                        else:
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
                newValor = self.funciones.fromSetToOrd(valor)
                self.jsonFinal["CHARACTERS"][llave] = set(newValor)
            elif(isinstance(valor, set)):
                newValor = self.funciones.fromSetToOrd(valor)
                self.jsonFinal["CHARACTERS"][llave] = newValor
        # print(self.jsonFinal["CHARACTERS"])

        # ahora valuamos Susituimos el valor de los tokens por otros mas conocidos
        for llaveToken, valorToken in self.jsonFinal["TOKENS"].items():
            newValorToken = self.funciones.substituLlavesCorchetes(valorToken)
            newValorTokenAskVerification = self.funciones.alterateAskChain(
                newValorToken)
            newValorToken = self.funciones.substituLlavesCorchetesV2(
                newValorTokenAskVerification)
            newValorToken = newValorToken.replace(" ", "")
            # acá empieza la logica de sustiticion
            # print("VAlor por el token ", newValorToken)
            localDict = {}
            contadorDictTokens = 0
            acumuladorStrings = ""
            acumuladorExcept = ""

            for x in newValorToken:
                if(x == '(' and (contadorDictTokens not in self.bannedPositionsString)):
                    newTipoVar = variableER_Enum(tipoVar.LPARENTESIS, ord(x))
                    localDict[contadorDictTokens] = newTipoVar
                elif(x == ')' and (contadorDictTokens not in self.bannedPositionsString)):
                    newTipoVar = variableER_Enum(tipoVar.RPARENTESIS, ord(x))
                    localDict[contadorDictTokens] = newTipoVar
                elif(x == '*' and (contadorDictTokens not in self.bannedPositionsString)):
                    newTipoVar = variableER_Enum(tipoVar.KLEENE, ord(x))
                    localDict[contadorDictTokens] = newTipoVar
                elif(x == 'ε' and (contadorDictTokens not in self.bannedPositionsString)):
                    newTipoVar = variableER_Enum(tipoVar.EPSILON, ord(x))
                    localDict[contadorDictTokens] = newTipoVar
                elif(x == '|' and (contadorDictTokens not in self.bannedPositionsString)):
                    newTipoVar = variableER_Enum(tipoVar.OR, ord(x))
                    localDict[contadorDictTokens] = newTipoVar
                elif(x == '"' and (contadorDictTokens not in self.bannedPositionsString)):
                    contadorComillas = 0
                    for y in newValorToken:
                        if(y == '"'):
                            contadorComillas += 1
                    if(contadorComillas >= 2):
                        start = newValorToken.find('"')
                        if(start+1 not in self.bannedPositionsString):
                            contador = start+1
                            # agregamos esta posicion como ya no usable
                            posicionInicialString = contador
                            # print("Contador al inicio", posicionInicialString)
                            variableWhile = True
                            while variableWhile:
                                if(newValorToken[contador] == '"'):
                                    variableWhile = False
                                else:
                                    contador = contador+1
                            # agregamos esta posicion como ya no usable
                            posicionFinalString = contador
                            # print("contador al final", posicionFinalString)
                            # agregamos TODAS las posiciones banneadas
                            for x in range(posicionInicialString, posicionFinalString+1):
                                self.bannedPositionsString.append(x)
                            """ valorEntrecomillas = re.findall(
                                r'"(.*?)"', newValorToken[posicionInicialString-1:posicionFinalString]) """
                            valorEntrecomillasInicial = newValorToken[posicionInicialString: posicionFinalString]
                            if('.' in valorEntrecomillasInicial):
                                self.boolComillasPunto = True
                            # le agregamos los puntos
                            valorEntrecomillasFinal = self.funciones.alterateRE(
                                valorEntrecomillasInicial)
                            indexdePalabra = newValorToken.find(
                                valorEntrecomillasInicial)
                            if(indexdePalabra != 1):
                                # agregamos un append para mantener la unidad
                                newTipoVar = variableER_Enum(
                                    tipoVar.APPEND, ord("."))
                                localDict[contadorDictTokens] = newTipoVar
                                # self.bannedPositionsString.append(
                                # contadorDictTokens)
                                contadorDictTokens += 1
                            contadorInter = contadorDictTokens
                            if(self.boolComillasPunto):
                                for w in valorEntrecomillasFinal:
                                    if(w == '_'):
                                        varNuevaAppend = ""
                                        varNuevaAppend = variableER_Enum(
                                            tipoVar.APPEND, ord("."))
                                        localDict[contadorInter] = varNuevaAppend
                                        self.boolComillasPunto = False
                                    else:
                                        variableNueva = ""
                                        variableNueva = variableER_Enum(
                                            tipoVar.STRING, ord(w))
                                        localDict[contadorInter] = variableNueva
                                    """ self.bannedPositionsString.append(
                                        contadorInter) """
                                    contadorInter = contadorInter+1
                            else:
                                for w in valorEntrecomillasFinal:
                                    if(w == '.'):
                                        varNuevaAppend = ""
                                        varNuevaAppend = variableER_Enum(
                                            tipoVar.APPEND, ord("."))
                                        localDict[contadorInter] = varNuevaAppend
                                        self.boolComillasPunto = False
                                    else:
                                        variableNueva = ""
                                        variableNueva = variableER_Enum(
                                            tipoVar.STRING, ord(w))
                                        localDict[contadorInter] = variableNueva
                                    """ self.bannedPositionsString.append(
                                        contadorInter) """
                                    contadorInter = contadorInter+1
                            # print("el valor es :", valorEntrecomillasFinal)
                            """ if(newValorToken[contadorDictTokens+1] != '' or newValorToken[contadorDictTokens+1] != ' ' and self.boolComillasPunto):
                                print("el valor es :", valorEntrecomillasFinal)
                                contadorDictTokens = start
                            else:
                                print("el valor es :", valorEntrecomillasFinal)
                                contadorDictTokens = start """
                        contadorDictTokens = start
                else:  # de lo contrario acumulamos
                    if(contadorDictTokens not in self.bannedPositionsString):
                        acumuladorStrings += x
                        wordExists, value = self.checkIfCharExists(
                            acumuladorStrings)
                        if(wordExists and len(value) > 0):  # si existe el char
                            # convertimos los strings a ints
                            # funcioncitas.fromSetToOrd(value)
                            newValueSet = value
                            newTipoVarEntero = variableER_Enum(
                                tipoVar.IDENT, newValueSet)
                            newTipoVarEntero.setNombreIdentificador(
                                acumuladorStrings)
                            start = newValorToken.find(acumuladorStrings)
                            localDict[contadorDictTokens] = newTipoVarEntero
                            longitud = len(newValorToken)
                            if((contadorDictTokens+1) < longitud):
                                if(newValorToken[contadorDictTokens-len(acumuladorStrings)] == ')' or
                                   newValorToken[contadorDictTokens-len(acumuladorStrings)] == ']' or
                                   newValorToken[contadorDictTokens-len(acumuladorStrings)] == '}') and (newValorToken[contadorDictTokens+1] == '(' or
                                                                                                         newValorToken[contadorDictTokens+1] == '[' or
                                                                                                         newValorToken[contadorDictTokens+1] == '{'):

                                    appendAnterior = variableER_Enum(
                                        tipoVar.APPEND, ord('.'))
                                    appendSiguiente = variableER_Enum(
                                        tipoVar.APPEND, ord('.'))
                                    resta = contadorDictTokens - \
                                        len(acumuladorStrings)+1
                                    localDict[contadorDictTokens] = appendAnterior
                                    localDict[resta] = newTipoVarEntero
                                    localDict[resta+1] = appendSiguiente
                                    contadorDictTokens += 1

                                else:
                                    if((newValorToken[contadorDictTokens+1] == '(' or
                                        newValorToken[contadorDictTokens+1] == '[' or
                                            newValorToken[contadorDictTokens+1] == '{')):
                                        newTipoVar = variableER_Enum(
                                            tipoVar.APPEND, ord('.'))
                                        localDict[contadorDictTokens +
                                                  1] = newTipoVar
                                        contadorDictTokens += 1
                                    elif(newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == '*' or
                                            newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == ')' or
                                            newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == ']' or
                                            newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == '}'):
                                        indexdePalabra = newValorToken.find(
                                            acumuladorStrings)
                                        newTipoVar = variableER_Enum(
                                            tipoVar.APPEND, ord('.'))
                                        resta = contadorDictTokens - \
                                            len(acumuladorStrings)+1
                                        localDict[contadorDictTokens] = newTipoVar
                                        localDict[resta] = newTipoVarEntero
                                        contadorDictTokens += 1

                            elif(newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == '*' or newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == ')' or newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == ']' or newValorToken[contadorDictTokens-len(acumuladorStrings)-1] == '}'):
                                newTipoVar = variableER_Enum(
                                    tipoVar.APPEND, ord('.'))
                                resta = contadorDictTokens - \
                                    len(acumuladorStrings)+1
                                localDict[contadorDictTokens] = newTipoVar
                                localDict[resta] = newTipoVarEntero
                                contadorDictTokens += 1

                            # agregamos TODAS las posiciones banneadas
                            acumuladorStrings = ""
                        """ elif(acumuladorStrings == "EXCEPT"):
                            # colocamos la variable global en true
                            self.isEXCET = True
                            acumuladorStrings = ""
                        elif(self.isEXCET):
                            self.acumuladorExcept += x
                            if(self.acumuladorExcept == "KEYWORDS"):
                                self.acumuladorExcept = ""
                                self.isEXCET = False
                                newTipoVar = variableER_Enum(
                                    tipoVar.EXCEPT, self.jsonFinal["KEYWORDS"])
                                newTipoVar.setNombreIdentificador("KEYWORDS")
                                localDict[contadorDictTokens] = newTipoVar """

                contadorDictTokens += 1

            contadorDictTokens += 1
            newTipoVar = variableER_Enum(
                tipoVar.APPEND, ord("."))
            localDict[contadorDictTokens] = newTipoVar
            contadorDictTokens += 1
            newTipoVar = variableER_Enum(
                tipoVar.ACEPTACION, ('#-'+llaveToken))
            newTipoVar.setNombreIdentificador(llaveToken)
            localDict[contadorDictTokens] = newTipoVar
            contadorDictTokens += 1
            # ahora cerramos el parentesis
            newTipoVar = variableER_Enum(
                tipoVar.RPARENTESIS, ord(")"))
            localDict[contadorDictTokens] = newTipoVar
            contadorDictTokens += 1
            # creamos un nuevo diccionario
            localDictEncerrado = {}
            contadorEncerrado = contadorDictTokens
            newTipoVar = variableER_Enum(
                tipoVar.LPARENTESIS, ord("("))
            localDictEncerrado[contadorEncerrado] = newTipoVar
            contadorEncerrado += 1
            for llave, valor in localDict.items():
                localDictEncerrado[contadorEncerrado] = valor
                contadorEncerrado += 1

            self.jsonFinal["TOKENS"][llaveToken] = localDictEncerrado
            contadorDictTokens = 0
            self.bannedPositionsString = []

        """  print(self.jsonFinal["KEYWORDS"])
        for llave, valor in self.jsonFinal["TOKENS"].items():
            print("LLAVE: ", llave)
            print(self.jsonFinal["TOKENS"][llave])
            # for numeroItem, valorItem in valor.items():
                # print(
                # f'Identificador: {valorItem.getIdenficador()} value: {valorItem.getValueIdentificador()}')
                # print(valorItem) """

        """ for x, y in self.jsonFinal.items():
            for valor, pedazito in y.items():
                print(valor)
                print(f'Tipo de la llave {type(valor)}')
                print(pedazito)
                print(f'Tipo del valor {type(pedazito)}') """
        # print("Nombre compilador: "+self.nombreCompilador)
        # pp(self.lineasPalabras)


reader = Reader()
