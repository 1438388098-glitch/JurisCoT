# JurisCoT — 法学思维链推理引擎

> 项目性质：**LawAutoPaper 的前置独立子项目**
> 定位：一个可独立运行、独立测试的法学 CoT 推理库
> 输入：法律问题 + 相关文献/法条/案例/数据/域外法
> 支持：**6 种法学论文类型**，每种对应独立 CoT 模板
> 输出：结构化推理链 + 学术正文段落
> 验收后以 Python 包形式嵌入 LawAutoPaper

---

## 论文类型概览

JurisCoT 支持 6 种法学论文类型，每种有独立的 CoT 模板、章节结构和 Step 4c 输出变体：

| # | 论文类型 | 典型场景 | CoT 步骤数 | Step 4c 变体 | 特色输入 |
|---|---------|---------|-----------|-------------|---------|
| 1 | **理论辨析型** | 课程论文、法理论文 | 6 | 学说立场 | — |
| 2 | **案例分析型** | 判决评析论文 | 8 | 学说立场 | 案件材料 |
| 3 | **制度比较型** | 比较法论文 | 6 | 借鉴建议 | 域外法条 |
| 4 | **实证研究型** | 数据驱动论文 | 6 | 学说立场 | 数据发现 |
| 5 | **立法建议型** | 修法建议论文 | 6 | 条文草案 | 域外法（可选） |
| 6 | **文献综述型** | 综述论文 | 4 | 研究空白 | — |

---

## 一、为什么独立

| 问题 | 合在 LawAutoPaper 一起做 | 独立出来做 |
|------|------------------------|-----------|
| CoT 质量不确定时，整套代码都不敢动 | 拖慢全局 | 只影响 JurisCoT 自身 |
| 需要反复调 prompt、跑验证 | 每次都要配 Streamlit 环境 | 命令行直接跑，秒级反馈 |
| 验证通过后怎么接入 | 代码耦合，重构痛苦 | `pip install -e .` 即插即用 |
| 每天 1 小时，精力有限 | 一天搞 CoT，一天搞 UI，效率低 | 专注一件事，日日有进展 |

---

## 二、JurisCoT 的范围

```
╔═══════════════════════════════════════════════════════════╗
║                     JurisCoT 的范围                       ║
║                                                           ║
║  输入：                                                    ║
║    - 论文主题 + 章节主题                                    ║
║    - 论文类型（6 种：理论/案例/比较/实证/立法/综述）           ║
║    - 相关法条原文                                           ║
║    - 相关文献文本块（RAG 检索结果，外部传入）                  ║
║    - 相关案例描述（案例型）                                   ║
║    - 域外法条（比较型）                                       ║
║    - 数据发现（实证型）                                       ║
║    - 本章前置上下文（前一章的结论摘要，如有）                   ║
║                                                           ║
║  输出：                                                    ║
║    - 每个 CoT 子步骤的结构化 JSON                            ║
║    - 最终润色后的学术正文段落                                 ║
║    - 引用的文献来源 ID 列表                                  ║
║    - 推理置信度标记                                          ║
║                                                           ║
║  ╔═══════════════════════════════════════════════════════╗ ║
║  ║              JurisCoT 不负责的部分                      ║ ║
║  ║                                                       ║ ║
║  ║  ❌ PDF 解析          → LawAutoPaper 负责              ║ ║
║  ║  ❌ 向量检索/Chroma   → LawAutoPaper 负责，结果传入     ║ ║
║  ║  ❌ 文献导入/管理     → LawAutoPaper 负责              ║ ║
║  ║  ❌ Word 排版         → LawAutoPaper 负责              ║ ║
║  ║  ❌ Streamlit 界面    → LawAutoPaper 负责              ║ ║
║  ║  ❌ 用户交互          → LawAutoPaper 负责              ║ ║
║  ╚═══════════════════════════════════════════════════════╝ ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 三、核心接口设计

JurisCoT 对外只暴露一个核心函数和几个辅助函数：

```python
import os
from juriscot import ReasoningEngine, PaperType, ChapterType

# 1. 创建引擎（只需配置一次；密钥从环境变量读取，不要硬编码进代码）
engine = ReasoningEngine(
    api_key=os.environ["JURISCOT_API_KEY"],
    base_url="https://api.deepseek.com",
    model="deepseek-v4-pro",
)

