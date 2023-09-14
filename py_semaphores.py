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
import random

# Global Variables
# Lock asegura la exclusion mutua similar al caso de semáforo
lock = threading.Lock()

# Functions
# GENERAL
####################################################################################

def productor_consumidor():
    # Búfer compartido
    buffer = []
    buffer_size = 5
    tiempo_segundos = 5
    start_time = time.time()

    # Semáforos
    mutex = threading.Semaphore(1)  # Semáforo para exclusión mutua
    empty = threading.Semaphore(buffer_size)  # Semáforo para espacios vacíos en el búfer
    full = threading.Semaphore(0)  # Semáforo para elementos en el búfer

    # Función para el productor
    def producer(id):
        nonlocal buffer
        while (time.time() - start_time) < tiempo_segundos:
            item = random.randint(1, 100)  # Generar un elemento aleatorio
            empty.acquire()  # Esperar a que haya espacio en el búfer
            mutex.acquire()  # Entrar en la sección crítica
            buffer.append(item)  # Colocar el elemento en el búfer
            print(f"Productor {id} produjo {item}, Búfer: {buffer}")
            mutex.release()  # Salir de la sección crítica
            full.release()  # Notificar al consumidor que hay un elemento en el búfer
            time.sleep(random.uniform(0.1, 0.5))  # Esperar un tiempo aleatorio
        mutex.release()
        full.release()

    # Función para el consumidor
    def consumer():
        nonlocal buffer
        while (time.time() - start_time) < tiempo_segundos:
            full.acquire()  # Esperar a que haya elementos en el búfer
            mutex.acquire()  # Entrar en la sección crítica
            item = buffer.pop(0)  # Tomar el primer elemento del búfer
            print(f"Consumidor consumió {item}, Búfer: {buffer}")
            mutex.release()  # Salir de la sección crítica
            empty.release()  # Notificar a los productores que hay espacio en el búfer
            time.sleep(random.uniform(0.1, 0.5))  # Esperar un tiempo aleatorio
        mutex.release()
        empty.release()

    # Crear hilos para los productores
    producer_thread1 = threading.Thread(target=producer, args=(1,))
    producer_thread2 = threading.Thread(target=producer, args=(2,))

    # Crear hilo para el consumidor
    consumer_thread = threading.Thread(target=consumer)

    # Iniciar los hilos
    producer_thread1.start()
    producer_thread2.start()
    consumer_thread.start()

    # Esperar a que los hilos terminen (esto nunca sucede en este ejemplo)
    producer_thread1.join()
    producer_thread2.join()
    consumer_thread.join()

####################################################################################

def rendezvous_2():
    # Semáforos
    semaphore_A = threading.Semaphore(0)
    semaphore_B = threading.Semaphore(0)

    # Función del proceso A
    def proceso_A():
        print("Proceso A - Operaciones antes del encuentro")
        semaphore_B.release()  # Permite que el proceso B avance
        semaphore_A.acquire()  # Espera hasta que el proceso B lo autorice
        print("Proceso A - Operaciones después del encuentro")

    # Función del proceso B
    def proceso_B():
        print("Proceso B - Operaciones antes del encuentro")
        semaphore_B.acquire()  # Espera hasta que el proceso A lo autorice
        semaphore_A.release()  # Permite que el proceso A avance
        print("Proceso B - Operaciones después del encuentro")

    # Crear hilos para los procesos A y B
    thread_A = threading.Thread(target=proceso_A)
    thread_B = threading.Thread(target=proceso_B)

    # Iniciar los hilos
    thread_A.start()
    thread_B.start()

    # Esperar a que los hilos terminen (esto nunca sucede en este ejemplo)
    thread_A.join()
    thread_B.join()

####################################################################################

def rendezvous_N():
    N = 5  # Cambia N según el número de procesos que desees

    # Semáforos
    semaphores = [threading.Semaphore(0) for _ in range(N)]

    # Función para un proceso genérico
    def proceso(id):
        nonlocal N
        print(f"Proceso {id} - Operaciones antes del encuentro")
        
        if id < N - 1:
            semaphores[id + 1].release()  # Permite que el siguiente proceso avance
        
        semaphores[id].acquire()  # Espera hasta que el proceso anterior lo autorice
        
        print(f"Proceso {id} - Operaciones después del encuentro")

    # Crear hilos para los procesos
    threads = [threading.Thread(target=proceso, args=(i,)) for i in range(N)]

    # Iniciar los hilos
    for thread in threads:
        thread.start()

    # Liberar el primer proceso para iniciar la secuencia
    semaphores[0].release()

    # Esperar a que los hilos terminen (esto nunca sucede en este ejemplo)
    for thread in threads:
        thread.join()

