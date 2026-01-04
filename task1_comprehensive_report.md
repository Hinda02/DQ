# TASK SET 1 - INTERPRETING ALGORITHMIC FUNCTIONAL DEPENDENCIES

**Assignment:** Beyond Patterns: Meaningful Functional Dependencies with Classical Algorithms and LLMs
**Analyzed by:** Task Set 1 Analysis
**Date:** January 4, 2026
**Algorithm:** TANE (pre-computed FDs provided)

---

## EXECUTIVE SUMMARY

This report analyzes 11 datasets from the UCI Machine Learning Repository and their pre-computed minimal functional dependencies discovered using the TANE algorithm. The analysis reveals significant variation in FD complexity across datasets, from simple datasets with 1 FD to extremely complex ones with thousands of dependencies.

**Key Findings:**
- **9 datasets analyzed** successfully (adult and horse FD files were empty)
- **Total FDs analyzed:** 9,157 functional dependencies
- **Complexity range:** 1 FD (balance-scale, chess, nursery) to 8,296 FDs (hepatitis)
- **Suspicious patterns identified:** 6,807 trivial/suspicious dependencies (74% of total)
- **ID-based columns detected:** 1 potential ID column (bridges dataset: "E1")

---

## 1. SUMMARY STATISTICS

| Dataset | Total FDs | Avg LHS Size | Max LHS Freq | Columns | Rows | Complexity |
|---------|-----------|--------------|--------------|---------|------|------------|
| **iris** | 4 | 3.00 | 3 | 5 | 150 | Simple |
| **balance-scale** | 1 | 1.00 | 1 | 5 | 625 | Simple |
| **chess** | 1 | 6.00 | 1 | 7 | 28,056 | Simple |
| **abalone** | 137 | 4.22 | 116 | 9 | 4,177 | Medium |
| **nursery** | 1 | 7.00 | 1 | 9 | 12,960 | Simple |
| **breast-cancer-wisconsin** | 46 | 2.70 | 40 | 11 | 699 | Medium |
| **bridges** | 144 | 3.69 | 90 | 13 | 108 | Medium |
| **echocardiogram** | 527 | 3.22 | 312 | 13 | 132 | Complex |
| **hepatitis** | 8,296 | 3.76 | 8,011 | 20 | 155 | Very Complex |
| **adult** | - | - | - | 14 | 48,842 | (FD file empty) |
| **horse** | - | - | - | 27 | 300 | (FD file empty) |

**Note:** adult_fds and horse_fds files were found to be empty (0 bytes). According to the assignment documentation, these should contain 78 and 128,726 FDs respectively.

---

## 2. DETAILED DATASET ANALYSIS

### 2.1 IRIS (Simple Classification Dataset)

**Statistics:**
- Total FDs: 4
- Average LHS size: 3.0
- File format: Index-based

**FD Structure:**
All 4 FDs predict the species (Iris-setosa) from combinations of 3 physical measurements:
- Sepal length, sepal width, petal length, petal width → Species

**Observations:**
- **Meaningful pattern:** Physical characteristics determine species (biologically sensible)
- All FDs use 3 attributes to determine the class
- No ID-based or trivial dependencies
- This is a clean, interpretable set of FDs

**Top Determinants (LHS):**
- Attributes 1, 2, 4, 5 each appear 3 times

**Assessment:** ✅ All FDs appear meaningful and represent real biological relationships

---

### 2.2 BALANCE-SCALE (Minimal Dependencies)

**Statistics:**
- Total FDs: 1
- Average LHS size: 1.0
- File format: Index-based

**FD Structure:**
- Single FD: `1 → B`
- One attribute determines another attribute

**Observations:**
- **Simplest dataset** in the collection
- Single determinant pattern
- Likely represents a derived or calculated field

**Assessment:** ⚠️ Need domain knowledge to assess if this is meaningful or encoding-based

---

### 2.3 CHESS (Composite Key Pattern)

**Statistics:**
- Total FDs: 1
- Average LHS size: 6.0
- File format: Index-based

**FD Structure:**
- Single FD with 6 attributes: `1,2,3,a,b,c → draw`
- All board position attributes together determine the outcome

**Observations:**
- **Large determinant** (6 attributes for a single FD)
- Represents composite key pattern
- Makes logical sense: chess position determines game outcome
- Large LHS suggests this might be dataset-specific rather than a general chess rule

**Assessment:** ⚠️ Formally valid but may be **accidental** - true only in this specific dataset

---

