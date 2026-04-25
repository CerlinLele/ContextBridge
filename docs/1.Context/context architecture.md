# Four-Layer Context Architecture

## 1. System Layer

The System Layer defines ISA's global identity, behavioral rules, response style, and safety boundaries. It determines who the assistant is, how it should handle information, and how it should avoid giving unsupported or misleading answers.

In this project, ISA is defined as a domain-aware Intelligent Study Assistant for developers working with complex business systems. Its primary users are junior developers, software engineers, technical support engineers, and other technical team members who need to understand business context while working on payroll, superannuation, HR technology, compliance reporting, or HR/payroll integration products.

The goal of the System Layer is to ensure that ISA does not behave like a generic chatbot. Instead, it should help users bridge the gap between technical implementation and business understanding. ISA should explain business concepts, workflows, terminology, and the reasoning behind system behavior in a way that is clear and useful for developers.

### System Prompt

```text
You are ContextBridge ISA, an Intelligent Study Assistant designed to help developers understand complex business domains.

Your primary users are junior developers, software engineers, and technical team members who need to understand business context while working on complex systems, especially in payroll, superannuation, HR technology, and compliance-related products.

Your goal is to bridge the gap between technical implementation and business understanding. You should help users understand business concepts, workflows, terminology, and the reasoning behind system behavior.

When answering:
- Use clear and structured explanations.
- Adapt the explanation to a junior developer's knowledge level.
- Prefer answers grounded in retrieved documents or provided context.
- Clearly separate confirmed information from assumptions.
- If the provided context is insufficient, say what is missing.
- Avoid hallucinating business rules, compliance requirements, or system behavior.
- For compliance-related topics, remind the user to verify with official documentation or a domain expert.
- Explain how the business concept may affect implementation when relevant.
- Provide follow-up questions that help the user continue learning.

You should not:
- Pretend to know internal business rules that were not provided.
- Give legal, financial, payroll, tax, or compliance advice as final authority.
- Invent document sources or citations.
- Overload beginner users with unnecessary jargon.
```

### Design Rationale

This layer is important because the target domain contains high-context and high-risk business knowledge. Payroll, superannuation, tax reporting, compliance workflows, and enterprise integrations often depend on specific rules, documents, and stakeholder decisions. A general chatbot may provide plausible but incorrect explanations.

By defining a strict System Layer, ISA is guided to:

1. Prioritize clarity for junior developers.
2. Use retrieved or provided context as the basis for answers.
3. Identify missing information instead of guessing.
4. Avoid unsupported compliance or payroll claims.
5. Connect business concepts to practical software development tasks.

This makes ISA more reliable as a learning assistant for complex business systems.

## 2. Retrieved Layer

The Retrieved Layer provides the external knowledge that ISA uses to answer user questions. This layer is especially important for ContextBridge ISA because the main problem is not only language generation, but also access to the right business and technical context.

In complex business systems, important knowledge is often distributed across multiple sources. A developer may need to check product documentation, API specifications, onboarding notes, tickets, business rules, compliance references, and existing implementation details before they can fully understand a feature. The Retrieved Layer is designed to collect and provide the most relevant pieces of this knowledge at answer time.

For the MVP, the Retrieved Layer will focus on a limited but realistic knowledge base related to payroll, superannuation, HR technology, and system integration. The goal is not to build a complete enterprise knowledge system, but to test whether retrieved context can help ISA provide more accurate, grounded, and useful answers.

### MVP Demo Knowledge Base

For this project, I will not use confidential company documents from previous work. Instead, I will create a small synthetic demo knowledge base based on public domain concepts and simplified mock business rules. This approach keeps the project safe while still simulating the type of fragmented business context that developers often need to understand in real projects.

The demo knowledge base will include five document types:

1. Domain Glossary
   A glossary explaining key terms such as payroll, superannuation, Single Touch Payroll, ATO, clearing house, contribution, validation, pay event, and reporting status.

2. Workflow Document
   A simplified payroll reporting workflow, such as employee payroll data collection, validation, submission, response handling, and status update.

3. Mock API Specification
   A mock API document for endpoints such as `POST /payroll/reports`, including request fields, response fields, validation errors, and status codes.

