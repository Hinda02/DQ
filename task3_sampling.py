#!/usr/bin/env python3
"""
Task Set 3 - Sampling and FD Hypotheses
Create random and stratified samples for LLM FD hypothesis generation

CRITICAL: Do NOT show full dataset or FD list to LLM
Only show sample data and ask for likely FDs
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

class DatasetSampler:
    """Create random and stratified samples for FD hypothesis testing"""

    def __init__(self, dataset_name, max_sample_size=50):
        self.dataset_name = dataset_name
        self.max_sample_size = max_sample_size
        self.csv_path = f"/home/user/DQ/{dataset_name}.csv"
        self.df = None
        self.samples = {}

    def load_data(self):
        """Load CSV data"""
        try:
            # Try to load without headers first
            self.df = pd.read_csv(self.csv_path, header=None)

            # Check if first row looks like header (contains letters)
            first_row = self.df.iloc[0].astype(str)
            if any(any(c.isalpha() for c in str(val)) for val in first_row):
                # Reload with header
                self.df = pd.read_csv(self.csv_path)
            else:
                # Use generic column names
                self.df.columns = [f"col_{i+1}" for i in range(len(self.df.columns))]

            print(f"Loaded {self.dataset_name}: {len(self.df)} rows, {len(self.df.columns)} columns")
            return True
        except Exception as e:
            print(f"Error loading {self.dataset_name}: {e}")
            return False

    def create_random_sample(self, n=None):
        """Create random sample (uniform distribution)"""
        if n is None:
            n = min(self.max_sample_size, len(self.df))

        sample = self.df.sample(n=n, random_state=42)
        self.samples['random'] = sample

        print(f"  Random sample: {len(sample)} rows")
        return sample

    def create_stratified_sample(self, n=None):
        """Create stratified sample based on last column (often the class/target)"""
        if n is None:
            n = min(self.max_sample_size, len(self.df))

        # Use last column for stratification (often the target variable)
        last_col = self.df.columns[-1]

        try:
            # Get value counts for stratification
            value_counts = self.df[last_col].value_counts()

            # Calculate samples per class (proportional)
            samples_per_class = {}
            total_classes = len(value_counts)

            for value, count in value_counts.items():
                # Proportional allocation
                proportion = count / len(self.df)
                samples_per_class[value] = max(1, int(n * proportion))

            # Adjust to exactly n samples
            total_allocated = sum(samples_per_class.values())
            if total_allocated > n:
                # Reduce largest class
                largest_class = max(samples_per_class, key=samples_per_class.get)
                samples_per_class[largest_class] -= (total_allocated - n)

            # Sample from each class
            stratified_samples = []
            for value, sample_size in samples_per_class.items():
                class_data = self.df[self.df[last_col] == value]
                if len(class_data) >= sample_size:
                    sample = class_data.sample(n=sample_size, random_state=42)
                else:
                    sample = class_data  # Take all if not enough
                stratified_samples.append(sample)

            sample = pd.concat(stratified_samples).sample(frac=1, random_state=42)  # Shuffle
            self.samples['stratified'] = sample

            print(f"  Stratified sample: {len(sample)} rows (stratified by {last_col})")
            return sample

        except Exception as e:
            print(f"  Stratification failed: {e}, using random sample instead")
            return self.create_random_sample(n)

    def create_biased_sample(self, n=None):
        """Create biased sample (e.g., only specific values, outliers, etc.)"""
        if n is None:
            n = min(self.max_sample_size, len(self.df))

        # Strategy: Sample from extreme/unusual values
        # Bias toward first and last rows (temporal/insertion order bias)

        first_quarter = len(self.df) // 4
        last_quarter = len(self.df) - (len(self.df) // 4)

        # Take mostly from beginning and end (temporal bias)
        first_part = self.df.iloc[:first_quarter].sample(n=n//2, random_state=42, replace=len(self.df[:first_quarter]) < n//2)
        last_part = self.df.iloc[last_quarter:].sample(n=n//2, random_state=42, replace=len(self.df[last_quarter:]) < n//2)

        sample = pd.concat([first_part, last_part]).sample(frac=1, random_state=42)
        self.samples['biased'] = sample

        print(f"  Biased sample: {len(sample)} rows (temporal bias: first/last quarters)")
        return sample

    def create_cluster_sample(self, n=None):
        """Create cluster-based sample (geographic/group clustering)"""
        if n is None:
            n = min(self.max_sample_size, len(self.df))

        # Strategy: Sample heavily from one category
        last_col = self.df.columns[-1]

        try:
            # Find most common value
            most_common = self.df[last_col].value_counts().index[0]

            # Take 80% from most common, 20% from others
            common_samples = self.df[self.df[last_col] == most_common].sample(
                n=min(int(n * 0.8), len(self.df[self.df[last_col] == most_common])),
                random_state=42
            )
            other_samples = self.df[self.df[last_col] != most_common].sample(
                n=min(int(n * 0.2), len(self.df[self.df[last_col] != most_common])),
                random_state=42
            )

            sample = pd.concat([common_samples, other_samples]).sample(frac=1, random_state=42)
            self.samples['cluster'] = sample

            print(f"  Cluster sample: {len(sample)} rows (80% from '{most_common}')")
            return sample

        except Exception as e:
            print(f"  Clustering failed: {e}, using random sample instead")
            return self.create_random_sample(n)

    def save_samples(self):
        """Save samples to files"""
        output_dir = Path("/home/user/DQ/task3_samples")
        output_dir.mkdir(exist_ok=True)

        for sample_type, sample in self.samples.items():
            # Save as CSV
            csv_path = output_dir / f"{self.dataset_name}_{sample_type}.csv"
            sample.to_csv(csv_path, index=False)

            # Save metadata
            metadata = {
                'dataset': self.dataset_name,
                'sample_type': sample_type,
                'sample_size': len(sample),
                'original_size': len(self.df),
                'columns': list(sample.columns),
                'sample_rows': sample.head(10).to_dict(orient='records')
            }

            json_path = output_dir / f"{self.dataset_name}_{sample_type}.json"
            with open(json_path, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)

        print(f"  Saved {len(self.samples)} samples to {output_dir}/")


def sample_all_datasets():
    """Create samples for all datasets"""
    datasets = [
        'iris', 'balance-scale', 'chess', 'abalone', 'nursery',
        'breast-cancer-wisconsin', 'bridges', 'echocardiogram', 'hepatitis'
    ]

    all_samples = {}

    for dataset in datasets:
        print(f"\n{'='*80}")
        print(f"Sampling: {dataset}")
        print('='*80)

        sampler = DatasetSampler(dataset, max_sample_size=50)

        if sampler.load_data():
            # Create different sample types
            sampler.create_random_sample(n=min(50, len(sampler.df)))
            sampler.create_stratified_sample(n=min(50, len(sampler.df)))
            sampler.create_biased_sample(n=min(50, len(sampler.df)))

            # Save samples
            sampler.save_samples()

            all_samples[dataset] = {
                'total_rows': len(sampler.df),
                'total_columns': len(sampler.df.columns),
                'samples_created': list(sampler.samples.keys()),
                'column_names': list(sampler.df.columns)
            }
        else:
            print(f"  Skipped {dataset} (failed to load)")

    # Save summary
    summary_path = Path("/home/user/DQ/task3_samples/sampling_summary.json")
    with open(summary_path, 'w') as f:
        json.dump(all_samples, f, indent=2)

    print(f"\n{'='*80}")
    print(f"Sampling complete! Summary saved to: {summary_path}")
    print('='*80)

    return all_samples


if __name__ == "__main__":
    print("Task Set 3 - Sampling for FD Hypothesis Generation")
    print("="*80)
    print("\nIMPORTANT: These samples will be shown to LLM WITHOUT full dataset or FD list!")
    print("LLM will generate FD hypotheses from limited data only.\n")

    samples = sample_all_datasets()

    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("1. Show samples to LLM (NOT full dataset)")
    print("2. Ask: 'What functional dependencies might exist in this data?'")
    print("3. Collect FD hypotheses")
    print("4. Validate against full dataset")
    print("5. Analyze false positives and sampling bias")
    print("="*80)