### 2.4 ABALONE (Medium Complexity with Suspicious Patterns)

**Statistics:**
- Total FDs: 137
- Average LHS size: 4.22
- File format: Index-based
- **Suspicious FDs:** 19 (14% of total)

**FD Structure:**
- Mix of simple and complex determinants
- 40 FDs have 5+ attributes in LHS (large determinants)
- Heavy reliance on numeric measurements

**Top Determinants (LHS):**
1. "15" appears 116 times (85% of FDs) ⚠️
2. "101" appears 84 times
3. "514" appears 79 times

**Top Dependents (RHS):**
1. "15" appears 34 times
2. "M" appears 25 times
3. "365" appears 17 times

**Problematic Patterns Identified:**

**Trivial Dependencies (19 cases):**
```
Examples:
- 101,15,514 → 15          (RHS appears in LHS)
- 15,2245,514 → 15         (RHS appears in LHS)
- 095,101,2245,15 → 15     (RHS appears in LHS)
```

These are **degenerate FDs** where an attribute determines itself (trivially true but meaningless).

**Large Determinants (40 FDs with 5+ attributes):**
```
Examples:
- 095,101,365,455,15 → M           (5 attributes)
- 095,101,365,455,15 → 514         (5 attributes)
- 095,365,455,514,15 → 2245        (5 attributes)
```

**Observations:**
- **Attribute "15"** appears extremely frequently (potential ID or key field)
- Many **overfitted FDs** with excessive LHS size
- Trivial dependencies suggest algorithm artifact rather than real constraints

**Assessment:** ⚠️ High noise-to-signal ratio; many meaningless dependencies

---

### 2.5 NURSERY (Single Complex FD)

**Statistics:**
- Total FDs: 1
- Average LHS size: 7.0
- File format: JSON-LD
- **Suspicious FDs:** 1 (100%)

**FD Structure:**
```
1,complete,convenient,nonprob,proper,recommended,usual → recommend
```

**Observations:**
- **Largest single-FD determinant** (7 attributes)
- All input features determine the classification
- Flagged as suspicious due to very large LHS

**Assessment:** ⚠️ **Likely overfitted** - represents entire decision rule rather than minimal constraint

---

### 2.6 BREAST-CANCER-WISCONSIN (ID Column Patterns)

**Statistics:**
- Total FDs: 46
- Average LHS size: 2.70
- File format: Index-based
- **Suspicious FDs:** 22 (48% of total)

**Top Determinants (LHS):**
1. "1" appears 40 times (87% of FDs) 🚨
2. "1000025" appears 27 times
3. "5" appears 26 times

**Top Dependents (RHS):**
1. "2" appears 31 times (67% as dependent)
2. "1" appears 15 times

**Problematic Patterns:**

**Highly Suspicious ID Column:**
- Attribute "1" appears as determinant in 40/46 FDs
- Attribute "1000025" looks like a record ID (appears 27 times)

**Trivial Dependencies (22 cases):**
```
Examples:
- 1000025,2 → 2              (RHS in LHS)
- 1,1000025,5 → 1            (RHS in LHS, appears 8 times!)
- 1,1000025,3 → 1            (RHS in LHS)
```

**Assessment:** 🚨 **Degenerate FDs dominated by ID columns** - most FDs are meaningless

---

### 2.7 BRIDGES (ID Column Detected)

**Statistics:**
- Total FDs: 144
- Average LHS size: 3.69
- File format: JSON-LD
- **ID column identified:** "E1"
- **Suspicious FDs:** 12 (8% of total)

**Top Determinants (LHS):**
1. "?" appears 90 times (missing value marker)
2. "3" appears 66 times
3. "WOOD" appears 54 times

**Potential ID Column:**
- **"E1"** appears as single determinant in 12 FDs ⚠️
- Suggests "E1" is a bridge identifier that determines all other attributes

**Large Determinants:**
- 43 FDs have 5+ attributes (30% of total)

**Examples:**
```
E1 → M
E1 → 3
E1 → 1818
E1 → HIGHWAY
... (12 FDs total)
```

**Trivial Dependencies (12 cases):**
```
Examples:
- 3,?,S,WOOD → WOOD
- 3,?,HIGHWAY,WOOD → WOOD
- ?,HIGHWAY,M,THROUGH,WOOD → WOOD
```

**Observations:**
- **"E1" is likely a bridge ID** (classic degenerate FD pattern)
- Heavy presence of "?" (missing values) in determinants
- Mix of numeric ("3", "1818") and categorical ("WOOD", "HIGHWAY") attributes

