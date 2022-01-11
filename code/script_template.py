import defopt

#
# All your functions (that will be called by main()) go here.
#

def main(infile: str, outfile: str):
    """
    Run the program.

    :param str infile: input file
    :param str outfile: output file
    """

    print('Input file: ', infile)
    print('Output file: ', outfile)


if __name__ == '__main__':

    defopt.run(main)