4. Business Rules Document
   A small set of demo rules, such as required fields, validation timing, missing data handling, submission status transitions, and retry behavior.

5. FAQ / Onboarding Notes
   Beginner-friendly notes for junior developers, including questions such as "What is STP?", "Why do we validate payroll data before submission?", and "What should a developer check before changing reporting logic?"

These documents will be intentionally small, controlled, and easy to evaluate. They will be used to test whether ISA can retrieve the right context and explain complex business concepts without relying on private company materials.

### Knowledge Sources

The Retrieved Layer may include the following types of sources:

1. Course materials and bootcamp notes.
2. Business domain documentation.
3. Product requirement documents.
4. API documentation.
5. User stories and development tickets.
6. FAQ and onboarding materials.
7. Glossaries for payroll, superannuation, and HR technology terms.
8. Public online resources for general domain concepts, such as official government pages, industry explainers, and public technical documentation.
9. Selected external references for broader background knowledge.

Public online resources will be used to support general understanding of domain concepts. They should not replace project-specific documentation, internal business rules, or expert verification for compliance-sensitive decisions.

### Retrieved Context Example

```json
{
  "retrieved_context": [
    {
      "source_id": "payroll_stp_overview_001",
      "source_type": "business_document",
      "title": "Single Touch Payroll Overview",
      "content": "Single Touch Payroll is a reporting mechanism where employers report payroll information to the ATO each time they pay employees.",
      "relevance_reason": "The user asked about a payroll reporting feature related to STP."
    },
    {
      "source_id": "integration_api_003",
      "source_type": "api_documentation",
      "title": "Payroll Reporting API",
      "content": "The payroll reporting endpoint submits pay event data and returns validation results for missing or invalid fields.",
      "relevance_reason": "The user is trying to understand how the business process maps to an API call."
    }
  ]
}
```

### Retrieval Rules

ISA should use the Retrieved Layer according to the following rules:

1. Prefer retrieved documents over general model knowledge when answering domain-specific questions.
2. Use the retrieved context to ground explanations and reduce hallucination.
3. Mention when an answer is based on retrieved information.
4. If retrieved context is incomplete or inconsistent, clearly state the limitation.
5. Do not invent citations, document names, or business rules.
6. For compliance-sensitive topics, treat retrieved context as supporting material rather than final legal or financial authority.

### Design Rationale

The Retrieved Layer is necessary because business context is usually not stored in one place. In real development work, a junior developer may understand the code but still miss the business reason behind it. By retrieving relevant documentation and presenting it together with the user's question, ISA can provide answers that are more specific than a generic chatbot.

This layer also supports future RAG implementation. Documents can be chunked, embedded, stored in a vector database, and retrieved based on semantic similarity to the user's question. The retrieved chunks will then be passed into the model as context, allowing ISA to generate grounded answers with source references.

In the final system, the Retrieved Layer should help ISA answer questions such as:

1. What does this payroll term mean?
2. Why does this workflow require validation before submission?
3. Which document explains this business rule?
4. How does this business concept affect the API or implementation?
5. What information is missing before this ticket can be implemented safely?

## 3. Task Layer: Input Schema

The Task Layer defines the specific user request that ISA needs to handle in a single interaction. While the System Layer defines the assistant's global behavior and the Retrieved Layer provides supporting knowledge, the Task Input Schema captures the user's immediate goal, question, role, constraints, and available context.

This layer is important because the same retrieved document may need to be explained differently depending on the user's role and task. For example, a junior developer may need a beginner-friendly explanation of a payroll concept, while a senior engineer may need implementation implications, edge cases, or integration risks.

The Input Schema helps ISA understand:

1. Who is asking the question.
2. What the user is trying to achieve.
3. What level of explanation is appropriate.
4. What context has already been provided.
5. Whether source references, assumptions, or follow-up questions are required.

### Input Schema

```json
{
  "user_profile": {
    "role": "junior developer",
    "domain_knowledge_level": "beginner",
    "technical_knowledge_level": "intermediate",
    "current_context": "working on a payroll reporting feature"
  },
  "task": {
    "task_type": "explain_business_context",
    "user_question": "What does Single Touch Payroll mean in this feature?",
    "user_goal": "understand the business meaning before implementing the ticket",
    "expected_depth": "practical explanation for development work"
  },
  "provided_context": {
    "ticket_summary": "The user is updating a payroll reporting workflow that submits pay event data.",
    "code_or_error": null,
    "user_notes": "The ticket mentions STP validation but does not explain the business rule."
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
```

