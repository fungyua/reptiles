# -*- coding: utf-8 -*-
from multiprocessing import Queue

from database.link_database import link_database
from database.write.datawrite import writedata


@link_database
def data_writer(cur, qd):
    print('数据写入器启动')
    while True:
        if not qd.empty():
            data = qd.get()
            writedata(cur, data)


if __name__ == '__main__':
    qd = Queue()
    data_writer(qd)
