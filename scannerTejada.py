

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
        # abrimos todos los files
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


objeSCanner = Scanner()
