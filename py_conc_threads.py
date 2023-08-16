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
def avanzar_caballo(nombre, distancia_recorrida, distancia_total, ganador_event, ganadores_historico, race_progress):
    while (distancia_recorrida < distancia_total):
        if ganador_event.is_set():
            return
        
        salto = random.randint(1, 6)
        #salto = 1

        if (distancia_recorrida + salto) >= distancia_total:
            # Detener a los otros caballos
            ganador_event.set()
            
            distancia_recorrida = distancia_total
            print(f"{nombre} ha recorrido {distancia_recorrida} metros.")
            # Guarda el progreso del caballo
            race_progress.append((nombre, distancia_recorrida))   
            
            # Uso de lock para impresión única del término de carrera, como SEMAFORO para sección critca
            if print_lock.acquire(blocking=False):  # Devuelve false si ya esta lockeado. // WAIT
                print("\n*--------** La Carrera Termino **--------*")
                print("\nTenemos un Ganador!!")
                print(f"\n{nombre} ganó!\n")
                # Quita el lock // SIGNAL
                print_lock.release()
                ganadores_historico.append(nombre)   
                return 
        else:
            distancia_recorrida += salto 
            print(f"{nombre} ha recorrido {distancia_recorrida} metros.")
            # Guarda el progreso del caballo
            race_progress.append((nombre, distancia_recorrida))   
                    
        time.sleep(0.9) # Timer para evitar impresiones fuera de lugar     

def carrera(distancia_total, race_count):
    
    print(f"\n*--------** Comienza la Carrera {race_count}!! **--------*")
    
    # Lista de progreso de pasos por caballo
    race_progress = []
    
    while True:
        caballos = []
        ganador_event = threading.Event()
        ganadores_historico = []

        for i in range(1, 11):
            distancia_recorrida = 0
            caballo_thread = threading.Thread(target=avanzar_caballo, args=(f"Caballo {i}", distancia_recorrida, distancia_total, ganador_event, ganadores_historico, race_progress))
            caballos.append(caballo_thread)

        for caballo in caballos:
            caballo.start()

        ganador_event.wait() # Espera el evento del caballo ganador
        for caballo in caballos:
            caballo.join(0.1) # Termina el thread donde sea que este

        if ganadores_historico:
            # Plot
            # Progreso de caballos
            fig, ax = plt.subplots(figsize=(6, 6))
            for horse, progress in race_progress:
                ax.plot(range(1, progress + 1), [horse] * progress, label=horse)
            ax.set_xlabel('Distancia Recorrida')
            ax.set_ylabel('Caballo')
            ax.set_title(f'Progreso de los Caballos en la Carrera {race_count}')
            plt.tight_layout()

            plt.show()
            
            return ganadores_historico[-1]  # Devolver el último ganador

def main():
    distancia_total = 20
    carreras = 6

    # Lista de ganadores por cada carrera
    ganadores_historicos = []

    for race_count in range(1, carreras + 1):
        ganador = carrera(distancia_total, race_count)
        if ganador:
            ganadores_historicos.append(ganador)
    
    print("Los Ganadores Historicos son:")
    print(ganadores_historicos)

    # Contar las victorias de cada caballo
    conteo_victorias = Counter(ganadores_historicos)
    # Imprime lista con nombres de caballos del 1 al 10
    nombres_caballos = [f"Caballo {i}" for i in range(1, 11)]  
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
print("  Implementar una 'carrera de caballos' usando threads, donde cada 'caballo' es un")
print("  Thread o bien un objeto de una clase que sea sub clase de Thread, y contendrá   ")
print("  una posición dada por un número entero. El ciclo de vida de este objeto es      ")
print("  incrementar la posición en variados instantes de tiempo, mientras no haya llegado")
print("  a la meta, la cual es simplemente un entero prefijado. Una vez que un caballo   ")
print("  llegue a la meta, se debe informar en pantalla cuál fue el ganador, luego de lo ")
print("  cual los demás caballos no deberán seguir corriendo. Imprimir durante todo el   ")
print("  ciclo las posiciones de los caballos, o bien de alguna manera el camino que va  ")
print("  recorriendo cada uno (usando símbolos Ascii). El programa podría producir un    ")
print("  ganador disitnto cada vez que se corra. Opcionalmente, extender el funcionamiento")
print("  a un array de n caballos, donde n puede ser un parámetro.                       ")
print("  Puntos a Cumplir:                       ")
print("  1- Definir  10 caballos para correr una carrera, cada caballo es un thread.     ")
print("  2- Definir una distancia de 20.                                                 ")
print("  3- Todos los caballos corren moviendose en saltos 1 a 1, o aleatorios.          ")
print("  4- Sólo un caballo puede ganar, y cuando lo hace deben frenarse todos los demás.")
print("  5- Implementar un semáforo con lock de Thread para limitar la sección crìtica.  ")
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
print(" Es la ejecución de varios procesos en sus infinitas posibilidades de combinación ")
print(" de orden, es decir, que se desconoce el orden de ejecución de dichos procesos.   ")
print("                                                                                  ")
print("                           ********* SEMÁFORO *********                           ")
print("                                                                                  ")
print(" Variable o tipo de dato abstracto utilizado para el acceso a un recurso común    ")
print(" requerido por múltiples threads, o para evitar problema de acceso a sección      ")
print(" crítica en sistemas concurrentes.")
print("                                                                                  ")

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
print("  Al utilizar un lock de la librería de Thread en la impresión del fin de carrera ")
print("  se puede evitar el ingreso de threads a la misma sección, dejando la impresión  ")
print("  solamente para el thread que finalice primero.                                  ")
print("                                                                                  ")
print("  NOTA1: en la línea 23 puede verse el salto de caballo unitario, en caso de querer")
print("  probar la primera conclusión. Esta comentado pero funcional, requiere comentar el")
print("  salto aleatorio para evitar errores.                                            ")
print("                                                                                  ")
print("  NOTA2: en la línea 35 y 40 se agrega el lock a la impresión, en caso de removerlas")
print("  y correr el programa, podrá observarse la impresión de más de un thread que finaliza.")
print("                                                                                  ")