# Knowledge Base 目录结构

> 本目录存储从原始 PDF 文档提取并处理后的知识库内容，供 Vector DB 使用。

---

## 目录说明

```
knowledge_base/
├── raw/                    # 原始 PDF 文件
│   ├── tech/              # 技术标准文档
│   ├── policy/            # 政策法规文档（后续）
│   └── product/           # 产品文档（后续）
│
├── extracted/              # 提取后的 Markdown
│   ├── tech/              # 技术标准 Markdown
│   ├── policy/            # 政策法规 Markdown（后续）
│   └── product/           # 产品文档 Markdown（后续）
│
├── snapshots/              # 历史版本快照
│   └── 2026-06/           # 按月份组织
│
└── metadata/
    └── index.json         # 文件元数据索引
```

---

## 当前状态

### Phase 1：技术标准（P0）

**原始 PDF（`raw/tech/`）：**
- `Schedule_2_Terms_and_Definitions_v2.1.pdf`
- `Schedule_4a_ContributionsMIG_v2.0.pdf`
- `Schedule_6_Error_Code_Management_v2.0.pdf`

**提取后 Markdown（`extracted/tech/`）：**
- `superstream_schedule2_terms.md` - 术语表（预计 5k 字）
- `superstream_schedule4a_fields.md` - 字段定义 + 验证规则（预计 12k 字）
- `superstream_schedule6_errors.md` - 错误码表（预计 5k 字）

---

## Markdown 文件格式

每个提取后的 Markdown 文件应包含以下头部元数据：

```markdown
---
source: https://softwaredevelopers.ato.gov.au/sites/default/files/...
source_file: Schedule_2_Terms_and_Definitions_v2.1.pdf
snapshot_date: 2026-06-24
category: tech-standard
version: 2.1
doc_type: superstream-schedule
keywords: [USI, TFN, SuperStream, terminology]
extraction_method: manual | automated
extracted_sections: [terms, abbreviations, data-types]
---

# [文档标题]

## 提取说明
- 提取范围：[说明提取了哪些章节]
- 忽略内容：[说明忽略了哪些内容]

[正文内容...]
```

---

## 提取原则

### ✅ 提取内容

1. **核心定义**：所有术语、缩写、数据类型
2. **字段规范**：名称、类型、长度、必填性、验证规则
3. **错误码表**：代码、类别、说明、建议操作
4. **示例代码**：request/response 示例、XML Schema 片段
5. **合规要求**："MUST"/"SHOULD" 类型的规则

### ⛔ 忽略内容

1. 目录、版本历史、致谢
2. 文档编制过程说明
3. 通用免责声明
4. 重复的法律声明

---

## 快照策略

历史快照按月份组织在 `snapshots/YYYY-MM/` 下：

- 用于记录关键文档的时间点版本
- 文件名格式：`{doc_name}_v{version}_snapshot.md`
- 保留原始提取时的元数据

---

## 元数据索引

`metadata/index.json` 记录所有文档的元信息：

```json
{
  "files": [
    {
      "id": "schedule2_v2.1",
      "source_file": "Schedule_2_Terms_and_Definitions_v2.1.pdf",
      "extracted_file": "extracted/tech/superstream_schedule2_terms.md",
      "snapshot_file": "snapshots/2026-06/schedule2_v2.1_snapshot.md",
      "extraction_date": "2026-06-24",
      "word_count": 5200,
      "status": "extracted | pending | processing",
      "version": "2.1",
      "category": "tech-standard"
    }
  ]
}
```

---

## 后续扩展

### Phase 2：政策法规（P1）
- `raw/policy/` - 政策 PDF
- `extracted/policy/` - 提取后的政策文档

### Phase 3：产品文档（P1）
- `raw/product/` - Wrkr 博客、产品说明
- `extracted/product/` - 提取后的产品文档

---

## 参考文档

- [Vector DB 策略](../docs/0.%20References/vector-db-strategy.md)
- [数据来源清单](../docs/0.%20References/knowledge-base-references.md)
- [存储架构决策](../docs/0.%20References/storage-architecture-decision.md)