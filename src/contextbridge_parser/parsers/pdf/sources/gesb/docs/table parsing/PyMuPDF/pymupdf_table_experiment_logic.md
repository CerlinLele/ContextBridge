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

这个方法的职责是把当前页的 word list 按行切开。它不负责判断 word 属于哪一列，
也不直接解析 `Requirements`。它只根据 `row_starts` 决定每个业务 row 的纵向范围，
然后把这个范围内的 words 交给 `_build_row()`。

输入包括：

```text
page_number: 当前页码
words: 当前页所有 word，来自 _page_words()
row_starts: 当前页所有 row start，来自 _find_row_starts()
layout: 当前页 layout，来自 _detect_table_layout()
```

核心代码是：

```python
def _extract_rows_from_words(
    page_number: int,
    words: list[dict[str, Any]],
    row_starts: list[dict[str, Any]],
    layout: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = []
    for index, row_start in enumerate(row_starts):
        next_y = (
            row_starts[index + 1]["y0"]
            if index + 1 < len(row_starts)
            else _next_section_or_page_end(words, row_start["y0"])
        )
        row_words = [
            word for word in words if row_start["y0"] - 1 <= word["y0"] < next_y - 0.5
        ]
        row = _build_row(page_number, row_start, next_y, row_words, layout["x_ranges"])
        rows.append(row)
    return rows
```

`row_start` 通常是第一列里的数字 word，例如 column number `23`。

每一行的纵向范围是：

```text
当前 row_start.y0
到下一个 row_start.y0
```

如果已经是当前页最后一个 row start，就用 `_next_section_or_page_end()` 找下一节标题
作为结束位置；找不到时使用 `9999.0` 作为页尾兜底。

`_next_section_or_page_end(words, start_y)` 的职责就是处理这种“当前 row 是页面最后一个
row start”的情况。它会尝试在当前 row 后面找下一节标题，并把下一节标题的 `y0`
作为当前 row 的结束位置。

核心代码是：

```python
def _next_section_or_page_end(words: list[dict[str, Any]], start_y: float) -> float:
    candidates = []
    for word in words:
        if word["y0"] <= start_y:
            continue
        if word["x0"] < 80 and re.fullmatch(r"1[01]\.\d+(?:\.\d+)?\.", word["text"]):
            candidates.append(word["y0"])
    return min(candidates) if candidates else 9999.0
```

它的判断规则是：

```text
只看当前 row start 后面的 word: word["y0"] > start_y
只看页面左侧的 word: word["x0"] < 80
只匹配类似 10.1. / 10.2.3. / 11.4. / 11.4.3. 的 section heading
```

section heading regex 是：

```python
r"1[01]\.\d+(?:\.\d+)?\."
```

拆开看：

```text
1[01]: 只允许 10 或 11 开头
\.   : 点号
\d+  : 一段数字
(?:\.\d+)?: 可选的第二级 .数字
\.   : 结尾点号
```

如果找到多个候选 section heading，它返回最靠上的那个：

```python
return min(candidates)
```

如果没有找到候选，就返回：

```python
9999.0
```

这个值远大于正常页面高度，相当于让后续 row word 收集逻辑把当前 row start 之后的
剩余 words 都当成这一行的一部分。

这个方法的风险是：

```text
regex 只认 10.x. 和 11.x.，章节编号变化时会失效
如果 section heading 被 PyMuPDF 拆成多个 word，可能匹配不到
如果最后一行后面有 footer、note 或 repeated table header，但没有 section heading，可能被吞进 row
9999.0 是粗粒度页尾兜底，容易放大最后一行污染
```

所以它是一个实用但明显 source-specific 的 row boundary fallback。

收集 row words 时使用了两个小 buffer：

```python
row_start["y0"] - 1 <= word["y0"] < next_y - 0.5
```

含义是：

```text
row_start["y0"] - 1: 起点稍微往上放宽，避免漏掉同一视觉行里 y0 略高的 word
next_y - 0.5: 终点稍微往上收紧，避免把下一行 row start 附近的 word 吃进来
```

