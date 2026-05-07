# System Prompt Analysis

## Summary

The current system prompt is a solid v1 foundation. It clearly defines ISA's identity, target users, main responsibility, response style, and several important safety boundaries.

Using the basic four-part framework from the learning materials, it already covers:

- Role definition
- Responsibility scope
- Behavioral expectations
- Limitations

However, compared with the stronger "Agent behavior contract" standard described in the learning materials, the current prompt is still closer to a role description than a complete operational system prompt.

It should be improved so that ISA can behave more consistently in a real Context Engineering or RAG-based system.

## Main Gaps

### 1. Capability Boundaries Are Not Explicit Enough

The prompt says ISA should help users understand business concepts, workflows, terminology, and system behavior, but it does not clearly define the specific task types ISA supports.

Recommended supported task types include:

- Explain business concepts
- Summarize retrieved documents
- Clarify requirements
- Map business rules to technical implementation
- Identify missing context
- Generate follow-up questions

Without this boundary, the model may interpret its scope too broadly.

### 2. Output Format Is Not Stable Enough

The prompt says ISA should use clear and structured explanations, but it does not define a stable response format.

This may cause inconsistent answers across interactions, making the system harder to evaluate, display in a UI, or connect with downstream workflows.

A stronger version should define a standard structure, such as:

- Short answer
- Detailed explanation
- Technical relevance
- Evidence or source references
- Assumptions and uncertainties
- Follow-up questions

### 3. Retrieved Context Rules Are Not Operational Enough

The current prompt says ISA should prefer answers grounded in retrieved documents or provided context. This is useful, but not specific enough for a RAG system.

It should define:

- How to reference retrieved sources
- What to do when retrieved context is incomplete
- What to do when retrieved sources conflict
- When general knowledge can be used
- Which claims must be marked as assumptions
- Whether to include source IDs, titles, or document types

This is important for groundedness and hallucination control.

### 4. Workflow Is Missing

The prompt contains answer principles but does not define a task workflow.

A stronger ISA workflow could be:

1. Identify the user's intent.
2. Check provided and retrieved context.
3. Separate confirmed facts from assumptions.
4. Explain the business meaning.
5. Connect the concept to implementation impact.
6. State missing or uncertain context.
7. Suggest useful follow-up questions.

This would make ISA's behavior more predictable.

### 5. High-Risk Domain Rules Need More Specific Boundaries

The current prompt correctly says ISA should not give legal, financial, payroll, tax, or compliance advice as final authority.

However, the high-risk boundaries should be more concrete.

Allowed behavior could include:

- Explain general business concepts
- Summarize provided or retrieved documents
- Identify possible implementation implications
- Suggest what should be verified with official sources or domain experts

Not allowed behavior should include:

- Making final legal or compliance decisions
- Calculating official payroll, tax, or superannuation obligations
- Inventing ATO, payroll, or superannuation rules
- Presenting mock or demo rules as real company policy

### 6. Failure Paths Are Not Fully Defined

The current prompt says ISA should say what is missing when context is insufficient, but it does not define how ISA should recover from different failure cases.

It should specify behavior for cases such as:

- No retrieved context is available
- Retrieved documents are inconsistent
- The user asks for an unsupported compliance decision
- The user's question is outside ISA's intended scope
- The model cannot determine whether a claim is supported

For each case, ISA should explain the limitation and give the user a useful next step.

### 7. Tool Rules Are Missing

If ISA will later use retrieval, search, document reading, or code inspection tools, the system prompt should define tool-use rules.

Useful rules include:

- When to retrieve documents
- When not to answer from memory
- How to handle empty retrieval results
- How to cite tool results
- How to handle tool errors
- Never invent information that tools did not return

Even if tools are not implemented yet, the prompt can reserve a section for future tool behavior.

### 8. Examples And Counterexamples Are Missing

The learning materials emphasize that examples help stabilize behavior. The current prompt does not include examples, so the model has less guidance on what a good ISA answer should look like.

Useful examples could cover:

- A user asking what Single Touch Payroll means
- A user asking how a business rule affects validation logic
- A user asking for a final compliance decision that ISA should not provide

Short examples and counterexamples would reduce ambiguity.

### 9. Dynamic Context Injection Is Not Defined

The current system prompt is fully static. It does not specify which runtime values should be injected by the system.

Useful dynamic context may include:

- User role
- Domain knowledge level
- Technical knowledge level
- Current task type
- Current date
- Retrieved documents
- Available tools
- Source trust level

This matters because ContextBridge is intended to become a context system, not just a single static prompt.

### 10. Versioning And Evaluation Are Not Explicit

Saving this prompt under `v1` is a good first step, but the prompt itself does not include version metadata, intended use cases, known limitations, or evaluation criteria.

Future versions should record:

- Version number
- Purpose
- Applicable scenarios
- Known limitations
- Evaluation examples
- Main changes from the previous version

This will make prompt iteration easier to manage.

## Overall Assessment

The current prompt is suitable as a v1 persona and safety baseline. It solves the basic question of who ISA is, who it serves, and what it should avoid.

It is not yet a complete production-style Agent system prompt. The next version should focus on:

- Clear capability boundaries
- Stable output format
- RAG and retrieved-context rules
- Explicit workflow
- Allowed and Not Allowed safety boundaries
- Failure handling
- Tool-use rules
- A small number of examples
- Runtime context injection
- Versioning and evaluation support

## Recommended Next Step

Create a `v2` system prompt that keeps the current identity and safety intent, but reorganizes it into modular sections:

- Identity
- Capabilities
- Limitations
- Runtime Context
- Workflow
- Retrieved Context Rules
- Safety Rules
- Output Format
- Examples
- Version Notes
