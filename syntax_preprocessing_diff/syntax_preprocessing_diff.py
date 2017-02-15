import json
import argparse
import pandas
import os

def yield_lines(file):
    with open(file, 'r', encoding='utf_8') as f:
        yield from f


def diff(in_file_1, in_file_2, out_file):
    assert os.path.exists(os.path.dirname(out_file)), 'Output file directory "' + os.path.dirname(out_file) + '" does not exist.'
    differences = []
    lines_1 = yield_lines(in_file_1)
    lines_2 = yield_lines(in_file_2)
    c = 0
    while True:
        c += 1
        if c%100000 == 0:
            print('.', end='', flush=True)
            if c%1000000 == 0:
                print(c, 'tokens,', len(differences), 'differences')
        try:
            line_1 = next(lines_1)
        except StopIteration:
            line_1 = None
        try:
            line_2 = next(lines_2)
        except StopIteration:
            line_2 = None
        if line_1 is None and line_2 is None:
            break
        if line_1 != line_2:
            assert line_1 is not None, in_file_1 + ' is too short'
            assert line_2 is not None, in_file_2 + ' is too short'
            token_1, syntax_pp_1 = json.loads(line_1.rstrip())
            token_2, syntax_pp_2 = json.loads(line_2.rstrip())
            assert token_1 == token_2, 'different tokens'
            for a, b in zip(syntax_pp_1, syntax_pp_2):
                if a != b:
                    differences.append({'token':token_1, in_file_1: a, in_file_2:b})
                    break
    df = pandas.DataFrame.from_records(differences, columns=['token', in_file_1, in_file_2])
    df.to_csv(out_file, index=False)
    print(c-1, 'tokens')
    print(len(differences), 'differences written to', out_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Find diff of syntax preprocessing of tokens.")
    parser.add_argument('in_file_1', type=str, help='First input file.')
    parser.add_argument('in_file_2', type=str, help='Second input file.')
    parser.add_argument('out_file', type=str, help='Output file.')
    args = parser.parse_args()
    diff(args.in_file_1, args.in_file_2, args.out_file)