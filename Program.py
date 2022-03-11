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


