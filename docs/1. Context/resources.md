# Public Resources for Retrieved Context

This document lists public and safe resources that can be used to build the Retrieved Layer for ContextBridge ISA. The project should not use confidential company documents, real employee data, private payroll records, or internal materials from previous work.

The goal is to combine public domain knowledge with synthetic demo documents to simulate the type of fragmented business context that developers often need to understand in real projects.

## Recommended Sources

### 1. ATO Single Touch Payroll

URL: https://www.ato.gov.au/businesses-and-organisations/hiring-and-paying-your-workers/single-touch-payroll

Use for:

1. Single Touch Payroll concepts.
2. Employer reporting workflow.
3. STP reporting options.
4. Domain glossary terms.
5. Beginner-friendly FAQ content.

Suitable demo documents:

1. Domain Glossary.
2. Workflow Document.
3. FAQ / Onboarding Notes.

### 2. ATO Software Developers - STP Document Library

URL: https://softwaredevelopers.ato.gov.au/STPdocumentlibrary

Use for:

1. STP technical documentation.
2. Business implementation guidance.
3. Developer-oriented terminology.
4. Testing and implementation context.

Suitable demo documents:

1. Mock API Specification.
2. Business Rules Document.
3. Developer Onboarding Notes.

### 3. ATO SuperStream for Employers

URL: https://www.ato.gov.au/businesses-and-organisations/super-for-employers/paying-super-contributions/how-to-pay-super/superstream-for-employers

Use for:

1. Super contribution workflow.
2. SuperStream data and payment process.
3. Clearing house concepts.
4. Payment and data matching context.

Suitable demo documents:

1. Workflow Document.
2. Business Rules Document.
3. Domain Glossary.

### 4. ATO Super Payment Due Dates

URL: https://www.ato.gov.au/businesses-and-organisations/super-for-employers/paying-super-contributions/super-payment-due-dates

Use for:

1. Super payment due dates.
2. Employer obligations.
3. Date-based validation examples.
4. Compliance-sensitive workflow context.

Suitable demo documents:

1. Business Rules Document.
2. FAQ / Onboarding Notes.
3. Validation Rules.

### 5. Fair Work Ombudsman - Pay Slips

URL: https://www.fairwork.gov.au/pay-and-wages/paying-wages/pay-slips

Use for:

1. Pay slip requirements.
2. Required fields.
3. Timing requirements.
4. Payroll record explanation.

Suitable demo documents:

1. Business Rules Document.
2. Sample Payroll Requirements.
3. FAQ / Onboarding Notes.

### 6. Fair Work Ombudsman - Templates

URL: https://www.fairwork.gov.au/tools-and-resources/templates

Use for:

1. Pay slip templates.
2. Time and wage record examples.
3. Employee details templates.
4. Timesheet examples.

Suitable demo documents:

1. Sample Forms.
2. Mock Records.
3. RAG Demo Documents.

### 7. ABS Single Touch Payroll Methodology

URL: https://www.abs.gov.au/statistics/detailed-methodology-information/concepts-sources-methods/labour-statistics-concepts-sources-and-methods/2023/methods-four-pillars-labour-statistics/administrative-data/single-touch-payroll-stp

Use for:

1. STP as a public administrative data source.
2. Background context for payroll data.
3. Data coverage and limitations.
4. High-level domain explanation.

Suitable demo documents:

1. Background Context.
2. Domain Explanation.
3. Data Source Notes.

### 8. ABS Payroll Jobs

URL: https://www.abs.gov.au/statistics/labour/jobs/payroll-jobs/latest-release

Use for:

1. Public payroll jobs and wages statistics.
2. Example public datasets.
3. Analytics-oriented demo data.

Suitable demo documents:

1. Sample Dataset.
2. Analytics Demo.
3. Data Interpretation Notes.

### 9. Mockaroo

URL: https://mockaroo.com/

Use for:

1. Synthetic employee records.
2. Synthetic payroll records.
3. Mock timesheet data.
4. Mock API request and response payloads.

Suitable demo documents:

1. Synthetic Employee Data.
2. Mock API Payloads.
3. Test CSV / JSON Files.

### 10. GESB SAFF Payroll Data Specification