**Assessment:** ⚠️ Contains **degenerate FDs** (E1 as ID) + some **encoding-based FDs** (e.g., year values)

---

### 2.8 ECHOCARDIOGRAM (High Complexity, Many Trivial FDs)

**Statistics:**
- Total FDs: 527
- Average LHS size: 3.22
- File format: Index-based
- **Suspicious FDs:** 118 (22% of total)

**Top Determinants (LHS):**
1. "1" appears 312 times (59% of FDs) 🚨
2. "0" appears 261 times (50%)
3. "600" appears 220 times

**Top Dependents (RHS):**
1. "0" appears 144 times
2. "1" appears 137 times

**Problematic Patterns:**

**Trivial Dependencies (118 cases - 22% of all FDs!):**
```
Examples:
- 1,600 → 1
- 1,11,600 → 1
- 0,11,600 → 0
- 260,1,71 → 1
```

**Observations:**
- **Attributes "0", "1", "600"** dominate the FD set
- These numeric column names suggest position-based indexing
- 1 in 5 FDs is trivially true (RHS in LHS)
- High algorithmic noise

**Assessment:** 🚨 **High noise dataset** - algorithm discovered many artifacts

---

### 2.9 HEPATITIS (Extremely Complex, Highest FD Count)

**Statistics:**
- Total FDs: 8,296 (largest in dataset)
- Average LHS size: 3.76
- File format: Index-based
- **Suspicious FDs:** 6,654 (80% of total!) 🚨
- **Large determinants:** 1,244 FDs with 5+ attributes (15%)

**Top Determinants (LHS):**
1. "2" appears 8,011 times (97% of all FDs!) 🚨🚨🚨
2. "1" appears 5,909 times (71%)
3. "18" appears 3,905 times (47%)

**Top Dependents (RHS):**
1. "2" appears 6,232 times (75% as dependent)
2. "1" appears 1,010 times

**Critical Observations:**

**Attribute "2" Dominance:**
- Appears in **97% of all FDs**
- Appears as RHS in 75% of FDs
- This is a **clear ID or constant field pattern**

**Massive Triviality Problem:**
- **6,654 trivial FDs** (80% of all dependencies)
- Most common pattern: `...,2,... → 2` (attribute 2 determines itself)

**Examples of Trivial FDs:**
```
18,2,85 → 2
2,30,85 → 2
00,2,30 → 2
18,2,0 → 2
... (6,654 similar cases)
```

**Large Determinants (1,244 FDs):**
```
Examples:
- 1,00,18,2,? → 30      (5 attributes)
- 1,00,18,2,? → 2       (5 attributes, also trivial!)
- 1,00,18,2,? → 1       (5 attributes)
```

**Assessment:** 🚨🚨🚨 **SEVERE ALGORITHM ARTIFACT PROBLEM**
- 80% of FDs are meaningless
- Dominated by a single attribute ("2")
- Likely a data quality issue or constant column
- This dataset exemplifies why semantic filtering is crucial

---

## 3. CROSS-DATASET PATTERNS AND INSIGHTS

### 3.1 Relationship Between Dataset Size and FD Count

**Observation:** No clear correlation between number of rows and FD count

| Dataset | Rows | FDs | FDs per 1000 rows |
|---------|------|-----|-------------------|
| chess | 28,056 | 1 | 0.04 |
| nursery | 12,960 | 1 | 0.08 |
| hepatitis | 155 | 8,296 | 53,522 🚨 |
| echocardiogram | 132 | 527 | 3,992 |
| iris | 150 | 4 | 27 |

**Insight:** Small datasets (hepatitis: 155 rows) can have thousands of FDs, while large datasets (chess: 28K rows) may have very few. **FD count is more related to:**
- Number of columns
- Data diversity
- Presence of ID/key columns
- Algorithm overfitting on small samples

### 3.2 Trivial FD Distribution

**Total Trivial FDs Across All Datasets:** 6,807 out of 9,157 (74% 🚨)

| Dataset | Total FDs | Trivial FDs | % Trivial |
|---------|-----------|-------------|-----------|
| hepatitis | 8,296 | 6,654 | **80%** |
| echocardiogram | 527 | 118 | **22%** |
| breast-cancer-wisconsin | 46 | 22 | **48%** |
| abalone | 137 | 19 | **14%** |
| bridges | 144 | 12 | **8%** |
| nursery | 1 | 1 | **100%** |
| iris | 4 | 0 | 0% ✅ |
| balance-scale | 1 | 0 | 0% ✅ |
| chess | 1 | 0 | 0% ✅ |

