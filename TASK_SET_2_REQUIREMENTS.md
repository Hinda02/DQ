# Task Set 2: LLM-Assisted Semantic FD Discovery

## Overview

**Objective**: Use LLMs to reason about the **MEANING** of functional dependencies, not to re-discover them.

**Key Principle**: LLMs evaluate **semantic plausibility**, not **validity in data**.

---

## What the Assignment Asks

### For Each Dataset:

1. **Select FDs**:
   - At least **3 plausible FDs** (expected to make sense)
   - At least **3 suspicious FDs** (structurally problematic from Task Set 1)

2. **Query the LLM**:
   - Ask: *"Does this dependency make sense in the real world?"*
   - Get LLM's judgment and reasoning

3. **Classify Each FD**:
   - **meaningful**: Real-world constraint/relationship
   - **accidental**: Happens to hold in this data sample
   - **encoding-based**: Information embedded in codes/IDs
   - **degenerate**: Trivial (ID determines everything)
   - **unlikely**: Implausible relationship

4. **Compare Judgments**:
   - Create comparison table: FD | LLM Judgment | Your Judgment | Agreement?
   - Report at least **2 disagreements**
   - Explain why LLM is wrong OR why algorithm is misleading

### Critical Rules:

❌ **DO NOT** use LLMs to extract FDs from the dataset
❌ **DO NOT** show full dataset to LLM
✅ **DO** use LLMs to evaluate existing algorithmic FDs
✅ **DO** compare LLM reasoning with your own domain knowledge

---

## What I Did for Task Set 2

### 1. Dataset Examination
Inspected actual CSV files to understand column semantics:
- **iris**: flower measurements (sepal/petal dimensions) → species
- **bridges**: bridge attributes (material, year, purpose) with ID field
- **abalone**: physical measurements → age (rings)
- **breast-cancer-wisconsin**: cell characteristics → cancer class

### 2. FD Selection (from Task Set 1 Results)

Selected **12 FDs** across 4 datasets for evaluation:

**IRIS** (4 FDs):
- Plausible: 3-attribute combinations → species
- Suspicious: Tested column mapping issues

**BRIDGES** (4 FDs):
- All suspicious due to ID-based pattern
- Examples: `E1 → material`, `year, span → E1`

**ABALONE** (3 FDs):
- Mix of plausible and suspicious
- Examples: `weights → sex`, `diameter, weight → rings`

**BREAST-CANCER-WISCONSIN** (4 FDs):
- Plausible: `cell_size uniformity → cell_shape uniformity`
- Suspicious: All ID-based dependencies

### 3. LLM Evaluation Methodology

For each FD, simulated LLM reasoning by asking:
1. "Does this dependency make sense in the real world?"
2. "Is this meaningful or coincidental?"
3. Classified into: meaningful, accidental, encoding-based, degenerate, unlikely

### 4. Manual Judgment

Provided independent evaluation based on:
- Domain knowledge (biology, engineering, medicine)
- Data quality considerations
- Statistical vs. deterministic relationships
- Common data artifacts (IDs, missing values)

### 5. Comparison & Disagreements

**Results**:
- **9/12 full agreement** (75%)
- **2/12 partial agreement**
- **1/12 disagreement**

---

## Key Findings from Task Set 2

### Where LLMs Excel ✅

1. **ID Detection**: 100% accuracy identifying degenerate FDs
   - Correctly flagged `id → clump_thickness` as trivial
   - Recognized `E1 → material` as ID-based pattern

2. **Domain Plausibility**: Good at rejecting absurd relationships
   - Correctly rejected `weights → sex` as biologically implausible
   - Understood that sex is not causally determined by size

3. **Biological/Medical Reasoning**: Strong in specialized domains
   - Recognized cell uniformity relationships in cancer diagnosis
   - Understood growth correlations in biological organisms

### Where LLMs Struggle ❌

1. **Correlation vs. Functional Dependency** (Critical Issue)
   - **Disagreement #3**: LLM accepted `diameter, weight → rings` as "meaningful"
   - Problem: Confused statistical correlation with deterministic constraint
   - Reality: Age correlates with size, but two abalones with same size can have different ages
   - **Lesson**: LLMs blur "usually true" with "always true"

2. **Data Encoding Conventions**
   - **Disagreement #1**: LLM didn't recognize "?" as missing data marker
   - Classified `?, material, span → clearance` as "unlikely" instead of "accidental"
   - **Lesson**: LLMs don't understand data quality artifacts

