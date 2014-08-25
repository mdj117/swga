import argparse
import ConfigParser
import os
import re
import sys
import csv
from operator import attrgetter
import PrimerSets


def main():
    config = ConfigParser.SafeConfigParser()
    cfg_file = os.environ.get('swga_params', PrimerSets.default_config_file)
    defaults = {}
    if os.path.isfile(cfg_file):
        config.read([cfg_file])
        defaults = dict(config.items('filter_primers'))

    parser = argparse.ArgumentParser(description="""Filter primers according to
    specified criteria.""")
    parser.set_defaults(**defaults)

    parser.add_argument('-M', '--max_bg_binding', action='store', type=int,
    help="""Max times a primer can bind to bg genome. (default: %(default)s)""")

    parser.add_argument('-n', '--num_primers', action='store', type=int,
    help="""Max number of primers to use after filtering.
    (default: %(default)s)""")

    parser.add_argument('-i', '--input', action='store',
    help="""Input file where each row contains a primer, fg binding #,
    bg binding #, and fg/bg binding ratio, separated by whitespace.
    (default: stdin)""",
    default=sys.stdin, type=argparse.FileType('r'))

    parser.add_argument('-o', '--output', action='store',
    type=argparse.FileType('w',0), default=sys.stdout,
    help="""Filename to store the filtered primers (tab-delimited).
    (default: stdout)""")

    parser.add_argument('-v', '--verbose', action='store_true',
    help="Display warnings (default: %(default)s)")

    args = parser.parse_args()
    if not args.quiet and args.input.name == '<stdin>':
        sys.stderr.write("Receiving input from stdin...\n")
    primers = filter_primers(args)
    writer = csv.writer(args.output, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(primers)


def filter_primers(args):
    primers = PrimerSets.read_primer_file(args.input, False, args.verbose)
    # sort by bg binding count
    primers = sorted(primers, key=attrgetter("bg_freq"))
    # remove primers that bind too many times to bg
    primers = [p for p in primers if p.bg_freq <= args.max_bg_binding]
    # sort by fg/bg ratio
    primers = sorted(primers, key=attrgetter("ratio"))
    # return only the top <n>
    return primers[0:args.num_primers]


if __name__ == '__main__':
    main()
