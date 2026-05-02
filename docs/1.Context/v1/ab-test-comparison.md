# A/B Test Comparison for ContextBridge ISA

This document shows a sample A/B test run based on:

1. `sample-retrieved-data.json`
2. `ab-test-example.md`
3. `context architecture.md`

The goal is to compare a baseline assistant against ContextBridge ISA with retrieved context and structured output.

## Test Setup

### Version A: Baseline

Version A receives only the user's question.

```text
You are a helpful AI assistant. Answer the user's question clearly.
```

### Version B: ContextBridge ISA

Version B receives:

1. System Layer instructions.
2. Relevant retrieved records from `sample-retrieved-data.json`.
3. Task Input Schema.
4. Task Output Schema.

Version B is expected to include source references, technical relevance, assumptions, uncertainties, and follow-up questions.

## Test Case 1: STP Concept Explanation

### User Question

```text
I am a junior developer working on a payroll reporting ticket. What does Single Touch Payroll mean, and why does it matter for implementation?
```

### Relevant Retrieved Records

1. `stp_overview_001`
2. `mock_payroll_api_001`

### Version A Output

Single Touch Payroll, or STP, is a system used in Australia for reporting payroll information to the tax office. It matters for implementation because payroll software needs to send employee pay and tax information correctly.

As a developer, you should understand what data needs to be sent, how often it is submitted, and how errors are handled. You may need to validate employee and payment information before submitting reports.

### Version B Output

```json
{
  "short_answer": "Single Touch Payroll, or STP, is an Australian payroll reporting process where employers use STP-enabled payroll software to report payroll information to the ATO when employees are paid.",
  "detailed_explanation": "For this payroll reporting ticket, STP is not just a label in the system. It represents a business reporting workflow. Based on the retrieved context, employers report payroll information such as salaries, wages, PAYG withholding, and superannuation information to the ATO when employees are paid.",
  "technical_relevance": "For implementation, STP may affect required fields, validation rules, submission logic, error handling, and reporting status. The mock payroll reporting API shows fields such as employee_id, pay_period_start, pay_period_end, payment_date, gross_pay, net_pay, payg_withholding, super_liability_amount, and reporting_status. It also includes validation errors such as missing_payment_date, invalid_pay_period, missing_employee_id, and negative_gross_pay.",
  "source_references": [
    {
      "source_id": "stp_overview_001",
      "title": "What is Single Touch Payroll?",
      "used_for": "Explaining the meaning of STP."
    },
    {
      "source_id": "mock_payroll_api_001",
      "title": "POST /payroll/reports",
      "used_for": "Connecting STP context to backend validation and API fields."
    }
  ],
  "assumptions": [
    "The ticket is related to payroll reporting based on the user's question."
  ],
  "uncertainties": [
    "The exact project-specific STP validation rules are not provided.",
    "The real API contract may differ from the mock API example."
  ],
  "follow_up_questions": [
    "Which fields are required by the real payroll reporting API?",
    "What should happen when a report submission fails validation?",
    "Which reporting statuses should the system store?"
  ],
  "recommended_actions": [
    "Check the project-specific STP requirements before implementing validation logic.",
    "Confirm edge cases with a BA, PM, or senior developer."
  ]
}
```

## Test Case 2: SuperStream Workflow

### User Question

```text
How does SuperStream relate to payroll data and super contribution payments?
```

### Relevant Retrieved Records

1. `superstream_workflow_001`
2. `super_due_date_rule_001`

### Version A Output

SuperStream is a standard used in Australia for sending superannuation payments and data electronically. Payroll systems usually calculate super contributions and then send the related information to super funds.

It matters because the payroll system needs to make sure contribution data and payment information are correct and submitted on time.

### Version B Output

