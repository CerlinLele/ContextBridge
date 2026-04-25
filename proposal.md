# ISA Proposal

# 具体问题

在复杂业务系统开发中，开发者很难快速理解业务上下文，导致需求理解、功能实现和跨团队沟通成本较高。

# 行业：

Payroll / Superannuation / HR Technology / FinTech

# 问题描述：

在我之前参与 WRKR Pay 相关项目开发时，我发现业务背景非常复杂。系统不仅涉及普通的软件功能开发，还包含 payroll、superannuation、Single Touch Payroll、合规校验、HR/payroll 系统集成等多个业务领域。很多关键知识分散在产品文档、已有代码、业务规则、合规要求以及和同事的沟通中。

作为开发者，我经常需要花大量时间理解某个功能背后的业务逻辑，确认需求含义，以及判断代码实现是否符合真实业务流程。这导致沟通成本很高，也容易因为业务理解不完整而产生返工。

因此，我希望通过 ISA 项目探索如何构建一个智能学习助手，帮助用户基于可信文档和上下文快速理解复杂知识，降低学习和沟通成本。

# 用户画像

# 谁是主要用户？

主要用户是刚加入复杂业务系统项目的 junior developer、software engineer、technical support engineer，或者需要快速理解业务逻辑的技术团队成员。

他们通常具备一定的编程能力，但对具体行业知识不熟悉，例如 payroll、superannuation、compliance reporting、HR/payroll integration 等业务背景。他们需要在较短时间内理解产品逻辑，并把业务规则正确转化为代码实现。

# 他们的主要痛点是什么？

他们的主要痛点是业务知识门槛高、信息分散、上下文难以快速建立。

在实际开发中，开发者往往需要同时阅读产品文档、代码、ticket、历史讨论记录，并向 senior developer、BA 或 product manager 反复确认需求。很多业务规则不是单独存在于一个文档中，而是分散在系统行为、历史决策和合规要求里。

这会导致几个问题：理解需求耗时长，沟通成本高；新人难以独立完成开发任务；业务理解不完整时容易造成返工；团队中的 senior 成员也会被大量重复性解释打断。

# 现有方案

# 目前有哪些解决方案？

目前常见的解决方案包括：

1. 阅读内部文档、Confluence、Wiki 或产品说明。
2. 查看已有代码、API 文档和历史 ticket。
3. 向 senior developer、business analyst、product manager 或 domain expert 提问。
4. 参加 onboarding session 或 team knowledge sharing。
5. 使用普通搜索工具或通用 AI chatbot 辅助理解概念。

# 这些方案有什么不足？

这些方案的问题是缺少统一、上下文相关、可追溯的知识入口。

内部文档通常不完整或更新不及时，开发者很难判断哪些内容仍然准确。代码能展示系统如何实现，但不一定解释为什么这样设计。向同事提问虽然有效，但依赖他人的时间，也会增加团队沟通负担。Onboarding 和 knowledge sharing 通常是一次性的，无法覆盖开发过程中不断出现的具体问题。

普通 AI chatbot 可以解释通用概念，但不了解公司内部文档、项目上下文和具体业务规则，因此回答可能过于泛化，甚至不准确。对于 payroll 和 superannuation 这类高合规要求的业务场景，缺乏可靠来源和可验证依据是一个明显不足。

# MVP 范围

## 这个项目的最小可行产品（MVP）是什么？

这个项目的 MVP 是一个面向复杂业务知识学习的 Intelligent Study Assistant。用户可以上传或使用预设的课程/业务文档，然后通过聊天界面提出问题。系统会基于文档内容进行检索和回答，并尽量给出相关来源，帮助用户快速理解复杂概念、业务流程和开发任务背景。

MVP 不追求覆盖完整企业知识库，而是聚焦一个有限但真实的知识场景，例如 payroll / superannuation / HR system integration 相关资料，验证 AI assistant 是否能降低开发者理解业务上下文的成本。

## 12 周内你希望实现哪些核心功能？

12 周内希望实现以下核心功能：

1. Prompt-based Q&A
   构建基础聊天助手，通过 system prompt 限定 ISA 的角色、回答风格和使用场景。

2. RAG-based document Q&A
   支持导入课程文档或业务资料，将文档切分、embedding，并存入 vector store。用户提问时，系统可以检索相关内容并生成基于资料的回答。

3. Source-grounded answers
   回答中尽量引用相关文档片段或来源，帮助用户判断答案是否可靠。

4. Tool-using Agent
   加入工具调用能力，例如搜索外部资料、查询术语解释、整理学习笔记或生成 follow-up questions。

5. Domain adaptation / Fine-tuning experiment
   使用小规模领域数据进行 fine-tuning 或 QLoRA 实验，让模型更适应特定业务领域的问答风格。

6. Evaluation pipeline
   建立基础评估流程，用一组测试问题评估回答准确性、相关性、groundedness 和用户体验。

# 评估指标

## 如何判断这个项目是否成功？

如果 ISA 能够帮助用户更快、更准确地理解复杂课程或业务知识，并减少对人工沟通的依赖，就可以认为项目是成功的。

具体来说，成功的 ISA 应该能够基于可信文档回答问题，解释复杂业务概念，给出清晰、结构化的答案，并在不确定时说明限制，而不是编造内容。对于开发者用户，它应该能帮助他们更快理解某个功能背后的业务逻辑和相关术语。

## 你会用哪些指标来评估效果？

可以使用以下指标评估效果：

1. Answer accuracy
   使用人工标注或标准答案，评估 ISA 回答是否正确。

2. Relevance
   判断回答是否真正解决用户问题，而不是给出泛泛解释。

3. Groundedness / Citation quality
   检查回答是否基于检索到的文档内容，是否能提供相关来源，是否存在 hallucination。

4. Retrieval quality
   评估 RAG 检索阶段是否能找到正确文档片段，例如使用 top-k accuracy 或人工判断相关性。

5. Response clarity
   评估回答是否清晰、结构化，是否适合 junior developer 理解。

6. Time saved
   比较用户使用 ISA 前后理解某个业务问题所需时间，观察是否能减少查文档和反复询问同事的时间。

7. User satisfaction
   通过简单问卷或评分收集用户反馈，例如答案是否有帮助、是否可信、是否愿意继续使用。