# 2. 跑一个章节的完整推理
result = engine.reason(
    paper_type=PaperType.CASE_ANALYSIS,     # 理论辨析型 or 案例分析型
    chapter=ChapterType.THEORETICAL_ANALYSIS,  # 哪个章节
    chapter_topic="正当防卫必要限度的判断标准",
    legal_provisions=[                        # 相关法条
        {"条文": "《刑法》第20条第2款", "原文": "正当防卫明显超过..."}
    ],
    literature_chunks=[                       # RAG 检索的文献文本块
        {"chunk_id": "L003_12", "text": "张明楷认为...", "source": "L003"},
    ],
    case_materials=[                          # 案例材料（案例型才有）
        {"案件名称": "于欢案", "案号": "...",  "关键情节": "..."},
    ],
    previous_conclusion=None,                 # 前一章的结论（如有）
)

# 3. 获取各部分结果
print(result.steps["step4c"].本文立场)   # Pydantic 对象
print(result.final_text)               # 润色后的段落（含脚注标记）
print(result.footnotes)                # 脚注列表（Step 5 自动生成）
print(result.citations)                # 使用的文献来源列表

# 4. 导出 JSON 日志（调试用）
result.to_json("logs/chapter_2.json")
```

---

## 四、文献-提示词映射层（结合模块）

这是用户上传的参考文献和 CoT 推理之间的**桥梁**。

### 4.1 数据流向

```
LawAutoPaper                          JurisCoT
──────────                            ────────
用户上传 PDF                           │
  → 解析 → Chroma 向量化               │
  → 按章节主题检索 top-K 文本块         │
  → 传入: literature_chunks []  ──────→ 文献映射层
                                          │
                                     ┌────┴────┐
                                     │ 按CoT步骤 │
                                     │ 分配文献  │
                                     └────┬────┘
                                          │
                              ┌───────────┼───────────┐
                              ▼           ▼           ▼
                          Step 1      Step 4a      Step 5
                          只给摘要    给详细观点   给完整推理链
```

### 4.2 每个 Step 需要什么文献内容

不同 CoT 步骤对文献的需求不同，不能把全部 chunk 原文一股脑塞进每个步骤：

| Step | 需要的文献内容 | 来源 |
|------|--------------|------|
| Step 1 | 文献摘要（每篇 1-2 句） | 从 chunk 中筛选摘要性文字 |
| Step 2 | 法条解释类文献的节选 | 从 chunk 中筛选包含法条号/法条解释的段落 |
| Step 3 | 案例评析类文献的节选 | 从 chunk 中筛选包含案例名称/案号的段落 |
| Step 4a | 所有文献的核心观点摘要 | 全部 chunk（需完整覆盖，避免遗漏学说）|
| Step 4b | 各学说的详细论述 | 按 Step 4a 识别的学说名二次检索相关 chunk |
| Step 4c | Step 4b 的评析结果（不需要新文献）| 上一步输出 |
| Step 4d | 案件相关文献 + 本文立场 | Step 3 输出 + Step 4c 输出 |
| Step 5 | 完整的推理链 + 所有引用来源 | 前 4 步的全部输出 |

### 4.3 实现：`src/literature_formatter.py`

```python
class LiteratureFormatter:
    """将原始文献块按 CoT 步骤的需求格式化。"""

    def __init__(self, chunks: List[文献块输入]):
        self.chunks = chunks

    def for_step1(self) -> str:
        """Step 1 只需要摘要 —— 每篇文献提取 1-2 句概要"""
        summaries = []
        for c in self.chunks:
            # 取出每篇 chunk 的前 200 字作为摘要
            summaries.append(f"[{c.source}] {c.text[:200]}...")
        return "\n".join(summaries)

    def for_step2(self, legal_ref: str) -> str:
        """Step 2 需要法条解释 —— 筛选含特定法条号的 chunk"""
        relevant = [c for c in self.chunks if legal_ref in c.text]
        return "\n---\n".join(f"[{c.source}] {c.text}" for c in relevant)

    def for_step3(self, case_name: str) -> str:
        """Step 3 需要案件评析 —— 筛选含特定案例名称的 chunk"""
        relevant = [c for c in self.chunks if case_name in c.text]
        return "\n---\n".join(f"[{c.source}] {c.text}" for c in relevant)

    def for_step4a(self) -> str:
        """Step 4a 需要完整覆盖 —— 返回全部 chunk 的核心观点"""
        return "\n---\n".join(f"[{c.source}] {c.text}" for c in self.chunks)

    def for_step4b(self, doctrine_names: List[str]) -> str:
        """Step 4b 按学说名二次筛选 —— 找出提及该学说的 chunk"""
        relevant = []
        for c in self.chunks:
            if any(name in c.text for name in doctrine_names):
                relevant.append(c)
        return "\n---\n".join(f"[{c.source}] {c.text}" for c in relevant)

    def get_all_sources(self) -> List[str]:
        """返回所有文献来源 ID 列表（引用标注用）"""
        return list(set(c.source for c in self.chunks))
