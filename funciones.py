"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: functions.py
Propósito: ESte programa tiene funciones útiles
V 1.0
"""
import json


class funciones():
    def __init__(self) -> None:
        self.arrayOperandos = []
        self.precedenceV2 = {'|': 1, '.': 2,
                             '*': 3, '?': 3, "+": 3}  # diccionario de precedencia version 2
        self.dictionaryNTL = {"0": "A", "1": "B", "2": "C",
                              "3": "D", "4": "E", "5": "F",
                              "6": "G", "7": "H",
                              "8": "I", "9": "J"}

    def printPrettyDictionary(self, d, indent=0):
        """
        this function prints pretty the dictionary,
        extracted from: https://stackoverflow.com/questions/3229419/how-to-pretty-print-nested-dictionaries
        """
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.printPrettyDictionary(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))

    def isOperand(self, ch):
        """
        REtorna TRUE si el caracter ingresado es un alfanumerico, FALSE de lo contrario
        *@param ch: el caracter a ser probado
        """
        if ch.isalnum() or ch == "ε" or ch == "#":
            return True
        return False

    def getDumpJson(self, dictionary):
        return json.dumps(dictionary, indent=2, default=str)
