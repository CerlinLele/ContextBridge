# SAFF Specifications

This section documents the official SAFF file format specifications from various sources.

## Available Specifications

### 1. GESB SuperStream Payroll Data Specification
**Source**: Global Employee Superannuation System Board (GESB)  
**File**: `superstream-payroll-data-specification.pdf`  
**Location**: `knowledge_base/sources/structured-business-file-formats/saff/specifications/gesb/`

**Content Coverage**:
- SuperStream Alternative File Format structure
- Payroll contribution file layout
- Field definitions and validation rules
- Record type specifications
- Data formatting requirements

**Key Tables**:
- Contribution file header and trailer records
- Member contribution records
- Fund specification records
- Validation rule definitions

**Parsed Artifacts**:
- `superstream-payroll-data-specification.dependency-trace.json` - Document structure analysis
- `superstream-payroll-data-specification.pymupdf-tables.json` - Extracted table metadata
- `superstream-payroll-data-specification.parsed.json` - Full content extraction

**Use Cases**:
- Field mapping reference for SAFF file parsing
- Validation rule implementation
- PDF table parsing test cases (structure-heavy tables)

---

### 2. ATO SuperStream Alternative File Format v1.0
**Source**: Australian Taxation Office (ATO)  
**File**: `superstream-alternative-file-format-v1.0.xlsx`  
**Location**: `knowledge_base/sources/structured-business-file-formats/saff/official/ato/`

**Content Coverage**:
- Official ATO SAFF format specification
- Record types and field requirements
- Data type specifications
- Validation requirements

**Use Cases**:
- Official reference for SAFF compliance
- Field-level validation rules
- Data type and format specifications

---

### 3. CSC PSSAP Extended Data Requirements
**Source**: Computer Support Corporation (CSC) - PSSAP system  
**File**: `pssap-saff-extended-data-requirements.pdf`  
**Location**: `knowledge_base/sources/structured-business-file-formats/saff/specifications/csc-pssap/`

**Content Coverage**:
- Extended SAFF data requirements for PSSAP system
- Additional fields beyond standard SAFF
- System-specific validation rules
- Data submission requirements

**Use Cases**:
- PSSAP-specific SAFF implementation
- Extended field documentation
- Provider-specific requirements

---

## Specification Comparison Matrix

| Aspect | GESB | ATO v1.0 | CSC PSSAP |
|--------|------|----------|-----------|
| **Focus** | Fund-specific payroll structure | Official SAFF standard | System-specific extensions |
| **Format** | PDF with detailed tables | Excel spreadsheet | PDF with detailed requirements |
| **Validation Rules** | Comprehensive | Complete | Extended |
| **Target Audience** | Fund implementers | Developers/Compliance | PSSAP users |

---

## How to Use These Specifications

1. **For SAFF file parsing**: Start with GESB or ATO specification
2. **For field validation**: Reference the specific field definitions in each spec
3. **For provider-specific work**: See CSC PSSAP for extended requirements
4. **For PDF parsing test cases**: GESB PDF is structure-heavy and excellent for testing

---

## Related Documentation

- [Parser Implementation Guide](../2.%20Implementation/parser-logic.md) - How we parse SAFF data
- [Table Parsing Approach](../2.%20Implementation/table-parsing/pymupdf-patterns.md) - Technical approach to extracting table data
- [Extraction Results](../3.%20Extraction%20Results/) - Parsed artifacts from these specifications
