#!/usr/bin/env python3

DEFAULT_OUTPUT_FILE = 'echo.txt'


def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--file',
                        dest='file',
                        required=True,
                        help='A txt file to generate file transfer statements for')
    parser.add_argument('--output',
                        dest='output',
                        default=DEFAULT_OUTPUT_FILE,
                        required=False,
                        help='An output file with prepared transfer statements, just copy past them in a target '
                             'shell. Default is ' + DEFAULT_OUTPUT_FILE)
    options = parser.parse_args()

    return options


def convert_to_echo_statements(source_file, destionation_file):
    print('Parsing {source_file}'.format(source_file=source_file))
    with open(source_file, 'r', encoding='utf-8') as source:
        source = [line.strip() for line in source.readlines()]
    assert source
    statements = []
    for line in source:
        if line == source[0]:
            statements.append("echo {line} > {destination_file}"
                              .format(line=line, destination_file=destionation_file))
        else:
            statements.append("echo {line} >> {destination_file}"
                              .format(line=line, destination_file=destionation_file))
    assert statements
    with open(destionation_file, 'w', encoding='utf-8') as destination:
        for line in statements:
            destination.write(line)
            destination.write('\n')
    print('Number of statements: {len}'.format(len=len(statements)))
    print('Saved to {destination}'.format(destination=destionation_file))



options = get_arguments()
convert_to_echo_statements(source_file=options.file, destionation_file=options.output)
