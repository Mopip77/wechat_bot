import multiprocessing as mp
import time

def  test(i):
    print('task {} is starting...'.format(i))
    time.sleep(1)
    print(i)
#     return True

def main():
    pool = mp.Pool(4)

    jobs = [pool.apply_async(test, args=(i,)) for i in range(10)]
    print('change status')
    check_fin = [j.get() for j in jobs]
    # pool.close()
    # pool.join()
    print(check_fin)
    print('finished')
    return True


main()