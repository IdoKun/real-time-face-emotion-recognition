import sys,argparse

from rtfer.feels import live_feels

# parse script arguments
parser=argparse.ArgumentParser()

parser.add_argument("--weight",help="Path to the model weight",type=str)

args=parser.parse_args()
print(args.weight)
live_feels(path_to_weight=args.weight)
