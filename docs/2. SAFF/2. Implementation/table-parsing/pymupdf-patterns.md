# PyMuPDF Table Parsing Patterns

This document consolidates reusable patterns for extracting and analyzing tables from SAFF specification PDFs using PyMuPDF.

## Core Patterns

### 1. Word-Level Extraction Pattern
Extracts words with their positions and bounding boxes from PDF content.

**Use when**: You need precise positional information about text elements
**Return**: Array of word objects with coordinates

**Key advantages**:
- Preserves layout information
- Enables coordinate-based grouping
- Works with complex formatting

---

### 2. Spatial Clustering Pattern
Groups words into columns and rows based on their coordinate proximity.

**Algorithm**:
- Collect word positions from page
- Detect column boundaries (x-axis clustering)
- Detect row boundaries (y-axis clustering)
- Group words into cells based on boundaries

**Use when**: Converting word positions into table structure

---

### 3. Header Detection Pattern
Identifies and validates table header rows.

**Characteristics to detect**:
- Font weight (often bold)
- Position (typically top of table)
- Alignment (centered or left-aligned)
- Content pattern (field names, descriptors)

**Use when**: Separating header information from data rows

---

### 4. Cell Boundary Inference Pattern
Determines table cell boundaries when they're not explicitly drawn.

**Approach**:
- Use column boundaries from word positions
- Use row boundaries from word positions
- Infer cell edges from spacing patterns
- Validate against document structure

**Use when**: Working with PDF tables that lack explicit cell borders

---

### 5. Multi-Row Content Pattern
Handles cells containing content that spans multiple lines.

**Processing steps**:
- Detect word groupings within same cell
- Preserve line breaks and internal structure
- Accumulate content within cell boundaries
- Maintain content order

**Use when**: Tables have cells with wrapped text or multiple lines

---

## Layout Analysis Techniques

### Column Detection
```
1. Extract all word x-coordinates
2. Find gaps indicating column boundaries
3. Classify gap sizes (major/minor)
4. Use major gaps as column separators
```

### Row Detection
```
1. Extract all word y-coordinates  
2. Find gaps indicating row boundaries
3. Account for within-row spacing
4. Use row boundaries for grouping
```

### Cell Reconstruction
```
1. For each column-row intersection
2. Find all words within boundaries
3. Sort words by position
4. Join words into cell content
5. Handle merged cells if present
```

---

## Data Type Handling

### Text Cells
- Preserve original formatting
- Handle multi-line content
- Extract and clean whitespace

### Numeric Cells
- Detect numeric content
- Preserve decimal formatting
- Handle special symbols (±, %, etc.)

### Reference Cells
- Capture reference markers
- Preserve note indicators
- Track cell relationships

### Empty Cells
- Explicitly track empty cells
- Distinguish empty from content-free
- Maintain grid structure

---

## Edge Cases & Workarounds

### Merged Cells
**Challenge**: Cell spans multiple columns/rows  
**Solution**: Detect merged regions and associate content appropriately

### Variable Column Widths
**Challenge**: Columns have different widths  
**Solution**: Use detected boundaries rather than fixed widths

### Overlapping Text
**Challenge**: Text from different cells overlaps  
**Solution**: Use y-coordinate separation as primary grouping

### Font Size Variation
**Challenge**: Different font sizes in table  
**Solution**: Group by position rather than relying on font metrics

---

## Validation Techniques

### Structural Validation
- Verify column count consistency
- Verify row count consistency
- Check for orphaned content

### Content Validation
- Verify expected field names in headers
- Check data type consistency
- Validate value ranges

### Positional Validation
- Confirm words are within expected boundaries
- Verify no content gaps
- Check coordinate continuity

---

## Performance Considerations

### Optimization Strategies
1. **Cache page analysis** - Don't re-analyze same page
2. **Batch coordinate calculations** - Process coordinates in bulk
3. **Use spatial indexing** - For large tables
4. **Incremental parsing** - Process tables one at a time

### Memory Management
- Stream large PDF processing
- Clear intermediate data structures
- Use generators for large result sets

---

## Integration with Parser

### Pipeline Integration
```
PDF Input 
  → Word Extraction (Pattern 1)
  → Spatial Clustering (Pattern 2)
  → Header Detection (Pattern 3)
  → Cell Boundary Inference (Pattern 4)
  → Multi-Row Content Assembly (Pattern 5)
  → JSON Output
```

### Error Recovery
- Graceful fallback for pattern failures
- Partial results on boundary issues
- Diagnostic output for debugging

---

## Testing Patterns

### Unit Tests
- Test each pattern independently
- Verify coordinate calculations
- Check boundary detection accuracy

### Integration Tests
- Full table extraction pipeline
- Multi-table document processing
- Format conversion validation

### Regression Tests
- Known problematic tables
- Format variations
- Edge case handling

---

## Future Enhancements

- Machine learning for header detection
- Graph-based table reconstruction
- Template-based parsing for repeated formats
- Confidence scoring for extracted cells

---

## References

- **Source**: `src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment_walkthrough.ipynb`
- **Quality Issues**: See [`quality-issues.md`](./quality-issues.md)
- **Implementation Plan**: See [`implementation-plan.md`](./implementation-plan.md)
