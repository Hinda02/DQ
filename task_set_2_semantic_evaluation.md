# TASK SET 2: LLM-Assisted Semantic FD Discovery

**Objective**: Use LLM reasoning to evaluate the **semantic plausibility** of algorithmically-discovered functional dependencies.

**Approach**: For selected FDs from Task Set 1, we ask: "Does this dependency make sense in the real world?"

---

## Dataset 1: IRIS

**Context**: Iris flower measurements (sepal length/width, petal length/width) → species classification

### Column Mapping
- Column 1: sepal_length
- Column 2: sepal_width
- Column 3: petal_length
- Column 4: petal_width
- Column 5: species

### Selected FDs

#### Plausible FDs

**FD1**: `petal_length, petal_width, sepal_length → species`
- **LLM Query**: "In botany, can three flower measurements (petal length, petal width, sepal length) uniquely determine the species of an iris?"
- **LLM Judgment**: **MEANINGFUL**
  - Reasoning: In botanical classification, multiple morphological measurements can distinguish species. Three measurements (especially petal characteristics which vary significantly between iris species) could plausibly determine species in a controlled dataset.
  - Confidence: High

- **Manual Judgment**: **MEANINGFUL**
  - This is a classic classification relationship. Iris species (setosa, versicolor, virginica) have distinct petal/sepal characteristics.
  - This is the basis of Fisher's famous iris dataset.

- **Agreement**: ✅ YES
- **Classification**: **meaningful**

---

**FD2**: `uniformity_cell_shape, petal_width, sepal_length → species`
- **CORRECTION**: Column 4 in iris is petal_width, not uniformity_cell_shape
- **Corrected FD**: `petal_width, petal_length, sepal_length → species`
- **LLM Judgment**: **MEANINGFUL** (same as FD1)
- **Manual Judgment**: **MEANINGFUL**
- **Agreement**: ✅ YES
- **Classification**: **meaningful**

#### Suspicious FDs

**FD3**: `petal_width, petal_length, petal_width → species`
- **CORRECTION**: This appears to be a different combination from Task Set 1
- **Actual FD from data**: `uniformity_cell_shape, petal_length, petal_width → species`
- **LLM Judgment**: **N/A** - Column name error, uniformity_cell_shape doesn't exist in iris
- **Manual Judgment**: **ERROR** - Invalid column mapping
- **Agreement**: ✅ YES - Both identify this as problematic
- **Classification**: **ERROR in analysis**

---

## Dataset 2: BRIDGES

**Context**: Bridge construction data (material, year, purpose, dimensions)

### Column Mapping
- E1: identifier (bridge ID)
- M: material
- 3: span
- 1818: erected_year
- HIGHWAY: purpose
- ?: missing/unknown length
- 2: lanes
- N: clear_g
- THROUGH: type
- WOOD: material_type
- SHORT: span_type
- S: rel_l

### Selected FDs

#### Suspicious FDs (ID-based pattern detected in Task Set 1)

**FD1**: `identifier → material`
- **LLM Query**: "Does a bridge's unique identifier determine its construction material?"
- **LLM Judgment**: **DEGENERATE**
  - Reasoning: An identifier (E1, E2, E3...) is a surrogate key. It doesn't causally determine material - rather, each bridge record has both an ID and a material. The ID just uniquely identifies the row.
  - This is a classic ID-based dependency: trivial but holds in data.
  - Confidence: Very High

- **Manual Judgment**: **DEGENERATE**
  - Clear ID pattern. E1, E2, E3... are unique row identifiers.
  - While valid in data, this provides no domain knowledge.

- **Agreement**: ✅ YES
- **Classification**: **degenerate** (ID-based)

---

**FD2**: `identifier → erected_year`
- **LLM Judgment**: **DEGENERATE**
- **Manual Judgment**: **DEGENERATE**
- **Agreement**: ✅ YES
- **Classification**: **degenerate** (ID-based)

---

**FD3**: `erected_year, span → identifier`
- **LLM Query**: "Do a bridge's construction year and span length uniquely determine its identifier?"
- **LLM Judgment**: **ACCIDENTAL**
  - Reasoning: This is backwards causality. The identifier doesn't emerge from year + span. Rather, this holds because in this particular sample, no two bridges happen to share the same year AND span.
  - This is coincidental to the dataset size and composition.
  - Confidence: High

- **Manual Judgment**: **ACCIDENTAL**
  - Agrees with LLM. This is sample-specific.
  - In a larger dataset, multiple bridges from the same year with the same span would violate this.

- **Agreement**: ✅ YES
- **Classification**: **accidental**

---

**FD4**: `length_missing, material_type, span → clear_g`
- **LLM Query**: "Can missing length indicator, material type, and span determine the clear_g (clearance) of a bridge?"
- **LLM Judgment**: **UNLIKELY**
  - Reasoning: Clear_g (clearance) is a specific measurement that depends on design requirements, not whether length data is missing. The missing data indicator "?" shouldn't determine physical properties.
  - This appears to be data artifact or spurious correlation.
  - Confidence: Medium-High

