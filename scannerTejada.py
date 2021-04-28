

# Nombre: Alejandro Tejada
# Curso: Diseño lenguajes de programacion
# Fecha: Abril 2021
#Programa: scannerTejada.py
# Propósito: Este programa tiene como fin leer el file de entrada
# V 1.0

# imports
import pickle


class Scanner():
    def __init__(self) -> None:
        self.diccionarioSiguientePos = {}
        self.AFDConstruidoFinal = []
        self.nodosAceptacion = {}
        self.abrirFiles()

    def abrirFiles(self):
        # abrimos todos los files y asignamos
        infile = open("dicionarioAFDFinal", 'rb')
        self.AFDConstruidoFinal = pickle.load(infile)
        infile.close()
        infile = open("diccionarioSiguientePos", 'rb')
        self.diccionarioSiguientePos = pickle.load(infile)
        infile.close()
        infile = open("diccionarioEstadosAceptacion", 'rb')
        self.nodosAceptacion = pickle.load(infile)
        infile.close()
        print("HOKISIW")

    def mover(self, estado, caracter):
        """
        Esta funcion retorna el siguiente estado
        """
        arrayEvaluar = self.AFDConstruidoFinal
        arrayMover = []
        for estados in estado:
            for x in arrayEvaluar:
                variableIn = (ord(caracter)) in x[2]
                if(variableIn and len(x[3]) > 0 and estados == x[0]):
                    estadoSiguiente = self.getStateNumberForArray(x[3])
                    if(estadoSiguiente not in arrayMover):
                        arrayMover.append(estadoSiguiente)

    def getFinalStateAFN(self):
        arrayValores = []
        estadosFinales = self.getFinalStateNumber()
        for valor in self.AFDConstruidoFinal:
            for x in estadosFinales:
                if(str(x) in valor[1]):
                    arrayValores.append(valor[0])

        arrayValores = list(
            dict.fromkeys(arrayValores))
        return arrayValores

    def getFinalStateAFNV2(self):
        arrayValores = []
        estadosFinales = self.getFinalStateNumber()
        for valor in self.AFDConstruidoFinal:
            for x in estadosFinales:
                if(str(x) in valor[1]):
                    if(valor[1] not in arrayValores):
                        arrayValores.append(valor[1])

        return arrayValores

    def getFinalStateNumber(self):
        array = []
        for numero, valor in self.diccionarioSiguientePos.items():
            if len(valor) == 0:
                array.append(numero)

        return array


objeSCanner = Scanner()
