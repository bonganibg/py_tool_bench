# pyToolBench 
A tool that can be used to benchmark and compare different approaches to solving a problem using Python. 

## Installation
To install the tool, run the following command:

```bash
pip install -r requirements.txt
```

## Usage
To run the tool, use the following command:

```bash
python main.py --group <group> --output <output>
```

Replace `<group>` with the group of benchmarks you want to run, and `<output>` with the desired output format (csv, json, or parquet).

The available groups are:
- `read_tools`: Benchmarks for reading data from different sources (e.g., file, minio, etc.)
- `query_tools`: Benchmarks for querying data using different tools (e.g., polars, pandas, etc.)
- `pipelines`: Benchmarks for building data pipelines using different tools (e.g., polars, pandas, etc.)
- `storage`: Benchmarks for storing data in different storage systems (e.g., file, minio, etc.)

The available output formats are:
- `csv`: Comma-separated values (CSV) file
- `json`: JavaScript Object Notation (JSON) file
- `parquet`: Apache Parquet file

## Example
To run the tool with the `read_tools` group and write the results to a CSV file, use the following command:

```bash
python main.py --group read_tools --output csv
```

This will run the benchmarks for the `read_tools` group and write the results to a CSV file named `results.csv` in the current directory.

## Configuration
The tool can be configured by creating a `benchmark_config.json` file in the root directory of the project. The file should contain a JSON object with the following structure:

```json
{
    "test_group": {
        "storage": [],
        "read_tools": [
            "file_parquet",
            "file_csv",
            "file_duckdb"
        ],
        "query_tools": [],
        "pipelines": []
    }
}
```

In this example, the `test_group` object has four keys: `storage`, `read_tools`, `query_tools`, and `pipelines`. Each of these keys is an array of strings, representing the names of the tools or storage systems that should be benchmarked.

For example, to benchmark the `file_parquet` and `file_csv` tools, you would add the following to the `benchmark_config.json` file:

```json
{
    "test_group": {
        "storage": [],
        "read_tools": [
            "file_parquet",
            "file_csv"
        ],
        "query_tools": [],
        "pipelines": []
    }
}
```