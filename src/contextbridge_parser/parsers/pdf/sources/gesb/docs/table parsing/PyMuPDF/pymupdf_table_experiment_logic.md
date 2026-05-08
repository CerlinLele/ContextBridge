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

`page.get_text("words", sort=True)` 返回的每一项是一个 tuple：

```text
(x0, y0, x1, y1, text, block_no, line_no, word_no)
```

`_page_words()` 本身不做业务解析，只是把 PyMuPDF 的 tuple 转成更容易读取和调试的 dict：

```python
{
    "x0": x0,
    "y0": y0,
    "x1": x1,
    "y1": y1,
    "text": text,
    "block_no": block_no,
    "line_no": line_no,
    "word_no": word_no,
}
```

字段含义：

```text
x0: word 左边界 x 坐标
y0: word 上边界 y 坐标
x1: word 右边界 x 坐标
y1: word 下边界 y 坐标
text: word 文本
block_no: PyMuPDF 识别出的文本块编号
line_no: 文本块里的行编号
word_no: 当前行里的 word 编号
```

`sort=True` 让 PyMuPDF 尽量按页面阅读顺序返回 words，但后续逻辑不能只依赖阅读顺序。
这个实验真正依赖的是每个 word 的坐标。

后续所有行、列、cell 的判断都主要依赖这些坐标。

具体来说：

```text
判断 word 属于哪一列: 看 x0 落在哪个 x range
判断 word 属于哪一行: 看 y0 和 row boundary
判断是否是 row start: 看 text 是否是数字，以及 x0/y0 是否符合表格行特征
判断 Requirements label/value: 看 x0 是否落在 requirements_label 或 requirements_value 范围
重组多行文本: 按 y0 和 x0 排序后拼接
```

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

`_find_header_words(words)` 的职责不是解析表格内容，而是判断当前页是否有一行
看起来像 GESB SAFF 表格表头。它先找候选的 `Column` word：

```python
column_candidates = [
    word
    for word in words
    if word["text"] == "Column" and word["x0"] < 80.0 and 40.0 <= word["y0"] <= 160.0
]
```

这些条件表达了几个页面布局假设：

```text
text == "Column": 表头第一列的文字必须是 Column
x0 < 80.0: 真正的表头 Column 应该在页面左侧
40.0 <= y0 <= 160.0: 表头应该在页面上方区域，而不是正文中间或页脚
```

找到候选 `Column` 后，它会取同一视觉行附近的 words：

```python
same_line = [
    word for word in words if abs(word["y0"] - column_word["y0"]) <= 5.0
]
```

这里的 `5.0` 是 y 坐标容忍度。PDF 中同一视觉行的多个 word 不一定有完全相同的
`y0`，所以需要允许少量上下偏差。

然后它在 `same_line` 里查找其他关键表头：

```python
for text in ("Field", "Description", "Requirements", "Required", "MIG", "DES"):
    matches = [word for word in same_line if word["text"] == text]
    if matches:
        header[text] = matches[0]
```

只有当所有关键表头都存在时，才返回 header dict：

```python
{
    "Column": column_word,
    "Field": field_word,
    "Description": description_word,
    "Requirements": requirements_word,
    "Required": required_word,
    "MIG": mig_word,
    "DES": des_word,
}
```

这些返回值仍然是 `_page_words()` 生成的 word dict，所以每个表头都带有
`x0/y0/x1/y1/text` 等坐标信息。`_detect_table_layout()` 后面正是使用这些
header word 的 `x0` 来推导各列的 x range。

如果没有找到完整表头，`_find_header_words(words)` 会返回 `None`。这会导致
`_detect_table_layout()` 进入 fallback 分支，使用 `DEFAULT_X_RANGES`。

这个规则的风险是：如果某页没有重复表头、表头跨行、表头文字被 PyMuPDF 拆分方式
和预期不同，或者表头 y 坐标超出 `40.0` 到 `160.0` 的范围，它就会失败。失败后
后续解析仍然可以运行，但更容易出现漏行、串列或 header contamination。

这个方法的目标是生成后续解析需要的 layout：

```python
{
    "x_ranges": x_ranges,
    "table_data_y_min": table_data_y_min,
    "source": "header_words" or "fallback",
}
```

其中：

```text
x_ranges: 每一列的 x 坐标范围
table_data_y_min: 表格数据区开始的 y 坐标
source: 这个 layout 是从表头推导出来的，还是使用 fallback 默认值
```

如果 `_find_header_words(words)` 没有找到完整表头，方法会直接返回 fallback layout：

```python
return {
    "x_ranges": DEFAULT_X_RANGES,
    "table_data_y_min": DEFAULT_TABLE_DATA_Y_MIN,
    "source": "fallback",
}
```

这意味着当前页没有可靠的表头坐标时，后续所有列判断都会依赖硬编码的
`DEFAULT_X_RANGES`。这能保证脚本继续运行，但准确性通常不如从当前页表头动态推导。

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