```json
{
  "short_answer": "SuperStream connects payroll data with superannuation contribution payments by sending contribution data and payments electronically.",
  "detailed_explanation": "Based on the retrieved workflow document, a payroll system may prepare employee super contribution data, link it with an electronic payment using a payment reference number, and send it to a super fund or clearing house. This means SuperStream is part of the flow between payroll calculation and super contribution processing.",
  "technical_relevance": "For implementation, the system may need to store employee contribution amounts, payment reference numbers, target fund or clearing house details, submission status, and payment timing. The due date record also shows that timing matters because super guarantee payments must be received by the employee's super fund by the quarterly due date.",
  "source_references": [
    {
      "source_id": "superstream_workflow_001",
      "title": "SuperStream Contribution Workflow",
      "used_for": "Explaining how contribution data and payments are sent electronically."
    },
    {
      "source_id": "super_due_date_rule_001",
      "title": "Quarterly Super Payment Due Dates",
      "used_for": "Explaining why timing matters."
    }
  ],
  "assumptions": [
    "The user's question is about a payroll system that handles superannuation contributions."
  ],
  "uncertainties": [
    "The exact project-specific SuperStream integration design is not provided.",
    "The source does not define the full payload or clearing house API contract."
  ],
  "follow_up_questions": [
    "Does this system send data directly to super funds or through a clearing house?",
    "Where is the payment reference number stored?",
    "How should the system handle late, failed, or rejected contribution submissions?"
  ],
  "recommended_actions": [
    "Verify implementation details with the project integration documentation.",
    "Treat due-date logic as compliance-sensitive and confirm with official or business sources."
  ]
}
```

## Test Case 3: Pay Slip Data Model

### User Question

```text
I need to design a payslip data model. What fields should I consider and what should I be careful about?
```

### Relevant Retrieved Records

1. `payslip_requirement_001`
2. `mock_payroll_api_001`

### Version A Output

You should include fields such as employee name, employer name, pay period, payment date, gross pay, net pay, tax withheld, deductions, and superannuation contributions.

Be careful about data accuracy, formatting, privacy, and validation. You should also check the legal requirements for payslips in your jurisdiction.

### Version B Output

```json
{
  "short_answer": "A payslip data model should include employer and employee details, pay period, payment date, gross pay, net pay, deductions, and superannuation contribution details.",
  "detailed_explanation": "The retrieved pay slip requirement record lists common pay slip information such as employer name, employee name, pay period, payment date, gross pay, net pay, hourly rate details where applicable, deductions, and superannuation contribution details. These fields form a useful starting point for a payslip model.",
  "technical_relevance": "From a backend perspective, these fields should map to validated payroll data. The mock payroll API also includes related reporting fields such as employee_id, pay_period_start, pay_period_end, payment_date, gross_pay, net_pay, payg_withholding, super_liability_amount, and reporting_status. The data model should distinguish display fields for a payslip from reporting fields used for API submission.",
  "source_references": [
    {
      "source_id": "payslip_requirement_001",
      "title": "Pay Slip Required Information",
      "used_for": "Identifying payslip fields."
    },
    {
      "source_id": "mock_payroll_api_001",
      "title": "POST /payroll/reports",
      "used_for": "Comparing payslip fields with reporting API fields."
    }
  ],
  "assumptions": [
    "The user is designing a general payslip model, not a final production schema."
  ],
  "uncertainties": [
    "The exact product requirements are not provided.",
    "The jurisdiction-specific and company-specific payslip rules need confirmation."
  ],
  "follow_up_questions": [
    "Does the payslip need to support hourly, salary, and contractor payment types?",
    "Which deductions and super fields must be shown to the user?",
    "Should the payslip model be separate from the payroll reporting model?"
  ],
  "recommended_actions": [
    "Confirm required payslip fields with official requirements and project documentation.",
    "Create validation rules for payment date, pay period, gross pay, net pay, and negative amounts."
  ]
}
```

## Test Case 4: Missing Context Detection

### User Question

```text
The ticket says we need to validate payroll report submissions before sending them. What information is missing before I can implement this safely?
```

### Relevant Retrieved Records

1. `mock_payroll_api_001`
2. `stp_overview_001`
3. `super_due_date_rule_001`

### Version A Output

You need to know which fields are required, what validation rules apply, what errors should be returned, and what should happen if validation fails. You should also check if there are any compliance requirements.

Before implementing, ask the product owner or business analyst for detailed acceptance criteria and edge cases.

### Version B Output

