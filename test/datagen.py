#!/usr/bin/env python3

from collections import OrderedDict

import click
import pandas as pd
import numpy as np


step = 10
startts = 1610000000
rng = np.random.default_rng()

def_count = 100
def_metricname = "node_temp_celsius"
def_minval = 45
def_maxval = 100


def gen_metric(count=def_count, metricname=def_metricname, minval=def_minval, maxval=def_maxval):
    timestamps = pd.DataFrame(range(startts, startts+(count*step), step), columns=["timestamp"])
    values = pd.DataFrame(rng.integers(minval, maxval, size=(count, 1)), columns=["value"])

    df = pd.concat([timestamps, values], axis=1)
    df.set_index("timestamp", inplace=True)

    df.insert(0, "__name__", metricname)

    return df


@click.command()
@click.option("--count", "-c", default=def_count, help=f"Number of rows per metric (default: {def_count})")
@click.option("--metric", "-m", "metricname", default=def_metricname, help=f"Metric name (default: {def_metricname})")
@click.option("--min", "minval", default=def_minval, help=f"Minimum generated value (default: {def_minval})")
@click.option("--max", "maxval", default=def_maxval, help=f"Minimum generated value (default: {def_maxval})")
@click.option("--column", "_columns", default=None, multiple=True,
                                    help="Add a column (format: header=value). Can be used multiple times.")
@click.option("--output", "-o", default=None, type=str, help="Output file (default: stdout)")
def main(count, metricname, minval, maxval, _columns, output):
    columns = OrderedDict()
    for col in _columns:
        header, value = col.split("=")
        columns[header] = value


    df = gen_metric(count, metricname, minval, maxval)

    for header in columns:
        df.insert(df.shape[1]-1, header, columns[header])

    if output is None or output=='-':
        print(df.to_csv(),end='')
    else:
        df.to_csv(output)


if __name__ == "__main__":
    main()
