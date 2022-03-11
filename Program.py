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
        with cpu.request() as req:
            yield req
            yield env.timeout(1)
            print("**************************STATE: RUNNING**************************************")
            print(f'PROCESO {id} EJECUTANDOSE, Tiempo: {env.now}            ')
            print("******************************************************************************")
            print()
            actions-=3            
        if(actions<=0):
            with cpu.request() as req:
                yield req
                yield env.timeout(1)
                ram_memory.put(memory_needed)
                process_terminated = True
                print("**************************STATE: TERMINATED***********************************")
                print(f'PROCESO {id} TERMINATED, Tiempo: {env.now}            ')
                print("******************************************************************************")
                print()
                finish_time=env.now
                global tiempo_ejecucion 
                tiempo_ejecucion += finish_time-start_time
        else:
            r = random.randint(1,2)
            if(r==1):
                with cpu.request() as req:
                    yield req
                    yield env.timeout(1)
                    ram_memory.put(memory_needed)
                    print("**************************STATE: WAITING**************************************")
                    print(f'PROCESO {id} EN ESPERA, numero de acciones: {actions} Tiempo: {env.now}')
                    print("******************************************************************************")
                    print()
            else:
                ram_memory.put(memory_needed)
                            
random.seed(RANDOM_SEED)
env = simpy.Environment()
cpu = simpy.Resource(env, capacity=CPU_CORES)
ram_memory = simpy.Container(env, init=CAPACITY, capacity =CAPACITY)
env.process(process_creator(env, cpu,ram_memory))
env.run()
prom = tiempo_ejecucion/PROCESS_NUMBER
print(f"promedio de ejecucion: {prom}")