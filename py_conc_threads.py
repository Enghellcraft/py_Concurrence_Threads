#
# TRABAJO PRACTICO DE SEMINARIO
#

# imports
import random
import threading
import time
import matplotlib.pyplot as plt
from collections import Counter

# Global Variables
# Generación de lock para evitar reimpresion por cada thread de: "Tenemos un Ganador!"
print_lock = threading.Lock()

# Functions
def avanzar_caballo(nombre, distancia_recorrida, distancia_total, ganador_event, ganadores_historico):
    while (distancia_recorrida < distancia_total):
        if ganador_event.is_set():
            return
        salto = random.randint(1, 6)
        #salto = 1
        if (distancia_recorrida + salto) >= distancia_total:
            distancia_recorrida = distancia_total
            # Detener a los otros caballos
            ganador_event.set()
            if print_lock.acquire(blocking=False):  # Devuelve false si ya esta lockeado
                print("\n*--------** La Carrera Termino **--------*")
                print("\nTenemos un Ganador!!")
                print(f"\n{nombre} ganó!\n")
                # Quita el lock
                print_lock.release()
                ganadores_historico.append(nombre)   
                return 
        else :
            distancia_recorrida += salto
            if not ganador_event.is_set():
                print(f"{nombre} ha recorrido {distancia_recorrida} metros.")
        time.sleep(0.8) # Timer para evitar impresiones fuera de lugar     

def carrera(distancia_total):
    
    print("\n*--------** Comienza la Carrera!! **--------*")
    while True:
        caballos = []
        ganador_event = threading.Event()
        ganadores_historico = []

        for i in range(1, 11):
            distancia_recorrida = 0
            caballo_thread = threading.Thread(target=avanzar_caballo, args=(f"Caballo {i}", distancia_recorrida, distancia_total, ganador_event, ganadores_historico))
            caballos.append(caballo_thread)

        for caballo in caballos:
            caballo.start()

        ganador_event.wait() # Espera el evento del caballo ganador
        for caballo in caballos:
            caballo.join(0.1) # Termina el thread donde sea que este

        if ganadores_historico:
            return ganadores_historico[-1]  # Devolver el último ganador

def main():
    distancia_total = 20
    carreras = 6

    ganadores_historicos = []

    for _ in range(carreras):
        ganador = carrera(distancia_total)
        if ganador:
            ganadores_historicos.append(ganador)
    
    print(ganadores_historicos)

    # Contar las victorias de cada caballo
    conteo_victorias = Counter(ganadores_historicos)
    nombres_caballos = [f"Caballo {i}" for i in range(1, 11)]  # Crear lista con nombres de caballos del 1 al 10
    victorias = [conteo_victorias[nombre] for nombre in nombres_caballos]

    # Plot
    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(nombres_caballos, victorias, alpha=0.7)
    plt.xlabel('Caballo')
    plt.ylabel('Cantidad de Victorias')
    plt.title('Distribución de Victorias en Carreras de Caballos')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

#  null) Task + Pres
print("                                                                                  ")
print("**********************************************************************************")
print("*                 SEMINARIO DE PROGRAMACION - 2023 - TP THREADS                  *")
print("**********************************************************************************")
print("    ALUMNOS:                                                                      ")
print("            • Bardales, Wilfredo                                                  ")
print("            • Martin, Denise                                                      ")
print("            • Paleari, Carolina                                                    ")
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
   
if __name__ == "__main__":
    main()   
    
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
print("  resulta en un sistema indeterminado de posibles salidas del proceso, donde,     ")
print("  siendo n la cantidad de threads, cada thread tiene una probabilidad de 1/n * 100%")
print("  de salir ganador (considerando casos ideales).                                  ")
print("                                                                                  ")