#
# TRABAJO PRACTICO DE SEMINARIO
#
#ALUMNOS:                                                                      
#       • Bardales, Wilfredo                                                  
#       • Martin, Denise                                                     
#       • Paleari, Carolina                                                  

# imports
import threading
import time
from queue import Queue

# Global Variables
# Lock asegura la exclusion mutua similar al caso de semáforo
lock = threading.Lock()

# Functions
# EX 1
def exclusion_mutua_n_threads():
    # Cola de espera para los turnos de cada thread
    turn_queue = Queue()

    def imprime_thread_ejecutandose():
        print("%s Funcionando en su turno" % str(threading.current_thread()))
        time.sleep(0.1)

    def encolado_de_thread():
        # Entrega un turno por cola al turno en ejecución
        turn_queue.put(threading.current_thread())

        # Espera hasta su turno
        while turn_queue.queue[0] is not threading.current_thread():
            pass

        # Con lock permite que sólo un thread acceda a la seccion crítica
        with lock:
            imprime_thread_ejecutandose()

        # Elimina al thread de la cola
        turn_queue.get()

    # Create and start an infinite number of threads
    # while True:
    for i in range(10):
        t = threading.Thread(target=encolado_de_thread)
        t.start()
        t.join()


#  null) Task + Pres
print("                                                                                  ")
print("**********************************************************************************")
print("*               SEMINARIO DE PROGRAMACION - 2023 - TP EXCLUSION MUTUA            *")
print("**********************************************************************************")
print("    ALUMNOS:                                                                      ")
print("            • Bardales, Wilfredo                                                  ")
print("            • Martin, Denise                                                      ")
print("            • Paleari, Carolina                                                   ")
print("                                                                                  ")
print("**********************************************************************************")
print("*                                   OBJETIVO                                     *")
print("**********************************************************************************")
print("  Entendimiento de funcionamiento y errores producidos en casos de Exclusión Mutua.")
print("                                                                                  ")
print("**********************************************************************************")
print("*                                   CONSIGNAS                                    *")
print("**********************************************************************************")
print("                                                                                  ")
print("  EJERCICIO 1:                                                                    ")
print("  Escribir en pseudocódigo el primer intento de solución de exclusión mutua       ")
print("  (que usa turnos) para N procesos.                                               ")
print("                                                                                  ")
print("  EJERCICIO 2:                                                                    ")
print("  Para Bakery de 2 procesos p y q, describir un escenario en que las variables    ")
print("  np y nq crecen ilimitadamente.                                                  ")
print("                                                                                  ")
print("  EJERCICIO 3:                                                                    ")
print("  Escribir una versión de Bakery para 3 procesos, lo más simple que se pueda.     ")
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
print("                      ********* SECCIÓN CRÍTICA *********                         ")
print("                                                                                  ")
print(" Porción de código que debe ser ejecutada única y atómicamente.                   ")
print("                                                                                   ")
print("                           ********* SEMÁFORO *********                           ")
print("                                                                                  ")
print(" Variable o tipo de dato abstracto utilizado para el acceso a un recurso común    ")
print(" requerido por múltiples threads, o para evitar problema de acceso a sección      ")
print(" crítica en sistemas concurrentes.                                                ")
print("                                                                                  ")
print("                      ********* EXCLUSIÓN MUTUA *********                         ")
print("                                                                                  ")
print(" Evitar que varios hilos accedan simultáneamente a sección crítica, esencialmente")
print(" para evitar condiciones de carrera y garantizar la integridad de los datos       ")
print(" compartidos.                                                                     ")
print("                                                                                  ")

# II) Development
print("                                                                                  ")
print("**********************************************************************************")
print("*                        SOLUCION A EXCLUSION MUTUA                              *")
print("**********************************************************************************")
print("                                                                                  ")
exclusion_mutua_n_threads()
print("                                                                                  ")
print("**********************************************************************************")
print("*                        BAKERY ALGORITHM: 2 PROCESOS                            *")
print("**********************************************************************************")
print("                                                                                  ")

print("                                                                                  ")
print("**********************************************************************************")
print("*                        BAKERY ALGORITHM: N PROCESOS                            *")
print("**********************************************************************************")
print("                                                                                  ")
   

    
# III)  Conclusions
print("**********************************************************************************")
print("*                                CONCLUSIONES                                    *")
print("**********************************************************************************")
print("  BLAH")
print("                                                                                  ")
print("  NOTA1: en la línea 44 puede descomentarse el 'while true' y permitir infitos    ")
print("         threads ejecutarse y encolarse. Para evitar dejar ad infinitum el mismo  ")
print("         se le dio un rango de 10 threads.                                        ")

