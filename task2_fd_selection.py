#!/usr/bin/env python3
"""
Task Set 2 - LLM-Assisted Semantic FD Discovery
Select representative FDs for semantic evaluation
"""

import json
import csv
from collections import defaultdict

class FDSelector:
    """Select plausible and suspicious FDs for LLM evaluation"""

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.csv_path = f"/home/user/DQ/{dataset_name}.csv"
        self.fd_path = f"/home/user/DQ/{dataset_name}_fds"
        self.columns = []
        self.column_map = {}
        self.fds = []
        self.sample_data = []

    def read_csv_sample(self, limit=10):
        """Read sample rows from CSV to understand data"""
        with open(self.csv_path, 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    # Check if first row is header
                    if any(c.isalpha() for c in ','.join(row)):
                        self.columns = row
                        continue
                    else:
                        self.columns = [f"col_{j+1}" for j in range(len(row))]
                        self.sample_data.append(row)
                if i >= limit:
                    break
                self.sample_data.append(row)
        return self.sample_data

    def parse_index_format(self):
        """Parse index-based FD format"""
        with open(self.fd_path, 'r') as f:
            lines = f.readlines()

        section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith('# TABLES'):
                section = 'tables'
            elif line.startswith('# COLUMN'):
                section = 'columns'
            elif line.startswith('# RESULTS'):
                section = 'results'
            elif section == 'columns':
                parts = line.split('\t')
                if len(parts) == 2:
                    col_name = parts[0].split('.')[-1]
                    col_idx = parts[1]
                    self.column_map[col_idx] = col_name
            elif section == 'results':
                if '->' in line:
                    lhs, rhs = line.split('->')
                    lhs_cols = lhs.split(',') if lhs else []

                    lhs_names = [self.column_map.get(c, f"col_{c}") for c in lhs_cols]
                    rhs_name = self.column_map.get(rhs, f"col_{rhs}")

                    self.fds.append({
                        'lhs': lhs_names,
                        'rhs': rhs_name,
                        'lhs_size': len(lhs_names),
                        'original': line
                    })

    def parse_json_format(self):
        """Parse JSON-LD FD format"""
        with open(self.fd_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    fd_obj = json.loads(line)

                    lhs_cols = []
                    if 'determinant' in fd_obj and 'columnIdentifiers' in fd_obj['determinant']:
                        for col in fd_obj['determinant']['columnIdentifiers']:
                            lhs_cols.append(col.get('columnIdentifier', '?'))

                    rhs_col = None
                    if 'dependant' in fd_obj:
                        rhs_col = fd_obj['dependant'].get('columnIdentifier', '?')

                    self.fds.append({
                        'lhs': lhs_cols,
                        'rhs': rhs_col,
                        'lhs_size': len(lhs_cols),
                        'original': line
                    })
                except json.JSONDecodeError:
                    continue

    def load_fds(self):
        """Load FDs from file"""
        # Detect format
        with open(self.fd_path, 'r') as f:
            first_line = f.readline().strip()

        if first_line.startswith('{'):
            self.parse_json_format()
        else:
            self.parse_index_format()

        return self.fds

    def select_plausible(self, count=3):
        """Select plausible FDs for evaluation"""
        plausible = []

        # Criteria for plausible FDs:
        # - Small to medium LHS size (1-3 attributes)
        # - Not trivial (RHS not in LHS)
        # - Not too many similar patterns

        for fd in self.fds:
            if len(plausible) >= count:
                break

            # Skip trivial
            if fd['rhs'] in fd['lhs']:
                continue

            # Prefer smaller LHS
            if fd['lhs_size'] <= 3:
                plausible.append(fd)

        return plausible

    def select_suspicious(self, count=3):
        """Select suspicious FDs for evaluation"""
        suspicious = []

        # Criteria for suspicious FDs:
        # - Trivial (RHS in LHS)
        # - Very large LHS (5+ attributes)
        # - Single attribute appears very frequently

        for fd in self.fds:
            if len(suspicious) >= count:
                break

            # Trivial FDs
            if fd['rhs'] in fd['lhs']:
                suspicious.append(fd)
                continue

            # Very large LHS
            if fd['lhs_size'] >= 5:
                suspicious.append(fd)

        return suspicious


def select_fds_for_all_datasets():
    """Select FDs from all datasets for Task Set 2"""
    datasets = [
        'iris', 'balance-scale', 'chess', 'abalone', 'nursery',
        'breast-cancer-wisconsin', 'bridges', 'echocardiogram', 'hepatitis'
    ]

    all_selections = {}

    for dataset in datasets:
        print(f"\n{'='*80}")
        print(f"Selecting FDs from: {dataset}")
        print('='*80)

        selector = FDSelector(dataset)

        try:
            # Load data
            selector.read_csv_sample(5)
            selector.load_fds()

            # Select FDs
            plausible = selector.select_plausible(3)
            suspicious = selector.select_suspicious(3)

            all_selections[dataset] = {
                'columns': selector.columns,
                'sample_data': selector.sample_data,
                'plausible': plausible,
                'suspicious': suspicious
            }

            print(f"  Columns: {', '.join(selector.columns)}")
            print(f"  Total FDs: {len(selector.fds)}")
            print(f"  Selected plausible: {len(plausible)}")
            print(f"  Selected suspicious: {len(suspicious)}")

        except Exception as e:
            print(f"  Error: {e}")

    return all_selections


if __name__ == "__main__":
    selections = select_fds_for_all_datasets()

    # Save selections to file
    with open('/home/user/DQ/task2_selected_fds.json', 'w') as f:
        json.dump(selections, f, indent=2)

    print("\n" + "="*80)
    print("FD selections saved to: task2_selected_fds.json")
    print("="*80)
