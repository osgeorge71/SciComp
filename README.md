# SciComp
Homeworks and projects about Scientific Computing course

En este archivo se encuentran las clases de soporte para ejecutar el método de Montecarlo.
El código está escrito en lenguaje Python en su versión 3.
Existe una clase Función que implementa la función a integrar. Para este caso en particular la función de distribución de energía en el decaimiento del neutrón.
Esta función se extrae el libro de Introduction to elementary Particles de Griffiths, en la sección 9.3 página 318.

También está la clase Montecarlo que se encarga de implementar el método con el número de muestras indicado en los argumentos de los métodos.
El método principal se encabeza de la siguiente manera:
def calcIntegral(self,f,x1,x2,nSamples):
donde f es el objeto que encapsula la función a integrar,
x1 y x2 delimitan el intervalo de integración y 
nSamples indica el número de muestras a tomar para realizar el proceso.