### Field Definitions

| Field | Purpose |
| --- | --- |
| `user_profile.role` | Identifies the user's role, such as junior developer, software engineer, support engineer, or technical lead. |
| `user_profile.domain_knowledge_level` | Describes how familiar the user is with the business domain. |
| `user_profile.technical_knowledge_level` | Describes the user's software engineering knowledge level. |
| `user_profile.current_context` | Provides the user's current work situation, such as onboarding, reading a ticket, debugging an issue, or implementing a feature. |
| `task.task_type` | Classifies the user request, such as concept explanation, document summary, implementation clarification, or follow-up question generation. |
| `task.user_question` | Stores the user's actual question. |
| `task.user_goal` | Explains what the user wants to achieve after receiving the answer. |
| `task.expected_depth` | Defines how detailed the response should be. |
| `provided_context.ticket_summary` | Captures any ticket or feature summary provided by the user. |
| `provided_context.code_or_error` | Captures relevant code snippets, logs, or errors if the question is technical. |
| `provided_context.user_notes` | Captures extra notes or assumptions provided by the user. |
| `constraints.answer_language` | Defines the expected response language. |
| `constraints.answer_style` | Defines the preferred explanation style. |
| `constraints.include_source_references` | Indicates whether ISA should include source references from retrieved documents. |
| `constraints.include_technical_relevance` | Indicates whether ISA should explain how the business concept affects development work. |
| `constraints.avoid_unsupported_assumptions` | Ensures ISA identifies missing information rather than guessing. |
| `constraints.include_follow_up_questions` | Indicates whether ISA should suggest useful next questions. |

### Supported Task Types

The MVP will support the following task types:

1. `explain_business_context`
   Explain a business concept, workflow, or domain term in a developer-friendly way.

2. `summarize_document`
   Summarize a retrieved document or selected source material.

3. `clarify_requirement`
   Help the user understand a ticket, requirement, or product behavior.

4. `map_business_to_technical`
   Explain how a business rule affects APIs, data models, validation, or system behavior.

5. `identify_missing_context`
   Identify what information is missing before the user can confidently implement a feature.

6. `generate_follow_up_questions`
   Suggest questions the user should ask a BA, PM, senior developer, or domain expert.

### Design Rationale

The Input Schema makes each user interaction more structured and easier to evaluate. Instead of sending only a raw question to the model, ISA receives enough context to adapt its answer to the user's role, knowledge level, task, and constraints.

This is especially useful for complex business domains because a correct answer is not always the same as a useful answer. A junior developer may need a simple explanation first, followed by implementation relevance and suggested follow-up questions. The Input Schema helps ISA generate responses that are grounded, targeted, and practical.

## 4. Task Layer: Output Schema

The Output Schema defines how ISA should structure its response for each user request. This layer makes the assistant's output more consistent, easier to evaluate, and more useful for developers who need to understand complex business context.

In ContextBridge ISA, the response should not be a long unstructured paragraph. It should separate the direct answer, detailed explanation, technical relevance, source references, assumptions, uncertainties, and suggested follow-up questions. This structure helps users understand not only the answer, but also the confidence and evidence behind it.

### Output Schema

```json
{
  "answer": {
    "short_answer": "A concise answer to the user's question.",
    "detailed_explanation": "A clear explanation adapted to the user's role and knowledge level.",
    "technical_relevance": "How this business concept or requirement affects implementation, APIs, validation, data models, or system behavior."
  },
  "evidence": {
    "source_references": [
      {
        "source_id": "payroll_stp_overview_001",
        "source_type": "business_document",
        "title": "Single Touch Payroll Overview",
        "used_for": "Explaining the meaning of STP in payroll reporting."
      }
    ],
    "grounded_claims": [
      "Claims that are directly supported by retrieved context."
    ]
  },
  "reasoning_boundary": {
    "assumptions": [
      "Any assumptions made because the user did not provide complete context."
    ],
    "uncertainties": [
      "Any missing or unclear information that should be verified."
    ],
    "requires_human_verification": true
  },
  "next_steps": {
    "follow_up_questions": [
      "What validation rules apply to this payroll reporting workflow?",
      "Which API endpoint submits the STP pay event data?"
    ],
    "recommended_actions": [
      "Check the linked business rule document before implementing the validation logic."
    ]
  }
}
```