- **Manual Judgment**: **ENCODING-BASED or ACCIDENTAL**
  - The "?" (missing value marker) suggests data quality issue.
  - Could be that records with missing length have other systematic differences.
  - Likely accidental pattern in this small dataset (108 rows).

- **Agreement**: ⚠️ PARTIAL
  - Both agree it's suspicious
  - Differ on classification: LLM says "unlikely", manual says "accidental"
  - **Disagreement #1**: LLM didn't recognize that "?" is a missing data marker, focused on implausibility. Manual analysis recognizes data quality artifact.

---

## Dataset 3: ABALONE

**Context**: Abalone physical measurements → age prediction (rings)

### Column Mapping
- Column 1: sex (M/F/I for infant)
- Column 2: length
- Column 3: diameter
- Column 4: height
- Column 5: whole_weight
- Column 6: shucked_weight
- Column 7: viscera_weight
- Column 8: shell_weight
- Column 9: rings (age indicator)

### Selected FDs

#### Plausible FDs

**FD1**: `viscera_weight, shell_weight, whole_weight → sex`
- **LLM Query**: "Can three weight measurements determine the sex of an abalone?"
- **LLM Judgment**: **UNLIKELY**
  - Reasoning: Sex (M/F/I) is a biological characteristic determined at development, not by size/weight. While there may be statistical correlations (males might average larger), weights don't DETERMINE sex in a functional dependency sense.
  - An infant (I) vs adult is plausible from weight, but M vs F is not causally determined by measurements.
  - Confidence: High

- **Manual Judgment**: **ACCIDENTAL**
  - Agree with LLM that this doesn't make biological sense.
  - Likely holds in this sample by coincidence (perhaps gender distribution correlates with age/size in this sample).

- **Agreement**: ⚠️ PARTIAL
  - Both agree it's not meaningful
  - Differ on classification: LLM says "unlikely" (implausible), manual says "accidental" (sample-specific)
  - **Disagreement #2**: Semantic nuance - "unlikely" suggests it's absurd, "accidental" suggests it happens to hold but isn't reliable.

---

**FD2**: `diameter, whole_weight → rings`
- **LLM Query**: "Can diameter and weight determine the number of rings (age) in an abalone?"
- **LLM Judgment**: **MEANINGFUL (with caveats)**
  - Reasoning: Age correlates with size in biological organisms. While not perfectly deterministic (individuals grow at different rates), diameter + weight could approximate age.
  - However, this is more of a predictive correlation than a functional constraint.
  - Confidence: Medium

- **Manual Judgment**: **ACCIDENTAL**
  - While there's biological correlation, this is NOT a functional dependency in the strict sense.
  - Two abalones with same diameter/weight can have different ages (different growth rates).
  - Holds in this dataset but would break with more samples.

- **Agreement**: ❌ NO
  - **Disagreement #3**: LLM accepts this as "meaningful with caveats" due to biological correlation. Manual analysis rejects it because correlation ≠ functional dependency.
  - This reveals LLM tendency to accept statistical relationships as functional dependencies.

#### Suspicious FDs

**FD3**: `viscera_weight, shell_weight, whole_weight → length`
- **LLM Query**: "Can three weight measurements determine the length of an abalone?"
- **LLM Judgment**: **ACCIDENTAL**
  - Reasoning: While weights and length correlate (larger = heavier), three weights don't uniquely determine length. You can have two abalones with similar weights but different proportions (one longer/thinner, one shorter/wider).
  - This holds in the sample but is coincidental.
  - Confidence: High

- **Manual Judgment**: **ACCIDENTAL**
  - Agree completely. This is overfitted pattern.

- **Agreement**: ✅ YES
- **Classification**: **accidental**

---

## Dataset 4: BREAST CANCER WISCONSIN

**Context**: Cell characteristics → cancer diagnosis (benign/malignant)

### Column Mapping
- Column 1: id (patient identifier)
- Column 2: clump_thickness
- Column 3: uniformity_cell_size
- Column 4: uniformity_cell_shape
- Column 5: marginal_adhesion
- Column 6: class (2=benign, 4=malignant)

### Selected FDs

#### Plausible FDs

**FD1**: `uniformity_cell_size → uniformity_cell_shape`
- **LLM Query**: "Does uniformity of cell size determine uniformity of cell shape in cancer cells?"
- **LLM Judgment**: **MEANINGFUL**
  - Reasoning: In cell biology, uniform cell size and uniform cell shape are related characteristics. Cells that are uniform in size tend to also be uniform in shape, especially in well-differentiated (benign) tissue.
  - This reflects underlying cellular organization.
  - Confidence: Medium-High

- **Manual Judgment**: **MEANINGFUL (or ENCODING-BASED)**
  - These two features are likely correlated in medical observations.
  - Could also be encoding-based if doctors assess both on the same scale based on similar criteria.
  - Reasonable domain relationship.

- **Agreement**: ✅ YES
- **Classification**: **meaningful**

#### Suspicious FDs

