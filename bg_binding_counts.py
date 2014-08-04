from argparse import ArgumentParser
import sys

def bg_binding_freq(primer, bg):
    count = start = 0
    while True:
        start = bg.find(primer, start) + 1
        if start > 0:
            count += 1
        else:
            return count


def main():
    parser = ArgumentParser(description='''Finds the number of times a set of primers
    binds to a genome. Outputs file where each line is formatted [primer <tab> count]''')
    parser.add_argument('-p', '--primers',
                        help='File with one primer per line',
                        action='store', required=True) 
    parser.add_argument('-g', '--genome',
                        help='Background genome in FASTA format.',
                        action='store', required=True)
    parser.add_argument('-o', '--output',
                        help="File to write results to.", required=True)
    args = vars(parser.parse_args())

    print("Reading background genome into memory...")
    with open(args['genome']) as bg_handle:
        bg = "".join(_.strip('\n') for i, _ in enumerate(bg_handle.readlines()) if i > 0)
        print("\tdone.")

    with open(args['primers']) as primers:
        with open(args['output'], 'w') as output:
            for primer in primers:
                primer = primer.strip('\n')
                bind_freq = bg_binding_freq(primer, bg)
                output.write('{}\t{}\n'.format(primer, bind_freq))
                sys.stdout.write('{}\t{}\n'.format(primer, bind_freq))


if __name__ == '__main__':
        main()