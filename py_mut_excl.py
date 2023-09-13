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
def shuffle_threads(input_target):
    threads = []

    for i in range(N):
        t = threading.Thread(target=input_target, args=(i,), name=f"Thread-{i+1}")
        threads.append(t)

    random.shuffle(threads)

    for t in threads: 
        t.start()

    for t in threads:
        t.join() 

# EX N THREADS EXCLUSIÓN MUTUA
def mutual_exclusion_n_threads(num_processes):

    want = [False] * num_processes  # Array de procesos q quieren entrar a seccion critica
    turn = [0] * num_processes  # Array que indica el turno de cada thread
    
    def imprime_thread_ejecutandose(turn): # id del proceso
        print(threading.current_thread().name, "está en la sección crítica, en su turno", turn)
        time.sleep(0.1)    

    def encolado_de_thread(pid):
        nonlocal want, turn

        # Flag indicador de querer ingreso a seccion critica
        want[pid] = True

        # Encuentra el máximo entre threads
        max_turn = max(turn)

        # Establece el turno para el thread actual
        turn[pid] = 1 + max_turn

        # Espera el turno del thread
        for i in range(num_processes):
            if i != pid:
                # Espera mientras otros threads quieren ingresar a seccion critica y es su turno
                while want[i] and (turn[i] < turn[pid] or (turn[i] == turn[pid] and i < pid)):
                    pass

        # Critical section
        imprime_thread_ejecutandose(turn[pid])
        time.sleep(0.1)
            
        # Salida
        want[pid] = False
    
    shuffle_threads(encolado_de_thread)

        
# EX 2 THREADS BAKERY
def lamport_bakery_2_threads(tiempo_segundos):
    np = 0  # Contador del proceso P
    nq = 0  # Contador del proceso Q

    def process_p():
        nonlocal np
        start_time = time.time()
        while (time.time() - start_time) < tiempo_segundos:
            # Non-critical section
                
            # Incrementa np y espera que nq sea cero o np <= nq
            lock.acquire()
            np = nq + 1
            while nq != 0 and np > nq:
                lock.release()
                lock.acquire()
            lock.release()

            # Critical section
            lock.acquire()
            print("PROCESO P: -- Valor de np:", np , "y valor nq:", nq)
            print("Proceso P esta en su sección crítica")
            lock.release()
           
            time.sleep(0.8)

    def process_q():
        nonlocal nq
        start_time = time.time()
        while (time.time() - start_time) < tiempo_segundos:
            # Non-critical section

            # Incrementa nq y espera que np sea cero o nq < np
            lock.acquire()
            nq = np + 1
            while np != 0 and nq >= np:
                lock.release()
                lock.acquire()
            lock.release()

            # Critical section
            lock.acquire()
            print("PROCESO Q  -- Valor de nq:", nq, "y valor de np:", np)
            print("Proceso Q esta en su sección crítica")
            lock.release()
            
            time.sleep(0.8)
            
    p = threading.Thread(target=process_p)
    
    q = threading.Thread(target=process_q)
    p.start()
    q.start()
    p.join()
    q.join()

