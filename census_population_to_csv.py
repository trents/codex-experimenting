#!/usr/bin/env python3
"""
Convert CENSUS_POPULATION_STATE.tsv to a two-column CSV with state name and total population.
"""
import csv
import sys

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Convert a Census population TSV to CSV of state and total population'
    )
    parser.add_argument(
        'input_tsv',
        help='Path to CENSUS_POPULATION_STATE.tsv file'
    )
    parser.add_argument(
        'output_csv',
        nargs='?', default='state_population.csv',
        help='Path to output CSV file (default: state_population.csv)'
    )
    args = parser.parse_args()

    # Read TSV header and find estimate columns for each state
    with open(args.input_tsv, newline='') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        try:
            header = next(reader)
        except StopIteration:
            sys.exit('Error: TSV file is empty')

        states = []
        estimate_indices = []
        for idx, col in enumerate(header):
            if col.endswith('!!Estimate'):
                state = col.split('!!', 1)[0]
                states.append(state)
                estimate_indices.append(idx)

        # Find the 'Total population' row
        total_row = None
        for row in reader:
            if not row:
                continue
            if row[0].strip() == 'Total population':
                total_row = row
                break
        if total_row is None:
            sys.exit('Error: Total population row not found in TSV')

    # Extract total population for each state
    results = []
    for state, idx in zip(states, estimate_indices):
        try:
            val = total_row[idx]
        except IndexError:
            sys.exit(f'Error: Missing data for state {state}')
        # Remove commas and convert to integer-like string
        pop = val.replace(',', '')
        results.append((state, pop))

    # Write output CSV
    with open(args.output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['State', 'TotalPopulation'])
        for state, pop in results:
            writer.writerow([state, pop])

if __name__ == '__main__':  # pragma: no cover
    main()