### Field Definitions

| Field | Purpose |
| --- | --- |
| `answer.short_answer` | Provides a direct and concise response to the user's question. |
| `answer.detailed_explanation` | Explains the concept or requirement in a beginner-friendly and structured way. |
| `answer.technical_relevance` | Connects the business context to software implementation concerns. |
| `evidence.source_references` | Lists the retrieved documents or chunks used to support the answer. |
| `evidence.grounded_claims` | Identifies claims that are directly supported by retrieved context. |
| `reasoning_boundary.assumptions` | Makes any necessary assumptions explicit. |
| `reasoning_boundary.uncertainties` | Identifies missing, incomplete, or unclear information. |
| `reasoning_boundary.requires_human_verification` | Indicates whether a BA, PM, senior developer, compliance specialist, or official document should verify the answer. |
| `next_steps.follow_up_questions` | Suggests useful questions the user can ask next. |
| `next_steps.recommended_actions` | Suggests practical next actions for learning, clarification, or implementation. |

### Example Output

```json
{
  "answer": {
    "short_answer": "Single Touch Payroll is a payroll reporting process where employers report payroll information to the ATO when employees are paid.",
    "detailed_explanation": "In this feature, STP likely refers to the process of submitting payroll event data, such as employee pay, tax, and superannuation-related information, as part of a payroll reporting workflow. For a junior developer, the key idea is that STP is not just a UI label or API name. It represents a business and compliance process that may require specific data fields, validation rules, and submission timing.",
    "technical_relevance": "From an implementation perspective, STP may affect which fields are required, how validation errors are handled, when data is submitted, and how the system records reporting status."
  },
  "evidence": {
    "source_references": [
      {
        "source_id": "payroll_stp_overview_001",
        "source_type": "business_document",
        "title": "Single Touch Payroll Overview",
        "used_for": "Explaining the general meaning of STP in payroll reporting."
      }
    ],
    "grounded_claims": [
      "STP is related to payroll reporting.",
      "STP may require validation before submission."
    ]
  },
  "reasoning_boundary": {
    "assumptions": [
      "The feature is related to payroll reporting based on the user's ticket summary."
    ],
    "uncertainties": [
      "The exact validation rules are not available in the provided context.",
      "The specific API endpoint is not confirmed."
    ],
    "requires_human_verification": true
  },
  "next_steps": {
    "follow_up_questions": [
      "Which fields are required for this STP submission?",
      "Where is the validation rule documented?",
      "What should happen when the external reporting service rejects the submission?"
    ],
    "recommended_actions": [
      "Review the business rule document before implementing validation logic.",
      "Confirm edge cases with a BA or senior developer."
    ]
  }
}
```

### Output Rules

ISA should follow these output rules:

1. Start with a short answer before giving details.
2. Explain business concepts in a way that is understandable for the user's knowledge level.
3. Include technical relevance when the task is related to development work.
4. Include source references when retrieved context is available.
5. Clearly separate supported claims from assumptions.
6. State uncertainty instead of filling gaps with unsupported information.
7. Recommend human verification for compliance-sensitive or business-critical topics.
8. Provide follow-up questions that help the user clarify requirements or continue learning.

### Design Rationale

The Output Schema is designed to make ISA's responses reliable and actionable. In complex domains such as payroll and superannuation, users need more than a fluent explanation. They need to know what is supported by retrieved documents, what is assumed, what remains uncertain, and what they should check next.

This structure also supports evaluation. The response can be assessed across multiple dimensions, including answer accuracy, relevance, groundedness, source quality, uncertainty handling, and practical usefulness for developers.

By enforcing a structured output, ISA becomes easier to test, compare, and improve across the different phases of the project, including prompt-based Q&A, RAG, tool-using agents, fine-tuning, and evaluation.
