import threading


def func_1(n):
    global a, b
    for i in range(n):
        print(f'{i}: func_1 wait lock_A', flush=True)
        with lock_A:
            print(f'{i}: func_1 take lock_A', flush=True)
            a += 1
            print(f'{i}: func_1 wait lock_B', flush=True)
            with lock_B:
                print(f'{i}: func_1 take lock_B', flush=True)
                b += 1


def func_2(n):
    global a, b
    for i in range(n):
        print(f'{i}: func_2 wait lock_B', flush=True)
        with lock_B:
            print(f'{i}: func_2 take lock_B', flush=True)
            b += 1
            print(f'{i}: func_2 wait lock_A', flush=True)
            with lock_A:
                print(f'{i}: func_2 take lock_A', flush=True)
                a += 1


a = 0
b = 0
lock_A = threading.RLock()
lock_B = threading.RLock()
N = 10

thread_1 = threading.Thread(target=func_1, args=(N,))
thread_2 = threading.Thread(target=func_2, args=(N,))
thread_1.start()
thread_2.start()
thread_1.join()
thread_2.join()
print(a, b)