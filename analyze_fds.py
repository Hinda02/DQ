#!/usr/bin/env python3
"""
Task Set 1: Interpreting Algorithmic FDs
Structural analysis of functional dependencies without semantic interpretation
"""

import json
import re
from collections import defaultdict, Counter
from pathlib import Path

def parse_simple_format(lines):
    """Parse simple format FDs like: 3,2,1->5"""
    fds = []
    in_results = False
    for line in lines:
        line = line.strip()
        if line == "# RESULTS":
            in_results = True
            continue
        if in_results and line and not line.startswith("#"):
            if "->" in line:
                parts = line.split("->")
                lhs = parts[0].strip().split(",")
                rhs = parts[1].strip()
                fds.append((lhs, rhs))
    return fds

def parse_json_format(lines):
    """Parse JSON format FDs"""
    fds = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            fd_obj = json.loads(line)
            if fd_obj.get("type") == "FunctionalDependency":
                lhs_cols = [c["columnIdentifier"] for c in fd_obj["determinant"]["columnIdentifiers"]]
                rhs_col = fd_obj["dependant"]["columnIdentifier"]
                fds.append((lhs_cols, rhs_col))
        except:
            pass
    return fds

def analyze_fds(dataset_name, fds):
    """Analyze FD characteristics"""
    if not fds:
        return None

    num_fds = len(fds)
    lhs_sizes = [len(lhs) for lhs, _ in fds]
    avg_lhs_size = sum(lhs_sizes) / len(lhs_sizes) if lhs_sizes else 0
    max_lhs_size = max(lhs_sizes) if lhs_sizes else 0
    min_lhs_size = min(lhs_sizes) if lhs_sizes else 0

    # Attribute frequency
    lhs_attrs = Counter()
    rhs_attrs = Counter()
    all_attrs = set()

    for lhs, rhs in fds:
        for attr in lhs:
            lhs_attrs[attr] += 1
            all_attrs.add(attr)
        rhs_attrs[rhs] += 1
        all_attrs.add(rhs)

    # Identify patterns
    single_attr_determinants = [fd for fd in fds if len(fd[0]) == 1]
    large_determinants = [fd for fd in fds if len(fd[0]) >= 4]

    # ID-like patterns: single attribute that determines many others
    potential_ids = []
    for attr in all_attrs:
        attr_as_single_det = [(lhs, rhs) for lhs, rhs in single_attr_determinants if lhs[0] == attr]
        if len(attr_as_single_det) >= 3:  # Determines 3+ attributes
            potential_ids.append((attr, len(attr_as_single_det)))

    # Attributes that appear very frequently on LHS
    freq_lhs_attrs = [(attr, count) for attr, count in lhs_attrs.most_common(5)]

    # Attributes that appear very frequently on RHS
    freq_rhs_attrs = [(attr, count) for attr, count in rhs_attrs.most_common(5)]

    return {
        'dataset': dataset_name,
        'num_fds': num_fds,
        'avg_lhs_size': round(avg_lhs_size, 2),
        'min_lhs_size': min_lhs_size,
        'max_lhs_size': max_lhs_size,
        'num_single_det': len(single_attr_determinants),
        'num_large_det': len(large_determinants),
        'potential_ids': potential_ids,
        'top_lhs_attrs': freq_lhs_attrs,
        'top_rhs_attrs': freq_rhs_attrs,
        'total_attrs': len(all_attrs)
    }

def main():
    datasets = [
        'iris', 'balance-scale', 'chess', 'abalone', 'nursery',
        'breast-cancer-wisconsin', 'bridges', 'echocardiogram',
        'adult', 'hepatitis', 'horse'
    ]

    results = []

    for dataset in datasets:
        fds_file = Path(f'/home/user/DQ/{dataset}_fds')
        if not fds_file.exists():
            print(f"⚠ {dataset}: FDS file not found")
            continue

        with open(fds_file, 'r') as f:
            lines = f.readlines()

        # Try to determine format and parse
        first_line = lines[0].strip() if lines else ""

        if first_line.startswith('{'):
            fds = parse_json_format(lines)
        elif first_line.startswith('#'):
            fds = parse_simple_format(lines)
        else:
            print(f"⚠ {dataset}: Unknown format")
            continue

        analysis = analyze_fds(dataset, fds)
        if analysis:
            results.append(analysis)
            print(f"✓ {dataset}: {analysis['num_fds']} FDs analyzed")

    # Generate report
    print("\n" + "="*80)
    print("TASK SET 1: STRUCTURAL ANALYSIS OF FUNCTIONAL DEPENDENCIES")
    print("="*80)
    print("\nNOTE: This is a purely STRUCTURAL analysis - no semantic interpretation")
    print("\n" + "-"*80)

    for r in results:
        print(f"\nDataset: {r['dataset']}")
        print(f"  Total FDs: {r['num_fds']}")
        print(f"  Avg LHS size: {r['avg_lhs_size']} (range: {r['min_lhs_size']}-{r['max_lhs_size']})")
        print(f"  Single-attribute determinants: {r['num_single_det']}")
        print(f"  Large determinants (≥4 attrs): {r['num_large_det']}")
        print(f"  Total unique attributes: {r['total_attrs']}")

        if r['potential_ids']:
            print(f"  ⚠ Potential ID-like attributes (single attr → many):")
            for attr, count in r['potential_ids']:
                print(f"      '{attr}' determines {count} other attributes")

        if r['top_lhs_attrs']:
            print(f"  Most frequent LHS attributes:")
            for attr, count in r['top_lhs_attrs'][:3]:
                print(f"      '{attr}': appears in {count} FDs")

        if r['num_large_det'] > 0:
            print(f"  ⚠ SUSPICIOUS: {r['num_large_det']} FDs with ≥4 attributes on LHS (potential overfitting)")

        if r['num_fds'] > 100:
            print(f"  ⚠ SUSPICIOUS: Very large number of FDs ({r['num_fds']})")

    print("\n" + "="*80)
    print("SUSPICIOUS PATTERNS IDENTIFIED (Structural Only):")
    print("="*80)

    for r in results:
        suspicious = []

        if r['potential_ids']:
            suspicious.append(f"ID-like pattern detected ({len(r['potential_ids'])} candidates)")

        if r['num_large_det'] > 10:
            suspicious.append(f"Many large determinants ({r['num_large_det']})")

        if r['num_fds'] > 1000:
            suspicious.append(f"Extremely high FD count ({r['num_fds']})")

        if r['avg_lhs_size'] > 3:
            suspicious.append(f"High avg LHS size ({r['avg_lhs_size']})")

        if suspicious:
            print(f"\n{r['dataset']}:")
            for s in suspicious:
                print(f"  • {s}")

    # Summary table
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    print(f"{'Dataset':<25} {'#FDs':<10} {'Avg LHS':<10} {'Max LHS':<10} {'Single Det':<12}")
    print("-"*80)
    for r in results:
        print(f"{r['dataset']:<25} {r['num_fds']:<10} {r['avg_lhs_size']:<10} {r['max_lhs_size']:<10} {r['num_single_det']:<12}")

if __name__ == "__main__":
    main()
