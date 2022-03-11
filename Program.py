import random
import simpy
#/***************************************************
#PARAMETROS
PROCESS_NUMBER = 25
RANDOM_SEED = 30
CPU_CORES = 1
INTERVAL = 10
CAPACITY = 20
#***************************************************/

def program_process(env, process_system, id):
    env=env
    name = id
    process_system = process_system
    memory = random.randint(1,10)
    env.process(state_new(process_system, id, memory, env))

def state_new(process_system, id, memory, env):
    memory_needed = random.randint(1,10)
    print("**************************STATE: NEW**************************************")
    print(f'PROCESO {id} INICIADO, memoria utilizada: {memory_needed} Tiempo: {env.now}')
    print("**************************************************************************")
    print()
    with process_system.cpu.request() as req:
        yield req
        yield process_system.ram_memory.get(memory)
        state_ready(process_system, id, memory, env, 0)

def state_ready(process_system, id, memory, env, actions):
    if(actions ==0):
        actions = random.randint(1,10) 
    print("**************************STATE: READY**************************************")
    print(f'PROCESO {id} LISTO PARA EJECUCION, numero de acciones: {actions} Tiempo: {env.now}')
    print("****************************************************************************")
    print()
    state_running(process_system, id, memory, env, actions)

def state_running(process_system, id, memory, env, actions):
    print("**************************STATE: RUNNING**************************************")
    print(f'               PROCESO {id} EJECUTANDOSE, Tiempo: {env.now}            ')
    print("******************************************************************************")
    print()
    actions-=3
    if(actions<=0):
        state_terminated(id, env)
        process_system.ram_memory.put(memory)
    else:
        r = random.randint(1,2)
        if(r==1):
            state_waiting(process_system, id, memory, env, actions)
            process_system.ram_memory.put(memory)
        else:
            process_system.ram_memory.put(memory)
            with process_system.cpu.request() as req:
                req
                process_system.ram_memory.get(memory)
                state_ready(process_system, id, memory, env, actions)
        
def state_terminated(id, env):
    print("**************************STATE: TERMINATED***********************************")
    print(f'               PROCESO {id} TERMINATED, Tiempo: {env.now}            ')
    print("******************************************************************************")
    print()

def state_waiting(process_system, id, memory, env, actions):
    print("**************************STATE: WAITING**************************************")
    print(f'PROCESO {id} EN ESPERA, numero de acciones: {actions} Tiempo: {env.now}')
    print("******************************************************************************")
    print()
    with process_system.cpu.request() as req:
        req
        process_system.ram_memory.get(memory)
        state_ready(process_system, id, memory, env, actions)
        
class system():
    def __init__(self, env):
        self.cpu = simpy.Resource(env, capacity=CPU_CORES)
        self.ram_memory = simpy.Container(env, init=CAPACITY, capacity =CAPACITY)


def process_creator(env, process_system):
    for j in range (PROCESS_NUMBER):
        program_process(env, process_system, j)
        process_delay = random.expovariate(1.0/INTERVAL)
        yield env.timeout(process_delay)

random.seed(RANDOM_SEED)
env = simpy.Environment()
process_system = system(env)
env.process(process_creator(env, process_system))
env.run()


