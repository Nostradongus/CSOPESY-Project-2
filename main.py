"""
CSOPESY Project 2 - Synchronization Problems

S13 Group 2
- LOPEZ, Angel
- JADIE, Joshue Salvador

Last Updated: 06/02/22
"""
# for threads implementation 
from threading import *

# for simulating process work in critical section
from time import sleep

def execute_blue(process_id):
    # get global process synchronization variables
    global blue_mutex, green_mutex, slots, blue_access
    global limit, b, g
    
    # get access lock to fitting room, decreasing number of accesses
    # for this color
    blue_access.acquire()
    
    # if green threads have claimed the fitting room, wait until
    # lock is released
    while green_mutex.locked():
        pass

    # if fitting is currently not claimed by both blue and green threads
    if blue_mutex.locked() == False and green_mutex.locked() == False:
        # let blue threads claim the fitting room
        blue_mutex.acquire()
            
        # blue thread is the first to enter the fitting room as having acquired
        # the lock
        print("Blue only.")
        
    # check if there are available slots in the fitting room
    slots.acquire()
    
    # print blue thread's information
    print("{0} Blue".format(process_id))
    
    # simulate work in critical section
    sleep(0.5)
    
    # blue thread is done with its work, increase number of blue threads executed
    global blue_executed
    blue_executed += 1
    
    # release slot
    slots.release()
    
    # get updated number of executed green threads
    global green_executed
    
    # if blue thread is the last in the fitting room, give access to the other color
    if blue_executed == b or (blue_executed % limit == 0 and green_executed != g):
        # fitting room is currently empty
        print("Empty fitting room.")
        
        # release color lock, only if there are remaining green threads to be executed
        if green_executed != g:
            blue_mutex.release()
        
    # wait until green threads have acquired the color lock, if all green threads
    # have not yet been executed
    while green_mutex.locked() == False and green_executed != g: 
        pass
    
    # release access lock
    blue_access.release()

def execute_green(process_id):
    # get global process synchronization variables
    global blue_mutex, green_mutex, slots, green_access
    global limit, b, g
    
    # get access lock to fitting room, decrease number of accesses
    # for this color
    green_access.acquire()
    
    # if blue threads have claimed the fitting room, wait until 
    # lock is released
    while blue_mutex.locked():
        pass
    
    # if fitting room is currently not claimed by both green and blue threads
    if green_mutex.locked() == False and blue_mutex.locked() == False:
        # let green threads claim the fitting room
        green_mutex.acquire()
        
        # green thread is the first to enter the fitting room as having acquired
        # the lock 
        print("Green only.")
        
    # check if there are available slots in the fitting room
    slots.acquire()
    
    # print green thread's information 
    print("{0} Green".format(process_id))
    
    # simulate work in critical section
    sleep(0.5)
    
    # green thread is done with its work, decrease current number of threads to be executed
    global green_executed
    green_executed += 1
    
    # release slot
    slots.release()
    
    # get updated number of executed blue threads
    global blue_executed
    
    # if green thread is the last in the fitting room, give access to the other color
    if green_executed == g or (green_executed % limit == 0 and blue_executed != b):
        # fitting room is currently empty
        print("Empty fitting room.")
        
        # release color lock, only if there are remaining blue threads to be executed
        if blue_executed != b:
            green_mutex.release()
    
    # wait until blue threads have acquired the color lock, if all blue threads
    # have not yet been executed
    while blue_mutex.locked() == False and blue_executed != b:
        pass
    
    # release access lock
    green_access.release()

# get number of fitting room slots (n), blue threads (b), and green
# threads (g)
n, b, g = map(int, input("Input values: ").split())
    
# initialize global process synchronization variables
blue_mutex = Lock()                    # to allow only blue threads to access the fitting room
green_mutex = Lock()                   # to allow only green threads to access the fitting room
slots = BoundedSemaphore(n)            # counting semaphore for fitting room slots, with value == number of fitting room slots
limit = n + 5                          # for fitting room access limit, to avoid starvation in other color
blue_access = BoundedSemaphore(limit)  # counting semaphore for fitting room access limit to blue threads
green_access = BoundedSemaphore(limit) # counting semaphore for fitting room access limit to green threads
blue_executed = 0                      # number of blue processes executed
green_executed = 0                     # number of green processes executed
    
# initialize and execute blue processes
for i in range(1, b+1):
    Thread(target = execute_blue, args = (i,)).start() 
    
# initialize and execute green processes
for i in range(1, g+1):
    Thread(target = execute_green, args = (i,)).start()