URL: https://www.gesb.wa.gov.au/__data/assets/pdf_file/0020/2675/superstream_payroll_data_specification.pdf

Use for:

1. SuperStream Alternative File Format examples.
2. Payroll contribution file structure.
3. Field-level validation and mapping examples.
4. Complex PDF table parsing test cases.

Suitable demo documents:

1. SAFF File Format Notes.
2. Field Mapping Reference.
3. Parser Test PDF.
4. Payroll Contribution Validation Rules.

Notes:

1. SAFF means SuperStream Alternative File Format.
2. This is a fund-specific payroll data specification and should be used as public demo context, not as the only authoritative SuperStream reference.
3. It is useful for testing structure-aware PDF parsing because the PDF contains specification sections, tables, and field-level rules.

### 11. Mercer SAFF Support Guide - Employer Portal

URL: https://www.mercerfinancialservices.com/content/dam/mercer/Aus/attachments/MST/MercerSpectrum/SAFF%20Support%20Guide%20-%20Employer%20Portal.pdf

Use for:

1. SAFF file upload workflow examples.
2. Employer portal contribution submission context.
3. Operational guidance around preparing and submitting SAFF files.
4. Screenshot-heavy PDF parsing and retrieval test cases.

Suitable demo documents:

1. SAFF Upload Workflow Notes.
2. Employer Portal Contribution Guide.
3. Operational FAQ.
4. Parser Test PDF.

Notes:

1. This is a provider-specific support guide and should be used as public demo context.
2. It complements the GESB SAFF payroll data specification by showing an employer portal workflow rather than only field-level file structure.
3. It is useful for testing parser behavior on PDFs with screenshots, step-by-step instructions, and operational guidance.

### 12. ATO SuperStream Data and Payment Standards Guidance Notes

URL: https://softwaredevelopers.ato.gov.au/SSTC/Guidance

Use for:

1. Official SuperStream guidance note index.
2. Historical and current technical guidance around SuperStream implementation.
3. Context for how ATO guidance complements MIGs and user guides.
4. Finding SAFF-related historical guidance references.

Suitable demo documents:

1. SuperStream Guidance Index Notes.
2. SAFF Guidance Background.
3. Technical Guidance Summary.
4. Implementation Context Notes.

Notes:

1. This page is an official ATO Software Developers guidance index, not a single SAFF file specification.
2. It includes a historical `G015 SuperStream alternative file format guidance` entry and references an example alternative format file.
3. It is useful for official context and traceability, while provider PDFs such as GESB and Mercer are better parser test sources.

## Suggested MVP Document Set

For the first version of the Retrieved Layer, prepare a small and controlled document set:

1. `domain-glossary.md`
   A glossary explaining payroll, superannuation, Single Touch Payroll, ATO, clearing house, contribution, validation, pay event, and reporting status.

2. `payroll-reporting-workflow.md`
   A simplified workflow covering employee payroll data collection, validation, submission, response handling, and status update.

3. `mock-payroll-reporting-api.md`
   A mock API specification for endpoints such as `POST /payroll/reports`, including request fields, response fields, validation errors, and status codes.

4. `demo-business-rules.md`
   A small set of demo rules covering required fields, validation timing, missing data handling, submission status transitions, and retry behavior.

5. `developer-faq.md`
   Beginner-friendly onboarding notes for junior developers, including common questions about STP, validation, payroll reporting, and implementation risks.

6. `saff-file-format-notes.md`
   Notes extracted from a public SAFF payroll data specification, including contribution file structure, field mapping examples, and validation considerations.

7. `saff-upload-workflow-notes.md`
   Notes extracted from a public employer portal SAFF support guide, including upload workflow, operational steps, and common submission considerations.

8. `superstream-guidance-index-notes.md`
   Notes extracted from ATO SuperStream guidance notes, including how guidance notes relate to MIGs, user guides, and historical SAFF references.

## Usage Notes

Public resources should be used for general domain understanding and safe demo context. They should not be treated as final legal, tax, payroll, or compliance advice.

For compliance-sensitive topics, ISA should still recommend verification with official documentation, a domain expert, or the relevant business stakeholder.

Synthetic data should not include real employee names, real TFNs, real payroll records, real company records, or confidential materials from previous work.
