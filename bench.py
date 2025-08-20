from src.benchmark import benchmark
from src.operations import *
import argparse
import json
from typing import List
import polars as pl
import os

test_functions = {
    "file_parquet": file_parquest,
    "file_csv": file_csv,
    "file_duckdb": file_duckdb,
    "minio_parquet": minio_parquet,
    "minio_csv": minio_csv,
    "minio_duckdb": minio_duckdb,
    "tool_parquet_polars_load": tool_parquet_polars_load,
    "tool_parquet_pandas_load": tool_parquet_pandas_load,
    "tool_csv_polars_load": tool_csv_polars_load,
    "tool_csv_pandas_load": tool_csv_pandas_load,
    "tool_duckdb_polars_load": tool_duckdb_polars_load,
    "tool_duckdb_pandas_load": tool_duckdb_pandas_load,
    "tool_polars_query": tool_polars_query,
    "tool_pandas_query": tool_pandas_query
}

def __get_test_group_types(group: str) -> List[str]:
    try:
        with open("benchmark_config.json") as f:
            config = json.load(f)
            config = config.get('test_group', {})
    except FileNotFoundError:
        print("No benchmark config file found. Please create one in the root directory of the project.")
        exit(1)
    
    return config.get(group, [])

def __create_results_directory():
    # Check if the results directory exists
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

def run_benchmarks(group: str, output: str):
    test_group_types = __get_test_group_types(group)
    df = pl.DataFrame({}, schema={
        'func': pl.Utf8,
        'input_size': pl.UInt32,
        'cpu': pl.Float64,
        'mem': pl.Float64,
        'duration': pl.Float64
    })

    for func_name in test_group_types:
        func = test_functions.get(func_name, None)        
        
        if not func:
            print(f"No function found for {func_name}")
            continue

        results = benchmark(func, input_size=200, iter=1)                
        df = pl.concat([df, results], how="vertical")

    __write_results(df, output)
        
    

def main():
    parser = argparse.ArgumentParser(description="Run benchmarks for the different tools that can be used for building an efficient data pipeline")

    parser.add_argument("--group", "-g", help="The group of related benchmarks to run", choices=["read_tools", "query_tools", "pipelines", "storage"], type=str)
    parser.add_argument("--output", "-o", help="The output file to write the results to", type=str, choices=["csv", "json", "parquet"])

    args = parser.parse_args()

    print(args)

    group = args.group
    output = args.output

    run_benchmarks(group, output)

if __name__ == "__main__":
    main()