**Key Insight:** The majority of discovered FDs are trivial (RHS in LHS). This is a **critical finding** showing that **algorithmic FD discovery produces 3x more noise than signal**.

### 3.3 ID Column Detection

**Identified Degenerate FD Patterns:**

1. **bridges.csv:** "E1" appears as single determinant in 12 FDs
   - Pattern: `E1 → {M, 3, 1818, HIGHWAY, ...}`
   - Assessment: Clear ID column

2. **breast-cancer-wisconsin.csv:** "1" appears in 40/46 FDs, "1000025" appears in 27 FDs
   - Pattern: ID columns dominating all dependencies
   - Assessment: Degenerate dataset

3. **hepatitis.csv:** "2" appears in 8,011/8,296 FDs
   - Pattern: Single attribute in 97% of FDs
   - Assessment: Likely constant or ID field

**Total ID-based FDs:** ~8,070 (88% of all FDs)

### 3.4 Average LHS Size Analysis

**Distribution:**

| LHS Size Range | Count | Datasets |
|----------------|-------|----------|
| 1.0 | 1 | balance-scale |
| 2.0 - 3.0 | 3 | breast-cancer-wisconsin, echocardiogram |
| 3.0 - 4.0 | 3 | iris, bridges, hepatitis |
| 4.0 - 5.0 | 1 | abalone |
| 6.0+ | 2 | chess, nursery |

**Insight:** Most datasets have **moderate LHS sizes (2-4 attributes)**. Datasets with very large average LHS (6-7) typically have only 1 FD representing the entire decision function.

---

## 4. CLASSES OF MEANINGLESS FDS IDENTIFIED

### 4.1 Degenerate FDs (ID Explains Everything)

**Examples:**
```
bridges:     E1 → M, E1 → 3, E1 → 1818, ...
breast-cancer-wisconsin: 1000025,... → ...
hepatitis:   2,... → ... (in 97% of FDs)
```

**Count:** ~8,070 FDs (88%)
**Assessment:** These add no domain knowledge - just artifacts of unique identifiers

### 4.2 Trivial FDs (RHS in LHS)

**Examples:**
```
abalone:      101,15,514 → 15
hepatitis:    18,2,85 → 2
echocardiogram: 1,600 → 1
bridges:      3,?,S,WOOD → WOOD
```

**Count:** 6,807 FDs (74%)
**Assessment:** Mathematically true but semantically empty

### 4.3 Overfitted FDs (Excessive LHS Size)

**Examples:**
```
nursery:  1,complete,convenient,nonprob,proper,recommended,usual → recommend (7 attrs)
chess:    1,2,3,a,b,c → draw (6 attrs)
abalone:  095,101,365,455,15 → M (5 attrs)
```

**Count:** 1,328 FDs with 5+ attributes (15%)
**Assessment:** Likely sample-specific, won't generalize

### 4.4 Encoding-Based FDs (Suspected)

**Examples:**
```
bridges: 1818,... → ... (year value as determinant)
breast-cancer-wisconsin: 1000025,... → ... (numeric ID code)
```

**Count:** Unknown (requires domain knowledge)
**Assessment:** Information embedded in coded identifiers

---

## 5. KEY FINDINGS AND RECOMMENDATIONS

### Finding 1: Massive Noise in Algorithmic Output
- **74% of all FDs are trivial** (RHS appears in LHS)
- **88% are ID-based or degenerate**
- Only ~12% of FDs are potentially meaningful

**Recommendation:** Implement **mandatory semantic filtering** before human review

### Finding 2: Small Datasets → High FD Counts
- hepatitis (155 rows) has 8,296 FDs
- echocardiogram (132 rows) has 527 FDs

**Explanation:** Small samples → many accidental dependencies
**Recommendation:** Apply stricter minimality criteria or confidence thresholds

### Finding 3: ID Columns Dominate Output
- Single attributes appear in 50-97% of FDs
- Classic degenerate FD pattern

**Recommendation:** Pre-filter likely ID columns before FD discovery:
- High cardinality (unique values)
- Numeric sequences
- Column names matching ID patterns

### Finding 4: Dataset Size ≠ FD Complexity
- Large datasets (chess: 28K rows) can have 1 FD
- Small datasets (hepatitis: 155 rows) can have 8K FDs

**Insight:** FD complexity depends on:
- Number of columns
- Data diversity
- Functional relationships (not row count)

