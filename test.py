from threading import Thread

a = []

def incrementer(n):
    for i in range(n):
        a.append('1')

def deleter(n):
    global a
    for i in range(n):
        a = []

def indexer(n):
    for _ in range(n):
        a[0]

n = 1000000

thread_1 = Thread(target=incrementer, args=(n, ))
thread_1.start()
thread_3 = Thread(target=deleter, args=(n, ))
thread_3.start()
thread_2 = Thread(target=indexer, args=(n, ))
thread_2.start()

thread_1.join()
thread_2.join()
thread_3.join()
print(a)