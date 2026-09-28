# JurisCoT — 法学思维链推理引擎

> LawAutoPaper 的前置独立子项目。一个可独立运行、独立测试的法学 Chain-of-Thought 推理库。

**TL;DR (English)** — JurisCoT is a standalone library of legal Chain-of-Thought prompt
templates for Chinese legal academic writing, serving as the core reasoning component of
LawAutoPaper. It ships six paper-type CoT templates (theory / case analysis / comparative /
empirical / legislative / literature review) with a small CLI (`juriscot list|show|run`) to
inspect them. v0.1 covers template asset management only — the model inference pipeline is
not implemented yet (see TASKS.md), and `run` reports that honestly instead of faking a call.
MIT licensed.

## 概述

JurisCoT 接收法律问题及相关文献/法条/案例/数据/域外法，通过结构化的 CoT 模板生成推理链和学术正文段落。

- **输入**：法律问题 + 参考文献/法条/案例/数据/域外法
- **输出**：结构化推理链 + 学术正文段落
- **验收后**：以 Python 包形式嵌入 LawAutoPaper

**当前状态（v0.1）**：

- 已实现：6 类论文 CoT 模板与提示词资产、模板管理 CLI（`list` / `show`）、测试套件
- 未实现：模型推理链路（prompt_loader / pipeline / engine，见 TASKS.md 第 29-37 天排期）。
  `run` 是模型调用的入口占位——无 API Key 时明确报错；有 Key 时也如实提示功能未实现，不会假装成功。

## 支持的论文类型

| # | 论文类型 | 典型场景 | CoT 步骤 |
|---|---------|---------|---------|
| 1 | **理论辨析型** | 课程论文、法理论文 | 6 步 |
| 2 | **案例分析型** | 判决评析论文 | 8 步 |
| 3 | **制度比较型** | 比较法论文 | 6 步 |
| 4 | **实证研究型** | 数据驱动论文 | 6 步 |
| 5 | **立法建议型** | 修法建议论文 | 6 步 |
| 6 | **文献综述型** | 综述论文 | 4 步 |

## 快速开始

需要 Python >= 3.10。

```bash
# 1. 安装（含 juriscot 控制台脚本）
pip install -e .

# 2. 列出全部论文类型及其 CoT 链路
juriscot list

# 3. 查看某类型的模板详情（英文代码或中文名均可）
juriscot show theory
juriscot show 案例分析

# 4.（可选）模型调用入口 —— v0.1 尚未接入模型，行为如下：
#    - 未提供 API Key：明确报错退出（退出码 2）
#    - 提供 API Key：如实提示推理链路尚未实现（退出码 3）
cp .env.example .env      # 按需填入 JURISCOT_API_KEY（.env 已被 gitignore）
juriscot run --type theory --topic "论数据产权的法律属性"
```

退出码约定：`0` 成功；`2` 用法/配置错误（参数非法、缺 API Key 等）；`3` 功能未实现。

不安装直接跑也可以：在仓库根目录执行 `py -3.13 -m src.cli list`（任意 Python >= 3.10 均可）。

## 运行测试

```bash
py -3.13 -m pytest tests -q
# 或任意 Python >= 3.10：python -m pytest tests -q
```

覆盖：模板加载完整性（6 类模板可解析、字段齐全、链路每步有对应提示词文件）与 CLI 行为（list / show / run 的成功与报错路径）。

## 项目结构

```
JurisCoT/
├── src/                  # 核心源码
│   ├── __init__.py
│   ├── schemas.py       # 数据模式定义
│   ├── types.py         # 类型定义
│   └── cli.py           # 命令行入口（list / show / run）
├── prompts/             # CoT 提示词资产
│   ├── base/            # 角色设定与法学论证规则
│   ├── cot/             # Step 1-5 各步提示词（含 4c 变体）
│   └── templates/       # 6 类论文类型的链路模板（YAML）
├── tests/               # 模板完整性 + CLI 行为测试
├── .env.example         # 环境变量示例（占位符，不含真实值）
├── DESIGN.md            # 完整设计文档
├── TASKS.md             # 工程任务单
├── LICENSE              # MIT
└── pyproject.toml       # 项目配置
```

## 开发计划

详见 [TASKS.md](./TASKS.md) — 40 天工程任务单，每天 1 小时，一天一项。

## License

[MIT](./LICENSE)
