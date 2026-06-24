# 存储架构决策：为什么不用 LLM Wiki

> 本文档说明为什么本项目不采用 LLM Wiki，以及推荐的简化存储方案。

---

## 决策结论

**不建议使用专门的 LLM Wiki**。对本项目来说过度设计。

---

## 为什么不需要 LLM Wiki

### 1. 规模不匹配

- **本项目规模**：核心库 48k 字，约 300-400 个 vectors
- **LLM Wiki 适用场景**：企业级知识库（数十万到数百万词条）
- **结论**：简单的 Vector DB（Pinecone/Chroma/Weaviate）+ Markdown 文件足够

### 2. 结构已经足够清晰

- 内容已有明确分类：技术标准、政策法规、产品核心
- 不需要复杂的 wiki 页面关系和跨引用
- Markdown + 前置元数据（source、date、category）即可满足需求

### 3. 维护成本过高

- LLM Wiki 需要专门维护页面结构、链接关系
- 本项目内容更新频率低：
  - 技术标准：季度检查
  - 产品文档：月度检查
- 简单的文件替换比维护 wiki 条目更高效

### 4. 查询模式简单

- **主要查询**：语义检索（"什么是 USI"、"如何发送 contribution 消息"）
- **不需要**：复杂的知识图谱查询（"A 与 B 的关系"、"所有依赖 C 的概念"）
- **结论**：Vector similarity search 足够

---

## 推荐方案：简化文件架构

### 目录结构

```
vector_db/
├── core/
│   ├── tech/
│   │   ├── superstream_schedule2_terms.md
│   │   ├── superstream_schedule4a_fields.md
│   │   └── superstream_schedule6_errors.md
│   ├── policy/
│   │   ├── payday_super_core.md
│   │   └── timeline_2026.md
│   └── product/
│       ├── wrkr_features.md
│       └── wrkr_blogs_migration.md
├── snapshots/          # 历史快照
└── index.json         # 元数据索引
```

### 文件头部元数据

每个 Markdown 文件包含结构化元数据：

```markdown
---
source: https://softwaredevelopers.ato.gov.au/...
snapshot_date: 2026-06-24
category: tech-standard
version: 2.0
keywords: [USI, TFN, SuperStream, contribution]
---
```

### 核心优势

1. **简单易维护**：直接编辑 Markdown 文件
2. **版本控制友好**：Git 可以轻松追踪变更
3. **可读性强**：开发者可以直接查看源文件
4. **成本低**：无需额外工具或服务
5. **灵活扩展**：需要时可以轻松添加新分类

---

## 什么时候才需要 LLM Wiki

只有在以下情况才考虑升级到 LLM Wiki：

### 规模触发条件

- ✅ 内容规模 > 100 万字
- ✅ 需要复杂的概念关系图谱
- ✅ 多人协作编辑知识条目
- ✅ 需要动态生成衍生内容
- ✅ 知识库需要支持复杂的跨引用查询

### 当前状态

- ❌ 核心库仅 48k 字
- ❌ 单人维护为主
- ❌ 查询以语义检索为主
- ❌ 内容更新频率低

**结论**：本项目离 LLM Wiki 的应用场景还很远。

---

## 技术栈对比

| 特性 | 简化方案（推荐） | LLM Wiki |
|------|----------------|----------|
| 初始成本 | 低（几乎为零） | 高（需要搭建维护） |
| 维护复杂度 | 低 | 高 |
| 查询延迟 | < 500ms | 1-3s |
| 适用规模 | < 10 万字 | > 50 万字 |
| 学习曲线 | 平缓 | 陡峭 |
| 扩展性 | 中等 | 高 |

---

## 实施建议

### Phase 1：使用简化方案（当前）

1. 按 `vector-db-strategy.md` 中的三层架构实施
2. 使用 Pinecone 免费层 + Markdown 文件
3. 核心库控制在 48k 字以内

### Phase 2：监控与评估（3-6 个月后）

监控以下指标决定是否需要升级：

| 指标 | 当前目标 | 升级阈值 |
|------|---------|---------|
| 内容总量 | 48k 字 | > 20 万字 |
| 查询类型 | 语义检索 | 需要知识图谱 |
| 更新频率 | 月度 | 每周多次 |
| 协作人数 | 1-2 人 | > 5 人 |

### Phase 3：渐进升级路径（如需要）

如果指标触发升级阈值：

1. 先尝试 Notion + Vector DB 混合方案
2. 评估开源 LLM Wiki 方案（如 Obsidian Publish + 插件）
3. 最后考虑自建专门的 LLM Wiki 系统

---

## 参考文档

- [vector-db-strategy.md](./vector-db-strategy.md) - 完整的 Vector DB 三层架构设计
- [knowledge-base-references.md](./knowledge-base-references.md) - 数据来源清单

---

**最后更新**: 2026-06-24
**决策状态**: ✅ 已确认采用简化方案