然后它收集这个 y 范围内的所有 words，并交给 `_build_row()` 生成结构化 row：

```python
row = _build_row(page_number, row_start, next_y, row_words, layout["x_ranges"])
```

`_build_row()` 后续会使用 `layout["x_ranges"]` 判断每个 word 属于哪一列。

这个方法依赖几个关键假设：

```text
每个业务 row 都有一个可靠的 row_start
row_starts 已经按页面 y 坐标顺序排列
两个 row_start 之间的 words 都属于前一个业务 row
最后一个 row 可以通过下一节标题或页尾确定结束位置
```

它的风险也来自这些假设：

```text
如果漏掉某个 row_start，上一行可能吞掉这个漏掉行的内容
如果误识别出一个假的 row_start，真实业务行可能被切断
如果 section heading 或 repeated table header 落在两个 row_start 之间，可能混入 row
如果最后一行没有找到合适结束点，可能一直吃到页尾
```

之前质量检查里看到的 header contamination、section contamination 和部分 missing
column numbers，都可能和这里的 row boundary 策略有关。

## Cell Assignment

`_build_row()` 会把 row words 按 `x0` 分配到对应 cell。

这个函数是从“坐标分组”转换到“结构化业务 row”的关键步骤。它接收
`_extract_rows_from_words()` 切出来的一行 words，然后根据列坐标范围组装成最终 row dict。

函数签名是：

```python
def _build_row(
    page_number: int,
    row_start: dict[str, Any],
    next_y: float,
    row_words: list[dict[str, Any]],
    x_ranges: dict[str, tuple[float, float]],
) -> dict[str, Any]:
```

输入含义：

```text
page_number: 当前页码
row_start: 当前行第一列的数字 word，例如 column number 23
next_y: 当前行结束 y 坐标
row_words: 当前行 y 范围内的所有 words
x_ranges: 当前页每一列的 x 坐标范围
```

它先建立一个按列名收集 words 的容器：

```python
cells: dict[str, list[dict[str, Any]]] = defaultdict(list)
```

然后遍历当前行的每个 word，根据 `word["x0"]` 判断它属于哪一列：

```python
for word in row_words:
    cell_name = _cell_name_for_x(word["x0"], x_ranges)
    if cell_name:
        cells[cell_name].append(word)
```

分配逻辑在 `_cell_name_for_x()`：

```text
如果 min_x <= word.x0 < max_x
就把 word 放入对应列
```

也就是说，`_build_row()` 本身不直接硬编码每一列的位置，而是依赖前面
`_detect_table_layout()` 生成的 `x_ranges`。

`Requirements` 列会被特殊处理：

```python
requirement_lines = _requirements_lines(
    cells["requirements_label"], cells["requirements_value"]
)
```

原因是 `Requirements` 在视觉上不是一个普通长文本列，而是一个嵌套 key-value
结构。例如：

```text
Mandatory:    Yes
Data Type:    String
Length:       7
Value(s):     VERSION
```

所以 `_build_row()` 不直接把 `requirements_label` 和 `requirements_value` 简单拼接，
而是交给 `_requirements_lines()` 按 y 坐标配对，生成：