# EX 3/N THREADS BAKERY
def lamport_bakery_n_threads(num_processes):
    # indica el numero de cola del proceso, devolviendo un booleano
    choosing = [False] * num_processes
    # guarda el numero de ticket del thread
    tickets = [0] * num_processes

    def bakery_algorithm(process_id):
        choosing[process_id] = True # elige el proceso en true
        # asigna un numero  de cola y lo incrementa uno para asegurar que su numero es unico y no hay numeros mas grandes de cola
        tickets[process_id] = max(tickets) + 1 
        choosing[process_id] = False # vuelve a false el procesi cuando ya tiene un numero de cola

        for j in range(num_processes):
            while choosing[j]:# loop que espera hasta que el proceso j tome su numero
                pass
            # loop que espera que el turno del proceso actual para entrar a seccion critica
            # compara los numeros e ids de los procesos para saber el orden de entrada a seccion critica
            while tickets[j] != 0 and (tickets[j] < tickets[process_id] or (tickets[j] == tickets[process_id] and j < process_id)):
                pass

        # Critical section
        print(threading.current_thread().name, "está en la sección crítica")
        time.sleep(0.1)

        tickets[process_id] = False

    shuffle_threads(bakery_algorithm)

        
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
print("                      ********* ALGORITMO DE DEKKER *********                     ")
print("                                                                                  ")
print(" Plantea una solución al problema de exclusión mutua, asignando a dos procesos    ")
print(" que comparten un recurso de un solo uso, una memoria compartida para su comunicación.")
print(" PASOS:                                                                           ")
print("  I) Declara un array de valores booleanos llamado flag con dos elementos, y una  ")
print("     variable entera llamada turn que puede tomar los valores 0 o 1. Estos se     ")
print("     utilizarán para controlar el acceso a la sección crítica.                    ")
print("  II) Cada proceso sigue el siguiente ciclo hasta su finalización:                ")
print("     a)  Establece el indicador [i] en verdadero para indicar que el proceso      ")
print("         desea ingresar a la sección crítica.                                     ")
print("     b)  Comprueba si el otro proceso (j) también quiere ingresar a la sección    ")
print("         crítica (la bandera [j] es verdadera).                                   ")
print("     c)  Si es el turno del otro proceso (el turno es j), ingresa a un ciclo de   ")
print("         espera ocupada hasta que ya no sea el turno del otro proceso.            ")
print("     d)  Ingresa a la sección crítica y realice las operaciones requeridas.       ")
print("     e)  Establece turn en j para indicar que ahora es el turno del otro proceso. ")
print("     f)  Establece el indicador [i] en falso para indicar que el proceso ha       ")
print("         terminado de ejecutar la sección crítica.                                ")
print("     g)  Continúe con la sección restante del proceso.                            ")
print("                                                                                  ")
print("                       ********* ALGORITMO BAKERY *********                       ")
print("                                                                                  ")
print(" Diseñado para evitar que subprocesos concurrentes entren en secciones críticas de")
print(" código simultáneamente, garantizando la seguridad e integridad de los recursos   ")
print(" compartidos entre múltiples subprocesos.                                         ")
print(" PASOS:                                                                           ")
print("  I) Cada proceso mantiene dos matrices: elección y número. La matriz de elección ")
print("     se utiliza para indicar si un proceso está eligiendo actualmente su número, y")
print("     la matriz de números representa el orden en el que los procesos solicitaron  ")
print("     acceso a la sección crítica.                                                 ")
print(" II) Cuando un proceso quiere ingresar a la sección crítica, sigue estos pasos:   ")
print("     a)  Establece su indicador de elección en verdadero, lo que indica que está  ")
print("         eligiendo su número.                                                     ")
print("     b)  Encuentra el número máximo en la matriz numérica y lo incrementa en 1    ")
print("         para obtener su propio número único.                                     ")
print("     c)  Fija su propio número al número obtenido.                                ")
print("     d)  Establece su indicador de elección en falso, lo que indica que ha        ")
print("         terminado de elegir su número.                                           ")
print(" III) Una vez que un proceso ha obtenido su número, espera hasta que su número sea")
print("     el más pequeño entre todos los procesos o hasta que ningún otro proceso elija")
print("     un número.                                                                   ")
print(" IV) Cuando un proceso ingresa a la sección crítica, realiza las operaciones      ")
print("     requeridas.                                                                  ")
print(" V) Una vez que el proceso termina de ejecutar la sección crítica, establece su   ")
print("    número en 0, lo que indica que ya no necesita acceso a la sección crítica     ")
print("                                                                                  ")

N = int(input("Ingrese la Cantidad de Threads: "))

