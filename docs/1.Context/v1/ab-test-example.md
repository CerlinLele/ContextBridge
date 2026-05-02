# A/B Test Example for ContextBridge ISA

This document defines a small A/B test for evaluating whether the four-layer context architecture improves ISA's answer quality.

## Test Goal

Evaluate whether ISA gives more accurate, grounded, and developer-useful answers when it uses the Retrieved Layer and structured Task Output Schema.

## Hypothesis

Version B will perform better than Version A because it uses retrieved context from `sample-retrieved-data.json` and follows the structured output rules defined in `context architecture.md`.

## Test Variants

### Version A: Baseline Assistant

Version A uses only a simple system prompt and the user's question. It does not receive retrieved documents and does not need to follow the structured output schema.

Example behavior:

```text
You are a helpful AI assistant. Answer the user's question clearly.
```

### Version B: ContextBridge ISA

Version B uses:

1. System Layer from `context architecture.md`.
2. Retrieved Layer using relevant records from `sample-retrieved-data.json`.
3. Task Input Schema.
4. Task Output Schema.

Version B must include:

1. Short answer.
2. Detailed explanation.
3. Technical relevance.
4. Source references.
5. Assumptions and uncertainties.
6. Follow-up questions or recommended actions.

## Test Dataset

Use the following sample retrieved records:

1. `stp_overview_001`
2. `superstream_workflow_001`
3. `super_due_date_rule_001`
4. `payslip_requirement_001`
5. `mock_payroll_api_001`

## Test Questions

### Test Case 1: STP Concept Explanation

User question:

```text
I am a junior developer working on a payroll reporting ticket. What does Single Touch Payroll mean, and why does it matter for implementation?
```

Relevant retrieved records:

1. `stp_overview_001`
2. `mock_payroll_api_001`

Expected good answer:

1. Explains STP as an Australian payroll reporting process.
2. Mentions that employers report payroll information to the ATO when employees are paid.
3. Connects STP to required fields, validation, submission timing, and reporting status.
4. References retrieved sources.
5. States uncertainty if exact project-specific validation rules are not provided.

### Test Case 2: SuperStream Workflow

User question:

```text
How does SuperStream relate to payroll data and super contribution payments?
```

Relevant retrieved records:

1. `superstream_workflow_001`
2. `super_due_date_rule_001`

Expected good answer:

1. Explains that SuperStream sends super contribution data and payments electronically.
2. Mentions the link between employee contribution data, payment reference, super fund, or clearing house.
3. Explains why payment timing matters.
4. Avoids giving final compliance advice.
5. Suggests checking official or project-specific rules.

### Test Case 3: Pay Slip Data Model

User question:

```text
I need to design a payslip data model. What fields should I consider and what should I be careful about?
```

Relevant retrieved records:

1. `payslip_requirement_001`
2. `mock_payroll_api_001`

Expected good answer:

1. Lists key fields such as employer name, employee name, pay period, payment date, gross pay, net pay, deductions, and superannuation details.
2. Connects those fields to possible validation and backend data modelling.
3. Separates general public requirements from project-specific rules.
4. Suggests follow-up questions about exact product requirements.

### Test Case 4: Missing Context Detection

User question:

```text
The ticket says we need to validate payroll report submissions before sending them. What information is missing before I can implement this safely?
```

Relevant retrieved records:

1. `mock_payroll_api_001`
2. `stp_overview_001`
3. `super_due_date_rule_001`

Expected good answer:

1. Identifies missing validation rules.
2. Asks which fields are required.
3. Asks what should happen on validation failure.
4. Asks whether rules are based on STP, super payment dates, or project-specific requirements.
5. Recommends confirming with a BA, PM, senior developer, or official documentation.

## Prompt Setup

### Version A Prompt

```text
You are a helpful AI assistant. Answer the user's question clearly.

User question:
{user_question}
```

### Version B Prompt

```text
System:
You are ContextBridge ISA, an Intelligent Study Assistant designed to help developers understand complex business domains.

Use clear and structured explanations. Prefer answers grounded in retrieved documents or provided context. Clearly separate confirmed information from assumptions. If the provided context is insufficient, say what is missing. Avoid hallucinating business rules, compliance requirements, or system behavior.

Retrieved context:
{retrieved_context}

Task input:
{
  "user_profile": {
    "role": "junior developer",
    "domain_knowledge_level": "beginner",
    "technical_knowledge_level": "intermediate",
    "current_context": "working on a payroll or superannuation feature"
  },
  "task": {
    "task_type": "explain_business_context",
    "user_question": "{user_question}",
    "user_goal": "understand the business meaning and implementation impact",
    "expected_depth": "practical explanation for development work"
  },
  "constraints": {
    "answer_language": "English",
    "answer_style": "clear, structured, and beginner-friendly",
    "include_source_references": true,
    "include_technical_relevance": true,
    "avoid_unsupported_assumptions": true,
    "include_follow_up_questions": true
  }
}

Return the answer using the Task Output Schema:
- short_answer
- detailed_explanation
- technical_relevance
- source_references
- assumptions
- uncertainties
- follow_up_questions
- recommended_actions
```

## Evaluation Metrics

Score each answer from 1 to 5 for each metric.

| Metric | Description |
| --- | --- |
| Accuracy | The answer is factually correct based on the sample retrieved data. |
| Relevance | The answer directly addresses the user's question. |
| Groundedness | The answer is clearly supported by retrieved sources. |
| Technical usefulness | The answer explains how the business context affects implementation. |
| Uncertainty handling | The answer identifies missing context instead of guessing. |
| Clarity | The answer is understandable for a junior developer. |

## Scoring Template

| Test Case | Version | Accuracy | Relevance | Groundedness | Technical Usefulness | Uncertainty Handling | Clarity | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A |  |  |  |  |  |  |  |
| 1 | B |  |  |  |  |  |  |  |
| 2 | A |  |  |  |  |  |  |  |
| 2 | B |  |  |  |  |  |  |  |
| 3 | A |  |  |  |  |  |  |  |
| 3 | B |  |  |  |  |  |  |  |
| 4 | A |  |  |  |  |  |  |  |
| 4 | B |  |  |  |  |  |  |  |

## Success Criteria

The A/B test is considered successful if Version B shows clear improvement over Version A in:

1. Groundedness.
2. Technical usefulness.
3. Uncertainty handling.
4. Overall total score.

The expected result is that Version B may be longer, but it should be more reliable, traceable, and useful for junior developers working with complex business context.

## Example Result Summary

```text
Version B performed better because it used retrieved records to explain domain concepts, connected the explanation to implementation work, and clearly identified missing project-specific information. Version A provided a general explanation, but it was less grounded and did not consistently distinguish between public domain knowledge and assumptions.
```
