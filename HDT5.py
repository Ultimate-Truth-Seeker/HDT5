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
    
    
    cpu = CPU(env)
   # env.process(cpu.processCPU(env))
    env.run()
    
class task:
    def __init__(self, i, env):
        self.name = "Process" + str(i)
        self.m = random.randint(MINmem, MAXmem)
        self.inst = random.randint(MINinst, MAXinst)
        print("New " + self.name + " at " + str(env.now) + ", memory: " + str(self.m) + ", inst: " +str(self.inst))

    def add(self, env, RAM, waiting, ready):
        if RAM.level < self.m:
            waiting.append(self)
            print(self.name + " added to waiting stack at " + str(env.now))
        else:
            RAM.get(self.m)
            ready.append(self)
            print(self.name + " added to ready stack at " + str(env.now))
            

class CPU:
    def __init__(self, env):
        self.RAM = simpy.Container(env, 100, 100)
        self.waiting = []
        self.ready = []
        self.tasking = env.process(self.genTasks(env))
        

    def genTasks(self, env):
        for i in range(processes):
            p = task(i, env)
            p.add(env, self.RAM, self.waiting, self.ready)
            env.process(self.processCPU(env))
            yield env.timeout(random.expovariate(1.0/EXP))
            

    def processCPU(self, env):
        
            while len(self.ready) > 0:
                p = self.ready.pop()
                self.RAM.put(p.m)
                p.inst -= 3
                yield env.timeout(1)
                if p.inst > 0:
                    x = random.randint(1, 2)
                    if x == 1:
                        print(p.name + " added to waiting stack at " + str(env.now))
                        self.waiting.append(p)
                    elif x == 2:
                        print(p.name + " readded to ready at " + str(env.now))
                        self.ready.append(p)
                        self.RAM.get(p.m)
                else:
                    print(p.name + " ended at " + str(env.now))
                if len(self.waiting) != 0:
                    while self.waiting[len(self.waiting) - 1].m <= self.RAM.level:
                        self.RAM.get(self.waiting[len(self.waiting) - 1].m)
                        self.ready.append(self.waiting.pop())
                        print(self.ready[len(self.ready) - 1].name + " added to ready stack at " + str(env.now))
                        if len(self.waiting) == 0:
                            break
                
            
                
            
            
    



main()
    
    

