# This program help to read and interpret the results from infer_experiment.py

import sys
import os


# def the function
def get_strand(file, quant):
    """
    This function fetches probable strand from result spilt out from
    infer_experiment
    Args:
        file: A txt file obtained from infer_experiment.py command on bam file
        quant: This is the read quantifier to be used. "FC" for feature count,
                'HiSAT2' for HiSAT2 quantifier
    """

    # start the task
    with open(file, "r") as f:
        results = f.read().splitlines()[-2:]
    pct_standness = {
        "FR": float(results[0].rsplit(" ")[-1]),
        "RF": float(results[1].rsplit(" ")[-1]),
    }
    for key, value in pct_standness.items():
        if (pct_standness[key]) > 0.50:
            strand = key
        else:
            strand = None

    # Strand information
    if strand == "RF" or strand == "R":
        fc_strand = "2"
    elif strand == "FR" or strand == "F":
        fc_strand = "1"
    else:
        fc_strand = "0"
    if quant == "FC":
        return int(fc_strand)
    elif quant == "HiSAT":
        return strand


if __name__ == "__main__":
    # Verify inputs from command line
    if len(sys.argv) != 3:
        print("error: add the rseqc result file and quantifier of choice")
        print("Example: python getStrand.py result_file FC")
        sys.exit(1)
    fileIn = sys.argv[1]
    if not os.path.isfile(fileIn):
        print("error: {} does not exist".format(fileIn))
        sys.exit(1)
    quantifier = sys.argv[2]
    if quantifier != "FC" and quantifier != "HiSAT":
        print("error: add a quantifier FC or HiSAT")
        sys.exit(1)
    else:
        read_strand = get_strand(file=fileIn, quant=quantifier)
        print(read_strand)
