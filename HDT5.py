import simpy
import random

""" Programa para simulación de uso de CPU, por Roberto Nájera """

randomSeed = 1 # Common seed for random generation
processes = 25 # Total processes
EXP = 10 # parameter for exponential growth
CPUinst = 3
MINmem = 1
MAXmem = 10
MINinst = 1
MAXinst = 10

def main():
    random.seed(randomSeed)
    env = simpy.Environment()
    
    
    RAM = simpy.Container(env, 100, 100)
    env.process(CPU(env, RAM))
    env.run()
    


def CPU(env, RAM):
    for i in range(processes):
        m = random.uniform(MINmem, MAXmem)
        inst = random.uniform(MINinst, MAXinst)
        RAM.get(m)
        p = execute(str(i), env, RAM, m, inst)
        env.process(p)
        yield env.timeout(random.expovariate(1.0/EXP))

def execute(name, env, RAM, memory, instructions):
    
    yield env.timeout(1)
    
    
    

