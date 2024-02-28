import simpy
import random
import statistics

"Programa para simulaciones de CPU, por Roberto Nájera"

randomSeed = 42 # Common seed for random generation
processes = 200 # Total processes
interval = 1 # parameter for exponential growth
CPUinst = 3 # Instructions that the CPU can do per time step
processors = 2 # number of available CPUs
RAMsize = 100
MINmem = 1
MAXmem = 10
MINinst = 1
MAXinst = 10

random.seed(randomSeed)
env = simpy.Environment()
ram = simpy.Container(env, RAMsize, RAMsize)
CPUs = simpy.Resource(env, processors)
times = []

def generatePrograms(env):
    for i in range(processes):
            print(str(env.now) + " New program " + str(i))
            env.process(computeProgram(env, i, 0))
            yield env.timeout(random.expovariate(1.0/interval))


def computeProgram(env, i, n, m = random.randint(MINmem, MAXmem), inst = random.randint(MINinst, MAXinst), time = None):
    time = env.now
    t = env.now
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
        env.process(computeProgram(env, i, decition, m, inst, t))
    else:
        yield ram.put(m)
        print(str(env.now) + " Program " + str(i) + " terminated")
        times.append(env.now - time)
        #print(env.now - time)
    
    
    

env.process(generatePrograms(env))

env.run()
# Estadísticas
print("mean: " + str(statistics.mean(times)) + " stdev: " + str(statistics.stdev(times)))
