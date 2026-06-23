# ContextBridge ISA Technical Selection Analysis

## 1. Project Context

ContextBridge ISA is an Intelligent Study Assistant for developers working with complex business domains such as payroll, superannuation, HR technology, compliance reporting, and system integration.

The core problem is not only answering questions. The project needs to help junior developers understand fragmented business context from trusted documents, explain how domain knowledge affects implementation, and avoid unsupported claims in compliance-sensitive areas.

Based on the proposal and the current context architecture, the most important product requirements are:

1. Answer questions using trusted documents.
2. Provide source references where possible.
3. Explain business concepts in developer-friendly language.
4. Connect business rules to APIs, validation, data models, and workflows.
5. State assumptions and missing information clearly.
6. Support evaluation of accuracy, relevance, groundedness, retrieval quality, and clarity.

This means the technical selection should prioritize groundedness, traceability, and evaluation over model customization or autonomous behavior.

## 2. Candidate AI Application Patterns

The four candidate patterns are:

1. Prompting: direct prompt engineering.
2. RAG: retrieval-augmented generation.
3. Fine-tuning: model adaptation using a domain-specific dataset.
4. Agents: tool-using or autonomous decision-making systems.

For this project, these patterns should not be treated as equal alternatives. They serve different roles in the architecture.

## 3. Recommended Selection

The recommended architecture is:

```text
Prompting + RAG as the MVP core
Limited Agent capability as an optional enhancement
Fine-tuning as a later experiment, not the main MVP dependency
```

In short:

1. Use Prompting to define ISA's role, answer format, safety boundaries, and uncertainty handling.
2. Use RAG as the main knowledge-grounding mechanism.
3. Use Agents only for controlled tool workflows such as source lookup, note organization, or follow-up question generation.
4. Use Fine-tuning only as an experiment for response style or task consistency after enough evaluation data exists.

## 4. Pattern-by-Pattern Analysis

### 4.1 Prompting

Prompting is necessary, but it is not enough as the main solution.

It is useful for:

1. Defining ISA as a developer-focused study assistant.
2. Enforcing structured output.
3. Asking the model to separate confirmed information, assumptions, and uncertainties.
4. Improving answer clarity for junior developers.
5. Setting safety rules for payroll, tax, and compliance-sensitive topics.

For this project, Prompting maps directly to the System Layer and Task Layer in the four-layer context architecture.

However, Prompting alone cannot solve the main project problem because the business knowledge is fragmented across documents, APIs, tickets, onboarding notes, and domain references. A prompt-only assistant may produce clear but generic answers, and it may hallucinate project-specific rules.

Verdict:

Prompting should be used as the foundation, but not as the main technical differentiator.

### 4.2 RAG

RAG should be the core technical choice for ContextBridge ISA.

It is useful for:

1. Retrieving relevant document chunks from a controlled knowledge base.
2. Grounding answers in trusted sources.
3. Providing source references.
4. Reducing hallucination in complex business domains.
5. Supporting evaluation of retrieval quality and answer groundedness.
6. Simulating how developers use product docs, API docs, business rules, and onboarding notes in real work.

RAG maps directly to the Retrieved Layer in the current context architecture. It also supports the MVP requirement for source-grounded document Q&A.

This project is a strong RAG fit because users are not mainly asking for creative generation. They need reliable explanations based on known material. The assistant should be able to say, "This is supported by these documents" or "This information is missing."

The recommended MVP RAG scope is:

1. Prepare a small safe demo knowledge base.
2. Split documents into chunks.
3. Create embeddings.
4. Store chunks in a vector store.
5. Retrieve top-k relevant chunks for each question.
6. Generate answers using the retrieved context and structured output schema.
7. Show source references and uncertainty boundaries.
8. Evaluate retrieval and answer quality using test questions.

Verdict:

RAG should be the primary architecture for the MVP.

### 4.3 Fine-tuning

Fine-tuning should not be the main MVP architecture.

It may be useful for:

1. Making answers consistently follow the desired structure.
2. Adapting tone to junior developers.
3. Improving classification of task types.
4. Producing consistent follow-up questions or explanation style.

However, it has important limitations for this project:

1. Fine-tuning does not automatically give the model access to current project documents.
2. It is weaker than RAG for source-grounded answers.
3. It requires a good training dataset, which the project likely does not have at the beginning.
4. It can increase project complexity within a 12-week scope.
5. It does not solve citation quality or retrieval quality.

For a compliance-sensitive domain, fine-tuning is risky if used as a substitute for retrieved evidence. The model may learn the style of business explanations without being able to verify whether a claim is supported by the current source material.

The best role for fine-tuning is a later experiment after the RAG baseline is working. A small dataset can be used to compare whether fine-tuning improves answer format, clarity, or task consistency.

Verdict:

Fine-tuning should be positioned as an experiment or stretch goal, not a core dependency.

### 4.4 Agents