# II) Development
print("                                                                                  ")
print("**********************************************************************************")
print("*                          SOLUCION A EXCLUSION MUTUA                            *")
print("**********************************************************************************")
print("                                                                                  ")
mutual_exclusion_n_threads(N)
print("                                                                                  ")
print("**********************************************************************************")
print("*                          LAMPORT BAKERY: 2 PROCESOS                            *")
print("**********************************************************************************")
print("                                                                                  ")
TIEMPO = int(input("Ingrese la Cantidad de SEGUNDOS para el ejercicio 2: "))
lamport_bakery_2_threads(TIEMPO)
print("                                                                                  ")
print("**********************************************************************************")
print("*                          LAMPORT BAKERY: N PROCESOS                            *")
print("**********************************************************************************")
print("                                                                                  ")
lamport_bakery_n_threads(N)  

    
# III)  Conclusions
print("                                                                                  ")
print("**********************************************************************************")
print("*                                CONCLUSIONES                                    *")
print("**********************************************************************************")
print(" El Algoritmo de Dekker es sólo uno de los muchos algoritmos para lograr la       ")
print("    exclusión mutua.                                                              ")
print(" PROS:                                                                            ")
print("     • Proporciona una solución sencilla y eficaz para que dos procesos compartan ")
print("       una sección crítica sin interferir entre sí.                               ")
print("     • Solo requiere memoria compartida para la comunicación, lo que facilita su  ")
print("       implementación en sistemas que no admiten sincronizacines más avanzadas.   ")
print("     • Es un algoritmo clásico que se utiliza a menudo para enseñar los conceptos ")
print("       básicos de concurrencia y sincronización.                                  ")
print(" CONS:                                                                            ")
print("     • El algoritmo de Dekker tiene un problema conocido como aplazamiento        ")
print("       indefinido, donde un proceso puede retrasarse indefinidamente si el otro   ")
print("       proceso ingresa continuamente a la sección crítica. Esto puede llevar a una")
print("       situación en la que un proceso comienza y nunca tiene la oportunidad de    ")
print("       ejecutar la sección crítica.                                               ")
print("     • El algoritmo se basa en la espera ocupada, lo que puede hacer perder tiempo")
print("       de CPU y no es adecuado para sistemas con recursos limitados o requisitos  ")
print("       de tiempo real.                                                            ")
print("     • Solo admite la exclusión mutua entre dos procesos. Ampliarlo a más de dos  ")
print("       procesos requiere modificaciones y complejidad adicionales.                ")
print(" Podría decirse entonces que los mayores problemas de este algoritmo sería la     ")
print(" posibilidad de Starvation y Contención por Terminación, ya que si un proceso     ")
print(" termina antes de ingresar a la sección crítica, el otro podría quedarse esperando")
print(" indefinidamente.                                                                 ")
print("                                                                                  ")
print(" En el Ejercicio 1, se realiza un enfoque simple por turnos para lograr la        ")
print(" la exclusión mutua, basado en el planteo del Algoritmo de Dekker. Garantiza que  ")
print(" solo un hilo ingrese a la sección crítica a la vez y otros esperen su turno.     ")
print(" PROS:                                                                            ")
print("     • El código garantiza la exclusión mutua, lo que impide el acceso simultáneo ")
print("       a la sección crítica y evita condiciones de carrera.                       ")
print("     • Es fácil de entender e implementar, utilizando técnicas básicas de         ")
print("       sincronización.                                                            ")
print("     • El código utiliza un enfoque por turnos, que garantiza la equidad. Cada hilo")
print("       tiene la oportunidad de ingresar a la sección crítica en forma de turnos.  ")
print(" CONS:                                                                            ")
print("     • El código implica una espera ocupada, lo que es ineficiente en términos    ")
print("       de utilización de recursos.                                                ")
print("     • El enfoque basado en turnos puede generar contención y reducción del      ")
print("       rendimiento, especialmente con una gran cantidad de subprocesos.           ")
print("     • El código no maneja casos excepcionales como fallas de subprocesos o       ")
print("       interrupciones del sistema. Tampoco proporciona ningún mecanismo para la   ")
print("       programación basada en prioridades.                                        ")
print(" El código esta llevado para n procesos pero no significa en este caso que sea eficiente")
print(" porque puede producir un cuello de botella a mayor cantidad de threads en ejecución.")
print(" Podría mejorarse entonces con locks, semáforos o exchange.                       ")
print("                                                                                  ")
print(" El Algoritmo Bakery diferentes variaciones e implementaciones con sus propias    ")
print("   compensaciones y optimizaciones.                                               ")
print(" PROS:                                                                            ")
print("     • El algoritmo de panadería es una de las soluciones conocidas más simples al")
print("       problema de exclusión mutua para el caso general de N procesos.            ")
print("     • Garantiza el uso justo de los recursos compartidos en un entorno de        ")
print("       subprocesos múltiples.                                                     ")
print("     • Puede manejar cualquier cantidad de procesos sin degradar el rendimiento,  ")
print("       lo que lo hace escalable.                                                  ")
print(" CONS:                                                                            ")
print("     • El algoritmo de panadería es susceptible al problema de starvation.        ")
print("       Si a un proceso se le asigna un número alto, es posible que tenga que      ")
print("       esperar indefinidamente antes de poder acceder a la sección crítica        ")
print("     • La complejidad del mensaje del algoritmo de panadería es relativamente    ")
print("       alta y requiere 3 (N - 1) mensajes por entrada o salida en la sección crítica.")
print(" Podría decirse entonces que el mayor problemas de este algoritmo sería la        ")
print(" Contención por Terminación, ya que si un proceso ya que no es confiable en caso  ")
print(" de falla del proceso. Si alguno de los procesos se detiene, puede provocar la    ")
print(" interrupción del progreso de todo el sistema. si un proceso termina antes de su  ")
print(" turno para ingresar a la sección crítica, tiene que comenzar de nuevo en la cola ")
print(" de procesos generando contención ya que es posible que sea necesario volver a    ")
print(" poner en cola el proceso finalizado y reiniciar el proceso de adquisición de un  ")
print(" número de ticket, lo que podría retrasar la entrada de otros procesos a la       ")
print(" sección crítica.                                                                 ")
print("                                                                                  ")
print(" En el Ejercicio 2, se pudo quitar el límite de tickets de np y nq, mediante      ")
print(" la eliminación del reseteo de np y nq al terminar los procesos correspondientes  ")
print(" como en el código original propuesto en Ben Ari Slides.                          ")
print(" Dicha implementación se realizó con el propósito de verificar su posibilidad,    ")
print(" sin embargo, a fines prácticos, la misma no representa ninguna ventaja, al contrario")
print(" tener dos procesos con tickets tan altos, entorpece el procesamiento demorándolo ")
print(" innecesariamente.                                                                ")
print("                                                                                  ")
print(" En el Ejercicio 3, se realiza un enfoque simple por tickets para lograr la       ")
print(" la exclusión mutua, basado en el planteo del Algoritmo Bakery. Garantiza que     ")
print(" solo el hilo con el menor número de ticket, ingrese a la sección crítica a la   ")
print(" vez y otros esperen su turno.                                                    ")
print(" PROS:                                                                            ")
print("     • El código garantiza la exclusión mutua, lo que impide el acceso simultáneo ")
print("       a la sección crítica y evita condiciones de carrera.                       ")
print("     • Proporciona equidad al asignar números de ticket y permitir que los hilos  ")
print("       ingresen a la sección crítica en orden secuencial.                         ")
print("     • El algoritmo puede manejar un número variable de subprocesos y garantiza   ")
print("       que todos los subprocesos eventualmente tengan la oportunidad de ingresar a")
print("       la sección crítica.                                                        ")
print(" CONS:                                                                            ")
print("     • El código implica una espera ocupada, ya que cada hilo verifica continuamente")
print("       la condición en un bucle hasta que puede ingresar a la sección crítica.    ")
print("     • El código no maneja casos excepcionales como fallas de subprocesos o       ")
print("       interrupciones del sistema.                                                ")
print("     • Puede que no se escale bien con una gran cantidad de subprocesos. A medida ")
print("       que aumenta el número de subprocesos, la contienda por ingresar a la sección")
print("       crítica puede aumentar, lo que lleva a un rendimiento reducido.            ")
print(" A pesar de poder manejar n procesos, esto no significa que sea escalable ya que  ")
print(" mientras mas procesos entren en ejecución, más espera ocupada se produce, al     ")
print(" checkear continuamente la condicion hasta poder accesar (cond = true).           ")
print("                                                                                  ")
print("  NOTA1: en la línea 300 se ingresa por consola la cantidad de threads a correr   ")
print("         para evitar llegar a numeros infinitos. Es posible reiniciar la aplicación")
print("         para poder comprobar que pueden utilizarse hasta n threads.              ")
print("                                                                                  ")
print("  NOTA2: en la línea 307 se ingresa por consola un timer en el caso de 2 procesos ")
print("         en el segundo ejercicio, ya que al permitir los np y nq aumentar         ")
print("         ilimitadamente, el mismo no terminaría sino hasta que llegue al límite   ")
print("         de operaciones posibles en una ejecución, preestablecido por python.     ")
print("                                                                                  ")
print("  NOTA3: en la línea 24 la función shuffle_threads se estableció para semejar a la ")
print("         idea de aleatoriedad de los threads en ejecución, en caso contrario los  ")
print("         mismos ingresan en el mismo orden en que comienzan a ejecutarse por la   ")
print("         mínima diferencia de tiempo en la que se toma dicho hilo para ejecutarse.")
print("                                                                                  ")
print("               ____                                                               ")
print("              /    \	                                                             ")
print("             |  u  u|                                                             ")
print("             |    \ |  .-''#%&#&%#``-.                                            ")
print("              \  = /  ((%&#&#&%&VK&%&))                                           ")
print("               |  |    `-._#%&##&%_.-'                                            ")
print("               /\/\`--.   `-."".-'                                                ")
print("               |  |    \   /`./                                                   ")
print("               |\/|  \  `-'  /                                                    ")
print("               || |   \     /                                                     ")