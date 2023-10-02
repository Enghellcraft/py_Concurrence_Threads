#
# TRABAJO PRACTICO DE SEMINARIO
#
#ALUMNOS:                                                                      
#       • Bardales, Wilfredo                                                  
#       • Martin, Denise                                                     
#       • Paleari, Carolina                                                  

# imports
import threading
import simpy
import random
import time
import sys
import matplotlib.pyplot as plt

# CON THREADS

def threads():

  NUM_PHILOSOPHERS = 5
  philosophers = []
  forks = [threading.Lock() for _ in range(NUM_PHILOSOPHERS)]

  def philosopher(id):
    left_fork = forks[id]
    right_fork = forks[(id + 1) % NUM_PHILOSOPHERS]

    while True:
        print(f'Philosopher {id} is thinking')
        time.sleep(0.8)
        # Think for a while

        left_fork.acquire()
        print(f'Philosopher {id} picked up left fork')
        right_fork.acquire()
        print(f'Philosopher {id} picked up right fork and is eating')
        time.sleep(0.8)
        # Eat for a while
  
        right_fork.release()
        print(f'Philosopher {id} released right fork')
        left_fork.release()
        print(f'Philosopher {id} released left fork')

  for i in range(NUM_PHILOSOPHERS):
      philosophers.append(threading.Thread(target=philosopher, args=(i,)))

  for philosopher_thread in philosophers:
      philosopher_thread.start()

  for philosopher_thread in philosophers:
      philosopher_thread.join()

# SIN THREADS


def sinThreads():
    # Definir una clase para representar a los filósofos
    class Filosofo:
        def __init__(self, env, nombre, tenedor_izq, tenedor_der, num):
            self.env = env
            self.nombre = nombre
            self.tenedor_izq = tenedor_izq
            self.tenedor_der = tenedor_der
            self.num = num
            self.comiendo = False
            self.tiempos = []  # Lista para registrar los tiempos de las acciones
            env.process(self.filosofar())

        def filosofar(self):
            while True:
                self.tiempos.append((self.env.now, self.comiendo))
                yield self.env.timeout(random.uniform(1, 2))  # Aumentamos el rango para hacerlo más lento
                self.tiempos.append((self.env.now, self.comiendo))
                yield self.env.process(self.comer())

        def comer(self):
            with self.tenedor_izq.request() as tenedor_izq_req:
                yield tenedor_izq_req
                with self.tenedor_der.request() as tenedor_der_req:
                    yield tenedor_der_req
                    self.comiendo = True
                    self.tiempos.append((self.env.now, self.comiendo))
                    yield self.env.timeout(random.uniform(1, 2))  # Aumentamos el rango para hacerlo más lento
                    self.comiendo = False
                    self.tiempos.append((self.env.now, self.comiendo))

    # Crear un entorno de simulación
    env = simpy.Environment()

    # Crear tenedores como recursos compartidos
    tenedores = [simpy.Resource(env) for _ in range(5)]

    # Crear filósofos
    filosofos = [Filosofo(env, f'Filósofo {i}', tenedores[i], tenedores[(i + 1) % 5], i) for i in range(5)]

    # Limitar a 2 filósofos comiendo al mismo tiempo
    limitador = simpy.Resource(env, capacity=2)

    # Inicializar listas para el gráfico
    tiempos = []
    estados = []
    nombres = [f.nombre for f in filosofos]

    # Ejecutar la simulación durante 10 segundos
    for tiempo_simulacion in range(1, 11):  # Cambiamos el rango de 1 a 10
        env.run(until=tiempo_simulacion)
        
        # Recopilar estados de los filósofos en este segundo
        estados_segundo = [filosofo.comiendo for filosofo in filosofos]
        estados.extend(estados_segundo)
        tiempos.extend([tiempo_simulacion] * len(filosofos))

        # Imprimir estados de los filósofos en este segundo
        print(f'Segundo {tiempo_simulacion}:')
        for i, filosofo in enumerate(filosofos):
            estado = 'Comiendo' if filosofo.comiendo else 'Pensando'
            print(f'  {filosofo.nombre}: {estado}')

    # Invertir colores (Verde = Comiendo, Rojo = Pensando)
    colores = ['green' if estado else 'red' for estado in estados]

    # Visualizar la simulación con matplotlib
    plt.figure(figsize=(10, 5))
    plt.scatter(tiempos, nombres * 10, c=colores, marker='o', s=50)
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Filósofo')
    plt.title('Simulación de los Filósofos (Verde = Comiendo, Rojo = Pensando)')
    plt.yticks(nombres)
    plt.xlim(0, 10)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

sinThreads()


