#!/usr/bin/env python3
"""
Task Set 3 - FD Hypothesis Generation and Validation
Generate FD hypotheses from samples and validate against full dataset

CRITICAL: Hypotheses generated from SAMPLE ONLY, without seeing full dataset or known FDs
"""

import pandas as pd
import json
from pathlib import Path
from itertools import combinations
import numpy as np

class FDHypothesisGenerator:
    """Generate and validate FD hypotheses from sample data"""

    def __init__(self, dataset_name, sample_type):
        self.dataset_name = dataset_name
        self.sample_type = sample_type
        self.sample_path = f"/home/user/DQ/task3_samples/{dataset_name}_{sample_type}.csv"
        self.full_data_path = f"/home/user/DQ/{dataset_name}.csv"
        self.sample_df = None
        self.full_df = None
        self.hypotheses = []

    def load_data(self):
        """Load sample and full dataset"""
        try:
            # Load sample
            self.sample_df = pd.read_csv(self.sample_path)

            # Load full dataset
            self.full_df = pd.read_csv(self.full_data_path)

            # Ensure column names match
            if len(self.full_df.columns) == len(self.sample_df.columns):
                self.full_df.columns = self.sample_df.columns

            print(f"  Loaded sample: {len(self.sample_df)} rows")
            print(f"  Loaded full dataset: {len(self.full_df)} rows")
            return True
        except Exception as e:
            print(f"  Error loading data: {e}")
            return False

    def check_fd_on_data(self, lhs_cols, rhs_col, df):
        """Check if LHS → RHS holds on given dataframe"""
        if not lhs_cols:  # Empty LHS
            # Check if RHS is constant
            return df[rhs_col].nunique() == 1

        try:
            # Group by LHS columns
            grouped = df.groupby(list(lhs_cols))[rhs_col].nunique()

            # FD holds if each LHS value maps to exactly one RHS value
            return (grouped == 1).all()
        except Exception as e:
            return False

    def generate_hypotheses_from_sample(self, max_lhs_size=3):
        """Generate FD hypotheses by analyzing the sample"""
        columns = list(self.sample_df.columns)
        hypotheses = []

        # For each potential RHS
        for rhs in columns:
            other_cols = [c for c in columns if c != rhs]

            # Try different LHS sizes (1 to max_lhs_size)
            for lhs_size in range(1, min(max_lhs_size + 1, len(other_cols) + 1)):
                for lhs_tuple in combinations(other_cols, lhs_size):
                    lhs = list(lhs_tuple)

                    # Check if FD holds on sample
                    if self.check_fd_on_data(lhs, rhs, self.sample_df):
                        hypotheses.append({
                            'lhs': lhs,
                            'rhs': rhs,
                            'lhs_size': len(lhs),
                            'source': 'sample_observation'
                        })

        # Also check for constant columns (empty LHS)
        for col in columns:
            if self.sample_df[col].nunique() == 1:
                hypotheses.append({
                    'lhs': [],
                    'rhs': col,
                    'lhs_size': 0,
                    'source': 'constant_in_sample'
                })

        return hypotheses

    def validate_hypothesis(self, hypothesis):
        """Validate a hypothesis against the full dataset"""
        lhs = hypothesis['lhs']
        rhs = hypothesis['rhs']

        # Check on sample
        holds_on_sample = self.check_fd_on_data(lhs, rhs, self.sample_df)

        # Check on full dataset
        holds_on_full = self.check_fd_on_data(lhs, rhs, self.full_df)

        # Classify the hypothesis
        if holds_on_sample and holds_on_full:
            classification = "TRUE_POSITIVE"  # Correct hypothesis
        elif holds_on_sample and not holds_on_full:
            classification = "FALSE_POSITIVE"  # Misleading sample
        elif not holds_on_sample and holds_on_full:
            classification = "IMPOSSIBLE"  # Should not happen
        else:
            classification = "FALSE_NEGATIVE"  # Doesn't hold anywhere

        return {
            'lhs': lhs,
            'rhs': rhs,
            'lhs_size': len(lhs),
            'holds_on_sample': holds_on_sample,
            'holds_on_full': holds_on_full,
            'classification': classification,
            'source': hypothesis.get('source', 'unknown')
        }

    def analyze_minimality(self, validated_hypotheses):
        """Check which FDs are non-minimal (can be reduced)"""
        true_fds = [h for h in validated_hypotheses if h['classification'] == 'TRUE_POSITIVE']

        non_minimal = []
        for fd in true_fds:
            if fd['lhs_size'] <= 1:
                continue  # Single attribute or empty LHS is minimal by definition

            lhs = fd['lhs']
            rhs = fd['rhs']

            # Check if any subset of LHS also determines RHS
            for subset_size in range(len(lhs)):
                for subset_tuple in combinations(lhs, subset_size):
                    subset = list(subset_tuple)
                    if self.check_fd_on_data(subset, rhs, self.full_df):
                        non_minimal.append({
                            'fd': f"{lhs} → {rhs}",
                            'lhs': lhs,
                            'rhs': rhs,
                            'minimal_lhs': subset,
                            'reduced_by': len(lhs) - len(subset)
                        })
                        break

        return non_minimal

    def run_analysis(self):
        """Complete analysis: generate hypotheses and validate"""
        print(f"\n{'='*80}")
        print(f"Dataset: {self.dataset_name} | Sample: {self.sample_type}")
        print('='*80)

        if not self.load_data():
            return None

        # Generate hypotheses from sample (limited to reasonable size)
        print(f"\n  Generating FD hypotheses from sample...")
        raw_hypotheses = self.generate_hypotheses_from_sample(max_lhs_size=3)
        print(f"  Found {len(raw_hypotheses)} potential FDs in sample")

        # Validate all hypotheses
        print(f"\n  Validating hypotheses against full dataset...")
        validated = []
        for hyp in raw_hypotheses:
            result = self.validate_hypothesis(hyp)
            validated.append(result)

        # Count classifications
        classifications = {}
        for v in validated:
            cls = v['classification']
            classifications[cls] = classifications.get(cls, 0) + 1

        print(f"\n  Validation Results:")
        for cls, count in sorted(classifications.items()):
            print(f"    {cls}: {count}")

        # Analyze minimality
        non_minimal = self.analyze_minimality(validated)
        if non_minimal:
            print(f"\n  Non-minimal FDs: {len(non_minimal)}")

        return {
            'dataset': self.dataset_name,
            'sample_type': self.sample_type,
            'sample_size': len(self.sample_df),
            'full_size': len(self.full_df),
            'total_hypotheses': len(raw_hypotheses),
            'validation_results': classifications,
            'validated_hypotheses': validated[:20],  # Save first 20 for inspection
            'non_minimal_fds': non_minimal[:10],  # Save first 10
            'false_positive_rate': classifications.get('FALSE_POSITIVE', 0) / len(validated) if validated else 0
        }

