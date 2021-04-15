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

    def getDumpJson(self, dictionary):
        """
        REtorna el dump de un diccionario para ser impreso en formato JSON
        dictionary: el diccionario para ser droppeado
        """
        return json.dumps(dictionary, indent=2, default=str)

    def removerPalabraSingle(self, string, palabra):
        """
        Remueve la palabra del string y los espacios extra que contenga el string. 
        Útil si la linea solamente tiene dos valores. Como:
        COMPILER AdaCS
        Nos retorna: AdaCS
        """
        string = string.replace(str(palabra), "")
        newString = string.replace(" ", "")
        return newString

    def isOperand(self, ch):
        """
        REtorna TRUE si el caracter ingresado es un alfanumerico, FALSE de lo contrario
        *@param ch: el caracter a ser probado
        """
        if ch != "+" and ch != "-":
            return True
        return False

    def is_op(self, a):
        """
        Testeamos si el caracter de entrada es un operando
        *@param a: caracter a ser probado
        """
        if a == '+' or a == '-':
            return True
        return False

    def sortString(self, str):
        """
        Hace sort de un string
        extraido de: https://www.geeksforgeeks.org/sort-string-characters/
        *@param: str: el string hacer sort
        """
        str = ''.join(sorted(str))
        return str

    def unionTwoStrings(self, string1, string2):
        """
        Une dos strings. Elimina duplicados.
        *@param: string1: el string a unir
        *@param: string2: el string a sumarle
        """
        res = ""
        temp = string1
        for i in string2:
            if i not in temp:
                string1 += i

        return string1

    def differenceTwoStrings(self, string1, string2):
        """
        Une dos strings. Elimina duplicados.
        *@param: string1: el string a unir
        *@param: string2: el string a sumarle
        """
        res = ""
        temp = string1
        for i in string2:
            if i in temp:
                string1 = string1.replace(i, '')

        return string1