#  null) Task + Pres
print("                                                                                  ")
print("**********************************************************************************")
print("*               SEMINARIO DE PROGRAMACION - 2023 - TP FILÓSOFOS COMENSALES            *")
print("**********************************************************************************")
print("    ALUMNOS:                                                                      ")
print("            • Bardales, Wilfredo                                                  ")
print("            • Martin, Denise                                                      ")
print("            • Paleari, Carolina                                                   ")
print("                                                                                  ")
print("**********************************************************************************")
print("*                                   OBJETIVO                                     *")
print("**********************************************************************************")
print(" Entendimiento de funcionamiento y errores producidos en casos de Filósofos Comensales.")
print("                                                                                  ")
print("**********************************************************************************")
print("*                                   CONSIGNAS                                    *")
print("**********************************************************************************")
print("                                                                                  ")

consigna = """Se pide construir una red de Petri que modele el problema de los filósofos \n
comensales, en este caso, para 5 filósofos, respetando todo lo requerido: \n
cada uno de los 5 tenedores es compartido por dos de los comensales sentados\n
en forma consecutiva, y cada uno de los filósofos necesita usar ambos \n
tenedores para poder comer.\n

En esta red, deberá existir alguna secuencia de disparos que vaya haciendo \n
pensar y comer a todos los filósofos en forma permanente (no se pide que \n
cualquier secuencia de disparos posible cumpla esto.)\n

Sugerencia: determinados lugares representarán los estados de los distintos\n
filósofos y/o de los recursos disponibles.\n

Tener presente que esta solución será distinta e independiente de las vistas \n
anteriormente (es decir la del lugar disponible y la del filósofo "zurdo").\n

Luego, contestar justificando si la red de Petri construida es acotada, \n
si es L1, si es L3 y si es persistente.\n"""
print(consigna)


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
teoria = """                      ********* EXCLUSIÓN MUTUA *********                         \n
es una situación en la que dos o más procesos no pueden continuar porque cada uno está \n
esperando que el otro libere un recurso. Esto puede provocar una parada o un \n
estancamiento del sistema, ya que no se puede avanzar. \n

             ********* ALGORITMO FILÓSOFOS COMENSALES *********               \n
El Problema de los Filósofos Comensales ilustra el concepto de deadlock. \n
En el mismo participan cinco filósofos sentados en una mesa redonda, con un \n
tenedor entre cada filósofo. Un filósofo debe tener ambos tenedores para comer, \n
pero sólo puede usar un tenedor a la vez. Los filósofos están tan absortos en\n
sus pensamientos filosóficos que se olvidan de tomar el otro tenedor. Esto lleva\n
a una situación en la que todos los filósofos esperan que su vecino deje el tenedor,\n
lo que resulta en un deadlock. \n
Para resolver el problema de deadlock, se pueden utilizar varios métodos:\ 
  ◘ Prevención: Esto implica establecer reglas que eviten que se produzca deadlock.\n
    Por ejemplo, en el problema del filósofo, esto podría implicar una regla según la \n
    cual un filósofo sólo puede tomar un tenedor si el otro está disponible.\n
  ◘ Detección y recuperación: esto implica detectar cuándo se ha producido deadlock\n
    y luego recuperarse del mismo. Esto podría implicar finalizar uno de los \n
    procesos o retroceder a un estado anterior.\n
  ◘ Evitar deadlock: esto implica el uso de algoritmos para garantizar que el \n
    sistema nunca entre en un estado de deadlock. Un ejemplo de esto es el \n
    algoritmo del banquero, que determina la cantidad máxima de recursos que \n
    se pueden asignar a cada filósofo sin causar deadlock.\n
"""

print(teoria)
 
    
# III)  Conclusions
print("                                                                                  ")
print("**********************************************************************************")
print("*                                CONCLUSIONES                                    *")
print("**********************************************************************************")
conclusiones = """
Si bien el problema de los filósofos comensales se utiliza como teoría para demostrar \n
el problema de exclusión mutua: deadlock, en sistemas operativos. Se puede reproducir \n
el esquema en este código, produciendo un algortimo capaz de ser impreso para demostrar \n
la posibilidad de al menos una secuencia capaz de evitar deadlock. \n

El código aquí se divide en dos partes principales: threads() y sinThreads().\n
  ◘ En la función threads(), el problema se resuelve: creando cinco hilos, \n
    cada uno de los cuales representa a un filósofo. A cada filósofo se le asigna una \n
    bifurcación única, y cada bifurcación está representada por threading.Lock. Cuando un\n
    filósofo quiere comer, debe adquirir ambos tenedores. Si no pueden, sueltan el \n
    tenedor que tienen y esperan para volver a intentarlo.\n
  ◘ En la función sinThreads(), el problema se resuelve: definiendo una clase Filósofo\n
    para representar a cada filósofo. Cada uno tiene un método filosófico que representa\n
    las acciones del filósofo. El método filosófico es un generador que simula al filósofo\n
    pensar, comer y esperar el tenedor. Las bifurcaciones están representadas por simpy.Resource\n
    que gestiona la disponibilidad de las bifurcaciones.\n

Se crea tambipen, un diagrama de dispersión para mostrar las acciones de los \n
filósofos a lo largo del tiempo. Cada filósofo está representado por un punto de la\n
trama. El color del punto indica si el filósofo está comiendo (verde) o pensando (rojo).\n
"""
print(conclusiones)