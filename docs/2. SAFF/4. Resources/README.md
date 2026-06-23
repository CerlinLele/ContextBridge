# SAFF Resources & References

This section provides external resources, operational guides, and reference materials related to SAFF (SuperStream Alternative File Format).

## External Resources

### Official Government Sources

#### 1. ATO SuperStream Documentation
**Source**: Australian Taxation Office (ATO)  
**URL**: https://softwaredevelopers.ato.gov.au/STPdocumentlibrary

**Content**:
- Official SuperStream technical documentation
- STP and SAFF specifications
- Implementation guidance
- Testing documentation

**Best For**:
- Official specification reference
- Compliance guidance
- Implementation requirements

---

#### 2. ATO SuperStream Guidance Index
**Source**: Australian Taxation Office (ATO)  
**URL**: https://softwaredevelopers.ato.gov.au/SSTC/Guidance

**Content**:
- Historical guidance notes (G015 on SAFF)
- Links to SAFF-related guidance
- Implementation context
- Version history

**Best For**:
- Historical context
- Official guidance traceability
- Finding specific guidance notes

---

#### 3. ATO Single Touch Payroll
**Source**: Australian Taxation Office (ATO)  
**URL**: https://www.ato.gov.au/businesses-and-organisations/hiring-and-paying-your-workers/single-touch-payroll

**Content**:
- STP concepts and requirements
- Employer reporting workflow
- STP reporting options
- FAQ and guidance

**Best For**:
- Domain understanding
- Employer perspective
- FAQ and common questions

---

### Industry Specifications

#### 4. GESB SuperStream Payroll Data Specification
**Source**: Global Employee Superannuation System Board (GESB)  
**URL**: https://www.gesb.wa.gov.au/__data/assets/pdf_file/0020/2675/superstream_payroll_data_specification.pdf

**Content**:
- Fund-specific SAFF implementation
- Detailed field definitions
- Validation rules
- Record type structures

**Best For**:
- Field-level reference
- Validation rule implementation
- Complex table examples

**Stored Locally**: `knowledge_base/sources/structured-business-file-formats/saff/specifications/gesb/superstream-payroll-data-specification.pdf`

---

#### 5. CSC PSSAP SAFF Extended Requirements
**Source**: Computer Support Corporation (CSC)  
**URL**: [Provider-specific implementation]

**Content**:
- PSSAP system SAFF requirements
- Extended data fields
- System-specific validation
- Submission procedures

**Best For**:
- PSSAP-specific implementation
- Extended field documentation
- Provider-specific guidance

**Stored Locally**: `knowledge_base/sources/structured-business-file-formats/saff/specifications/csc-pssap/pssap-saff-extended-data-requirements.pdf`

---

### Operational Guides

#### 6. Mercer SAFF Support Guide - Employer Portal
**Source**: Mercer Financial Services  
**URL**: https://www.mercerfinancialservices.com/content/dam/mercer/Aus/attachments/MST/MercerSpectrum/SAFF%20Support%20Guide%20-%20Employer%20Portal.pdf

**Content**:
- SAFF file upload workflow
- Employer portal procedures
- Step-by-step submission guides
- Troubleshooting and support

**Best For**:
- Operational procedures
- User workflow understanding
- Portal integration context
- Screenshot-based reference

**Stored Locally**: `knowledge_base/sources/structured-business-file-formats/saff/operational-guides/mercer/saff-support-guide-employer-portal.pdf`

---

### Superannuation Context

#### 7. ATO Super Payment Due Dates
**Source**: Australian Taxation Office (ATO)  
**URL**: https://www.ato.gov.au/businesses-and-organisations/super-for-employers/paying-super-contributions/super-payment-due-dates

**Content**:
- Super payment deadlines
- Employer obligations
- Compliance requirements
- Penalty information

**Best For**:
- Compliance context
- Date-based validation
- Business rules
- Deadline management

---

#### 8. ATO SuperStream for Employers
**Source**: Australian Taxation Office (ATO)  
**URL**: https://www.ato.gov.au/businesses-and-organisations/super-for-employers/paying-super/paying-super-contributions/how-to-pay-super/superstream-for-employers

**Content**:
- SuperStream submission process
- Data and payment standards
- Clearing house concepts
- Payment workflows

**Best For**:
- SuperStream process understanding
- Payment context
- Data standard overview
- Workflow documentation

---

### Payroll Context

#### 9. Fair Work Ombudsman - Pay Slips
**Source**: Fair Work Ombudsman (Australia)  
**URL**: https://www.fairwork.gov.au/pay-and-wages/paying-wages/pay-slips

**Content**:
- Pay slip requirements
- Required fields and formatting
- Timing and delivery
- Compliance requirements

**Best For**:
- Payroll data requirements
- Compliance documentation
- Field definitions
- Format specifications

---

#### 10. Fair Work Ombudsman - Templates
**Source**: Fair Work Ombudsman (Australia)  
**URL**: https://www.fairwork.gov.au/tools-and-resources/templates

**Content**:
- Pay slip templates
- Timsheet examples
- Employee records templates
- Various payroll forms

**Best For**:
- Template reference
- Sample data structure
- Practical examples
- Compliance forms

---

## Local Knowledge Base

