#
# TRABAJO PRACTICO DE SEMINARIO
#

# imports
import random
import threading
import time

# Global Variables
ganador = ""
caballos = []
distancias = []

# Thread & Functions

def participar():
    print()
    
def threadingStart():
    for i in range(caballos.len()):
        p = threading.Thread(target=participar)
        p.start()
        
def threadingJoin():
    for i in range(caballos.len()):
        #p.join()
        print()
        
def ganador():
    print(f"El ganador es: {ganador}")

#  null) Task + Pres
print("                                                                                  ")
print("**********************************************************************************")
print("*                 SEMINARIO DE PROGRAMACION - 2023 - TP THREADS                  *")
print("**********************************************************************************")
print("    ALUMNOS:                                                                      ")
print("            • Bardales, Wilfredo                                                  ")
print("            • Martin, Denise                                                      ")
print("            • Paliari, Crolina                                                    ")
print("                                                                                  ")
print("**********************************************************************************")
print("*                                   OBJETIVO                                     *")
print("**********************************************************************************")
print("  Lograr concurrencia de procesos mediante la creacion de threads en python.      ")
print("                                                                                  ")
print("**********************************************************************************")
print("*                                   CONSIGNAS                                    *")
print("**********************************************************************************")
print("                                                                                  ")
print("  CARRERA DE CABALLOS:                                                            ")
print("  1- Definir  10 caballos para correr una carrera, cada caballo es un thread.     ")
print("  2- Definir una distancia de 20.                                                 ")
print("  3- Todos los caballos corren moviendose en saltos 1 a 1, o aleatorios.          ")
print("  4- Sólo un caballo puede ganar, y cuando lo ahce deben frenarse todos los demás.")
print("                                                                                  ")
#  I) Theory
print("                                                                                  ")
print("**********************************************************************************")
print("*                                      TEORIA                                    *")
print("**********************************************************************************")
print("                                                                                  ")
print("                         ********* CONCURRENCIA *********                         ")
print("                                                                                  ")
print(" Es la capacidad de un sistema de procesar mas de un hilo de ejecución (thread o  ")
print(" proceso) al mismo tiempo.                                                        ")
print("                                                                                  ")
print("                            ********* THREAD *********                            ")
print("                                                                                  ")
print(" Es un proceso o unidad básica del sistema operativo que contiene toda la         ")
print(" información para ser ejecutado, es decir, tiempo del procesador asignado.        ")
print("                                                                                  ")
print("                  ********* EJECUCIÓN NO DETERMINISTA *********                   ")
print("                                                                                  ")
print(" Es la ejecución de varios procesos en sus infinitas pocibilidades de combinación ")
print(" de orden, es decir, que se desconoce el orden de ejecución de dichos procesos.   ")

# II) Development
print("                                                                                  ")
print("**********************************************************************************")
print("*                               CARRERA DE CABALLOS                              *")
print("**********************************************************************************")
print("                                                                                  ")

threadingStart()

threadingJoin()
    
# III)  Conclusions
print("**********************************************************************************")
print("*                                CONCLUSIONES                                    *")
print("**********************************************************************************")
print("  Al repetir el programa varias veces, puede observarse que los caballos ganadores")
print("  varían en cada una. Sin embargo si se hubiera establecido el paso de caballo en 1")
print("  los ganadores tendrían una tendencia probabilistica a ser los primeros threads  ")
print("  ejecutados; por eso se seleccionó el sistema aleatorio de pasos por caballo, para")
print("  disminuir esta leve probabilidad.                                               ")
print("                                                                                  ")
print("  El uso de threads aquí, muestra que la falta de prioridad en una concurrencia,  ")
print("  resulta en un sistema indeterminado de posibles salidas del proceso.            ")
print("                                                                                  ")