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
      def __init__(self, env, nombre, tenedor_izq, tenedor_der):
          self.env = env
          self.nombre = nombre
          self.tenedor_izq = tenedor_izq
          self.tenedor_der = tenedor_der
          self.comiendo = False
          env.process(self.filosofar())

      def filosofar(self):
          while True:
              print(f'{self.nombre} está pensando.')
              yield self.env.timeout(random.randint(1, 5))  # El filósofo piensa durante un tiempo aleatorio
              print(f'{self.nombre} tiene hambre.')
              yield self.env.process(self.comer())

      def comer(self):
          with self.tenedor_izq.request() as tenedor_izq_req:
              yield tenedor_izq_req
              with self.tenedor_der.request() as tenedor_der_req:
                  yield tenedor_der_req
                  print(f'{self.nombre} está comiendo.')
                  self.comiendo = True
                  yield self.env.timeout(random.randint(1, 5))  # El filósofo come durante un tiempo aleatorio
                  self.comiendo = False
                  print(f'{self.nombre} ha terminado de comer y vuelve a pensar.')

  # Crear un entorno de simulación
  env = simpy.Environment()

  # Crear tenedores como recursos compartidos
  tenedores = [simpy.Resource(env) for _ in range(5)]

  # Crear filósofos
  filosofos = [Filosofo(env, f'Filósofo {i}', tenedores[i], tenedores[(i + 1) % 5]) for i in range(5)]

  # Iniciar la simulación
  env.run(until=20)  # Simular durante 20 unidades de tiempo


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

# threads()
sinThreads()