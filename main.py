"""
CSOPESY Project 2 - Synchronization Problems

S13 Group 2
- LOPEZ, Angel
- JADIE, Joshue Salvador

Last Updated: 06/11/22
"""
# for threads implementation 
from threading import * 

# for simulating process work in critical section
from time import sleep

def execute_blue():
    # get global process synchronization variables
    global blue_mutex, green_mutex, slots, blue_limit, green_limit
    global limit, b, g
    
    # get access lock to fitting room, decreasing number of accesses
    # for this color
    blue_limit.acquire()
    
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
        
    # get a slot in the fitting room, wait if no slot is available yet
    slots.acquire()
    
    # print blue thread's information
    print(current_thread().name)
    
    # simulate work in critical section
    sleep(1)
    
    # blue thread is done with its work, increase number of blue threads executed
    global blue_executed
    blue_executed += 1
    
    # release slot
    slots.release()
    
    # get updated number of executed green threads
    global green_executed
    
    # if blue thread is the last in the fitting room, give access lock to green threads
    if blue_executed == b or (blue_executed % limit == 0 and green_executed != g):
        # fitting room is currently empty
        print("Empty fitting room.")
        
        # if there are remaining green threads to be executed, give access lock to green threads
        if green_executed != g:
            # signal "limit" green threads so that they can access the fitting room
            for i in range(limit):
                green_limit.release()
            
            # release access lock 
            blue_mutex.release()
    # else if all green threads have already been executed, no more access limit for blue threads
    elif green_executed == g:
        blue_limit.release()

def execute_green():
    # get global process synchronization variables
    global blue_mutex, green_mutex, slots, green_limit, blue_limit
    global limit, b, g
    
    # get access lock to fitting room, decrease number of accesses
    # for this color
    green_limit.acquire()
    
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
        
    # get a slot in the fitting room, wait if no slot is available yet
    slots.acquire()
    
    # print green thread's information 
    print(current_thread().name)
    
    # simulate work in critical section
    sleep(1)
    
    # green thread is done with its work, decrease current number of threads to be executed
    global green_executed
    green_executed += 1
    
    # release slot
    slots.release()
    
    # get updated number of executed blue threads
    global blue_executed
    
    # if green thread is the last in the fitting room, give access lock to blue threads
    if green_executed == g or (green_executed % limit == 0 and blue_executed != b):
        # fitting room is currently empty
        print("Empty fitting room.")
        
        # if there are remaining blue threads to be executed, give access lock to blue threads
        if blue_executed != b:
            # signal "limit" blue threads so that they can access the fitting room
            for i in range(limit):
                blue_limit.release()
                
            # release access lock
            green_mutex.release()
    # else if all blue threads have already been executed, no more access limit for green threads
    elif blue_executed == b:
        green_limit.release()

# get number of fitting room slots (n), blue threads (b), and green
# threads (g)
n, b, g = map(int, input("Input values: ").split())
    
# initialize global process synchronization variables
blue_mutex = Lock()                    # to allow only blue threads to access the fitting room
green_mutex = Lock()                   # to allow only green threads to access the fitting room
slots = BoundedSemaphore(n)            # counting semaphore for fitting room slots, with value == number of fitting room slots
                                       # bounded so that it is restricted to values between 0 to 5 only
limit = n + 5                          # fitting room access limit per color, to avoid starvation (change value if needed)
blue_limit = Semaphore(limit)          # counting semaphore for fitting room access limit to blue threads, initialized to the defined access 
                                       # limit, as blue threads will access the fitting room first
green_limit = Semaphore(0)             # counting semaphore for fitting room access limit to green threads
                                       # initialized to zero (0), as blue threads will enter the fitting room first
blue_executed = 0                      # number of blue processes executed
green_executed = 0                     # number of green processes executed
    
# initialize and execute blue processes
for i in range(1, b+1):
    Thread(target = execute_blue, name="{0} Blue".format(i)).start()
    
# initialize and execute green processes
for i in range(1, g+1):
    Thread(target = execute_green, name="{0} Green".format(i)).start()
