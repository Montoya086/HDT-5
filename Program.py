import random
import simpy

PROCESS_NUMBER = 25
RANDOM_SEED = 30
CPU_CORES = 1
INTERVAL = 10
CAPACITY = 100
class Proceso:
    def new():
    def ready():
    def waiting():
    def running():
    def terminated():
class memory:
    def __init__(self, env, cpu_cores, cap):
        self.cpu = simpy.Resource(env, capacity=cpu_cores)
        self.ram = simpy.Container(env, init=cap, capacity =cap)


env = simpy.Environment()
sis = Sistema(env)
env.run()

