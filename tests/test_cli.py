"""CLI 行为测试：list 输出、show 已知/未知项、run 的无 Key 报错与未实现提示。

全部通过 src.cli.main(argv) 进程内调用，不依赖已安装的控制台脚本。
"""

import pytest

from src import cli

ALL_CODES = ["theory", "case", "comparative", "empirical", "legislative", "review"]
ALL_NAMES = ["理论辨析型", "案例分析型", "制度比较型", "实证研究型", "立法建议型", "文献综述型"]


@pytest.fixture(autouse=True)
def _isolated_env(monkeypatch):
    """隔离本机环境与仓库内可能存在的 .env：把两个 Key 变量置空（而非删除）。

    load_dotenv 不覆盖已存在的环境变量，置空可保证即使仓库根有真实 .env
    也不会注入 Key，影响「无 Key」路径的断言。
    """
    monkeypatch.setenv("JURISCOT_API_KEY", "")
    monkeypatch.setenv("OPENAI_API_KEY", "")


def _run(argv, capsys):
    code = cli.main(argv)
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_list_lists_all_types(capsys):
    code, out, _ = _run(["list"], capsys)
    assert code == 0
    for token in ALL_CODES + ALL_NAMES:
        assert token in out
    assert "step5_polish" in out  # 链路内容可见


def test_show_by_english_code(capsys):
    code, out, _ = _run(["show", "theory"], capsys)
    assert code == 0
    assert "理论辨析型" in out
    assert "step1_problem" in out and "step4c_position" in out
    assert "适用章节" in out
    assert "跳过 Step 3" in out  # 说明字段原文


def test_show_by_chinese_alias(capsys):
    code, out, _ = _run(["show", "案例分析"], capsys)
    assert code == 0
    assert "案例分析型" in out
    assert "step3_case" in out and "step4d_application" in out


def test_show_unknown_type_fails_with_exit_2(capsys):
    code, _, err = _run(["show", "不存在的类型"], capsys)
    assert code == 2
    assert "未知论文类型" in err


def test_list_reports_missing_template_dir(monkeypatch, capsys):
    """模板目录缺失时报错退出，而非静默输出空列表。"""
    monkeypatch.setattr(cli, "TEMPLATE_DIR", cli.REPO_ROOT / "prompts" / "__no_such_dir__")
    code, _, err = _run(["list"], capsys)
    assert code == 2
    assert "未找到模板目录" in err


def test_run_without_api_key_fails_clearly(capsys):
    code, _, err = _run(["run", "--type", "theory", "--topic", "测试主题"], capsys)
    assert code == 2
    assert "未提供 API Key" in err
    assert "JURISCOT_API_KEY" in err  # 告知如何补齐


def test_run_with_api_key_reports_unimplemented(capsys):
    """有 Key 也不假装成功：如实提示推理链路尚未实现。"""
    code, _, err = _run(
        ["run", "--type", "theory", "--topic", "测试主题", "--api-key", "sk-dummy"],
        capsys,
    )
    assert code == 3
    assert "尚未实现" in err


def test_run_with_unknown_type_fails_before_key_check(capsys):
    code, _, err = _run(["run", "--type", "bogus", "--topic", "t"], capsys)
    assert code == 2
    assert "未知论文类型" in err


def test_run_with_blank_topic_fails(capsys):
    code, _, err = _run(["run", "--type", "theory", "--topic", "   "], capsys)
    assert code == 2
    assert "--topic" in err


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--version"])
    assert exc_info.value.code == 0
    assert "juriscot" in capsys.readouterr().out
