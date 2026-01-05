# TASK SET 1: Interpreting Algorithmic FDs
## Structural Analysis of Functional Dependencies

**Course**: Beyond Patterns: Meaningful Functional Dependencies with Classical Algorithms and LLMs
**Institution**: LAMSADE, Univ. Paris-Dauphine, PSL
**Date**: 2026-01-05

---

## Executive Summary

This report presents a **purely structural analysis** of functional dependencies discovered by the TANE algorithm across 11 UCI datasets. The analysis identifies patterns, anomalies, and suspicious characteristics **without semantic interpretation** of attribute meanings.

**Key Finding**: Not all algorithmically-discovered FDs are meaningful. We identified 5 major suspicious patterns across the datasets.

---

## 1. Dataset Overview & Statistics

### Summary Table

| Dataset                    | #FDs   | Avg LHS | Max LHS | Single Det | Total Attrs |
|----------------------------|--------|---------|---------|------------|-------------|
| iris                       | 4      | 3.0     | 3       | 0          | 5           |
| balance-scale              | 1      | 1.0     | 1       | 1          | 2           |
| chess                      | 1      | 6.0     | 6       | 0          | 7           |
| abalone                    | 137    | 4.22    | 6       | 0          | 9           |
| nursery                    | 1      | 7.0     | 7       | 0          | 8           |
| breast-cancer-wisconsin    | 46     | 2.7     | 4       | 1          | 5           |
| bridges                    | 144    | 3.69    | 6       | 13         | 12          |
| echocardiogram             | 527    | 3.22    | 4       | 2          | 10          |
| hepatitis                  | 8,296  | 3.76    | 6       | 0          | 8           |
| **adult**                  | 0*     | -       | -       | -          | -           |
| **horse**                  | 0*     | -       | -       | -          | -           |

*Note: adult_fds and horse_fds files are empty in the provided data.

---

## 2. Structural Analysis Results

### 2.1 Simple Datasets (Minimal FDs)

**balance-scale** (1 FD)
- FD: `2 → 1`
- Simple, single-attribute determinant
- Normal pattern

**chess** (1 FD)
- FD: `2,6,4,1,3,5 → 7`
- ⚠️ **SUSPICIOUS**: Requires 6 out of 7 total attributes
- Pattern: Entire row (minus one column) determines last column
- Interpretation: Likely every row is unique, or target is computed from all inputs

**nursery** (1 FD)
- FD: `1, complete, convenient, nonprob, proper, recommended, usual → recommend`
- ⚠️ **SUSPICIOUS**: Requires 7 out of 8 total attributes
- Pattern: Nearly entire row determines one column
- Similar to chess - suggests target is function of all inputs

---

### 2.2 Medium Complexity Datasets

**iris** (4 FDs)
```
3,2,1 → 5
4,2,1 → 5
4,3,1 → 5
4,3,2 → 5
```
- All FDs have LHS size = 3
- All determine the same RHS (column 5)
- Pattern: Different 3-attribute combinations determine same target
- Relatively normal for classification dataset

**breast-cancer-wisconsin** (46 FDs)
- Avg LHS: 2.7 attributes
- Top LHS attribute: column '3' appears in 40/46 FDs (87%)
- ⚠️ **SUSPICIOUS**: One attribute dominates
- Pattern: Column 3 may be ID-like or highly informative

**abalone** (137 FDs)
- Avg LHS: 4.22 attributes
- 119 FDs (87%) have ≥4 attributes on LHS
- ⚠️ **SUSPICIOUS**: Very high average determinant size
- Top attributes: columns 7, 5, 6 appear in 77-84 FDs each
- Pattern: Overfitting - many attribute combinations needed

---

### 2.3 High Complexity Datasets

**bridges** (144 FDs)

**ID-LIKE PATTERN DETECTED:**
- Attribute 'E1' determines 12 other attributes:
  ```
  E1 → M
  E1 → 3
  E1 → 1818
  E1 → HIGHWAY
  E1 → ?
  E1 → 2
  E1 → N
  E1 → THROUGH
  E1 → WOOD
  E1 → SHORT
  E1 → S
  E1 → WOOD (duplicate)
  ```

