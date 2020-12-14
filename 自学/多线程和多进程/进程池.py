import multiprocessing
import time

start = time.time()


def index_pool(data):
    res = data * data
    return res


if __name__ == '__main__':
    data = list(range(100))
    pool = multiprocessing.Pool(processes=4)
    pool_out_puts = pool.map(index_pool, data)
    # pool_out_puts = pool.apply(index_pool, args=(10,))
    pool.close()
    # pool.join()
    print('Pool   {}'.format(pool_out_puts))
    end = time.time()
    print('Running time: %s Seconds' % (end - start))