**FD2**: `id → clump_thickness`
- **LLM Judgment**: **DEGENERATE**
- **Manual Judgment**: **DEGENERATE**
- **Agreement**: ✅ YES
- **Classification**: **degenerate** (ID-based)

---

**FD3**: `id → class`
- **LLM Judgment**: **DEGENERATE**
- **Manual Judgment**: **DEGENERATE**
- **Agreement**: ✅ YES
- **Classification**: **degenerate** (ID-based)

---

**FD4**: `uniformity_cell_size, id → clump_thickness`
- **LLM Query**: "Do cell size uniformity plus patient ID determine clump thickness?"
- **LLM Judgment**: **DEGENERATE**
  - Reasoning: The ID already uniquely determines everything (including clump_thickness). Adding uniformity_cell_size is redundant. This is still fundamentally an ID-based dependency.
  - Confidence: Very High

- **Manual Judgment**: **DEGENERATE**
  - Agree. ID dominates this dependency.

- **Agreement**: ✅ YES
- **Classification**: **degenerate** (ID-based)

---

## SUMMARY TABLE: All Evaluations

| Dataset | FD | LLM Judgment | Manual Judgment | Agreement? |
|---------|-----|--------------|-----------------|------------|
| iris | petal measurements → species | meaningful | meaningful | ✅ YES |
| bridges | identifier → material | degenerate | degenerate | ✅ YES |
| bridges | identifier → erected_year | degenerate | degenerate | ✅ YES |
| bridges | year, span → identifier | accidental | accidental | ✅ YES |
| bridges | length_missing, material, span → clearance | unlikely | accidental | ⚠️ PARTIAL |
| abalone | weights → sex | unlikely | accidental | ⚠️ PARTIAL |
| abalone | diameter, weight → rings | meaningful* | accidental | ❌ NO |
| abalone | weights → length | accidental | accidental | ✅ YES |
| breast-cancer | cell_size uniformity → cell_shape uniformity | meaningful | meaningful | ✅ YES |
| breast-cancer | id → clump_thickness | degenerate | degenerate | ✅ YES |
| breast-cancer | id → class | degenerate | degenerate | ✅ YES |
| breast-cancer | cell_size, id → clump_thickness | degenerate | degenerate | ✅ YES |

**Agreement Rate**: 9/12 full agreement (75%), 2/12 partial, 1/12 disagreement

---

## DISAGREEMENTS ANALYSIS

### Disagreement #1: Bridges - `length_missing, material_type, span → clear_g`

**LLM**: "unlikely" - focuses on semantic implausibility
**Manual**: "accidental" - recognizes data quality artifact

**Why the difference?**
- LLM focused on whether the relationship makes sense conceptually
- Manual analysis recognized "?" as a missing data marker, indicating data quality issue
- **LLM limitation**: Didn't recognize data encoding conventions (? = missing)

**Who is right?**
- **Manual is more accurate**. This is an accidental pattern caused by systematic missingness, not an implausible relationship.

---

### Disagreement #2: Abalone - `viscera_weight, shell_weight, whole_weight → sex`

**LLM**: "unlikely" - sex not causally determined by size
**Manual**: "accidental" - coincidental in sample

**Why the difference?**
- LLM focused on biological implausibility (sex ≠ f(size))
- Manual focused on whether it holds by chance in this dataset
- **Subtle distinction**: unlikely = doesn't make sense; accidental = happens to hold but unreliable

**Who is right?**
- **Both are valid perspectives**. LLM emphasizes domain knowledge (biology), manual emphasizes data sampling (statistical coincidence).

---

### Disagreement #3: Abalone - `diameter, whole_weight → rings` ⚠️ **MAJOR**

**LLM**: "meaningful (with caveats)" - accepts biological correlation
**Manual**: "accidental" - rejects because correlation ≠ functional dependency

**Why the difference?**
- **LLM confused correlation with functional dependency**
- Age correlates with size, but two abalones with identical size can have different ages
- **Critical error**: LLM accepted a statistical trend as a deterministic constraint

**Who is right?**
- **Manual is correct**. Functional dependencies must be EXACT constraints (if X then ALWAYS Y), not probabilistic correlations.
- **This is a key limitation of LLM reasoning**: tendency to accept strong correlations as functional dependencies.

---

## KEY INSIGHTS

### Where LLMs Excel
1. ✅ **ID detection**: Correctly identifies degenerate FDs (100% accuracy)
2. ✅ **Domain plausibility**: Good at rejecting absurd relationships (e.g., weights → sex)
3. ✅ **Biological/medical reasoning**: Understands cell biology, growth patterns

### Where LLMs Struggle
1. ❌ **Correlation vs. Causation**: Accepts statistical correlations as functional dependencies
2. ❌ **Data encoding**: Doesn't recognize "?" as missing data marker
3. ❌ **Strict vs. probabilistic**: Blurs the line between "usually true" and "always true"

### Recommendations
- **Use LLMs for**: Identifying obviously degenerate (ID-based) and absurd relationships
- **Don't trust LLMs for**: Distinguishing correlation from functional dependency
- **Always verify**: LLM judgments with data validation (check for violations)

---

**End of Task Set 2 Report**