```

### 4.4 在 Pipeline 中的调用位置

```
engine.reason(input)
    │
    ├── formatter = LiteratureFormatter(input.literature_chunks)
    │
    ├── Step 1:  prompt = load("step1") + formatter.for_step1()
    ├── Step 2:  prompt = load("step2") + formatter.for_step2(法条)
    ├── Step 3:  prompt = load("step3") + formatter.for_step3(案件名)
    ├── Step 4a: prompt = load("step4a") + formatter.for_step4a()
    ├── Step 4b: prompt = load("step4b") + formatter.for_step4b(step4a_result.学说名)
    ├── Step 4c: prompt = load("step4c") + step4a_result + step4b_result  (不需要文献)
    ├── Step 4d: prompt = load("step4d") + step3_result + step4c_result
    └── Step 5:  prompt = load("step5") + 全部前序结果 + formatter.get_all_sources()
```

> 关键设计：**Step 4b 使用了 Step 4a 的输出做二次筛选**。Step 4a 识别了"法益衡量说、基本相适应说、双重标准说"后，4b 只传提及这些学说名的 chunk，避免无关内容干扰模型。

---

## 五、内部推理链路

```
                   ┌─────────┐
                   │  输入    │
                   │(含文献块) │
                   └────┬────┘
                        │
                        ▼
              ┌──────────────────┐
              │ LiteratureFormatter│  ← 文献-提示词映射层
              │ 按 Step 分配文献   │
              └────────┬─────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
    ┌──────────────┐        ┌──────────────┐
    │ 理论型模板    │        │ 案例型模板    │
    │ Step 1→2     │        │ Step 1→2→3   │
    │ →4a→4b→4c→5  │        │ →4a→4b→4c    │
    │              │        │ →4d→5        │
    └──────────────┘        └──────────────┘
            │                       │
            └───────────┬───────────┘
                        │
                        ▼
                  ┌──────────┐
                  │ 结构化输出 │
                  │ + 质量标记  │
                  └──────────┘
```

每个 Step 的输入输出是完全确定的，不做任何隐式数据传递。

---

## 五、法条注入策略（反编造机制）

### 5.1 问题

模型可能会"回忆"训练数据中的法条——但训练数据可能包含旧法、已废止条文，或模型"记混"条文内容。这是比引用文献幻觉更严重的问题——法条号对不上，论文直接失去可信度。

### 5.2 解决思路

**不让模型"回忆"法条，改为从本地法条库检索原文后注入。**

```
选题确认时:
  AI 输出必引法条列表（如"刑法第20条"）

生成正文前:
  LawAutoPaper 从本地法条库检索:
    SELECT 原文 FROM 法条库 WHERE 法条号 IN ('刑法第20条', ...)
  → 得到原文 + 最后修订时间
  → 作为 legal_provisions 参数注入 JurisCoT

CoT Step 2 prompt 硬约束:
  "你只能引用 legal_provisions 列表中列出的法条。
   不得引用任何列表外的法条。
   如需引用列表外的法条，在输出中标注'需要补充法条：XX法第X条'，
   不得自行编造其内容。"

校验阶段:
  提取生成正文中的所有法条引用 → 与注入列表比对
  不匹配 → 标记"法条引用异常"
```

### 5.3 本地法条库

用户本地已整理 263 份中国法律文件（本地法条库，具体路径不入库）：

| 子目录 | 文件数 | 内容 |
|--------|--------|------|
| 法律/ | 70 | 全国人大及其常委会制定的法律 |
| 行政法规/ | 132 | 国务院制定的行政法规 |
| 司法解释/ | 59 | 最高人民法院/最高人民检察院司法解释 |
| 监察法规/ | 2 | 国家监察委员会制定的监察法规 |

**处理方案**：

```
法条库构建（属于 LawAutoPaper 的开发任务）：

1. 批量解析 PDF/DOCX
   - 文件命名格式统一：YYYY-MM-DD_法律名称.pdf
   - pdfplumber 提取文本内容

2. 提取条文结构化
   - 正则匹配 "第X条" 模式，切割为独立条文
   - 存储到 SQLite

