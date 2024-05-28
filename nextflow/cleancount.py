#!/usr/bin/env python
"""
Created on 2024-05-28 17:26:50
Module desc: 
@author: I.ojo
"""

import pandas as pd
import sys


def cleanCount(file):
    """
    Clean the count data from featureCounts and save the cleaned data to 'clean_count.tsv'.

    Parameters:
      file (str): The path to the input file containing the data to be cleaned.

    This function reads the data from the specified file, removes columns with names
    'Chr', 'Start', 'End', 'Strand', and 'Length', sorts the remaining columns,
    removes the trailing 'Aligned....' characters from the column names, and saves the cleaned
    data to a new file named 'clean_count.tsv' using tab as the separator.


    Example:
    cleanCount('counts.txt')
    # Reads data from 'counts.txt', performs cleaning, and saves to 'clean_count.tsv'
    """
    df = pd.read_table(file, comment="#", index_col=0)
    mask = ["Chr", "Start", "End", "Strand", "Length"]
    df.drop(columns=mask, inplace=True)
    cols_name = df.columns.sort_values()
    df = df[cols_name]
    newColumn = [col.rsplit(".Aligned")[0] for col in df.columns]
    df.columns = newColumn
    df.to_csv("clean_count.tsv", sep="\t")


if __name__ == "__main__":
    fileIn = sys.argv[1]
    cleanCount(file=fileIn)
