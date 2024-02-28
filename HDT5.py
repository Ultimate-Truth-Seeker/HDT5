import simpy
import random

randomSeed = 10 # Common seed for random generation
processes = 100 # Total processes
EXP = 1 # parameter for exponential growth
CPUinst = 3
processors = 1
MINmem = 1
MAXmem = 10
MINinst = 1
MAXinst = 10

env = simpy.Environment()
ram = simpy.Container(env, 100, 100)
CPUs = simpy.Resource(env, processors)

def generatePrograms(env):
    for i in range(processes):
            print(str(env.now) + " New program " + str(i))
            env.process(computeProgram(env, i, 0))
            yield env.timeout(random.expovariate(1.0/EXP))
    print(env.now)


def computeProgram(env, i, n, m = random.randint(MINmem, MAXmem), inst = random.randint(MINinst, MAXinst)):
    if n == 0:
        print(str(env.now) + " Program " + str(i) + " requesting for memory: " + str(m))
        yield ram.get(m)
    elif n == 1:
        print(str(env.now) + " Program " + str(i) + " waiting doing I/O")
        yield env.timeout(random.randint(1, 10)) # Simula operaciones de entrada y salida

    print(str(env.now) + " Program " + str(i) + " ready")
    req = CPUs.request()
    yield req
    print(str(env.now) + " Program " + str(i) + " running inst: " + str(inst))
    inst -= CPUinst
    yield env.timeout(1)
    CPUs.release(req)
    if inst > 0:
        decition = random.randint(1, 2)
        env.process(computeProgram(env, i, decition, m, inst))
    else:
        yield ram.put(m)
        print(str(env.now) + " Program " + str(i) + " terminated")
    
    
    

env.process(generatePrograms(env))


env.run()