3. 法条库表结构（SQLite）：
   CREATE TABLE provisions (
     id INTEGER PRIMARY KEY,
     法律名称 TEXT,          -- "中华人民共和国刑法"
     条文编号 TEXT,          -- "第20条"
     条文原文 TEXT,          -- 完整原文
     文件路径 TEXT,          -- 源文件路径
     最后修订 TEXT,          -- "2020-12-26"
     部门法 TEXT,            -- "刑法"
     来源 TEXT DEFAULT '本地法条库'
   );

4. 检索接口：
   def search_provisions(keywords: List[str]) -> List[法条输入]:
       """按法条号或关键词检索，返回可注入的法条列表"""
```

### 5.4 Step 2 Prompt 法条约束

在现有 prompt 基础上添加：

```
⚠️ 法条引用硬约束：
- 你只能引用输入中 legal_provisions 列表内的法条
- 引用时必须使用列表中提供的原文，不得改写
- 如需引用列表外的法条，必须在输出中添加：
  {"需要补充法条": ["XX法第X条"], "原因": "讨论XX问题时需引用"}
- 绝对禁止自行编造任何法条的内容或文号
```

### 5.5 遇到"需要但未存"的法条

模型可以提出需求，但必须标记清楚：

```
模型 Step 2 输出：
{
  "适用法条": "刑法第20条",
  "法条来源": "legal_provisions",      ← 来自注入
  "补充需求": [
    {"需要补充法条": "民法典第X条", "原因": "...", "状态": "本地未收录"}
  ]
}

质量报告中：
⚠️ 以下法条引用未经校验（法条库中未收录，请手动核实）：
  - 民法典第X条
```

---

## 六、验收标准（硬性）

JurisCoT 必须通过以下全部测试才算验收通过：

### 验收 1：格式符合性

```
测试：跑理论型模板和案例型模板各一次
标准：每一步的输出能被 Pydantic 成功解析，无 JSON 解析失败
      JSON 解析失败率 < 5%（允许 5% 的重试次数）
```

### 验收 2：推理完整性

```
测试：用 3 个不同部门法主题（刑法/民法/行政法各一）各跑一次理论型模板
标准：
  - Step 4a 识别的学说 ≥ 2 个
  - Step 4b 的评析中，每种学说都包含"理论依据"+"解释力"+"局限"三个字段
  - Step 4c 的理由 ≥ 2 条
```

### 验收 3：引用可溯源性

```
测试：在输入中提供已知的文献块，观察输出中的引用标注
标准：
  - 每个标注"来源文献"的学说都与输入的某个 chunk_id 对应
  - 不出现"来源文献: []"的空引用（如果引用了某文献但无来源）
```

### 验收 4：跨工具一致性

```
测试：同一组输入，连续跑 3 次（条件完全相同）
标准：3 次的 Step 4a 学说名称至少 2/3 一致
      3 次的 Step 4c 立场一致（不会今天选 A 说明天选 B 说）
