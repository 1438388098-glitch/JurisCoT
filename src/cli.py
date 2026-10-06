"""命令行入口 —— juriscot。

提供两类能力：
1. 模板资产管理：``list`` / ``show`` 列出并展示 6 类论文的 CoT 模板（纯本地，无需任何密钥）。
2. 模型调用入口：``run``。推理链路（prompt_loader / pipeline / engine，见 docs/roadmap-internal.md
   第 29-37 天）尚未实现——未提供 API Key 时明确报错；提供了 Key 也会如实提示
   功能未实现，绝不假装调用成功。

退出码：0 成功；2 用法/配置错误（参数非法、缺 API Key）；3 功能未实现。
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

from src import __version__
from src.types import PaperType

# 论文类型参数解析：英文代码 / 中文名均可
PAPER_TYPE_ALIASES: dict[str, PaperType] = {pt.value: pt for pt in PaperType}
PAPER_TYPE_ALIASES.update(
    {
        "理论辨析": PaperType.THEORY,
        "案例分析": PaperType.CASE_ANALYSIS,
        "制度比较": PaperType.COMPARATIVE,
        "实证研究": PaperType.EMPIRICAL,
        "立法建议": PaperType.LEGISLATIVE,
        "文献综述": PaperType.LITERATURE_REVIEW,
    }
)

TYPE_DISPLAY_NAMES: dict[PaperType, str] = {
    PaperType.THEORY: "理论辨析型",
    PaperType.CASE_ANALYSIS: "案例分析型",
    PaperType.COMPARATIVE: "制度比较型",
    PaperType.EMPIRICAL: "实证研究型",
    PaperType.LEGISLATIVE: "立法建议型",
    PaperType.LITERATURE_REVIEW: "文献综述型",
}

# 包根目录（仓库根）：prompts 资产随仓库分发，编辑安装 / 源码运行时都在此
REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"
TEMPLATE_DIR = PROMPTS_DIR / "templates"
COT_DIR = PROMPTS_DIR / "cot"

# 模板必备字段（与 prompts/templates/*.yaml 现有结构一致）
REQUIRED_TEMPLATE_FIELDS = ("适用章节", "CoT 链路", "说明")


class UsageError(Exception):
    """用法 / 配置错误，对应退出码 2。"""


# ────────────────────────────────────────────────────────────────
# 模板加载
# ────────────────────────────────────────────────────────────────

def load_templates() -> dict[PaperType, dict]:
    """加载并校验全部论文类型模板。

    任一类型模板缺失、无法解析或缺必备字段时抛 UsageError（宁可报错，不带病输出）。
    """
    if not TEMPLATE_DIR.is_dir():
        raise UsageError(
            f"未找到模板目录：{TEMPLATE_DIR}\n"
            "请在仓库根目录运行（pip install -e . 安装后仍需在仓库内执行，prompts 随仓库分发）。"
        )
    templates: dict[PaperType, dict] = {}
    for pt in PaperType:
        path = TEMPLATE_DIR / f"{pt.value}_type.yaml"
        if not path.is_file():
            raise UsageError(f"缺少论文类型模板：{path.name}")
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise UsageError(f"模板不是有效的 YAML 映射：{path.name}")
        missing = [field for field in REQUIRED_TEMPLATE_FIELDS if field not in data]
        if missing:
            raise UsageError(f"模板缺少必备字段 {missing}：{path.name}")
        templates[pt] = data
    return templates


def resolve_paper_type(name: str) -> PaperType:
    """把用户输入的论文类型（英文代码或中文名）解析为 PaperType。"""
    pt = PAPER_TYPE_ALIASES.get(name)
    if pt is None:
        known = "、".join(sorted(PAPER_TYPE_ALIASES))
        raise UsageError(f"未知论文类型：{name}（可用：{known}）")
    return pt


# ────────────────────────────────────────────────────────────────
# 子命令
# ────────────────────────────────────────────────────────────────

def cmd_list() -> int:
    """列出全部论文类型及其 CoT 链路。"""
    templates = load_templates()
    print(f"JurisCoT 共 {len(templates)} 类论文 CoT 模板：\n")
    for pt, data in templates.items():
        chain: list[str] = data["CoT 链路"]
        print(
            f"  {pt.value:<12} {TYPE_DISPLAY_NAMES[pt]}"
            f"  （{len(data['适用章节'])} 类章节，{len(chain)} 步）"
        )
        print(f"  {'':<12} 链路：{' -> '.join(chain)}")
    print("\n查看详情：juriscot show <类型>（如 theory 或 理论辨析）")
    return 0


def cmd_show(name: str) -> int:
    """展示某论文类型的模板详情，并核对链路各步是否有对应提示词文件。"""
    pt = resolve_paper_type(name)
    data = load_templates()[pt]
    print(f"# {TYPE_DISPLAY_NAMES[pt]}（{pt.value}）  模板：prompts/templates/{pt.value}_type.yaml\n")
    print("适用章节：")
    for chapter in data["适用章节"]:
        print(f"  - {chapter}")
    print("\nCoT 链路：")
    for step in data["CoT 链路"]:
        prompt_file = COT_DIR / f"{step}.md"
        status = "ok" if prompt_file.is_file() else "缺少提示词文件！"
        print(f"  - {step}  [{status}]")
    print(f"\n说明：\n{str(data['说明']).strip()}")
    return 0


def _resolve_api_key(api_key: str | None) -> str | None:
    """--api-key 参数优先，其次环境变量 JURISCOT_API_KEY / OPENAI_API_KEY。"""
    if api_key:
        return api_key
    return os.getenv("JURISCOT_API_KEY") or os.getenv("OPENAI_API_KEY") or None


def cmd_run(args: argparse.Namespace) -> int:
    """跑一个章节的 CoT 推理。

    诚实边界：v0.1 的推理链路尚未实现。缺 Key 明确报错；有 Key 也如实提示未实现，
    不发起任何「假装成功」的调用。
    """
    resolve_paper_type(args.type)
    if not (args.topic or "").strip():
        raise UsageError('run 需要提供章节主题：--topic "..."')
    if not _resolve_api_key(args.api_key):
        raise UsageError(
            "未提供 API Key：run 需要调用模型服务。\n"
            "请用 --api-key 传入，或在环境变量 / .env 中设置 JURISCOT_API_KEY"
            "（或 OPENAI_API_KEY），参考 .env.example。"
        )
    raise NotImplementedError(
        "模型推理链路尚未实现：v0.1 仅提供模板管理（list / show）。"
        "引擎实现排期见 docs/roadmap-internal.md 第 29-37 天。"
    )


# ────────────────────────────────────────────────────────────────
# 参数解析与入口
# ────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="juriscot",
        description="法学思维链推理引擎 —— CoT 模板管理与推理入口",
    )
    parser.add_argument("--version", action="version", version=f"juriscot {__version__}")
    sub = parser.add_subparsers(dest="command", required=True, metavar="{list,show,run}")

    sub.add_parser("list", help="列出全部论文类型及其 CoT 模板")

    p_show = sub.add_parser("show", help="展示某论文类型的模板详情")
    p_show.add_argument("name", help="论文类型：英文代码或中文名（如 theory / 理论辨析）")

    p_run = sub.add_parser("run", help="跑一个章节的 CoT 推理（需要 API Key）")
    p_run.add_argument("--type", required=True, help="论文类型：英文代码或中文名")
    p_run.add_argument("--topic", required=True, help="章节主题")
    p_run.add_argument(
        "--api-key",
        default=None,
        help="模型服务 API Key（缺省读环境变量 JURISCOT_API_KEY / OPENAI_API_KEY）",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    load_dotenv(REPO_ROOT / ".env")  # .env 存在时注入环境变量；不覆盖已有值
    args = build_parser().parse_args(argv)
    try:
        if args.command == "list":
            return cmd_list()
        if args.command == "show":
            return cmd_show(args.name)
        if args.command == "run":
            return cmd_run(args)
    except UsageError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    except NotImplementedError as exc:
        print(f"未实现：{exc}", file=sys.stderr)
        return 3
    return 2


if __name__ == "__main__":
    sys.exit(main())
