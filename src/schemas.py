"""
Pydantic 模型定义 —— JurisCoT 推理引擎所有结构化 Schema。
所有 CoT 步骤的输出必须符合对应 Schema，格式不符则自动重试。
"""

from pydantic import BaseModel, Field
from typing import List, Optional


# ═══════════════════════════════════════════════════════════════
# 引擎输入
# ═══════════════════════════════════════════════════════════════

class 法条输入(BaseModel):
    """法条注入 —— LawAutoPaper 从本地法条库检索后传入。
    模型只能引用此列表中的法条，不得自行编造。"""
    条文: str            # "《中华人民共和国刑法》第20条"
    原文: str            # 完整原文
    来源: str = "本地法条库"   # 数据来源标注
    最后修订: Optional[str] = None  # "2020-12-26"

class 文献块输入(BaseModel):
    chunk_id: str
    text: str
    source: str

class 案例输入(BaseModel):
    案件名称: str
    案号: str
    关键情节: str

class 域外法输入(BaseModel):
    """域外法律条文输入 —— 制度比较型论文需要"""
    国家地区: str           # "日本" / "德国" / "台湾地区"
    法条引用: str           # "日本刑法第36条"
    原文: str               # 完整原文（可为翻译文本）
    来源: Optional[str] = None

class 数据发现输入(BaseModel):
    """实证数据输入 —— 实证研究型论文需要"""
    指标名称: str
    数值描述: str
    数据来源: str
    分析维度: Optional[str] = None

class 推理输入(BaseModel):
    """一次推理的完整输入"""
    paper_type: str  # theory / case / comparative / empirical / legislative / review
    chapter: str
    chapter_topic: str
    legal_provisions: List[法条输入] = []
    literature_chunks: List[文献块输入] = []
    case_materials: Optional[List[案例输入]] = None       # 案例分析型
    foreign_laws: Optional[List[域外法输入]] = None        # 制度比较型
    data_findings: Optional[List[数据发现输入]] = None      # 实证研究型
    previous_conclusion: Optional[str] = None


# ═══════════════════════════════════════════════════════════════
# CoT Step 1-5 输出
# ═══════════════════════════════════════════════════════════════

class Step1输出(BaseModel):
    章节: str
    核心问题: str
    涉及部门法: str
    涉及具体制度: str
    争议程度: str
    问题拆解: List[str]

class 要件条目(BaseModel):
    要件: str
    说明: str

class Step2输出(BaseModel):
    适用法条: str
    法条原文: str
    构成要件: List[要件条目]
    争议要件: str
    解释路径: str
    理由: str

class 要件比对条目(BaseModel):
    要件: str
    满足: bool
    说明: str

class Step3输出(BaseModel):
    案件名称: str
    案号: str
    关键情节: str
    要件比对: List[要件比对条目]
    争议焦点: str
    学说参考: str

class 学说条目(BaseModel):
    学说: str
    核心主张: str
    代表学者: List[str]
    来源文献: List[str]

class Step4a输出(BaseModel):
    问题: str
    学说清单: List[学说条目]

class 学说评析条目(BaseModel):
    学说: str
    理论依据: str
    解释力: str
    局限: str
    来源文献: List[str]

class Step4b输出(BaseModel):
    评析: List[学说评析条目]
    学说关系: str

class 立场条目(BaseModel):
    """学说立场型 —— 理论辨析/案例分析/实证研究型"""
    支持的学说: str
    理由: List[str]
    理论修正: Optional[str] = None
    仍待解决的问题: Optional[str] = None

class 借鉴建议条目(BaseModel):
    """域外借鉴型 —— 制度比较型"""
    域外制度概述: str
    可借鉴之处: List[str]
    需警惕之处: List[str]      # 域外制度在本土可能不适用的方面
    建议方案: str
    仍待研究的问题: Optional[str] = None

class 立法建议条目(BaseModel):
    """条文建议型 —— 立法建议型"""
    现行条文不足: str
    修改建议: str               # 具体修改方案
    建议条文草案: str            # 修改后的完整条文
    立法理由: List[str]
    域外参考: Optional[str] = None

class 研究空白条目(BaseModel):
    """研究空白型 —— 文献综述型"""
    已有研究成果总结: str
    当前研究不足: List[str]
    值得深入的方向: List[str]
    方法论建议: Optional[str] = None

class Step4c输出(BaseModel):
    """本文立场 —— 根据论文类型使用不同子结构"""
    本文立场: 立场条目 | 借鉴建议条目 | 立法建议条目 | 研究空白条目

class Step4d输出(BaseModel):
    评价标准: str
    案件评价: dict
    结论: str
    理论印证: str

class Step5输出(BaseModel):
    内容: str
    引用列表: List[str]


# ═══════════════════════════════════════════════════════════════
# 引擎输出
# ═══════════════════════════════════════════════════════════════

class StepResult(BaseModel):
    """单个步骤的执行结果"""
    step_name: str
    status: str  # success / parse_failed / validation_failed / api_error
    raw_output: str
    parsed_output: Optional[dict] = None
    error: Optional[str] = None
    retry_count: int = 0
    elapsed_ms: int = 0

class 推理输出(BaseModel):
    """一次完整推理的输出"""
    input: 推理输入
    steps: dict  # {"step1": StepResult, "step2": StepResult, ...}
    final_text: Optional[str] = None
    citations: List[str] = []
    total_elapsed_ms: int = 0
    total_tokens: int = 0