```

---

## 七、文件结构

```
JurisCoT/
├── README.md                       # 项目说明 + 快速开始
├── pyproject.toml                  # pip install -e . 配置
├── requirements.txt                # openai + pydantic + pyyaml
├── DESIGN.md                       # 本文件
├── docs/roadmap-internal.md        # 维护者个人的 40 天工作排期
│
├── prompts/
│   ├── base/
│   │   ├── system_prompt.md        # 角色设定（从 LawAutoPaper 复用）
│   │   └── legal_rules.md          # 法学论证规则（从 LawAutoPaper 复用）
│   ├── cot/
│   │   ├── step1_problem.md
│   │   ├── step2_premise.md
│   │   ├── step3_case.md
│   │   ├── step4a_doctrines.md
│   │   ├── step4b_analysis.md
│   │   ├── step4c_position.md         # 学说立场型（理论/案例/实证）
│   │   ├── step4c_comparative.md      # 借鉴建议型（比较）
│   │   ├── step4c_legislative.md      # 条文草案型（立法建议）
│   │   ├── step4c_review.md           # 研究空白型（综述）
│   │   ├── step4d_application.md
│   │   └── step5_polish.md
│   └── templates/
│       ├── theory_type.yaml           # 理论辨析型
│       ├── case_type.yaml             # 案例分析型
│       ├── comparative_type.yaml      # 制度比较型
│       ├── empirical_type.yaml        # 实证研究型
│       ├── legislative_type.yaml      # 立法建议型
│       └── review_type.yaml           # 文献综述型
│
├── src/
│   ├── __init__.py
│   ├── engine.py                   # ReasoningEngine 主类
│   ├── prompt_loader.py            # 加载 + 变量替换
│   ├── literature_formatter.py     # ★ 文献-提示词映射层（结合模块）
│   ├── pipeline.py                 # 单步执行 + 链式调用
│   ├── schemas.py                  # 所有 Pydantic Schema
│   ├── types.py                    # PaperType / ChapterType 枚举
│   └── cli.py                      # 命令行测试入口
│
├── tests/
│   ├── test_data/                  # 测试用的 mock 输入
│   │   ├── criminal_case.json      # 刑法案例
│   │   ├── civil_theory.json       # 民法理论
│   │   └── admin_mixed.json        # 行政法混合
│   └── test_pipeline.py            # 验收测试
│
└── logs/                           # 每次运行的推理日志
```

---

## 八、技术细节

### 7.1 模型调用

自动开启 thinking 模式（法学推理需要内部思考链）：

```python
params = {
    "model": "deepseek-v4-pro",
    "messages": [...],
    "max_tokens": 16384,
    "extra_body": {"thinking": {"type": "enabled"}},
    "reasoning_effort": "high",
}
```

### 7.2 JSON 解析容错

模型输出可能包含 JSON 之外的文字（如思考过程）。解析策略：

```
1. 尝试直接 json.loads()
2. 失败 → 用正则提取 ```json ... ``` 代码块
3. 失败 → 用正则提取第一个 { ... } 对
4. 失败 → 自动重试一次（temperature 调低）
5. 仍失败 → 返回错误，记录日志
```

### 7.3 推理日志

每次推理自动保存完整日志到 `logs/`，包含：
- 输入参数
- 每个 step 的原始模型输出
- 每个 step 的解析结果
- 重试次数和错误信息
- 总耗时和 token 消耗

---

## 九、与 LawAutoPaper 的集成方式

JurisCoT 验收通过后，在 LawAutoPaper 中：

```python
# LawAutoPaper/src/agents/reasoning_agent.py

from juriscot import ReasoningEngine, PaperType, ChapterType

class 论证智能体:
    def __init__(self):
        self.engine = ReasoningEngine(...)

    def generate_chapter(self, chapter_spec, literature_chunks):
        # 1. 从 Chroma 检索相关文献块
        chunks = self.rag.retrieve(chapter_spec.topic, top_k=5)

        # 2. 调 JurisCoT 推理
        result = self.engine.reason(
            paper_type=chapter_spec.paper_type,
            chapter=chapter_spec.chapter_type,
            chapter_topic=chapter_spec.topic,
            legal_provisions=chapter_spec.provisions,
            literature_chunks=chunks,
            case_materials=chapter_spec.cases,
            previous_conclusion=self.previous_conclusion,
        )

        # 3. 返回润色后的段落
        return result.final_text
```

对 LawAutoPaper 来说，JurisCoT 就是一个**黑盒函数库**——传入结构化输入，拿到结构化输出。内部 CoT 细节完全透明但不需要关心。

---

## 十、验收通过定义

JurisCoT 满足以下全部条件即视为可嵌入 LawAutoPaper：

- [ ] 全部 4 项验收测试通过（格式/推理/引用/一致性）
- [ ] 3 个不同部门法的测试数据各跑 3 次，结果稳定
- [ ] CLI 可以直接运行：`python -m src.cli --input tests/test_data/criminal_case.json`
- [ ] 可 `pip install -e .` 安装为 Python 包
- [ ] `tests/test_pipeline.py` 全部通过

---

## 十一、从 LawAutoPaper 复用

以下文件直接复用，不重新设计：

| 源文件 | 目标 |
|--------|------|
| `LawAutoPaper/prompts/base/system_prompt.md` | `JurisCoT/prompts/base/` |
| `LawAutoPaper/prompts/base/legal_rules.md` | `JurisCoT/prompts/base/` |
| `LawAutoPaper/prompts/cot/step1_problem.md` 等 8 个 | `JurisCoT/prompts/cot/` |
| `LawAutoPaper/prompts/templates/theory_type.yaml` | `JurisCoT/prompts/templates/` |
| `LawAutoPaper/prompts/templates/case_type.yaml` | `JurisCoT/prompts/templates/` |
| `LawAutoPaper/src/models/schemas.py`（CoT 相关 Schema） | `JurisCoT/src/schemas.py` |

这些文件在 LawAutoPaper 项目中已写好骨架，移过来后需要**完善填充**（加完整示例、加约束条件）。