```python
[
    {"label": "Mandatory:", "value": "Yes"},
    {"label": "Data Type:", "value": "String"},
    {"label": "Length:", "value": "7"},
]
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

这些字段的来源是：

```python
return {
    "page_number": page_number,
    "bbox": _round_rect(
        (
            min((word["x0"] for word in row_words), default=row_start["x0"]),
            row_start["y0"],
            max((word["x1"] for word in row_words), default=row_start["x1"]),
            next_y,
        )
    ),
    "column_number": _first_int(_join_words(cells["column_number"])),
    "field_name": _join_words(cells["field_name"]),
    "description": _join_words(cells["description"]),
    "requirements_text": _join_requirement_lines(requirement_lines),
    "requirements_lines": requirement_lines,
    "requirements": _requirements_dict(requirement_lines),
    "required_by_gesb": _join_words(cells["required_by_gesb"]),
    "mig_reference": _join_words(cells["mig_reference"]),
    "des_reference": _join_words(cells["des_reference"]),
    "raw_text": _join_words(row_words),
}
```

关键字段说明：

```text
bbox: 当前 row 的边界框，格式是 [x0, y0, x1, y1]
column_number: 从 column_number cell 文本中提取第一个整数
field_name: field_name cell 的 words 拼接
description: description cell 的 words 拼接
requirements_text: requirements label/value 拼成的一段文本
requirements_lines: requirements 的 label/value 行数组
requirements: normalized requirements dict
required_by_gesb: Required by GESB? 列文本
mig_reference: MIG 2.0 Reference 列文本
des_reference: DES Spec 5.8 Reference 列文本
raw_text: 当前 row 所有 words 的拼接，用于调试
```

`bbox` 的计算方式是：

```text
x0: row_words 里的最小 x0，找不到时使用 row_start.x0
y0: row_start.y0
x1: row_words 里的最大 x1，找不到时使用 row_start.x1
y1: next_y
```

这个函数的风险是：

```text
如果 x_ranges 不准，word 会被分到错误列
如果 row_words 已经混入 header、section heading 或 footer，_build_row() 会照单全收
如果 word.x0 贴近列边界，可能被分到相邻列
Requirements label/value 依赖 y 坐标配对，多行 value 或错位时可能拼错
_join_words() 按 (y0, x0) 排序拼接，对复杂换行不一定完美
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

这个函数的作用是把 PyMuPDF 自带 `find_tables()` 识别出来的表格结果整理成摘要，
方便放进实验 JSON 里做对照分析。

它的核心逻辑是：

```python
def _find_tables_summary(page: fitz.Page) -> list[dict[str, Any]]:
    tables = []
    for table_index, table in enumerate(page.find_tables().tables):
        extracted = table.extract()
        tables.append(
            {
                "table_index": table_index,
                "bbox": _round_rect(table.bbox),
                "row_count": table.row_count,
                "col_count": table.col_count,
                "preview_rows": extracted[:6],
            }
        )
    return tables
```

`page.find_tables()` 会让 PyMuPDF 根据页面中的线条、边框、矩形、文本对齐等布局信号，
尝试识别表格区域。`tables` 是当前页识别出的 table 列表。

对每个 table，脚本会调用：

```python
extracted = table.extract()
```

`extract()` 返回一个二维数组，表示 PyMuPDF 识别到的表格 cell 内容。例如：

```python
[
    ["1", "Version", "Heading text", "", "Mandatory:", "Yes", "No", "N/A", "N/A"],
    ["", "", "", "", "Data Type:", "String", "", "", ""],
]
```

最终保存的摘要字段包括：

```text
table_index: 当前页第几个被 PyMuPDF 识别出的 table
bbox: table 边界框，格式是 [x0, y0, x1, y1]
row_count: PyMuPDF 识别出的行数
col_count: PyMuPDF 识别出的列数
preview_rows: table.extract() 的前 6 行，用于快速预览识别效果
```

`bbox` 会通过 `_round_rect(table.bbox)` 做三位小数 rounding，避免 JSON 里出现过长的
浮点数。

但它的结果只写入 `pages[].pymupdf_find_tables`，作为实验对照信息：

```text
table_index
bbox
row_count
col_count
preview_rows
```

这个脚本没有直接依赖 `find_tables()` 的结果来构建最终 `rows`。

主 row 构建路径仍然是：

```text
_page_words()
->_detect_table_layout()
->_find_row_starts()
->_extract_rows_from_words()
->_build_row()
```

因此 `_find_tables_summary()` 更像一个 diagnostic snapshot。它回答的问题是：

```text
PyMuPDF 自带 find_tables() 在当前页看到了哪些表格？
这些表格的 bbox、行数、列数是多少？
前几行内容看起来是否正确？
它有没有漏掉外层 field rows？
它是否能正确拆分 Requirements nested table？
```

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
