import argparse

description = """Yet another code generation.
Program takes one or more models, a bunch of templates and generates
source code from it
"""
parser = argparse.ArgumentParser(prog='yacg', description=description)

parser.add_argument_group('input')
parser.add_argument('--model', nargs='+', help='models to process')
parser.add_argument('--config', nargs='?', help='config file')
parser.add_argument_group('processing')
parser.add_argument('--template', nargs='+', help='template to process')
parser.add_argument_group('output')
parser.add_argument('--outputDir',  help='dir to write the output')


def main():
    args = parser.parse_args()
    print("the program args are: {}".format(args))


if __name__ == '__main__':
    main()

