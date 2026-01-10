#!/usr/bin/env python3
"""
Task Set 3: Validate LLM-Proposed Functional Dependencies

Validates FDs proposed by LLM on:
1. The sample data (should hold by construction)
2. The full dataset (may or may not hold)

Identifies:
- False positives (don't hold on full data)
- Non-minimal FDs (redundant attributes on LHS)
- Misleading FDs (semantically implausible)
"""

import csv
from collections import defaultdict
from parse_llm_fds import LLM_PROPOSED_FDS

def parse_fd(fd_string):
    """Parse FD string like '(1,2,3) → 4' or '1 → 2'"""
    parts = fd_string.split('→')
    if len(parts) != 2:
        return None, None

    lhs_str = parts[0].strip()
    rhs_str = parts[1].strip()

    # Parse LHS
    if lhs_str.startswith('(') and lhs_str.endswith(')'):
        lhs_str = lhs_str[1:-1]
    lhs_cols = [int(x.strip()) - 1 for x in lhs_str.split(',')]  # Convert to 0-based

    # Parse RHS
    rhs_col = int(rhs_str.strip()) - 1  # Convert to 0-based

    return lhs_cols, rhs_col

def read_csv_data(filepath):
    """Read CSV file and return rows"""
    rows = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # Skip empty rows
                rows.append(row)
    return rows

def validate_fd(rows, lhs_cols, rhs_col):
    """
    Check if FD holds in the data.
    Returns (holds, violations)
    """
    # Map LHS values to RHS values
    lhs_to_rhs = defaultdict(set)

    for row in rows:
        if len(row) <= max(lhs_cols + [rhs_col]):
            continue  # Skip rows that don't have enough columns

        # Extract LHS values
        lhs_values = tuple(row[i] for i in lhs_cols)
        rhs_value = row[rhs_col]

        lhs_to_rhs[lhs_values].add(rhs_value)

    # Check for violations
    violations = []
    for lhs_val, rhs_vals in lhs_to_rhs.items():
        if len(rhs_vals) > 1:
            violations.append((lhs_val, rhs_vals))

    holds = len(violations) == 0
    return holds, violations

def check_minimality(rows, lhs_cols, rhs_col):
    """
    Check if FD is minimal (no redundant attributes on LHS).
    Returns (is_minimal, redundant_attrs)
    """
    redundant = []

    for i, col in enumerate(lhs_cols):
        # Try removing this column from LHS
        reduced_lhs = lhs_cols[:i] + lhs_cols[i+1:]
        if len(reduced_lhs) == 0:
            continue

        # Check if reduced FD still holds
        holds, _ = validate_fd(rows, reduced_lhs, rhs_col)
        if holds:
            redundant.append(col + 1)  # Convert back to 1-based

    is_minimal = len(redundant) == 0
    return is_minimal, redundant

def main():
    print("="*80)
    print("TASK SET 3: VALIDATION OF LLM-PROPOSED FUNCTIONAL DEPENDENCIES")
    print("="*80)

    results = {}

    for sample_file, data in sorted(LLM_PROPOSED_FDS.items()):
        dataset = sample_file.replace('_biased.csv', '').replace('_random.csv', '').replace('_stratified.csv', '')
        sample_type = 'biased' if 'biased' in sample_file else ('random' if 'random' in sample_file else 'stratified')

        # Paths
        sample_path = f'/home/user/DQ/samples/{sample_file}'
        full_path = f'/home/user/DQ/{dataset}.csv'

        print(f"\n{'='*80}")
        print(f"DATASET: {dataset.upper()} ({sample_type} sample)")
        print(f"{'='*80}")

        # Read data
        try:
            sample_rows = read_csv_data(sample_path)
            full_rows = read_csv_data(full_path)
        except Exception as e:
            print(f"ERROR reading files: {e}")
            continue

        print(f"Sample size: {len(sample_rows)} rows")
        print(f"Full dataset: {len(full_rows)} rows")

        dataset_results = []

        for fd_str in data['fds']:
            print(f"\n  Proposed FD: {fd_str}")

            lhs_cols, rhs_col = parse_fd(fd_str)
            if lhs_cols is None:
                print(f"    ⚠ Could not parse FD")
                continue

            # Validate on sample
            sample_holds, sample_violations = validate_fd(sample_rows, lhs_cols, rhs_col)
            print(f"    ✓ Holds on sample: {sample_holds}")
            if not sample_holds:
                print(f"      Violations: {len(sample_violations)}")

            # Validate on full dataset
            full_holds, full_violations = validate_fd(full_rows, lhs_cols, rhs_col)
            print(f"    {'✓' if full_holds else '✗'} Holds on full dataset: {full_holds}")
            if not full_holds:
                print(f"      Violations: {len(full_violations)}")
                print(f"      Example violation: {full_violations[0] if full_violations else 'N/A'}")

            # Check minimality (on full dataset if it holds)
            if full_holds:
                is_minimal, redundant = check_minimality(full_rows, lhs_cols, rhs_col)
                print(f"    {'✓' if is_minimal else '⚠'} Minimal: {is_minimal}")
                if not is_minimal:
                    print(f"      Redundant columns: {redundant}")

            # Classify
            classification = []
            if not full_holds:
                classification.append("FALSE POSITIVE")
            if full_holds and not is_minimal:
                classification.append("NON-MINIMAL")
            if len(lhs_cols) >= 6:
                classification.append("OVERFITTED (large LHS)")
            if len(lhs_cols) == 1 and sample_file.split('_')[0] == 'bridges' and lhs_cols[0] == 0:
                classification.append("ID-BASED (degenerate)")

            if classification:
                print(f"    ⚠ Classification: {', '.join(classification)}")
            else:
                print(f"    ✓ Classification: Valid and meaningful")

            dataset_results.append({
                'fd': fd_str,
                'sample_holds': sample_holds,
                'full_holds': full_holds,
                'is_minimal': is_minimal if full_holds else None,
                'redundant': redundant if full_holds else None,
                'classification': classification
            })

        results[f"{dataset}_{sample_type}"] = dataset_results

    # Summary
    print("\n" + "="*80)
    print("SUMMARY: FALSE POSITIVES AND ISSUES")
    print("="*80)

    false_positives = []
    non_minimal = []
    overfitted = []

    for key, res_list in results.items():
        for res in res_list:
            if not res['full_holds']:
                false_positives.append(f"{key}: {res['fd']}")
            if res['is_minimal'] is not None and not res['is_minimal']:
                non_minimal.append(f"{key}: {res['fd']} (redundant: {res['redundant']})")
            if 'OVERFITTED' in ' '.join(res['classification']):
                overfitted.append(f"{key}: {res['fd']}")

    print(f"\nFalse Positives: {len(false_positives)}")
    for fp in false_positives:
        print(f"  • {fp}")

    print(f"\nNon-Minimal FDs: {len(non_minimal)}")
    for nm in non_minimal:
        print(f"  • {nm}")

    print(f"\nOverfitted FDs (≥6 attrs on LHS): {len(overfitted)}")
    for ov in overfitted:
        print(f"  • {ov}")

    return results

if __name__ == "__main__":
    results = main()
