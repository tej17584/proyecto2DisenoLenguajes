"""
Nombre: Alejandro Tejada
Curso: Diseño lenguajes de programacion
Fecha: Abril 2021
Programa: tipoVar.py
Propósito: Este programa tiene TODOS los posibles tipos de variable que pueden ser encontradas. Cada una 
V 1.0
"""
#! zona de imports
from enum import Enum


class tipoVar(int, Enum):
    IDENT = 0
    STRING = 1
    NUMBER = 2
    CHAR = 3
    ANY = 4
    UNION = 5
    DIFFERENCE = 6
    RANGE = 6
    APPEND = 7
    KLEENE = 8
    LPAR = 9
    RPAR = 10
    OR = 11
