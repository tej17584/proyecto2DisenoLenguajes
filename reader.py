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


class Reader:
    """
    La clase Reader lee el file y lo guarda en una estructura de datos adecuada
    """

    def __init__(self) -> None:
        self.streamCompleto = ""
        self.dictArchivoEntrada
        self.readDocumentAndPoblateStream()

    def readDocumentAndPoblateStream(self):
        """
        Lee el documento ENTERO y lo guarda en una variable, es un stream continuo
        """
        with open('ATGFilesExamples/ADACS.atg', 'r') as f:
            self.streamCompleto = f.read().replace('\n', '')
        f.close()

    def readDocument(self):
        """
        Lee el documento de entrada linea por linea y va guardandolo en un diccionario, esa será la estructura.
        Luego, hace dump con JSON para guardarlo de OTRA manera
        """
        lines = []
        with open('ATGFilesExamples/ADACS.atg', "r") as f:
            lines = f.readlines()
        f.close()

        for line in lines:
            if line == 'TOKENS\n':
                print("SOY UN TOKEEEEEEEEEEEEEEEEEE")


dictionary_nested = {"datacamp": {"Deep Learning": "Python",
                                  "Machine Learning": "Pandas"}, "linkedin": "jobs", "nvidia": "hardware"}


lasFunciones = funciones()

dumpedDictionary = lasFunciones.getDumpJson(dictionary_nested)
print(dumpedDictionary)