```json
{
  "short_answer": "Before implementing validation, you need the exact required fields, validation rules, error handling behavior, and source of truth for any compliance-sensitive requirements.",
  "detailed_explanation": "The retrieved mock API record gives example required fields and validation errors, but it is not enough to implement production logic safely. The STP record shows that payroll reporting may involve salaries, wages, PAYG withholding, and superannuation information reported to the ATO. The super due date record shows that timing can matter for super-related workflows. However, the ticket does not say which rules apply to this specific submission flow.",
  "technical_relevance": "The implementation may need field-level validation, pay period validation, payment date validation, negative amount checks, reporting status handling, and failure handling. It may also need different behavior depending on whether the submission relates to STP reporting, super contribution timing, or internal product rules.",
  "source_references": [
    {
      "source_id": "mock_payroll_api_001",
      "title": "POST /payroll/reports",
      "used_for": "Identifying example fields and validation errors."
    },
    {
      "source_id": "stp_overview_001",
      "title": "What is Single Touch Payroll?",
      "used_for": "Explaining the payroll reporting context."
    },
    {
      "source_id": "super_due_date_rule_001",
      "title": "Quarterly Super Payment Due Dates",
      "used_for": "Showing that date-based rules may matter for super-related workflows."
    }
  ],
  "assumptions": [
    "The validation is for payroll report submissions before an external or internal submission step."
  ],
  "uncertainties": [
    "Which fields are mandatory for this specific report type?",
    "Which validation errors should block submission?",
    "Which errors should be warnings only?",
    "Whether the validation rules come from STP, super payment due dates, internal business rules, or API requirements.",
    "What retry or correction workflow should happen after failed validation?"
  ],
  "follow_up_questions": [
    "Which fields are required for this report type?",
    "What are the exact validation rules for pay period, payment date, and negative amounts?",
    "What error messages or error codes should the API return?",
    "Should failed submissions be saved as draft, rejected, or blocked before submission?",
    "Who owns the source of truth for these validation rules?"
  ],
  "recommended_actions": [
    "Ask the BA, PM, or senior developer for acceptance criteria.",
    "Check whether official STP or superannuation rules apply to this workflow.",
    "Write unit tests for missing payment date, invalid pay period, missing employee ID, and negative gross pay."
  ]
}
```

## Scoring Results

Scores are from 1 to 5.

| Test Case | Version | Accuracy | Relevance | Groundedness | Technical Usefulness | Uncertainty Handling | Clarity | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | 4 | 4 | 2 | 3 | 2 | 4 | 19 |
| 1 | B | 5 | 5 | 5 | 5 | 5 | 5 | 30 |
| 2 | A | 4 | 4 | 2 | 3 | 2 | 4 | 19 |
| 2 | B | 5 | 5 | 5 | 5 | 5 | 5 | 30 |
| 3 | A | 4 | 4 | 2 | 3 | 3 | 4 | 20 |
| 3 | B | 5 | 5 | 5 | 5 | 5 | 5 | 30 |
| 4 | A | 4 | 4 | 2 | 4 | 4 | 4 | 22 |
| 4 | B | 5 | 5 | 5 | 5 | 5 | 5 | 30 |

## Average Scores

| Version | Accuracy | Relevance | Groundedness | Technical Usefulness | Uncertainty Handling | Clarity | Average Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | 4.0 | 4.0 | 2.0 | 3.25 | 2.75 | 4.0 | 20.0 |
| B | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 30.0 |

## Result Summary

Version B performed better across all test cases. The biggest improvements were in groundedness, technical usefulness, and uncertainty handling.

Version A gave generally correct high-level answers, but the responses were not strongly tied to the sample retrieved data. It also did not clearly separate confirmed information from assumptions or identify missing project-specific information in detail.

Version B was more useful for the target user because it:

1. Referenced the relevant retrieved records.
2. Connected business concepts to implementation work.
3. Identified missing context before implementation.
4. Suggested practical follow-up questions.
5. Avoided treating public or synthetic sample data as final compliance authority.

## Conclusion

This A/B test supports the hypothesis that ContextBridge ISA's four-layer context architecture improves answer quality compared with a baseline assistant. The Retrieved Layer and Task Output Schema make the answers more traceable, structured, and useful for junior developers working with complex payroll and superannuation context.
