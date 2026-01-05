#!/usr/bin/env python3
"""
Detailed analysis of specific suspicious FDs with examples
"""

import json
from pathlib import Path

def get_sample_fds(dataset, fds, num=5):
    """Get sample FDs to show examples"""
    return fds[:num]

def analyze_bridges_detailed():
    """Detailed analysis of bridges dataset - has ID pattern"""
    with open('/home/user/DQ/bridges_fds', 'r') as f:
        lines = f.readlines()

    fds = []
    for line in lines:
        line = line.strip()
        if line:
            try:
                fd_obj = json.loads(line)
                lhs_cols = [c["columnIdentifier"] for c in fd_obj["determinant"]["columnIdentifiers"]]
                rhs_col = fd_obj["dependant"]["columnIdentifier"]
                fds.append((lhs_cols, rhs_col))
            except:
                pass

    print("\n" + "="*80)
    print("DETAILED ANALYSIS: bridges dataset")
    print("="*80)

    # Find E1 as single determinant
    e1_determines = [rhs for lhs, rhs in fds if lhs == ['E1']]
    print(f"\n⚠ ID-LIKE PATTERN: Attribute 'E1' determines {len(e1_determines)} attributes:")
    for rhs in e1_determines[:10]:
        print(f"   E1 → {rhs}")
    print("   [Pattern: Single attribute determines many others - typical ID behavior]")

    # Large determinants
    large = [(lhs, rhs) for lhs, rhs in fds if len(lhs) >= 5]
    print(f"\n⚠ LARGE DETERMINANTS: {len(large)} FDs with ≥5 attributes on LHS")
    print("   Examples:")
    for lhs, rhs in large[:5]:
        lhs_str = ", ".join(lhs)
        print(f"   {lhs_str} → {rhs}")
    print("   [Pattern: Overfitted - too many attributes needed to determine one]")

def analyze_echocardiogram_detailed():
    """Detailed analysis of echocardiogram - 527 FDs"""
    with open('/home/user/DQ/echocardiogram_fds', 'r') as f:
        lines = f.readlines()

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

    print("\n" + "="*80)
    print("DETAILED ANALYSIS: echocardiogram dataset")
    print("="*80)
    print(f"\nTotal FDs: {len(fds)} (very high for 13 columns)")

    # Empty LHS
    empty_lhs = [fd for fd in fds if not fd[0] or fd[0] == ['']]
    if empty_lhs:
        print(f"\n⚠ DEGENERATE: {len(empty_lhs)} FDs with empty LHS (constant values):")
        for lhs, rhs in empty_lhs[:3]:
            print(f"   (empty) → {rhs}")
        print("   [Pattern: Column has constant value across all rows]")

    # Attribute 8 appears in many FDs
    attr8_lhs = [(lhs, rhs) for lhs, rhs in fds if '8' in lhs]
    print(f"\n⚠ FREQUENT ATTRIBUTE: Column '8' appears in {len(attr8_lhs)} FDs")
    print("   Sample FDs involving column 8:")
    for lhs, rhs in attr8_lhs[:5]:
        lhs_str = ", ".join(lhs)
        print(f"   {lhs_str} → {rhs}")
    print("   [Pattern: Column appears in majority of FDs - possibly ID or encoding]")

def analyze_hepatitis_detailed():
    """Detailed analysis of hepatitis - 8,296 FDs!"""
    with open('/home/user/DQ/hepatitis_fds', 'r') as f:
        lines = f.readlines()

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

    print("\n" + "="*80)
    print("DETAILED ANALYSIS: hepatitis dataset")
    print("="*80)
    print(f"\n⚠ EXTREME CASE: {len(fds)} FDs for only 20 columns!")
    print(f"   This dataset has {len(fds)} FDs - extremely high")
    print(f"   Ratio: {len(fds)/20:.1f} FDs per column")

    # Sample FDs with different LHS sizes
    by_size = {}
    for lhs, rhs in fds:
        size = len(lhs)
        if size not in by_size:
            by_size[size] = []
        by_size[size].append((lhs, rhs))

    print("\n   Distribution by LHS size:")
    for size in sorted(by_size.keys()):
        count = len(by_size[size])
        print(f"   LHS size {size}: {count} FDs ({100*count/len(fds):.1f}%)")

    print("\n   Examples of different complexity:")
    for size in sorted(by_size.keys())[:4]:
        lhs, rhs = by_size[size][0]
        lhs_str = ", ".join(lhs)
        print(f"   Size {size}: {lhs_str} → {rhs}")

    print("\n   [Pattern: Combinatorial explosion - many attribute combinations]")

def analyze_chess_nursery():
    """Analyze datasets with 6-7 attribute determinants"""
    print("\n" + "="*80)
    print("DETAILED ANALYSIS: chess & nursery (ALL attributes → 1)")
    print("="*80)

    # Chess
    with open('/home/user/DQ/chess_fds', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if "->" in line:
            print(f"\nChess dataset (7 columns):")
            print(f"   FD: {line.strip()}")
            print(f"   [Pattern: ALL 6 attributes needed to determine 1 - entire row is key]")

    # Nursery
    with open('/home/user/DQ/nursery_fds', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if '"type":"FunctionalDependency"' in line:
            obj = json.loads(line)
            lhs = [c["columnIdentifier"] for c in obj["determinant"]["columnIdentifiers"]]
            rhs = obj["dependant"]["columnIdentifier"]
            print(f"\nNursery dataset (9 columns):")
            print(f"   FD: {', '.join(lhs)} → {rhs}")
            print(f"   [Pattern: ALL 7 attributes needed to determine 1 - nearly entire row is key]")

def main():
    print("\n" + "="*80)
    print("TASK SET 1: DETAILED EXAMINATION OF SUSPICIOUS FUNCTIONAL DEPENDENCIES")
    print("="*80)
    print("\nStructural patterns identified WITHOUT semantic interpretation:")

    analyze_bridges_detailed()
    analyze_echocardiogram_detailed()
    analyze_hepatitis_detailed()
    analyze_chess_nursery()

    print("\n" + "="*80)
    print("SUMMARY OF STRUCTURAL SUSPICIONS")
    print("="*80)
    print("""
1. ID-BASED FDs: Single attribute determines many others
   - bridges: 'E1' → 12 attributes
   - Pattern suggests unique identifier

2. DEGENERATE FDs: Empty or minimal LHS
   - echocardiogram: Some FDs with empty determinant
   - Indicates constant column values

3. OVERFITTED FDs: Very large LHS (4-7 attributes)
   - chess: 6 → 1 (entire row minus one column)
   - nursery: 7 → 1 (entire row minus one column)
   - hepatitis: 5,229 FDs with ≥4 attributes
   - Pattern suggests combinatorial explosion or no true dependencies

4. EXCESSIVE FD COUNT:
   - hepatitis: 8,296 FDs (for 20 columns!)
   - echocardiogram: 527 FDs (for 13 columns)
   - Pattern suggests data quality issues or spurious correlations

5. FREQUENT ATTRIBUTES: Appear in majority of FDs
   - echocardiogram: column '8' in 312/527 FDs (59%)
   - hepatitis: column '1' in 8,011/8,296 FDs (97%)
   - Could indicate ID, encoding, or data artifact

NOTE: These are structural observations only. Task Set 2 will use LLMs
to assess semantic plausibility of selected FDs.
    """)

if __name__ == "__main__":
    main()