### Finding 5: Meaningful FDs Are Rare
- iris: 4/4 FDs appear meaningful (100%) ✅
- hepatitis: ~1,642/8,296 potentially meaningful (20%)
- Average: ~12% meaningful FDs

**Recommendation:** Focus human effort on datasets with clean FD patterns (like iris)

---

## 6. SUSPICIOUS DEPENDENCIES SUMMARY

### By Dataset:

| Dataset | Total FDs | Suspicious | % Suspicious | Primary Issue |
|---------|-----------|------------|--------------|---------------|
| **hepatitis** | 8,296 | 6,654 | **80%** | Trivial FDs |
| **nursery** | 1 | 1 | **100%** | Overfitted |
| **breast-cancer-wisconsin** | 46 | 22 | **48%** | ID columns + Trivial |
| **echocardiogram** | 527 | 118 | **22%** | Trivial FDs |
| **abalone** | 137 | 19 | **14%** | Trivial FDs |
| **bridges** | 144 | 12 | **8%** | ID column (E1) |
| **iris** | 4 | 0 | **0%** ✅ | None |
| **balance-scale** | 1 | 0 | **0%** | Unknown |
| **chess** | 1 | 0 | **0%** | Large LHS but plausible |

### Overall Noise Level: **74% of FDs are suspicious or meaningless**

---

## 7. IMPLICATIONS FOR TASK SETS 2-4

### For Task Set 2 (LLM-Assisted Semantic Discovery):

**Recommended Datasets for LLM Evaluation:**
1. **iris** - Clean FDs, biologically interpretable
2. **bridges** - Mix of meaningful + ID-based FDs
3. **abalone** - Good test case with mixed quality
4. **hepatitis** - Extreme noise, tests LLM's ability to detect triviality

**Recommended FD Samples:**

**Plausible FDs to test:**
```
iris: 4,2,1 → Iris-setosa (physical measurements → species)
bridges: 1818,3 → WOOD (year + span → material)
abalone: M → ... (sex → other attributes)
```

**Suspicious FDs to test:**
```
hepatitis: 18,2,85 → 2 (trivial - RHS in LHS)
breast-cancer-wisconsin: 1000025,2 → 2 (trivial + ID-based)
nursery: 1,complete,convenient,... → recommend (7-attribute overfitting)
abalone: 095,101,365,455,15 → M (5-attribute overfitting)
```

### For Task Set 3 (Sampling and Hypotheses):

**Warning:** Datasets with high FD counts (hepatitis, echocardiogram) are prone to:
- False positives from sampling
- Overfitted dependencies
- LLM hallucination due to trivial patterns

**Recommended approach:** Sample from clean datasets first (iris, bridges) to calibrate LLM behavior

### For Task Set 4 (Hybrid Discovery):

**Suggested Pipeline Components:**

1. **Pre-filter ID columns** (detect high cardinality, numeric sequences)
2. **Remove trivial FDs** (RHS in LHS check)
3. **Filter large determinants** (LHS > 5 attributes)
4. **LLM semantic filter** on remaining FDs
5. **Verification** against full dataset

**Expected noise reduction:** 74% → <20% with proper filtering

---

## 8. CONCLUSIONS

This analysis of 9 datasets and 9,157 functional dependencies reveals a **critical gap between algorithmic FD discovery and semantic meaningfulness**:

1. **Only ~12% of discovered FDs appear potentially meaningful**
2. **74% are trivial** (RHS appears in LHS)
3. **88% are degenerate** (ID-based or overfitted)
4. **Small datasets produce the most noise** (hepatitis: 155 rows, 8,296 FDs)
5. **ID columns dominate** algorithmic output

**Key Takeaway:** TANE algorithm is **syntactically correct but semantically blind**. Without filtering:
- 3x more noise than signal
- Human review is overwhelmed
- Useful dependencies are buried

This validates the assignment's central premise: **classical algorithms discover all patterns, not just meaningful ones**. Tasks 2-4 will explore how LLMs can help bridge this semantic gap.

---

## APPENDIX: NOTES ON MISSING DATA

**adult_fds** and **horse_fds** were found to be empty (0 bytes).

According to assignment documentation:
- adult.csv should have 78 FDs
- horse.csv should have 128,726 FDs

This analysis is based on the 9 datasets with valid FD files. If these files become available, they should be processed and integrated into this analysis.

---

**Analysis Complete**
**Next Steps:** Proceed to Task Set 2 (LLM-Assisted Semantic FD Discovery)
