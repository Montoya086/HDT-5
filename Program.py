#/***************************************************
#Autor: Andrés Estuardo Montoya Wilhelm
#Fecha de creación: 9/03/2022
#Ultima modificación: 11/03/2022
#***************************************************/
import random
import simpy
import statistics
#/***************************************************
#PARAMETROS
PROCESS_NUMBER = 100
RANDOM_SEED = 314159265359
CPU_CORES = 6
INTERVAL = 5
CAPACITY = 200
#***************************************************/

#/***************************************************
#VARIABLES GLOBALES
tiempo_ejecucion=0
tiempos = []
#***************************************************/
def process_creator(env, cpu,ram):
    for i in range (PROCESS_NUMBER):
        pp=program_process(env, i, cpu, ram)
        env.process(pp)
        process_delay = random.expovariate(1.0/INTERVAL)
        yield env.timeout(process_delay)

def program_process( env, id, cpu, ram):
    #estado de creación del proceso
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
    while process_terminated==False:#mientras el proceso no haya terminado, repetira el ciclo hasta acabar con sus acciones
        with cpu.request() as req:
            yield req
            yield env.timeout(1)
            yield ram.get(memory_needed)#revision y uso de memoria
            print("**************************STATE: READY**************************************")
            print(f'PROCESO {id} LISTO PARA EJECUCION, numero de acciones: {actions} Tiempo: {env.now}')
            print("****************************************************************************")
            print()
        with cpu.request() as req:#transferencia a estado running
            yield req
            yield env.timeout(1)
            print("**************************STATE: RUNNING**************************************")
            print(f'PROCESO {id} EJECUTANDOSE, Tiempo: {env.now}            ')
            print("******************************************************************************")
            print()
            actions-=3            
        if(actions<=0):#si el proceso ya no tiene mas acciones, pasara a terminated y acabará el ciclo
            with cpu.request() as req:
                yield req
                yield env.timeout(1)
                ram_memory.put(memory_needed)#devuelve la memoria usada
                process_terminated = True #fin del ciclo
                print("**************************STATE: TERMINATED***********************************")
                print(f'PROCESO {id} TERMINATED, Tiempo: {env.now}            ')
                print("******************************************************************************")
                print()
                finish_time=env.now
                #guardado de datos para estadisticos
                global tiempo_ejecucion
                global tiempos
                tiempo_ejecucion += finish_time-start_time
                tiempos.append(finish_time-start_time)
        else:#si el proceso sigue teniendo más acciones
            r = random.randint(1,2)#genera un numero al azar para mandarlo a waiting o al inicio
            if(r==1):#estado Waiting
                with cpu.request() as req:
                    yield req
                    yield env.timeout(1)
                    ram_memory.put(memory_needed)#devuelve la memoria usada
                    print("**************************STATE: WAITING**************************************")
                    print(f'PROCESO {id} EN ESPERA, numero de acciones: {actions} Tiempo: {env.now}')
                    print("******************************************************************************")
                    print()#regresa al inicio del ciclo para entrar en ready si hay memoria disponible
            else:
                ram_memory.put(memory_needed)#devuelve la memoria usada
                #regresa al inicio del ciclo para entrar en ready si hay memoria disponible
#inicialización de la simulación                      
random.seed(RANDOM_SEED)
env = simpy.Environment()
cpu = simpy.Resource(env, capacity=CPU_CORES)
ram_memory = simpy.Container(env, init=CAPACITY, capacity =CAPACITY)
env.process(process_creator(env, cpu,ram_memory))
env.run()
#Calculo de estadisticos
prom = tiempo_ejecucion/PROCESS_NUMBER
desvest = statistics.stdev(tiempos)
print(f"Tiempo promedio de ejecucion: {prom}")
print(f"Desviación estandar tiempo de ejecucion: {desvest}")