更具体地说，方法会先读取每个关键表头 word 的左边界坐标：

```python
column_x = header["Column"]["x0"]
field_x = header["Field"]["x0"]
description_x = header["Description"]["x0"]
requirements_x = header["Requirements"]["x0"]
required_x = header["Required"]["x0"]
mig_x = header["MIG"]["x0"]
des_x = header["DES"]["x0"]
```

然后用这些 header `x0` 推导列边界：

```python
x_ranges = {
    "column_number": (max(0.0, column_x - 12.0), field_x - 5.0),
    "field_name": (field_x - 5.0, description_x - 5.0),
    "description": (description_x - 5.0, requirements_x - 5.0),
    "requirements_label": (requirements_x - 5.0, requirements_x + 58.0),
    "requirements_value": (requirements_x + 58.0, required_x - 8.0),
    "required_by_gesb": (required_x - 5.0, mig_x - 2.0),
    "mig_reference": (mig_x - 2.0, des_x - 2.0),
    "des_reference": (des_x - 2.0, des_x + 80.0),
}
```

这些 `-5.0`、`+58.0`、`-8.0`、`+80.0` 是经验偏移量，用来把 header
word 的左边界扩展成实际 cell 范围。它不是通用 PDF 表格算法，而是针对当前
GESB SAFF 表格布局调出来的规则。

这些数字有两类来源。

第一类是 PyMuPDF 从当前页真实 word layer 里读出来的表头坐标：

```python
column_x = header["Column"]["x0"]
field_x = header["Field"]["x0"]
description_x = header["Description"]["x0"]
requirements_x = header["Requirements"]["x0"]
required_x = header["Required"]["x0"]
mig_x = header["MIG"]["x0"]
des_x = header["DES"]["x0"]
```

这些值不是手写的。它们来自页面上表头文字的左边界坐标。例如 `field_x` 是
`Field` 这个 word 的 `x0`。

第二类是人工调出来的 buffer / padding：

```text
-12.0
-5.0
+58.0
-8.0
-2.0
+80.0
```

这些值用于把“表头文字的左边界”转换成“整列 cell 的有效范围”。

例如：

```python
"field_name": (field_x - 5.0, description_x - 5.0)
```

含义是：

```text
field_name 列从 Field 表头左边界稍微往左 5pt 开始
field_name 列到 Description 表头左边界稍微往左 5pt 结束
```

这样做是因为实际 cell 内容不一定和表头文字完全左对齐，给一点 buffer 可以减少
贴边 word 被分到错误列的概率。

`Requirements` 的 `+58.0` 更特殊：

```python
"requirements_label": (requirements_x - 5.0, requirements_x + 58.0)
"requirements_value": (requirements_x + 58.0, required_x - 8.0)
```

这里不是切外层表格列，而是在 `Requirements` 这一大列内部再切出 label/value
两个子列：

```text
Mandatory:    Yes
Data Type:    String
Length:       7
Value(s):     VERSION
```

因此 `requirements_x + 58.0` 代表当前实验中观察到的 label/value 分界线。

这些数字通常是通过以下方式逐步确定的：

```text
查看 page.get_text("words") 输出的 x0/y0 坐标
查看 page.find_tables() 的 preview_rows 作为对照
检查生成 JSON 里哪些 word 串列或漏列
根据错分情况微调左右边界
重复运行实验并观察质量报告
```

所以这些值应该被理解为 GESB SAFF PDF 的 source-specific tuning，而不是通用
PDF table parser 参数。未来如果要迁移到其他 PDF，这些值应该进入 source profile
或 layout config，而不是写死在通用逻辑里。

后续可以把这些 magic numbers 命名化，例如：

```python
COLUMN_LEFT_PADDING = 12.0
COLUMN_GAP_PADDING = 5.0
REQUIREMENTS_LABEL_WIDTH = 58.0
REQUIRED_COLUMN_RIGHT_PADDING = 8.0
REFERENCE_GAP_PADDING = 2.0
DES_RIGHT_WIDTH = 80.0
```

这样调参时更容易看出每个数字的意图，也更容易迁移到其他 source。

`table_data_y_min` 使用：

```python
header["Column"]["y0"] + 10.0
```

也就是从表头行下方开始识别数据行，避免把表头文字本身当成 row start 或 row content。

这个方法的价值是：如果每页表头位置有轻微偏移，脚本可以按当前页真实表头动态计算
列范围，而不是完全依赖固定坐标。

它的风险是：当某页没有完整表头，或表头被 PyMuPDF 拆分得不符合预期时，会退回
fallback。fallback 页更容易出现漏行、串列或表头污染，所以后续优化可以考虑复用上一页
成功检测到的 `header_words` layout，而不是立即使用 `DEFAULT_X_RANGES`。

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
