from src.config import Config
from src.benchmark import benchmark
from src.operations import *
import argparse
from typing import List
import polars as pl
import os

config = Config()
    
def __create_results_directory():    
    if not os.path.exists("results"):
        os.makedirs("results")

def __write_results(results: pl.DataFrame, output: str):
    ext = output.split(".")[-1]    
    results_dir = "results"

    __create_results_directory()

    match ext:
        case "csv":
            results.write_csv("/".join([results_dir, output]))
        case "json":
            results.write_json("/".join([results_dir, output]))
        case "parquet":
            results.write_parquet("/".join([results_dir, output]))
        case _:
            print(f"Unsupported output format: {ext}")
            exit(1)

def run_benchmarks(operation_group: str, output: str):
    operation_group_functions = config.get(operation_group)

    df = pl.DataFrame({}, schema={
        'func': pl.Utf8,
        'input_size': pl.UInt32,
        'cpu': pl.Float64,
        'mem': pl.Float64,
        'duration': pl.Float64
    })

    for func in operation_group_functions:                
        results = benchmark(func, input_size=200, iter=1)                
        df = pl.concat([df, results], how="vertical")

    __write_results(df, output)
        
    

def main():
    # Get function groups
    operation_groups = config.get_groups().keys()

    parser = argparse.ArgumentParser(description="Run benchmarks for the different tools that can be used for building an efficient data pipeline")

    parser.add_argument("--group", "-g", help="The group of related benchmarks to run", choices=operation_groups, type=str)
    parser.add_argument("--output", "-o", help="The output file to write the results to", type=str)

    args = parser.parse_args()

    print(args)

    group = args.group
    output = args.output

    run_benchmarks(group, output)

if __name__ == "__main__":
    main()
