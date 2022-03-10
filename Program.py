import random
import simpy

class Sistem:
    def __init__(self, env):
        self.cpu = simpy.Resource(env, number=1)
        self.ram = simpy.Container(env, init=100, capacity=100)
        self.mon_proc = env.process(self.monitor_tank(env))