def analyze_all_samples():
    """Analyze all dataset samples"""
    datasets = [
        'iris', 'balance-scale', 'chess', 'abalone', 'nursery',
        'breast-cancer-wisconsin', 'bridges', 'echocardiogram', 'hepatitis'
    ]

    sample_types = ['random', 'stratified', 'biased']

    all_results = []

    for dataset in datasets:
        for sample_type in sample_types:
            generator = FDHypothesisGenerator(dataset, sample_type)
            result = generator.run_analysis()
            if result:
                all_results.append(result)

    # Save results
    output_path = Path("/home/user/DQ/task3_hypothesis_validation.json")
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\n{'='*80}")
    print(f"Analysis complete! Results saved to: {output_path}")
    print('='*80)

    # Summary statistics
    print(f"\n{'='*80}")
    print("SUMMARY STATISTICS")
    print('='*80)

    total_hypotheses = sum(r['total_hypotheses'] for r in all_results)
    total_false_positives = sum(r['validation_results'].get('FALSE_POSITIVE', 0) for r in all_results)
    total_true_positives = sum(r['validation_results'].get('TRUE_POSITIVE', 0) for r in all_results)

    print(f"Total hypotheses generated: {total_hypotheses}")
    print(f"True positives (valid FDs): {total_true_positives}")
    print(f"False positives (sample artifacts): {total_false_positives}")

    if total_hypotheses > 0:
        fp_rate = total_false_positives / total_hypotheses * 100
        print(f"Overall false positive rate: {fp_rate:.1f}%")

    return all_results

if __name__ == "__main__":
    print("Task Set 3 - FD Hypothesis Generation from Samples")
    print("="*80)
    print("\nCRITICAL: Generating hypotheses from SAMPLES ONLY")
    print("NOT using pre-computed FD lists or full datasets for generation!\n")

    results = analyze_all_samples()