### Processed Artifacts
Located in: `knowledge_base/processed/structured-business-file-formats/saff/`

- `specifications/gesb/superstream-payroll-data-specification.dependency-trace.json`
- `specifications/gesb/superstream-payroll-data-specification.pymupdf-tables.json`
- `specifications/gesb/superstream-payroll-data-specification.parsed.json`

See [Extraction Results](../3.%20Extraction%20Results/) for details.

---

### Source Documents
Located in: `knowledge_base/sources/structured-business-file-formats/saff/`

**Official Specifications**:
- `official/ato/superstream-alternative-file-format-v1.0.xlsx`
- `specifications/gesb/superstream-payroll-data-specification.pdf`
- `specifications/csc-pssap/pssap-saff-extended-data-requirements.pdf`

**Operational Guides**:
- `operational-guides/mercer/saff-support-guide-employer-portal.pdf`

---

## Reference Materials

### ABS Statistical Context
**Source**: Australian Bureau of Statistics (ABS)

**Payroll Jobs**: https://www.abs.gov.au/statistics/labour/jobs/payroll-jobs/latest-release
- Public payroll statistics
- Employment trends
- Aggregate data

**STP Methodology**: https://www.abs.gov.au/statistics/detailed-methodology-information/concepts-sources-methods/labour-statistics-concepts-sources-and-methods/2023/methods-four-pillars-labour-statistics/administrative-data/single-touch-payroll-stp
- Statistical context for STP
- Data coverage and limitations
- Methodology documentation

---

### Domain Glossary

#### Key Terms

| Term | Definition | Context |
|------|-----------|---------|
| **SAFF** | SuperStream Alternative File Format | File-based contribution submission |
| **SuperStream** | Standardized data exchange format | Super fund submission standard |
| **GESB** | Global Employee Superannuation System Board | Fund authority |
| **STP** | Single Touch Payroll | Real-time payroll reporting |
| **ATO** | Australian Taxation Office | Tax authority |
| **MIG** | Message Implementation Guide | SuperStream specification |
| **Clearing House** | Electronic payment processor | Contribution settlement |
| **PSSAP** | Public Sector Superannuation Accumulation Plan | Specific fund system |

---

## Resource Organization by Purpose

### For Understanding SAFF Format
1. Start: GESB Specification (local)
2. Reference: ATO Official SAFF Format
3. Deep Dive: [Specifications Documentation](../1.%20Specifications/)

### For Implementation
1. Start: [Parser Implementation](../2.%20Implementation/)
2. Reference: GESB Specification + ATO Guidance
3. Advanced: [Table Parsing Guide](../2.%20Implementation/table-parsing/)

### For Operational Context
1. Start: Mercer Support Guide (local)
2. Reference: ATO SuperStream for Employers
3. Compliance: ATO Super Payment Due Dates

### For Compliance
1. Start: ATO Guidance Index
2. Reference: Fair Work Ombudsman Resources
3. Validation: GESB Field Definitions

### For Testing
1. Start: [Extraction Results](../3.%20Extraction%20Results/)
2. Reference: GESB Specification (local)
3. Advanced: [Quality Issues](../2.%20Implementation/table-parsing/quality-issues.md)

---

## Accessing External Resources

### Online Access
Most external resources are publicly available at the URLs listed above. They are free to access for developers and researchers.

### Local Copies
Download public PDFs and store locally in `knowledge_base/sources/` for offline reference and testing.

### Legal & Licensing
- Government resources (ATO, ABS) are public domain
- GESB specification is public guidance
- Mercer guide is public support material
- Check specific sources for licensing terms

---

## Keeping Resources Current

### Update Frequency
- ATO guidance: Check annually
- GESB specification: Check when versions change
- Mercer guides: Check when portal updates
- Fair Work templates: Check annually

### Version Tracking
- Record download dates and versions
- Note any specification changes
- Track breaking changes in implementations
- Update local copies when significant changes occur

---

## Resource Contribution

### Found a New Resource?
Document it here with:
- Source and URL
- Content summary
- Best use case
- Local storage location (if applicable)

### Found an Issue?
Update the relevant resource section with:
- URL changes
- Content corrections
- New guidance related to SAFF

---

## Quick Reference URLs

```
ATO STP Documentation:
https://softwaredevelopers.ato.gov.au/STPdocumentlibrary

ATO SAFF Guidance:
https://softwaredevelopers.ato.gov.au/SSTC/Guidance

GESB SAFF Spec (PDF):
https://www.gesb.wa.gov.au/__data/assets/pdf_file/0020/2675/superstream_payroll_data_specification.pdf

Mercer SAFF Guide (PDF):
https://www.mercerfinancialservices.com/content/dam/mercer/Aus/attachments/MST/MercerSpectrum/SAFF%20Support%20Guide%20-%20Employer%20Portal.pdf

Fair Work Pay Slips:
https://www.fairwork.gov.au/pay-and-wages/paying-wages/pay-slips
```

---

## Related Documentation

- [SAFF Overview](../README.md) - Main SAFF hub
- [Specifications](../1.%20Specifications/) - Format specifications
- [Implementation](../2.%20Implementation/) - Parser implementation
- [Extraction Results](../3.%20Extraction%20Results/) - Parsed artifacts
