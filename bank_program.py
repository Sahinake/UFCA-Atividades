# Primeiro importamos os módulos necessários:
#   threading: para trabalhar com threads.
#   random: para gerar números aleatórios.
#   time: para controlar o tempo.

import threading
import random
import time

# Criamos uma variável para controlar o acesso aos caixas. Definimos 3 como contagem inicial, pois apenas três threads de clientes podem acessar os caixas ao mesmo tempo.
semaphore_box = threading.Semaphore(3)

# Criamos uma lista vazia, representando a fila de espera de clientes.
queue = []

# Definimos uma função "customers" que será executada por cada thread de clientes. O argumento "arrival_number" representa o número do cliente
def customers(arrival_number):
    global queue

    # Seção crítica.
    semaphore_box.acquire()
    print(f"Cliente de número {arrival_number} está sendo atendido em um dos caixas.\n")

    # Criamos uma variável "service_time" que representa o tempo de atendimento e recebe um inteiro aleatório entre 3 e 10.
    service_time = random.randint(3, 10)
    # Em seguida, fazemos a thread esperar, simulando o atendimento.
    time.sleep(service_time)
    print(f"Cliente de número {arrival_number} terminou o atendimento em {service_time} segundos.")
    semaphore_box.release()
    
# Definimos uma função "generate_customers" que será executada para gerar clientes.
def generate_customers():
    # Como a fila deve ter um número fixo de 30 clientes em espera, criamos um for de tamanho 31.
    for i in range(1,31):
        queue.append(i)
        print(f"Cliente {i} chegou e entrou na fila de espera.")
        # Aleatorizamos um tempo entre 1 e 3, e fazemos a thread esperar.
        time.sleep(random.randint(1, 3))


# Inicializamos a thread "thread_generator" para gerar clientes
thread_generator = threading.Thread(target=generate_customers)
thread_generator.start()

# Inicializamos uma lista vazia "threads_queue" para armazenar as threads dos clientes que estão sendo atendidos.
threads_queue = []

while True:
    # Se fila de espera não estiver vazia, pegamos o próximo cliente (o primeiro da lista) usando pop(0).
    if queue:
        current_customer = queue.pop(0)

        # Criamos uma nova thread "customer_thread" para atender o cliente atual e a adicionamos à lista "threads_queue".
        customer_thread = threading.Thread(target=customers, args=(current_customer,))
        threads_queue.append(customer_thread)
        customer_thread.start()

    # Se o "thread_generator" não estiver mais ativo e se não há mais threads de clientes ativos, saímos do loop infinito.
    if not thread_generator.is_alive() and not threads_queue:
        break

# Aguardamos todas as threads de atendimento terminarem
for thread in threads_queue:
    thread.join()

print("Todos os clientes foram atendidos!.")
