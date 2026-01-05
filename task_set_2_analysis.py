#!/usr/bin/env python3
"""
Task Set 2: LLM-Assisted Semantic FD Discovery

This script selects FDs for semantic evaluation and structures the analysis.
The actual LLM queries will be done interactively.
"""

import json

# Column name mappings based on UCI dataset documentation
COLUMN_NAMES = {
    'iris': {
        '1': 'sepal_length',
        '2': 'sepal_width',
        '3': 'petal_length',
        '4': 'petal_width',
        '5': 'species'
    },
    'bridges': {
        'E1': 'identifier',
        'M': 'material',
        '3': 'span',
        '1818': 'erected_year',
        'HIGHWAY': 'purpose',
        '?': 'length_missing',
        '2': 'lanes',
        'N': 'clear_g',
        'THROUGH': 'type',
        'WOOD': 'material_type',
        'SHORT': 'span_type',
        'S': 'rel_l'
    },
    'abalone': {
        '1': 'sex',
        '2': 'length',
        '3': 'diameter',
        '4': 'height',
        '5': 'whole_weight',
        '6': 'shucked_weight',
        '7': 'viscera_weight',
        '8': 'shell_weight',
        '9': 'rings'
    },
    'breast-cancer-wisconsin': {
        '1': 'id',
        '2': 'clump_thickness',
        '3': 'uniformity_cell_size',
        '4': 'uniformity_cell_shape',
        '5': 'marginal_adhesion',
        '6': 'class'
    },
    'hepatitis': {
        '1': 'class',
        '2': 'age',
        '3': 'sex',
        '4': 'steroid',
        '5': 'antivirals',
        '6': 'fatigue',
        '7': 'malaise',
        '8': 'anorexia'
    }
}

# Selected FDs for evaluation (from Task Set 1)
SELECTED_FDS = {
    'iris': {
        'plausible': [
            (['petal_length', 'petal_width', 'sepal_length'], 'species'),
            (['uniformity_cell_shape', 'petal_width', 'sepal_length'], 'species'),
            (['uniformity_cell_shape', 'petal_length', 'sepal_length'], 'species')
        ],
        'suspicious': [
            (['uniformity_cell_shape', 'petal_length', 'petal_width'], 'species')
        ]
    },
    'bridges': {
        'plausible': [],
        'suspicious': [
            (['identifier'], 'material'),
            (['identifier'], 'erected_year'),
            (['identifier'], 'purpose'),
            (['erected_year', 'span'], 'identifier'),
            (['length_missing', 'material_type', 'span'], 'clear_g')
        ]
    },
    'abalone': {
        'plausible': [
            (['viscera_weight', 'shell_weight', 'whole_weight'], 'sex'),
            (['diameter', 'whole_weight'], 'rings')
        ],
        'suspicious': [
            (['viscera_weight', 'shell_weight', 'whole_weight'], 'length'),
            (['shell_weight', 'shucked_weight', 'whole_weight'], 'height'),
            (['viscera_weight', 'diameter', 'whole_weight'], 'shell_weight')
        ]
    },
    'breast-cancer-wisconsin': {
        'plausible': [
            (['uniformity_cell_size'], 'uniformity_cell_shape'),
        ],
        'suspicious': [
            (['id'], 'clump_thickness'),
            (['id'], 'class'),
            (['uniformity_cell_size', 'id'], 'clump_thickness')
        ]
    }
}

def format_fd(lhs, rhs):
    """Format FD for display"""
    if isinstance(lhs, list):
        lhs_str = ", ".join(lhs)
    else:
        lhs_str = lhs
    return f"{lhs_str} → {rhs}"

def main():
    print("="*80)
    print("TASK SET 2: SELECTED FDs FOR SEMANTIC EVALUATION")
    print("="*80)

    for dataset, fds in SELECTED_FDS.items():
        print(f"\n{'='*80}")
        print(f"Dataset: {dataset.upper()}")
        print(f"{'='*80}")

        if fds.get('plausible'):
            print(f"\n✓ PLAUSIBLE FDs (Expected to make semantic sense):")
            for lhs, rhs in fds['plausible']:
                print(f"  • {format_fd(lhs, rhs)}")

        if fds.get('suspicious'):
            print(f"\n⚠ SUSPICIOUS FDs (Structurally identified as problematic):")
            for lhs, rhs in fds['suspicious']:
                print(f"  • {format_fd(lhs, rhs)}")

    print("\n" + "="*80)
    print("EVALUATION QUESTIONS FOR EACH FD:")
    print("="*80)
    print("""
For each FD above, we will ask:

1. "Does this functional dependency make sense in the real world?"
2. "Is this relationship meaningful or coincidental?"
3. Classify as:
   - meaningful: Real-world constraint/relationship
   - accidental: Happens to hold in this data sample
   - encoding-based: Information embedded in codes/IDs
   - degenerate: Trivial (ID determines everything)
   - unlikely: Implausible relationship

Output format:
| FD | LLM Judgment | Manual Judgment | Agreement? | Notes |
    """)

if __name__ == "__main__":
    main()
