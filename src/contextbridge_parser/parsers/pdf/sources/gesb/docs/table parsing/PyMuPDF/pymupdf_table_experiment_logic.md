# PyMuPDF Table Experiment Logic

This document explains the actual logic in
`pymupdf_table_experiment.py`.

该文件是一个 GESB SAFF 表格抽取实验脚本，不是生产 parser。它的目标是验证：
是否可以利用 PyMuPDF 提供的 word 坐标，比纯文本顺序解析更可靠地还原 SAFF
field table 的行和列。

## High-Level Flow

入口是 `extract_pymupdf_tables(source_path)`：

```text
PDF
-> open with PyMuPDF
-> iterate table pages
-> extract page words with coordinates
-> detect table column layout
-> detect row starts
-> collect PyMuPDF find_tables() summary
-> rebuild rows from word coordinates
-> emit experiment JSON
```

它只处理 `saff.py` 中定义的表格页范围：

```text
TABLE_PAGE_START = 10
TABLE_PAGE_END = 27
```

输出 JSON 包含三块主要内容：

```text
experiment
pages
rows
```

`pages` 保存每页的检测摘要和 `find_tables()` 对照结果。`rows` 保存脚本自己
根据 word 坐标重建出来的业务表格行。

## Relationship With Production Parser

该脚本从 `saff.py` 复用默认输入输出路径和页码范围：

```text
DEFAULT_OUTPUT_DIR
DEFAULT_SOURCE_PATH
TABLE_PAGE_START
TABLE_PAGE_END
```

但它不参与 `parse_gesb_saff_pdf()` 的生产解析流程。生产 parser 仍然是
`saff.py` 中基于 `pypdf` 文本行和正则规则的实现。

## Word Extraction

`_page_words(page)` 调用：

```python
page.get_text("words", sort=True)
```

每个 word 会被转换成 dict，并保留：

```text
x0
y0
x1
y1
text
block_no
line_no
word_no
```

后续所有行、列、cell 的判断都主要依赖这些坐标。

## Layout Detection

`_detect_table_layout(words)` 会先尝试从当前页表头推导列范围。

它调用 `_find_header_words(words)` 查找一行表头，要求：

```text
Column
Field
Description
Requirements
Required
MIG
DES
```

都出现在同一视觉行附近。

如果找到了表头，就根据这些 header word 的 `x0` 动态计算每一列的 x 范围：

```text
column_number
field_name
description
requirements_label
requirements_value
required_by_gesb
mig_reference
des_reference
```

其中 `Requirements` 被拆成两列：

```text
requirements_label
requirements_value
```

这是为了还原类似下面的嵌套 key-value 结构：

```text
Mandatory: Yes
Data Type: String
Length: 7
Value(s): VERSION
```

如果找不到表头，就使用 `DEFAULT_X_RANGES` 里的硬编码坐标范围，并把布局来源
标记为 `fallback`。

## Row Start Detection

`_find_row_starts(words, layout)` 用第一列的数字识别业务行开始。

一个 word 需要同时满足：

```text
word.y0 >= table_data_y_min
word.x0 位于 column_number 的 x 范围内
word.text 匹配 \d{1,3}
```

然后 `_looks_like_table_row_start()` 会再做一次校验，避免误把普通数字当成新行：

```text
同一视觉行内必须有 field_name 列内容
并且右侧参考列或 requirements 区域附近必须有内容
```

也就是说，行开始不是只看数字，还要看这个数字所在视觉行是否像一个完整的表格行。

## Row Reconstruction

`_extract_rows_from_words()` 遍历所有 row start。

每一行的纵向范围是：

```text
当前 row_start.y0
到下一个 row_start.y0
```

如果已经是当前页最后一个 row start，就用 `_next_section_or_page_end()` 找下一节标题
作为结束位置；找不到时使用 `9999.0` 作为页尾兜底。

然后它收集这个 y 范围内的所有 words，并交给 `_build_row()` 生成结构化 row。

## Cell Assignment

`_build_row()` 会把 row words 按 `x0` 分配到对应 cell。

分配逻辑在 `_cell_name_for_x()`：

```text
如果 min_x <= word.x0 < max_x
就把 word 放入对应列
```

最终 row 输出字段包括：

```text
page_number
bbox
column_number
field_name
description
requirements_text
requirements_lines
requirements
required_by_gesb
mig_reference
des_reference
raw_text
```

## Requirements Parsing

`Requirements` 是这个脚本里最重要的特殊处理。

PDF 中它视觉上是一个嵌套 key-value 表格，所以脚本把它拆成：

```text
requirements_label
requirements_value
```

`_requirements_lines(label_words, value_words)` 会：

1. 用 `_words_by_line()` 按 `y0` 把 label words 和 value words 各自分组。
2. 对每个 label line，用 `_nearest_line()` 找 y 坐标最接近的 value line。
3. 如果 value line 没有被任何 label 使用，就把它追加到最后一个 requirement value。

最后 `_requirements_dict()` 会把 label 映射成固定字段：

```text
mandatory
data_type
length
format
values
notes
```

支持的 label 包括：

```text
Mandatory
Data Type
Length
Format
Value(s)
Notes
```

## Role Of find_tables()

`_find_tables_summary(page)` 会调用：

```python
page.find_tables().tables
```

但它的结果只写入 `pages[].pymupdf_find_tables`，作为实验对照信息：

```text
table_index
bbox
row_count
col_count
preview_rows
```

这个脚本没有直接依赖 `find_tables()` 的结果来构建最终 `rows`。

原因是默认 `find_tables()` 在 SAFF PDF 上不完整：它能很好拆开某些
`Requirements` 嵌套表格，但会漏掉部分外层 field rows。因此主逻辑选择直接
使用 word 坐标重建行和列。

## Main Takeaway

这个实验脚本的核心不是“使用 PyMuPDF 自动识别表格”，而是：

```text
使用 PyMuPDF 的 word 坐标，按页面视觉布局手动重建 SAFF 表格结构。
```

`find_tables()` 是辅助诊断信号；真正的抽取路径是：

```text
_page_words()
->_detect_table_layout()
->_find_row_starts()
->_extract_rows_from_words()
->_build_row()
```