**LARGE DETERMINANTS:**
- 43 FDs with ≥5 attributes on LHS
- Examples:
  - `1818, HIGHWAY, M, N, SHORT → 2`
  - `?, HIGHWAY, M, S, THROUGH → N`
  - `3, N, S, SHORT, THROUGH → WOOD`

**Suspicious Patterns:**
1. **Degenerate FDs**: E1 appears to be a unique identifier
2. **Overfitted FDs**: Many 5-6 attribute combinations
3. **Attribute '?'**: Appears in 90 FDs - likely missing value marker

---

**echocardiogram** (527 FDs)

**EXTREME CASE**: 527 FDs for only 13 columns!

**DEGENERATE FD:**
- `(empty) → 9`
- Pattern: Column 9 has constant value (all rows identical)

**FREQUENT ATTRIBUTE:**
- Column '8' appears in 312/527 FDs (59%)
- Sample FDs:
  ```
  8, 1 → 2
  8 → 7
  8, 6 → 1
  8, 6 → 2
  8, 6 → 3
  ```

**Suspicious Patterns:**
1. Extremely high FD count suggests data quality issues
2. Column 8 likely ID-like or has encoding
3. Constant column indicates redundant data

---

**hepatitis** (8,296 FDs) ⚠️⚠️⚠️

**MOST EXTREME CASE**: 8,296 FDs for 20 columns!
- **Ratio**: 414.8 FDs per column
- This is abnormally high

**Distribution by LHS Size:**
- LHS size 2: 250 FDs (3.0%)
- LHS size 3: 2,817 FDs (34.0%)
- LHS size 4: 3,985 FDs (48.0%) ← largest group
- LHS size 5: 1,128 FDs (13.6%)
- LHS size 6: 116 FDs (1.4%)

**Frequent Attribute:**
- Column '1' appears in 8,011/8,296 FDs (97%!)

**Sample FDs:**
```
Size 2: 2, 8 → 1
Size 3: 6, 2, 7 → 1
Size 4: 4, 1, 2, 5 → 3
Size 5: 3, 4, 6, 1, 8 → 2
```

**Suspicious Patterns:**
1. **Combinatorial explosion**: Algorithm found nearly all possible attribute combinations
2. **Column 1 dominance**: Appears in 97% of FDs - almost certainly ID or key
3. **Overfitting**: 5,229 FDs (63%) have ≥4 attributes on LHS
4. Suggests either:
   - Very poor data quality
   - Spurious correlations in small dataset
   - Presence of unique IDs creating false dependencies

---

## 3. Classification of Suspicious Patterns

Based on structural analysis, we identified 5 categories of suspicious FDs:

### 3.1 ID-BASED FDs (Degenerate)
**Pattern**: Single attribute determines many others

**Examples**:
- bridges: `E1` → 12 attributes
- hepatitis: column `1` in 97% of FDs

**Why Suspicious**: Typical of unique identifiers. While valid in data, these are trivial from a knowledge perspective.

---

### 3.2 CONSTANT COLUMN FDs (Degenerate)
**Pattern**: Empty LHS or constant value

**Examples**:
- echocardiogram: `(empty) → 9`

**Why Suspicious**: Indicates column has same value in all rows - provides no information.

---

### 3.3 OVERFITTED FDs (Excessive LHS)
**Pattern**: Very large LHS (4+ attributes)

**Examples**:
- chess: 6 attributes → 1 (entire row minus one)
- nursery: 7 attributes → 1 (entire row minus one)
- hepatitis: 5,229 FDs with ≥4 attributes
- abalone: 119 FDs with ≥4 attributes

**Why Suspicious**:
- Violates parsimony principle
- May not generalize to new data
- Could be sample-specific accidents
- Often indicates no real dependencies exist

---

### 3.4 EXCESSIVE FD COUNT (Combinatorial Explosion)
**Pattern**: Abnormally high number of FDs

**Examples**:
- hepatitis: 8,296 FDs (414.8 per column)
- echocardiogram: 527 FDs (40.5 per column)

**Why Suspicious**:
- Suggests data quality issues
- Presence of IDs creating cascading dependencies
- Spurious correlations
- Possible data encoding artifacts

---

### 3.5 FREQUENT ATTRIBUTES (Potential Encoding)
**Pattern**: Attribute appears in majority of FDs

**Examples**:
- hepatitis: column 1 in 8,011/8,296 FDs (97%)
- echocardiogram: column 8 in 312/527 FDs (59%)
- breast-cancer-wisconsin: column 3 in 40/46 FDs (87%)

