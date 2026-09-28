"""模板资产完整性测试：全部模板可解析、字段齐全、链路步骤有对应提示词文件。"""

from pathlib import Path

import yaml

from src.types import PaperType

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = REPO_ROOT / "prompts" / "templates"
COT_DIR = REPO_ROOT / "prompts" / "cot"
BASE_DIR = REPO_ROOT / "prompts" / "base"


def _load_template(paper_type: PaperType) -> dict:
    path = TEMPLATE_DIR / f"{paper_type.value}_type.yaml"
    assert path.is_file(), f"缺少模板文件：{path.name}"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_all_six_paper_types_have_parseable_template():
    for pt in PaperType:
        data = _load_template(pt)
        assert isinstance(data, dict), f"{pt.value}_type.yaml 不是有效的 YAML 映射"


def test_every_template_has_complete_fields():
    for pt in PaperType:
        data = _load_template(pt)
        chapters = data.get("适用章节")
        assert isinstance(chapters, list) and chapters, f"{pt.value} 缺少适用章节"
        assert all(isinstance(c, str) and c.strip() for c in chapters)

        chain = data.get("CoT 链路")
        assert isinstance(chain, list) and chain, f"{pt.value} 缺少 CoT 链路"
        assert all(isinstance(s, str) and s.strip() for s in chain)
        assert len(set(chain)) == len(chain), f"{pt.value} 链路存在重复步骤"

        assert isinstance(data.get("说明"), str) and data["说明"].strip(), f"{pt.value} 缺少说明"


def test_every_chain_step_has_prompt_file():
    for pt in PaperType:
        for step in _load_template(pt)["CoT 链路"]:
            prompt_file = COT_DIR / f"{step}.md"
            assert prompt_file.is_file(), f"{pt.value} 链路步骤 {step} 缺少 prompts/cot/{step}.md"
            assert prompt_file.read_text(encoding="utf-8").strip(), f"{step}.md 内容为空"


def test_base_prompts_exist_and_nonempty():
    for name in ("system_prompt.md", "legal_rules.md"):
        path = BASE_DIR / name
        assert path.is_file(), f"缺少基础提示词：{name}"
        assert path.read_text(encoding="utf-8").startswith("#"), f"{name} 内容异常"