####################################################################################


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
print("  Describir en pseudocódigo una solución al problema de productor-consumidor, para")
print("  el caso de 2 productores y 1 consumidor, todos sobre un mismo buffer. Escribir  ")
print("  todas las aclaraciones que sean necesarias.                                     ")
print("                                                                                  ")
print("  EJERCICIO 2:                                                                    ")
print("  En pseudocódigo, usando semáforos, resolver el problema del 'rendez-vous'.      ")
print("  Consiste en tener dos procesos, tales que uno de ellos mientras ejecuta deberá  ")
print("  alcanzar un punto (o marca) dentro de su código, y lo mismo con otro proceso.   ")
print("  El primero de ambos que llegue a la marca correspondiente deberá quedarse esperando")
print("  a que el otro proceso llegue a su marca, y recién en el momento en que el otro  ")
print("  haya llegado, ambos podrán continuar ejecutando su código a partir de allí.     ")
print("                                                                                  ")
print("  EJERCICIO 3:                                                                    ")
print("  Escribir o discutir luego una solución análoga del rendez-vous para 3 o más     ")
print("  procesos, cada uno con su código y su marca dada.                               ")
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
print(" CONDICIONES DE BUENA CONCURRENCIA:                                               ")
print("   ◘ Pre-protocolos: no deben tener errores, detenciones inesperadas y/o salidas. ")
print("   ◘ Post-protocolos: no deben tener errores, detenciones inesperadas y/o salidas.")
print("   ◘ Sección Crítica: no debe tener errores, detenciones inesperadas y/o salidas. ")
print("   ◘ Sección NO Crítica: debe la salida del programa.                             ")
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
print("                       ******** SECCIÓN CRÍTICA *********                         ")
print("                                                                                  ")
print(" Porción de código que debe ser ejecutada única y atómicamente.                   ")
print("                                                                                  ")
print("                          ********* SEMÁFORO *********                            ")
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
print(" PROBLEMAS:                                                                       ")
print("   ◘ Problema de Exclusión Mutua: requiere que no haya mas de un proceso en       ")
print("              ejecución en la sección crítica. Imposibilita el interleaving.      ")
print("   ◘ Problema de Deadlock: se produce cuando varios procesos quedan a la espera de")
print("              otro o de un recurso de otro y no pueden ejecutartse ya que no los  ")
print("              obtienen. Se evita en casos de invariabilidad.                      ")
print("   ◘ Problema de Starvation: ocurre cuando un proceso no puede ingresar a su zona ")
print("              crítica por quedarse indefinidamente a la espera de un recurso. Es  ")
print("              evitable en los casos de cola.                                      ")
print("   ◘ Problema de Contención por Terminación: sucede cuando un proceso, que tiene  ")
print("              otro dependiente de él, termina y no permite continuar al dependiente.")
print("                                                                                  ")
print("               ********* PROBLEMA DE PRODUCTOR-CONSUMIDOR *********               ")
print("                                                                                  ")
print(" Plantea el problema de sincronización de multiprocesos                           ")
print(" Se describe la interacción entre dos procesos, un productor y un consumidor, que ")
print(" comparten un búfer de tamaño finito. El productor genera elementos y los almacena")
print(" en el búfer, mientras que el consumidor toma los elementos del búfer.            ")
print(" El problema consiste en garantizar que el productor no agregue más elementos de  ")
print(" los que el búfer puede contener y que el consumidor no intente tomar un elemento ")
print(" si el búfer está vacío.                                                          ")
print(" La idea para la solución es que ambos procesos (productor y consumidor) se ejecuten")
print(" simultáneamente y se 'despiertan' o 'duermen' según el estado del búfer.         ")
print(" Concretamente, el productor agrega elementos mientras quede espacio en el búfer  ")
print(" y, en el momento en que se llene el búfer, se pone a 'dormir'.                   ")
print(" Cuando el consumidor toma un elemento, notifica al productor que puede comenzar  ")
print(" a trabajar nuevamente. En caso contrario, si el búfer se vacía, el consumidor    ")
print(" se pone a dormir y, en el momento en que el productor agrega un elemento, crea   ")
print(" una señal para despertarlo.                                                      ")
print(" Una implementación adecuada del problema utiliza semáforos para manejar la       ")
print(" sincronización entre los procesos y evitar condiciones de carrera.               ")
print("                                                                                  ")
print("                    ********* PROBLEMA DE RANDEZ-VOUS *********                   ")
print("                                                                                  ")
print(" Plantea el problema en el que dos o más procesos o hilos necesitan comunicarse o ")
print(" sincronizarse para realizar alguna tarea conjuntamente. Es relevante en contexto ")
print(" de sistemas concurrentes y multiprocesadores, donde los procesos pueden ejecutarse")
print(" de forma simultánea o en paralelo .                                              ")
print(" El rendezvous es un mecanismo de sincronización que permite a los procesos esperar")
print(" a que otros lleguen a un punto específico del programa antes de continuar con su ")
print(" ejecución. Esto es útil en situaciones en las que varios procesos deben coordinar")
print(" sus acciones o compartir recursos, como en el productor-consumidor, ya que permite")
print(" a los procesos trabajar de manera eficiente y sin conflictos al compartir recursos")
print(" y coordinar sus acciones. La implementación adecuada del rendezvous es esencial  ")
print(" para evitar condiciones de carrera, deadlocks y otros problemas de concurrencia  ")
print("                                                                                  ")

