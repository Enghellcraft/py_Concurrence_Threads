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

consigna = """Se pide construir una red de Petri que modele el problema de los filósofos comensales, en este caso, para 5 filósofos, respetando todo lo requerido: cada uno de los 5 tenedores es compartido por dos de los comensales sentados en forma consecutiva, y cada uno de los filósofos necesita usar ambos tenedores para poder comer.

En esta red, deberá existir alguna secuencia de disparos que vaya haciendo pensar y comer a todos los filósofos en forma permanente. (No se pide que cualquier secuencia de disparos posible cumpla esto.)

Sugerencia: determinados lugares representarán los estados de los distintos filósofos y/o de los recursos disponibles.

Tener presente que esta solución será distinta e independiente de las vistas anteriormente (es decir la del lugar disponible y la del filósofo "zurdo").

Luego, contestar justificando si la red de Petri construida es acotada, si es L1, si es L3 y si es persistente."""
print(consigna)


#  I) Theory
print("                                                                                  ")
print("**********************************************************************************")
print("*                                      TEORIA                                    *")
print("**********************************************************************************")
print("                                                                                  ")
    
# III)  Conclusions
print("                                                                                  ")
print("**********************************************************************************")
print("*                                CONCLUSIONES                                    *")
print("**********************************************************************************")
