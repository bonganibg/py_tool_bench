import psutil
import os
from timeit import timeit
import polars as pl

process = psutil.Process(os.getpid())

def system_performance(func, *args, **kwargs):
    cpu_before = process.cpu_times()
    mem_before = process.memory_info().rss

    result = func(*args, **kwargs)

    cpu_after = process.cpu_times()
    mem_after = process.memory_info().rss

    memory_usage = mem_after - mem_before
    cpu_usage = cpu_after.user - cpu_before.user

    return cpu_usage, memory_usage

    

def time_performance(func,*args, **kwargs): 
    iter = kwargs.pop('iter', 100) or 1

    duration = timeit(lambda: func(**kwargs), number=iter)
    return duration / iter

def benchmark(func, *args, **kwargs) -> pl.DataFrame:
    cpu, mem = system_performance(func, *args, **kwargs)
    duration = time_performance(func, *args, **kwargs)   

    return pl.DataFrame({
        'func': func.__name__,
        'input_size': kwargs.get('input_size', None),
        'cpu': cpu,
        'mem': mem,
        'duration': duration
    }, schema={
        'func': pl.Utf8,
        'input_size': pl.UInt32,
        'cpu': pl.Float64,
        'mem': pl.Float64,
        'duration': pl.Float64
    })
    
