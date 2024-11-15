import json
import argparse
import sys

description = """Takes two JSON files as input
and aligns the order of the input file with the provided order by master
"""


parser = argparse.ArgumentParser(prog='sort_dict', description=description)
parser.add_argument('--master', help='path to the JSON file that provides the desired order')
parser.add_argument('--input', help='path to JSON file that needs the aligned order')
parser.add_argument('--output', help='path to the desired output file')


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def sort_dict(inputDict, masterDict):
    outputDict = {}
    if masterDict is not None:
        for k, v in masterDict.items():
            value = inputDict.get(k, None)            
            if value is not None:
                outputDict[k] = value
                if isinstance(value, dict):
                    outputDict[k] = sort_dict(value, v)
                else:
                    outputDict[k] = value
                inputDict.pop(k)
        for k, v in inputDict.items():
            outputDict[k] = v
    return outputDict

if __name__ == '__main__':
    args = parser.parse_args()
    if args.master is None:
        print("\nmissing input parameter '--master' for the file that provides the structure\n")
        sys.exit(1)
    if args.input is None:
        print("\nmissing parameter '--input' for the file to read\n")
        sys.exit(1)
    if args.output is None:
        print("\nmissing parameter '--output' for the output file to write\n")
        sys.exit(1)

    masterDict = load_json(args.master)
    inputDict = load_json(args.input)

    outputDict = {}

    for k, v in masterDict.items():
        value = inputDict.get(k, None)            
        if value is not None:
            if isinstance(value, dict):
                outputDict[k] = sort_dict(value, v)
            else:
                outputDict[k] = value
            inputDict.pop(k)
    for k, v in inputDict.items():
        outputDict[k] = v

    with open(args.output, 'w') as outfile:
        json.dump(outputDict, outfile, indent=2)

