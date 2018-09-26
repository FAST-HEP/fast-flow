#!/usr/bin/env python
"""
Demo using fast_flow to set up the processing chain from the config file
"""
from __future__ import print_function
from fast_flow.v1 import read_sequence_yaml
import logging
logging.getLogger(__name__).setLevel(logging.INFO)
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sequence_cfg", type=str,
                        help="Dataset config to run over")
    parser.add_argument("-n", "--nevents", type=int, default=10,
                        help="Number of events to run")
    parser.add_argument("-o", "--outdir", type=str, default=None,
                        help="Output directory (if wanted)")
    args = parser.parse_args()
    return args


def process_sequence(sequence, nevents):
    """
    This function is left up to the user to define.  This is also where the
    interaction between the sequences described in the config file is really
    defined (eg what each step must return, what it is given, how it should be
    called, etc).
    """
    for i in range(nevents):
        data = {}
        data["iteration"] = i
        for step in sequence:
            step(data)
        print(data)


if __name__ == "__main__":
    args = parse_args()

    sequence = read_sequence_yaml(args.sequence_cfg, output_dir=args.outdir)

    process_sequence(sequence, nevents=args.nevents)