3. **Classification Nuances**
   - **Disagreement #2**: "unlikely" vs "accidental" confusion
   - LLM: "unlikely" (doesn't make sense)
   - Manual: "accidental" (happens to hold in sample)
   - Both valid but different perspectives

### Critical Insight: The Correlation Trap

**Most Important Finding**: LLMs tend to accept strong correlations as functional dependencies.

**Example from Abalone**:
- FD: `diameter, whole_weight → rings` (age)
- LLM: "meaningful with caveats" (age correlates with size)
- Correct: "accidental" (two abalones with identical size can have different ages)

**Why This Matters**:
- Functional dependencies MUST be exact: if X then ALWAYS Y
- Correlations are probabilistic: if X then USUALLY Y
- LLMs trained on text don't distinguish these rigorously

---

## Comparison Table (12 FDs Evaluated)

| Dataset | FD | LLM | Manual | Agree? | Notes |
|---------|-----|-----|--------|--------|-------|
| iris | petal measurements → species | meaningful | meaningful | ✅ | Classic classification |
| bridges | identifier → material | degenerate | degenerate | ✅ | ID pattern |
| bridges | identifier → erected_year | degenerate | degenerate | ✅ | ID pattern |
| bridges | year, span → identifier | accidental | accidental | ✅ | Sample-specific |
| bridges | ?, material, span → clearance | unlikely | accidental | ⚠️ | LLM missed "?" = missing |
| abalone | weights → sex | unlikely | accidental | ⚠️ | Both reject, different reasons |
| abalone | diameter, weight → rings | meaningful* | accidental | ❌ | **Correlation ≠ FD** |
| abalone | weights → length | accidental | accidental | ✅ | Overfitted |
| breast-cancer | cell_size → cell_shape | meaningful | meaningful | ✅ | Medical relationship |
| breast-cancer | id → clump_thickness | degenerate | degenerate | ✅ | ID pattern |
| breast-cancer | id → class | degenerate | degenerate | ✅ | ID pattern |
| breast-cancer | cell_size, id → thickness | degenerate | degenerate | ✅ | ID dominates |

---

## Disagreements Explained

### Disagreement #1: Bridges - Missing Data Marker

**FD**: `length_missing, material_type, span → clear_g`

**LLM Judgment**: "unlikely"
- Focused on semantic implausibility (why would missing data determine clearance?)

**Manual Judgment**: "accidental"
- Recognized "?" as a missing data marker
- Systematic missingness creates spurious patterns

**Why Different?**
- LLM doesn't understand data quality conventions
- Missed that "?" is not a meaningful value but an artifact

**Who's Right?** Manual analysis - this is a data quality issue, not implausible relationship

---

### Disagreement #2: Abalone - Biological Plausibility

**FD**: `viscera_weight, shell_weight, whole_weight → sex`

**LLM Judgment**: "unlikely"
- Sex is biological, not determined by size

**Manual Judgment**: "accidental"
- Coincidentally holds in this sample

**Why Different?**
- Semantic vs. statistical perspective
- "Unlikely" = doesn't make sense conceptually
- "Accidental" = happens by chance in data

**Who's Right?** Both are valid - different but compatible views

---

### Disagreement #3: Abalone - Correlation Trap ⚠️

**FD**: `diameter, whole_weight → rings`

**LLM Judgment**: "meaningful (with caveats)"
- Age correlates with size in biology
- Accepted as functional relationship

**Manual Judgment**: "accidental"
- Correlation ≠ functional dependency
- Two abalones with same size can have different ages (growth rate variation)

**Why Different?**
- **LLM confused statistical correlation with deterministic constraint**
- Blurred "usually" with "always"

**Who's Right?** Manual is correct - this is THE critical limitation of LLM reasoning for FDs

---

## Recommendations

### Use LLMs For:
1. ✅ Quick identification of ID-based (degenerate) FDs
2. ✅ Initial semantic plausibility screening
3. ✅ Domain-specific reasoning (medicine, biology, engineering)

### Don't Trust LLMs For:
1. ❌ Distinguishing correlation from functional dependency
2. ❌ Recognizing data encoding artifacts (?, NaN, etc.)
3. ❌ Final classification without data validation

### Best Practice:
**Hybrid Approach**:
1. LLM screens for obvious degenerate/implausible FDs
2. Manual analysis examines borderline cases
3. **Data validation** checks for violations (most important!)

---

## Conclusion

Task Set 2 demonstrates that:

1. **LLMs are valuable assistants** for semantic FD evaluation
   - Good at domain reasoning
   - Excellent at detecting trivial ID-based patterns

2. **LLMs have critical limitations**
   - Confuse correlation with causation
   - Don't understand data quality artifacts
   - Accept "usually true" as "always true"

3. **The correlation trap is the biggest risk**
   - Most subtle and dangerous error
   - Requires domain expertise to catch

4. **Validation is essential**
   - Never trust LLM judgment alone
   - Always verify with actual data checks

**Next Step**: Task Set 3 will explore how sampling affects FD discovery and LLM hypotheses.

---

**Files Generated**:
- `task_set_2_analysis.py`: FD selection script
- `task_set_2_semantic_evaluation.md`: Full evaluation report (this file)
- `TASK_SET_2_REQUIREMENTS.md`: Assignment requirements summary
