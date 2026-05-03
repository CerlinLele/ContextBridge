# ContextBridge ISA Proposal

## Project Name

ContextBridge ISA

## Specific Problem

Developers often struggle to quickly understand business context when working on complex business systems. This leads to high communication cost, slower requirement understanding, implementation uncertainty, and potential rework.

## Industry

Payroll / Superannuation / HR Technology / FinTech

## Problem Description

This project is motivated by my previous experience working on a WRKR Pay-related software project. During development, I found that the business context was highly complex. The system was not only about implementing software features, but also involved payroll, superannuation, Single Touch Payroll, compliance validation, and HR/payroll system integrations.

Important knowledge was distributed across product documentation, existing code, business rules, compliance requirements, and conversations with colleagues. As a developer, I often needed to spend a large amount of time understanding the business logic behind a feature, confirming requirement details, and checking whether the implementation matched the real business workflow.

This created high communication cost and made development less efficient. Incomplete business understanding could also lead to incorrect assumptions and rework.

Therefore, I want to use the ISA project to explore how to build an Intelligent Study Assistant that helps users understand complex knowledge through trusted documents, retrieved context, and structured explanations.

## User Persona

### Who Are the Main Users?

The main users are junior developers, software engineers, technical support engineers, and technical team members who need to quickly understand business logic in complex software projects.

These users usually have software development skills, but they may not be familiar with specific industry knowledge such as payroll, superannuation, compliance reporting, or HR/payroll integration. They need to understand product logic within a short period of time and translate business rules into correct technical implementation.

### What Are Their Main Pain Points?

Their main pain points are high domain knowledge barriers, fragmented information, and difficulty building context quickly.

In real development work, developers often need to read product documents, existing code, tickets, historical discussions, and then repeatedly ask senior developers, business analysts, or product managers for clarification. Many business rules are not stored in a single document. Instead, they are spread across system behavior, historical decisions, and compliance requirements.

This creates several problems:

1. Requirement understanding takes too much time.
2. Communication cost is high.
3. New team members find it difficult to work independently.
4. Incomplete business understanding may cause rework.
5. Senior team members are frequently interrupted by repeated explanation requests.

## Existing Solutions

### What Solutions Currently Exist?

Current solutions include:

1. Reading internal documentation, Confluence pages, Wikis, or product notes.
2. Reviewing existing code, API documentation, and historical tickets.
3. Asking senior developers, business analysts, product managers, or domain experts.
4. Attending onboarding sessions or team knowledge-sharing meetings.
5. Using general search engines or generic AI chatbots to understand concepts.

### What Are the Limitations of These Solutions?

These solutions lack a unified, context-aware, and traceable knowledge entry point.

Internal documentation is often incomplete or outdated, making it difficult for developers to know which information is still accurate. Code shows how the system is implemented, but it does not always explain why the system was designed that way. Asking colleagues is effective, but it depends on other people's availability and increases the communication burden on the team.

Onboarding sessions and knowledge-sharing meetings are often one-time activities and cannot cover every specific question that appears during development.

Generic AI chatbots can explain general concepts, but they do not understand project-specific documentation, business rules, or internal context. As a result, their answers may be too general or inaccurate. For domains such as payroll and superannuation, where compliance requirements are important, the lack of reliable sources and verifiable evidence is a major limitation.

## MVP Scope

### What Is the Minimum Viable Product?

The MVP is an Intelligent Study Assistant designed to help users learn complex business knowledge. Users can use a predefined set of course or business documents and ask questions through a chat interface. The system will retrieve relevant document context and generate answers based on that context, with source references where possible.

The MVP will not attempt to cover a full enterprise knowledge base. Instead, it will focus on a limited but realistic domain, such as payroll, superannuation, and HR system integration, to test whether an AI assistant can reduce the cost of understanding business context for developers.

### What Core Features Should Be Built Within 12 Weeks?

Within 12 weeks, I plan to implement the following core features:

1. Prompt-based Q&A
   Build a basic chat assistant and use a system prompt to define ISA's role, response style, and usage scenario.

2. RAG-based document Q&A
   Support importing course or business documents, splitting them into chunks, creating embeddings, storing them in a vector store, and retrieving relevant context when users ask questions.

3. Source-grounded answers
   Include relevant document snippets or source references in the answer so users can judge whether the response is reliable.

4. Tool-using Agent
   Add tool-calling capability, such as searching external resources, looking up terminology, organizing study notes, or generating follow-up questions.

5. Domain adaptation / Fine-tuning experiment
   Use a small domain-specific dataset to experiment with fine-tuning or QLoRA so the model can better adapt to the target domain and answer style.

6. Evaluation pipeline
   Build a basic evaluation process using a set of test questions to measure answer accuracy, relevance, groundedness, retrieval quality, and user experience.

## Evaluation Metrics

### How Will Project Success Be Judged?

The project will be considered successful if ISA helps users understand complex course or business knowledge faster and more accurately, while reducing dependence on repeated human clarification.

A successful ISA should answer questions based on trusted documents, explain complex business concepts clearly, provide structured responses, and state limitations when information is missing. It should avoid fabricating business rules or compliance-related information.

For developer users, ISA should help them understand the business logic and terminology behind a feature more efficiently.

### What Metrics Will Be Used?

The project can be evaluated using the following metrics:

1. Answer accuracy
   Use human review or reference answers to evaluate whether ISA's responses are correct.

2. Relevance
   Check whether the response directly addresses the user's question instead of giving a generic explanation.

3. Groundedness / Citation quality
   Evaluate whether the answer is based on retrieved documents, whether it provides relevant sources, and whether hallucination is present.

4. Retrieval quality
   Evaluate whether the RAG retrieval stage finds the correct document chunks, using top-k accuracy or manual relevance judgment.

5. Response clarity
   Evaluate whether the answer is clear, structured, and suitable for a junior developer.

6. Time saved
   Compare how long users take to understand a business problem with and without ISA.

7. User satisfaction
   Collect simple feedback scores on whether the answer is helpful, trustworthy, and useful enough for continued use.
