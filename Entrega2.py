"""
Created on Thu Mar 23 19:39:43 2023

@author: Alvaro Ezquerro

Entrega 2: Puente de Ambite
"""
from time import sleep
from random import normalvariate, randint
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 2
NPED = 2
TIME_CARS_NORTH = 0.5  # a new car enters each 0.5s
TIME_CARS_SOUTH = 0.5  # a new car enters each 0.5s
TIME_PED = 5 # a new pedestrian enters each 5s
TIME_IN_BRIDGE_CARS = (5, 1) # normal 1s, 0.5s
TIME_IN_BRIDGE_PEDESTRIAN = (30, 10) # normal 30s, 10s

'''
Monitor

In general, when whether a car or a pedestrians leave the bridge the
priority goes like this:
    Cars-> Randomly choses Cars or Pedestrians
    Pedestrians->Cars.

The pedestrians cross the bridge all at once, so there is no need of
adding self.PedestrianCross.notify_all() at the end of leaves_pedestrian.

The cars and pedestrians prints are comented so we can see better how
is the bridge status.
'''
class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.north = Value('i', 0) #Cars goin north on the bridge
        self.south = Value('i', 0) #Cars goin south on the bridge
        self.pedestrians = Value('i', 0) #Pedestrians on the bridge
        self.CarCross=Condition(self.mutex)
        self.PedestrianCross=Condition(self.mutex)
        #self.cond.wait_for(predicate of a bool fun) -> WaitC
        #self.cond.notify() -> SignalC
    
    def can_north(self) -> bool:
        return self.south.value==0 and self.pedestrians.value==0
        
    def can_south(self) -> bool:
        return self.north.value==0 and self.pedestrians.value==0
    
    def can_pedestrian(self) -> bool:
        return self.south.value==0 and self.north.value==0
    
    def nobody(self) -> bool:
        return self.pedestrians==0 and self.south==0 and self.north==0
    
    def wants_enter_car(self, direction: int) -> None:
        self.mutex.acquire()
        if direction==NORTH:
            self.CarCross.wait_for(self.can_north)
            self.north.value += 1
        else:
            self.CarCross.wait_for(self.can_south)
            self.south.value += 1
        self.mutex.release()

    def leaves_car(self, direction: int) -> None:
        self.mutex.acquire() 
        if direction==NORTH:
            self.north.value -= 1
        else:
            self.south.value -= 1
        who_calls_first=randint(0,1)
        if who_calls_first==1:
            self.PedestrianCross.notify_all()
            self.CarCross.notify_all()
        else:
            self.PedestrianCross.notify_all()
            self.CarCross.notify_all()
        self.mutex.release()

    def wants_enter_pedestrian(self) -> None:
        self.mutex.acquire()
        self.PedestrianCross.wait_for(self.can_pedestrian)
        self.pedestrians.value += 1
        self.mutex.release()

    def leaves_pedestrian(self) -> None:
        self.mutex.acquire()
        self.pedestrians.value -= 1
        self.CarCross.notify_all()
        self.mutex.release()
        
    def __repr__(self) -> str:
        return f'Monitor:\n Cars: -> {self.north.value}, <- {self.south.value}\n Pedestrians: {self.pedestrians.value}'

'''
Delay for crossing the bridge
'''

def delay_car_north() -> None:
    delay=normalvariate(TIME_IN_BRIDGE_CARS[0],TIME_IN_BRIDGE_CARS[1])
    delay=abs(delay)
    sleep(delay)

def delay_car_south() -> None:
    delay=normalvariate(TIME_IN_BRIDGE_CARS[0],TIME_IN_BRIDGE_CARS[1])
    delay=abs(delay)
    sleep(delay)

def delay_pedestrian() -> None:
    delay=normalvariate(TIME_IN_BRIDGE_PEDESTRIAN[0],TIME_IN_BRIDGE_PEDESTRIAN[1])
    delay=abs(delay)
    sleep(delay)


'''
Car and pedestrian
'''
def car(cid: int, direction: int, monitor: Monitor)  -> None:
    #print(f"car {cid} heading {direction} wants to enter.", flush=True)
    monitor.wants_enter_car(direction)
    #print(f"car {cid} heading {direction} enters the bridge.", flush=True)
    print(monitor, flush=True)
    if direction==NORTH :
        delay_car_north()
    else:
        delay_car_south()
    #print(f"car {cid} heading {direction} leaving the bridge.", flush=True)
    monitor.leaves_car(direction)
    print(monitor, flush=True)
    #print(f"car {cid} heading {direction} out of the bridge.\n{monitor}", flush=True)

def pedestrian(pid: int, monitor: Monitor) -> None:
    #print(f"pedestrian {pid} wants to enter.", flush=True)
    monitor.wants_enter_pedestrian()
    #print(f"pedestrian {pid} enters the bridge.\n{monitor}", flush=True)
    print(monitor, flush=True)
    delay_pedestrian()
    #print(f"pedestrian {pid} leaving the bridge.", flush=True)
    monitor.leaves_pedestrian()
    print(monitor, flush=True)
    #print(f"pedestrian {pid} out of the bridge.\n{monitor}", flush=True)


'''
Car and pedestrian generators
'''
def gen_pedestrian(monitor: Monitor) -> None:
    pid = 0
    plst = []
    for _ in range(NPED):
        pid += 1
        p = Process(target=pedestrian, args=(pid, monitor))
        p.start()
        plst.append(p)
        sleep(TIME_PED)

    for p in plst:
        p.join()

def gen_cars(direction: int, time_cars, monitor: Monitor) -> None:
    cid = 0
    plst = []
    for _ in range(NCARS):
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        plst.append(p)
        sleep(time_cars)

    for p in plst:
        p.join()



def main():
    monitor = Monitor()
    gcars_north = Process(target=gen_cars, args=(NORTH, TIME_CARS_NORTH, monitor))
    gcars_south = Process(target=gen_cars, args=(SOUTH, TIME_CARS_SOUTH, monitor))
    gped = Process(target=gen_pedestrian, args=(monitor,))
    gcars_north.start()
    gcars_south.start()
    gped.start()
    gcars_north.join()
    gcars_south.join()
    gped.join()


if __name__ == '__main__':
    main()
    print('FIN')
    
