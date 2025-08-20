import os
from src.config import Config

config = Config()

function_registry = {}

def benchmark_operator(name):
    def decorator(func):
        function_registry[name] = func
        config.append(name, func)
        return func
    
    return decorator