**Why Suspicious**:
- Could be ID field
- May contain encoded information
- Possibly artifact of data collection
- Might be computed/derived column

---

## 4. Detailed Dataset Suspicions

| Dataset                 | Primary Suspicion                          | Secondary Suspicion              |
|-------------------------|--------------------------------------------|----------------------------------|
| iris                    | None (normal)                              | -                                |
| balance-scale           | None (normal)                              | -                                |
| chess                   | **Overfitted** (6→1)                       | -                                |
| abalone                 | **Overfitted** (119 large LHS)             | High avg LHS (4.22)              |
| nursery                 | **Overfitted** (7→1)                       | -                                |
| breast-cancer-wisconsin | **Frequent attr** (col 3: 87%)             | -                                |
| bridges                 | **ID-based** (E1 → 12)                     | Many large determinants          |
| echocardiogram          | **Excessive count** (527 FDs)              | Constant column, Frequent attr   |
| hepatitis               | **EXTREME** (8,296 FDs, 97% have col 1)    | Combinatorial explosion          |

---

## 5. Attribute Frequency Analysis

### Top LHS (Determinant) Attributes

**Most frequently appearing on LEFT side of FDs:**

- **hepatitis**: column 1 (8,011 appearances - 97%)
- **echocardiogram**: column 8 (312 appearances - 59%)
- **bridges**: '?' (90 appearances - 63%)
- **abalone**: column 7 (84 appearances - 61%)
- **breast-cancer-wisconsin**: column 3 (40 appearances - 87%)

**Interpretation**: These attributes likely serve as IDs, have encoding, or contain information that correlates with many other columns.

---

## 6. Conclusions & Next Steps

### Key Findings

1. **Not all FDs are meaningful**: The TANE algorithm correctly identifies patterns that hold in data, but cannot distinguish:
   - Genuine domain constraints vs. sample accidents
   - Meaningful relationships vs. ID-based trivial dependencies
   - Real dependencies vs. overfitted combinations

2. **5 Suspicious Pattern Types Identified**:
   - ID-based (degenerate)
   - Constant columns (degenerate)
   - Overfitted (excessive LHS)
   - Excessive count (combinatorial explosion)
   - Frequent attributes (encoding/ID)

3. **Worst Offenders**:
   - **hepatitis**: 8,296 FDs - extreme combinatorial explosion
   - **echocardiogram**: 527 FDs + constant column
   - **bridges**: Clear ID attribute (E1)

### Limitations of Structural Analysis

This analysis is based ONLY on:
- Number of FDs
- LHS/RHS sizes
- Attribute frequency
- Patterns in FD structure

We did NOT consider:
- Column names or meanings
- Domain knowledge
- Semantic plausibility
- Actual data values

### Recommendations for Task Set 2

For LLM-assisted semantic analysis, prioritize:

1. **bridges**: Test if E1 is truly an ID
2. **hepatitis**: Investigate column 1's dominance
3. **chess/nursery**: Validate if 6-7 attribute dependencies are real
4. **echocardiogram**: Check constant column and frequent attributes
5. **abalone**: Examine if 4+ attribute combinations make sense

---

## 7. Appendix: Methodology

### Tools Used
- Python 3 with standard library
- Custom parsers for simple and JSON FD formats

### Metrics Computed
- Total FD count
- Average LHS size
- Min/Max LHS size
- Single-attribute determinants count
- Large determinants count (≥4 attributes)
- Attribute frequency (LHS and RHS)
- Potential ID detection (single attr → 3+ others)

### Suspicion Thresholds
- **Large LHS**: ≥4 attributes
- **Excessive FDs**: >100 for small datasets, >1000 for any dataset
- **High avg LHS**: >3.0
- **ID pattern**: Single attribute determines ≥3 others
- **Frequent attribute**: Appears in >50% of FDs

---

## 8. Files Generated

1. `analyze_fds.py` - Main statistical analysis script
2. `detailed_analysis.py` - Deep dive into suspicious patterns
3. `TASK_SET_1_REPORT.md` - This comprehensive report

---

**End of Task Set 1 Report**

*Next Step: Task Set 2 will use LLMs to evaluate semantic plausibility of selected FDs from each category.*
