#!/usr/bin/env python3
"""
Parse FDs_summary.xlsx and extract LLM-proposed functional dependencies
"""

# Parsed from Excel sharedStrings.xml and sheet1.xml
LLM_PROPOSED_FDS = {
    'abalone_biased.csv': {
        'rows': 45,
        'fds': ['(1,2,3,4,5,6,7,8) → 9']
    },
    'abalone_random.csv': {
        'rows': 34,
        'fds': ['(1,2,3,4,5,6,7,8) → 9']
    },
    'abalone_stratified.csv': {
        'rows': 33,
        'fds': ['(1,2,3,4,5,6,7,8) → 9']
    },
    'balance-scale_biased.csv': {
        'rows': 48,
        'fds': ['(1,3,4,5) → 2', '(2,3,4,5) → 1']
    },
    'balance-scale_random.csv': {
        'rows': 48,
        'fds': ['(2,3,4,5) → 1']
    },
    'breast-cancer-wisconsin_biased.csv': {
        'rows': 41,
        'fds': ['(1,2,3,4,5,6,7,8,9,10) → 11']
    },
    'breast-cancer-wisconsin_random.csv': {
        'rows': 46,
        'fds': ['(1,2,3,4,5,6,7,8,9,10) → 11']
    },
    'bridges_stratified.csv': {
        'rows': 45,
        'fds': ['1 → 2', '(3,4,5,6,7,8,9,10,11,12) → 13']
    },
    'bridges_random.csv': {
        'rows': 45,
        'fds': ['1 → 2', '(3,4,5,6,7,8,9,10,11,12) → 13']
    },
    'chess_stratified.csv': {
        'rows': 46,
        'fds': ['(1,2,3,4,5,6) → 7']
    },
    'chess_random.csv': {
        'rows': 46,
        'fds': ['(1,2,3,4,5,6) → 7']
    },
    'echocardiogram_biased.csv': {
        'rows': 46,
        'fds': ['(1,2,3,4,5,6,7,8,9,10,11) → 12']
    },
    'echocardiogram_random.csv': {
        'rows': 46,
        'fds': ['(1,2,3,4,5,6,7,8,9,10,11) → 12']
    },
    'hepatitis_stratified.csv': {
        'rows': 45,
        'fds': ['(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19) → 20']
    },
    'hepatitis_random.csv': {
        'rows': 45,
        'fds': ['(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19) → 20']
    },
    'iris_biased.csv': {
        'rows': 45,
        'fds': ['(1,2,3,4) → 5']
    },
    'iris_random.csv': {
        'rows': 45,
        'fds': ['(1,2,3,4) → 5']
    },
    'nursery_stratified.csv': {
        'rows': 45,
        'fds': ['8 → 9']  # From shared strings index 0
    },
    'nursery_random.csv': {
        'rows': 45,
        'fds': ['8 → 9']  # From shared strings index 0
    }
}

def print_summary():
    print("="*80)
    print("LLM-PROPOSED FUNCTIONAL DEPENDENCIES FROM SAMPLES")
    print("="*80)
    print("\nParsed from FDs_summary.xlsx")
    print("\nFormat: Sample File | Rows | LLM-Proposed FDs")
    print("-"*80)

    for sample_file, data in sorted(LLM_PROPOSED_FDS.items()):
        dataset = sample_file.replace('_biased.csv', '').replace('_random.csv', '').replace('_stratified.csv', '')
        sample_type = 'biased' if 'biased' in sample_file else ('random' if 'random' in sample_file else 'stratified')

        print(f"\n{dataset.upper()} ({sample_type} sample, {data['rows']} rows):")
        for fd in data['fds']:
            print(f"  • {fd}")

if __name__ == "__main__":
    print_summary()
