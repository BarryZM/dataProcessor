# -*- coding: utf-8 -*-
# -*- author: JeremySun -*-
# -*- dating: 19/10/24 -*-

# 模块载入
import os
import time
from functools import wraps

# 定义timer
def func_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        print('[Function: {name} start...]'.format(name=function.__name__))
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print('[Function: {name} finished, spent time: {time:.2f}s]'.format(name=function.__name__, time=t1 - t0))
        return result
    return function_timer

# 切分函数
@func_timer
def split_file(file_path, partial_size):
    file_dir, name = os.path.split(file_path)
    name, ext = os.path.splitext(name)
    file_dir = os.path.join(file_dir, name)

    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    part_no = 0
    stream = open(file_path, 'r', encoding='utf-8')

    while True:
        part_filename = os.path.join(file_dir, name + '_' + str(part_no) + ext)
        print('write start %s' % part_filename)
        part_stream = open(part_filename, 'w', encoding='utf-8')
        read_count = 0
        read_size = 1024 * 512
        read_count_once = 0

        while read_count < partial_size:
            read_content = stream.read(read_size)
            read_count_once = len(read_content)
            if read_count_once > 0:
                part_stream.write(read_content)
            else:
                break
            read_count += read_count_once
        part_stream.close()
        if read_count_once < read_size:
            break
        part_no += 1
    return print('Splitting is done')


if __name__ == '__main__':
    split_file(r'C:\Users\JeremySun\Desktop\Internship\Project02_corpusProcessor\english_text_pre.txt', 100 * 100 * 1000)