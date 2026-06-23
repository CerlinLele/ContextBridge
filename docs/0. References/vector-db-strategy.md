# Vector Database 内容策略

> 本文档说明哪些资料应该拿下来放进 vector database，哪些保留为链接即可。

---

## 决策框架

### ✅ 应该入库的内容

1. **核心法规与政策文档**
   - ATO Payday Super 官方指南（完整快照）
   - SuperStream 数据标准规范
   - Superannuation Guarantee 法案关键条款
   - 2026年政策变化关键时间点说明

2. **产品核心文档**
   - Wrkr 产品功能完整说明
价模型和计算逻辑
   - 核心博客文章（如迁移指南、操作指南）
   - FSG & PDS（金融服务指南和产品披露声明）

3. **技术标准与集成**
   - SuperStream 消息格式和数据结构
   - STP Phase 2 报告规范
   - Payroll 集成 API 文档（如有）

4. **行业上下文**
   - 超级年金系统运作机制概述
   - 小企业 super 合规常见问题
   - Bookkeeper / Payroll 专业人士工作流

5. **竞品对比分析**
   - SuperChoice / Beam / Xero / MYOB 功能对比
   - 定价模型差异
   - 目标用户群差异

### ⛔ 仅保留链接的内容

1. **实时更新内容**
   - 最新定价（频繁变动）
   - 产品 changelog 和 release notes
   - 政府最新公告和新闻

2. **海量资源库**
   - 完整的 legislation.gov.au
   - 行业协会完整资源库
   - 所有历史博客文章

3. **纯导航页面**
   - 官网首页
   - 产品目录页
   - 资源索引页

---

## 入库优先级

### P0 - 立即入库（回答用户问题必需）

| 资源 | 来源 | 预计字数 | 入库状态 |
|------|------|----------|----------|
| Payday Super 官方指南 | ATO | 5-10k | ⏳ 待入库 |
| Wrkr 产品功能说明 | wrkr.com.au/payday-super-clearing-house | 3-5k | ⏳ 待入库 |
| SuperStream 标准概述 | ATO SuperStream 页面 | 3-5k | ⏳ 待入库 |
| The ATO SBSCH Transition Guide | Wrkr 博客 2026-06-23 | 2-3k | ⏳ 待入库 |
| The Small Business Guide to Payday Super | Wrkr 博客 2026-06-22 | 3-4k | ⏳ 待入库 |

### P1 - 次要入库（补充上下文）

| 资源 | 来源 | 预计字数 | 入库状态 |
|------|------|----------|----------|
| Super for Employers 总览 | ATO | 4-6k | ⏳ 待入库 |
| STP Phase 2 规范 | ATO | 3-5k | ⏳ 待入库 |
| Paying Super for Contractors | Wrkr 博客 2026-06 | 2-3k | ⏳ 待入库 |
| Navigating the New Payday Super Rules | Wrkr 博客 2024-10-30 | 2-3k | ⏳ 待入库 |
| 竞品功能对比（整理） | 手动整理 | 2-3k | ⏳ 待创建 |

### P2 - 可选入库（深度理解）

| 资源 | 来源 | 预计字数 | 入库状态 |
|------|------|----------|----------|
| AIST 政策分析 | aist.asn.au | 视情况 | ⏳ 待评估 |
| ASFA 行业研究 | superannuation.asn.au | 视情况 | ⏳ 待评估 |
| ICB Bookkeeper 指南 | icb.org.au | 视情况 | ⏳ 待评估 |

---

## 抓取与处理策略

### 自动抓取友好

- ✅ Wrkr 官网大部分页面
- ✅ 行业协会公开资源
- ✅ Treasury / APRA 政策文档

### 需要浏览器手动访问

- ⚠️ ATO 网站（可能返回 403）
  - 解决方案：通过浏览器复制内容，或使用 Playwright 模拟浏览器
- ⚠️ 需要登录的资源
  - 解决方案：手动下载后入库

### 版本控制

对于关键文档，建议保存快照：

```
vector_db/
├── snapshots/
│   ├── ato_payday_super_2026-06.md     # 2026年6月版本
│   ├── wrkr_pricing_2026-06.md          # 定价快照
│   └── superstream_v2.md                # 标准版本2
```

快照文件头部注明：
```markdown
---
source: https://www.ato.gov.au/...
snapshot_date: 2026-06-24
v [ ] 内容是否稳定（不会频繁变动）？
- [ ] 内容是否对回答用户问题必需？
- [ ] 内容是否可以通过 API/爬虫获取？
- [ ] 是否需要保存历史版本？
- [ ] 文档是否已标注来源和日期？

入库后：

- [ ] 在 `knowledge-base-references.md` 中标注 "✅ 已入库"
- [ ] 记录入库日期和来源 URL
- [ ] 验证 embedding 质量（通过测试问题）

---

## 测试问题示例

用以下问题验证 vector DB 召回质量：

1. **基础概念**
   - "什么是 Payday Super？"
   - "SuperStream 是什么？"

2. **政策时间线**
   - "ATO 小企业清算所什么时候关闭？"
   - "2026年7月有什么重大变化？"

3. **产品功能**
   - "Wrkr 如何处理 contractor 的 super？"
   - "Wrkr 的定价模型是什么？"

4. **操作指南**
   - "如何从 ATO SBSCH 迁移到 Wrkr？"
   - "首次使用 Wrkr 需要准备什么信息？"

5. **合规要求**
   - "小企业支付 super 的法定时限是多久？"
   - "什么情况下需要使用 SuperStream？"

---

## 更新策略

| 内容类型 | 更新频率 | 触发条件 |
|----------|----------|----------|
| 法规文档 | 季度检查 | 政府公告新政策 |
| 产品文档 | 月度检查 | Wrkr 发布重大更新 |
| 博客文章 | 按需 | 新文章发布且与核心功能相关 |
| 竞品信息 | 季度检查 | 竞品发布重大功能 |
| 技术标准 | 年yday-super-clearing-house.md)