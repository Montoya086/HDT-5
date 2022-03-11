import random
import simpy
import statistics
#/***************************************************
#PARAMETROS
PROCESS_NUMBER = 10
RANDOM_SEED = 314159265359
CPU_CORES = 1
INTERVAL = 10
CAPACITY = 100
#***************************************************/
tiempo_ejecucion=0

def process_creator(env, cpu,ram):
    for i in range (PROCESS_NUMBER):
        pp=program_process(env, i, cpu, ram)
        env.process(pp)
        process_delay = random.expovariate(1.0/INTERVAL)
        yield env.timeout(process_delay)

def program_process( env, id, cpu, ram):
    start_time=0.0
    finish_time=0.0
    process_terminated = False
    memory_needed = random.randint(1,10)
    actions = random.randint(1,10) 
    print("**************************STATE: NEW**************************************")
    print(f'PROCESO {id} INICIADO, memoria utilizada: {memory_needed} Tiempo: {env.now}')
    print("**************************************************************************")
    print()
    start_time=env.now
    while process_terminated==False:
        with cpu.request() as req:
            yield req
            yield env.timeout(1)
            yield ram.get(memory_needed)
            print("**************************STATE: READY**************************************")
            print(f'PROCESO {id} LISTO PARA EJECUCION, numero de acciones: {actions} Tiempo: {env.now}')
            print("****************************************************************************")
            print()
