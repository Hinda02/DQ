#!/usr/bin/env python3
"""
Task Set 1 - Interpreting Algorithmic FDs
Analyzes pre-computed functional dependencies from TANE algorithm
"""

import json
import csv
from collections import defaultdict, Counter
from pathlib import Path

class FDAnalyzer:
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.fds = []
        self.columns = []
        self.column_map = {}

    def read_csv_columns(self, csv_path):
        """Read column names from CSV file"""
        with open(csv_path, 'r') as f:
            # Try to detect if first row has headers or data
            first_line = f.readline().strip()
            # Count columns
            cols = first_line.split(',')
            num_cols = len(cols)

            # Check if it looks like headers (contains letters)
            if any(c.isalpha() for c in first_line):
                self.columns = cols
            else:
                # No headers, use column indices
                self.columns = [f"col_{i+1}" for i in range(num_cols)]

        return self.columns

    def parse_index_format(self, fd_path):
        """Parse index-based FD format (e.g., iris_fds)"""
        with open(fd_path, 'r') as f:
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
                # Parse column mapping: e.g., "1.1.4	3"
                parts = line.split('\t')
                if len(parts) == 2:
                    col_name = parts[0].split('.')[-1]
                    col_idx = parts[1]
                    self.column_map[col_idx] = col_name
            elif section == 'results':
                # Parse FD: e.g., "3,2,1->5"
                if '->' in line:
                    lhs, rhs = line.split('->')
                    lhs_cols = lhs.split(',') if lhs else []

                    # Map indices to column names
                    lhs_names = [self.column_map.get(c, f"col_{c}") for c in lhs_cols]
                    rhs_name = self.column_map.get(rhs, f"col_{rhs}")

                    self.fds.append({
                        'lhs': lhs_names,
                        'rhs': rhs_name,
                        'lhs_size': len(lhs_names)
                    })

    def parse_json_format(self, fd_path):
        """Parse JSON-LD FD format (e.g., bridges_fds)"""
        with open(fd_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    fd_obj = json.loads(line)

                    # Extract LHS columns
                    lhs_cols = []
                    if 'determinant' in fd_obj and 'columnIdentifiers' in fd_obj['determinant']:
                        for col in fd_obj['determinant']['columnIdentifiers']:
                            lhs_cols.append(col.get('columnIdentifier', '?'))

                    # Extract RHS column
                    rhs_col = None
                    if 'dependant' in fd_obj:
                        rhs_col = fd_obj['dependant'].get('columnIdentifier', '?')

                    self.fds.append({
                        'lhs': lhs_cols,
                        'rhs': rhs_col,
                        'lhs_size': len(lhs_cols)
                    })
                except json.JSONDecodeError:
                    continue

    def analyze(self):
        """Compute statistics for the FDs"""
        if not self.fds:
            return None

        total_fds = len(self.fds)

        # Average LHS size
        avg_lhs_size = sum(fd['lhs_size'] for fd in self.fds) / total_fds

        # Attribute frequency
        lhs_counter = Counter()
        rhs_counter = Counter()

        for fd in self.fds:
            for attr in fd['lhs']:
                lhs_counter[attr] += 1
            rhs_counter[fd['rhs']] += 1

        # Identify ID-based FDs (single LHS attribute that appears in many FDs as sole determinant)
        single_lhs_fds = defaultdict(int)
        for fd in self.fds:
            if fd['lhs_size'] == 1:
                single_lhs_fds[fd['lhs'][0]] += 1

        # Find potential ID columns (appear as single LHS in many FDs)
        potential_ids = []
        for attr, count in single_lhs_fds.items():
            if count >= 3:  # Arbitrary threshold
                potential_ids.append((attr, count))

        # Very large determinants
        large_determinants = []
        for fd in self.fds:
            if fd['lhs_size'] >= 5:  # 5+ attributes in LHS
                large_determinants.append(fd)

        # Suspicious dependencies (very large LHS or unusual patterns)
        suspicious = []
        for fd in self.fds:
            # Very large LHS
            if fd['lhs_size'] >= 7:
                suspicious.append({
                    'fd': f"{','.join(fd['lhs'])} -> {fd['rhs']}",
                    'reason': f'Very large LHS ({fd["lhs_size"]} attributes)',
                    'lhs_size': fd['lhs_size']
                })
            # LHS contains RHS (trivial)
            elif fd['rhs'] in fd['lhs']:
                suspicious.append({
                    'fd': f"{','.join(fd['lhs'])} -> {fd['rhs']}",
                    'reason': 'RHS appears in LHS (trivial)',
                    'lhs_size': fd['lhs_size']
                })

        return {
            'dataset': self.dataset_name,
            'total_fds': total_fds,
            'avg_lhs_size': round(avg_lhs_size, 2),
            'lhs_frequency': dict(lhs_counter.most_common(10)),
            'rhs_frequency': dict(rhs_counter.most_common(10)),
            'potential_id_columns': sorted(potential_ids, key=lambda x: x[1], reverse=True),
            'large_determinants_count': len(large_determinants),
            'large_determinants_sample': large_determinants[:5],
            'suspicious_count': len(suspicious),
            'suspicious_sample': suspicious[:10]
        }


def analyze_all_datasets():
    """Analyze all datasets in the repository"""
    datasets = [
        'iris', 'balance-scale', 'chess', 'abalone', 'nursery',
        'breast-cancer-wisconsin', 'bridges', 'echocardiogram',
        'adult', 'hepatitis', 'horse'
    ]

    results = []

    for dataset in datasets:
        print(f"\nAnalyzing {dataset}...")

        analyzer = FDAnalyzer(dataset)

        # Read CSV to get columns
        csv_path = f"/home/user/DQ/{dataset}.csv"
        fd_path = f"/home/user/DQ/{dataset}_fds"

        try:
            analyzer.read_csv_columns(csv_path)

            # Detect format by reading first line
            with open(fd_path, 'r') as f:
                first_line = f.readline().strip()

            if first_line.startswith('{'):
                print(f"  Format: JSON-LD")
                analyzer.parse_json_format(fd_path)
            else:
                print(f"  Format: Index-based")
                analyzer.parse_index_format(fd_path)

            stats = analyzer.analyze()
            if stats:
                results.append(stats)
                print(f"  Total FDs: {stats['total_fds']}")
                print(f"  Avg LHS size: {stats['avg_lhs_size']}")

        except Exception as e:
            print(f"  Error: {e}")

    return results


def generate_report(results):
    """Generate comprehensive report for Task Set 1"""

    report = []
    report.append("=" * 80)
    report.append("TASK SET 1 - INTERPRETING ALGORITHMIC FUNCTIONAL DEPENDENCIES")
    report.append("=" * 80)
    report.append("")

    # Summary table
    report.append("1. SUMMARY STATISTICS")
    report.append("-" * 80)
    report.append(f"{'Dataset':<30} {'Total FDs':>12} {'Avg LHS Size':>15} {'Max LHS Freq':>15}")
    report.append("-" * 80)

    for r in results:
        max_lhs_freq = max(r['lhs_frequency'].values()) if r['lhs_frequency'] else 0
        report.append(f"{r['dataset']:<30} {r['total_fds']:>12} {r['avg_lhs_size']:>15.2f} {max_lhs_freq:>15}")

    report.append("-" * 80)
    report.append("")

    # Detailed analysis for each dataset
    for r in results:
        report.append("")
        report.append("=" * 80)
        report.append(f"DATASET: {r['dataset'].upper()}")
        report.append("=" * 80)
        report.append("")

        report.append(f"Total Functional Dependencies: {r['total_fds']}")
        report.append(f"Average LHS Size: {r['avg_lhs_size']}")
        report.append("")

        # Attribute frequency as LHS
        report.append("Top Attributes in LHS (Determinants):")
        if r['lhs_frequency']:
            for attr, count in list(r['lhs_frequency'].items())[:10]:
                report.append(f"  {attr}: {count} times")
        else:
            report.append("  None")
        report.append("")

        # Attribute frequency as RHS
        report.append("Top Attributes in RHS (Dependents):")
        if r['rhs_frequency']:
            for attr, count in list(r['rhs_frequency'].items())[:10]:
                report.append(f"  {attr}: {count} times")
        else:
            report.append("  None")
        report.append("")

        # Potential ID columns
        report.append("Potential ID Columns (Degenerate FDs):")
        if r['potential_id_columns']:
            for attr, count in r['potential_id_columns']:
                report.append(f"  {attr}: appears as single determinant in {count} FDs")
        else:
            report.append("  None identified")
        report.append("")

        # Large determinants
        report.append(f"FDs with Large Determinants (5+ attributes): {r['large_determinants_count']}")
        if r['large_determinants_sample']:
            report.append("  Sample:")
            for fd in r['large_determinants_sample']:
                report.append(f"    {','.join(fd['lhs'])} -> {fd['rhs']} (LHS size: {fd['lhs_size']})")
        report.append("")

        # Suspicious dependencies
        report.append(f"Suspicious Dependencies: {r['suspicious_count']}")
        if r['suspicious_sample']:
            report.append("  Sample:")
            for susp in r['suspicious_sample']:
                report.append(f"    {susp['fd']}")
                report.append(f"      Reason: {susp['reason']}")
        report.append("")

    return "\n".join(report)


if __name__ == "__main__":
    print("Task Set 1 - FD Analysis Starting...")
    print("=" * 80)

    results = analyze_all_datasets()

    report = generate_report(results)

    # Save report
    with open('/home/user/DQ/task1_report.txt', 'w') as f:
        f.write(report)

    print("\n" + report)
    print("\nReport saved to: task1_report.txt")
