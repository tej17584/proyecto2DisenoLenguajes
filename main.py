"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: main.py
Propósito: Este programa es el que lee los archivos
V 1.0
"""
# zona de import de librerías
from os import remove
from funciones import *
from pprint import pprint as pp
from posftixEvaluador import *
from tipoVar import *
from postFixTokens import *
from reader import *
import re
import os


# creamos las instancias de clases
instancia_reader = Reader()
instancia_funciones = funciones()


def menu():

    os.system('cls')  # NOTA para windows tienes que cambiar clear por cls
    print("Selecciona una opción")
    print("\t1 - Iniciar lectura y creacion de scanner")
    print("\t9 - salir")


while True:
    # Mostramos el menu
    menu()

    # solicituamos una opción al usuario
    opcionMenu = input("Ingresa un valor... ")
    expresion = ""
    palabra = ""
    if opcionMenu == "1":

        expresion = ""
        palabra = ""
        # primero obtenemos los tokens finales
        tokensFinales = instancia_reader.getTokensFinales()
        for llave, valueforPostfix in tokensFinales.items():
            instancia_posftixTokens = ConversionPostfixTokens()
            posftix = instancia_posftixTokens.infixToPostfix(valueforPostfix)
            pp(f'El postix de {llave} es')
            for x in posftix:
                pp(f' {x.getIdenficador()}  {x.getNombreIdentificador()}')

        input("Presiona ENTER para regresar al menú")
        """  # Probamos la funcionalidad
        expresion = input('Ingresa una expresión regular:  ')
        expresion = expresion.replace(' ', '')
        palabra = input('Ingresa una cadena para probar en los AFN:  ')
        palabra = palabra.replace(' ', '')
        obj = ConversionPostfixTokens()
        conversion = funciones()
        expresionAlterada1 = conversion.alterateAskChain(expresion)
        expresionAlterada2 = conversion.alteratePlusChain(expresionAlterada1)
        expresionAlteradaFinal = conversion.alterateRE(expresionAlterada2)
        lenguaje = conversion.getLanguage(expresionAlterada2)
        # print("El lenguaje es ", lenguaje)
        obj2 = AFNV(lenguaje, palabra)

        print("Expresion alterada", expresionAlteradaFinal)
        postFixValue = obj.infixToPostfix(expresionAlteradaFinal)
        if(postFixValue == "ERRORPOSTFIX"):
            input("Ha habido un error. Tu cadena le falta un ) paréntensis cerradura. \npulsa una tecla para continuar y volver a meter la cadena.")
        else:
            print("La postfija es ", postFixValue)
            strconv = postFixValue.split(' ')
            # print(strconv)
            AFNFinal = obj2.operatePostFix(strconv)
            obj3 = AFDV(lenguaje, AFNFinal, palabra)
            # print(AFNFinal, "\n")
            AFDFinal = obj3.getAFDFromAFN()
            # print(f'El resultado es: {resultado}')
            input("Presiona ENTER para volver a empezar") """

    elif opcionMenu == "9":
        break
    else:
        print("")
        input("No has pulsado ninguna opción correcta...\npulsa ENTER para continuar")
