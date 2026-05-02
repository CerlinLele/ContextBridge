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

## Usage Notes

Public resources should be used for general domain understanding and safe demo context. They should not be treated as final legal, tax, payroll, or compliance advice.

For compliance-sensitive topics, ISA should still recommend verification with official documentation, a domain expert, or the relevant business stakeholder.

Synthetic data should not include real employee names, real TFNs, real payroll records, real company records, or confidential materials from previous work.
