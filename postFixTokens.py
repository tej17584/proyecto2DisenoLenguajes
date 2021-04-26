"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: posftixTokens.py
Propósito: ESte programa toma el listado de tokens y lo convierte en posftix
V 1.0
"""

#! Zona de imports
from collections import OrderedDict
from funciones import *


class Conversion:
    # Constructor de las variables
    def __init__(self):
        self.top = -1  # ! límite
        # self.capacity = capacity  # capacidad o longitud de la cadena
        # El array se usa como un stack
        self.arrayOperandos = []
        # seteamos la precedencia. La suma y resta es 1, la multiplicacion y division son 2 y la exponenciacion es 3, siguiendo reglas de la aritmética
        self.outputPostfix = []
        self.precedence = {'+': 1, '-': 1}  # diccionario de precedencia
        self.concatenado = ''
        self.funciones = funciones()

    # método para ver si el stack esta vacío

    def isEmpty(self):
        return True if self.top == -1 else False

    # Retorna el valor de la cima del stack
    def peekTopOfStack(self):
        return self.arrayOperandos[-1]

    # hace pop de un elemento del stack
    def pop(self):
        if not self.isEmpty():  # si no esta vacío
            self.top -= 1  # el top es -1 para indicar que es vacío
            return self.arrayOperandos.pop()  # entonces jalamos
        else:
            return "$"  # de lo contrario un valor espaecial

    # hace push de un elemento
    def push(self, op):
        self.top += 1  # sumamos al top, en este caso, si es el primer elemento o unico, será 0 porque contiene un -1 por defecto
        self.arrayOperandos.append(op)  # se hace pop

    # Se verifica si la precedencia de un operandor es estrictamente menor que la del primer elemento del stack
    def mayorPrecedencia(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.peekTopOfStack()]
            return True if a <= b else False
        except KeyError:
            return False

    # Main, convierte infix a postfix
    def infixToPostfix(self, exp):
        # Iteramos sobre la exppresión
        for i in exp:
            # Si el caracter es un operando se añade al print final
            if self.funciones.isOperand(i):
                # self.outputPostfix.append(i)
                self.concatenado = self.concatenado+i
            elif self.funciones.is_op(i):
                if(self.concatenado != ''):
                    self.outputPostfix.append(self.concatenado)
                    self.concatenado = ''
                    # print(f'El valor múltiple era: {self.outputPostfix}')
                while len(self.arrayOperandos) > 0 and self.arrayOperandos[-1] != '(' and self.mayorPrecedencia(i):
                    top = self.pop()
                    self.outputPostfix.append(top)
                self.push(i)
            elif i == '(':  # Si tenemos un paréntesis abierto, se agrega al STACK
                self.push(i)
            # Si el caracter entrante es el cierre de paréntesis, hacemos pop y lo mandamos a outputPostfix hasta que encontremos otra abertura de paréntesis
            elif i == ')':
                if(self.concatenado != ''):
                    self.outputPostfix.append(self.concatenado)
                    self.concatenado = ''
                # mientras no sea vacío y sea distinto a "("
                while((not self.isEmpty()) and self.peekTopOfStack() != '('):
                    a = self.pop()  # hacemos pop
                    self.outputPostfix.append(a)  # agregamos al outputPostfix
                    if len(a) == 0:
                        print("No hay signo de cerrado de paréntesis")
                        return -1
                # si llegamos a la condicion del while, entonces retornamos -1 para salir
                if (not self.isEmpty() and self.peekTopOfStack() != '('):
                    return -1
                else:
                    self.pop()  # de lo contrario, hacemos pop de valores
            # Si encontramos un operador
            else:
                # mientras no sea vacío Y su precedencia sea menor a la del primer valor del stack
                while(not self.isEmpty() and self.mayorPrecedencia(i)):
                    # entonces agregamos a la salida el valor del stack
                    self.outputPostfix.append(self.pop())
                self.push(i)  # hacemos push del operando  al stack

        if(self.concatenado != ''):
            self.outputPostfix.append(self.concatenado)

        # HAcemos POP de TODOS los operadores en el stack
        # while not self.isEmpty():
            # self.outputPostfix.append(self.pop())

         # verificamos si existe un paréntesis abierto de más
        while len(self.arrayOperandos):
            caracter = self.pop()
            if caracter == "(":
                print("Hay un signo de paréntesis abierto de más")
                exit(-1)
            self.outputPostfix.append(caracter)

        # Imprimimos
        # print(" ".join(self.outputPostfix))
        return " ".join(self.outputPostfix)


expresion = input('Ingresa una expresión:  ')
expresion = expresion.replace(' ', '')
obj = Conversion()
postFixValue = obj.infixToPostfix(expresion)
print(f'El resultado es: {postFixValue}')
#strconv = postFixValue.split(' ')
#resultado = obj.operatePostFix(strconv)
#print("tipo de resultado ", type(resultado))
#print(f'El resultado de la operacion es es: {resultado}')
# This code is contributed by Nikhil Kumar Singh(nickzuck_007)
# # This code is contributed by Amarnath Reddy
# https://www.geeksforgeeks.org/stack-set-4-evaluation-postfix-expression/