Agents can be useful, but the project should avoid making autonomous agents the center of the MVP.

They are useful for controlled workflows such as:

1. Searching selected external public resources.
2. Looking up terminology.
3. Generating follow-up questions.
4. Organizing study notes.
5. Suggesting missing context checks before implementation.
6. Running evaluation workflows.

However, fully autonomous agents introduce risks:

1. More moving parts than necessary for the MVP.
2. Harder evaluation and debugging.
3. Higher chance of irrelevant tool use.
4. More difficult source-control and citation behavior.
5. Extra complexity when the main project value is document-grounded explanation.

For ContextBridge ISA, the agent should be tool-using but constrained. It should not freely decide business rules. It should use tools only when the task requires external lookup, note generation, or evaluation support.

Verdict:

Use Agents as a limited enhancement after the RAG Q&A flow is stable.

## 5. Decision Matrix

| Pattern | Fit for Project | Strength | Main Risk | Recommended Role |
| --- | --- | --- | --- | --- |
| Prompting | High | Defines assistant role, structure, and safety behavior | Not enough project-specific knowledge | Foundation |
| RAG | Very high | Grounds answers in trusted documents with references | Requires document preparation and retrieval evaluation | MVP core |
| Fine-tuning | Medium to low for MVP | Improves style and consistency | Does not solve source grounding; needs dataset | Later experiment |
| Agents | Medium | Adds tool workflows and task automation | Can overcomplicate MVP and reduce controllability | Limited enhancement |

## 6. Recommended MVP Architecture

The MVP should follow this flow:

```text
User question
  -> Task input construction
  -> Document retrieval
  -> Prompt assembly with retrieved context
  -> LLM answer generation
  -> Structured answer with sources, assumptions, uncertainties, and next steps
  -> Evaluation logging
```

The MVP should include:

1. A system prompt based on the System Layer.
2. A small synthetic payroll and superannuation knowledge base.
3. A document ingestion and chunking pipeline.
4. An embedding model and vector store.
5. Retrieval with top-k chunks.
6. A structured response schema.
7. Source references in answers.
8. A test question set and scoring rubric.

The MVP should avoid:

1. Treating fine-tuning as required for success.
2. Building a fully autonomous agent before the RAG pipeline works.
3. Using public resources as final compliance authority.
4. Using confidential company documents or real employee data.
5. Measuring success only by fluency instead of groundedness and usefulness.

## 7. Suggested 12-Week Implementation Plan

### Phase 1: Prompting Baseline

Build a basic chat assistant with:

1. System prompt.
2. Task input schema.
3. Structured output schema.
4. A small manually provided context example.

Goal:

Create a baseline that can explain domain concepts clearly, even before retrieval is implemented.

### Phase 2: RAG MVP

Build the document Q&A flow:

1. Prepare demo documents.
2. Chunk documents.
3. Generate embeddings.
4. Store chunks in a vector store.
5. Retrieve relevant chunks for user questions.
6. Generate grounded answers with source references.

Goal:

Validate that retrieved context improves accuracy, groundedness, and technical usefulness.

### Phase 3: Evaluation Pipeline

Build a small evaluation set:

1. STP concept explanation.
2. SuperStream workflow explanation.
3. Payslip data model question.
4. Missing context detection.
5. Payroll validation requirement clarification.

Score answers using:

1. Accuracy.
2. Relevance.
3. Groundedness.
4. Retrieval quality.
5. Technical usefulness.
6. Uncertainty handling.
7. Clarity.

Goal:

Show measurable improvement from baseline prompting to RAG-based ContextBridge ISA.

### Phase 4: Limited Agent Enhancement

Add controlled tool use only after RAG is stable.

Possible tools:

1. External public source lookup.
2. Glossary lookup.
3. Follow-up question generator.
4. Study note organizer.
5. Evaluation runner.

Goal:

Improve workflow usefulness without making autonomous behavior the main project risk.

### Phase 5: Fine-tuning Experiment

Run a small optional experiment if time allows.

Possible experiment:

1. Create a small dataset of question, retrieved context, and ideal structured answer.
2. Fine-tune or use a lightweight adaptation method.
3. Compare against the RAG baseline.
4. Measure whether it improves structure, clarity, or consistency.

Goal:

Treat fine-tuning as a research comparison, not a required production choice.

## 8. Final Recommendation

For ContextBridge ISA, the best technical selection is:

```text
Core: Prompting + RAG
Enhancement: constrained tool-using Agent
Experiment: Fine-tuning
```

This selection matches the real project goal: helping developers understand complex business context through trusted documents, retrieved evidence, structured explanations, and clear uncertainty handling.

RAG should be presented as the main technical architecture because it directly addresses the project's biggest problem: fragmented and high-risk business knowledge. Prompting supports behavior and format. Agents can improve workflows later. Fine-tuning is useful for experimentation, but it should not replace retrieval or source grounding.