# II) Development
print("                                                                                  ")
print("**********************************************************************************")
print("*                       PROBLEMA DE PRODUCTOR-CONSUMIDOR                         *")
print("**********************************************************************************")
print("                                                                                  ")
productor_consumidor()

print("                                                                                  ")
print("**********************************************************************************")
print("*                     PROBLEMA DE RANDEZ-VOUS: 2 PROCESOS                        *")
print("**********************************************************************************")
print("                                                                                  ")
rendezvous_2()

print("                                                                                  ")
print("**********************************************************************************")
print("*                PROBLEMA DE RANDEZ-VOUS: 2 PROCESOS: N PROCESOS                 *")
print("**********************************************************************************")
print("                                                                                  ")
rendezvous_N()

# III)  Conclusions
print("                                                                                  ")
print("**********************************************************************************")
print("*                                CONCLUSIONES                                    *")
print("**********************************************************************************")
print("  BLAH   ")
print("                                                                                  ")
print("  NOTA1: en la línea 310 se ingresa por consola la cantidad de threads a correr   ")
print("                                                                                  ")
print("   __________________________________________________________________________     ")
print("  |: : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : |    ")
print("  | : : : : : : : : : : : : : : : :_________________________: : : : : : : : :|    ")
print("  |: : : : : : : : : : : : : : : _)                         (_ : : : : : : : |   ")
print("  | : : : : : : : : : : : : : : )_ :  Club 40 Gift Shoppe :  _( : : : : : : :|    ")
print("  |: : Elevator  : : : :__________)_________________________(__________  : : |    ")
print("  | _____________ : _ :/ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ\: _ :|    ")
print("  ||  _________  | /_\ '.Z.'.Z.'.Z.'.Z.'.Z.'.Z.'.Z.'.Z.'.Z.'.Z.'.Z.'.Z.' /_\ |    ")
print("  || |    |    | |:=|=: |Flowers * Perfumes_________Lingerie * Candles| :=|=:|    ")
print("  || |    |    | | : : :|   ______    _  .'         '.  _    ______   |: : : |    ")
print("  || |    |    | |======| .' ,|,  '. /_\ |           | /_\ .'  ,|, '. |======|    ")
print("  || |    |    |:|Lounge| | ;;;;;  | =|= |           | =|= |  ;;;;; | |Casino|    ")
print("  || |    |    | |<---  | |_';;;'_n|     |  n______  |     |$_';;;'_| |  --->|    ")
print("  || |    |    | |      | |_|-;-|__|     |-|_______|-|     |__|-;-|_| |      |    ")
print("  || |    |    | |      | |________|     |           |     |________| |      |    ")
print("  || |    |    | |      |                |           |                |      |    ")
print("  |__|____|____|_|______|________________|           |________________|______|    ")








