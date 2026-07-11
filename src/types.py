"""类型定义 —— 枚举和常量。"""

from enum import Enum


class PaperType(str, Enum):
    """论文类型 → 决定使用哪套 CoT 模板和 step4c 输出变体"""
    THEORY = "theory"                 # 理论辨析型
    CASE_ANALYSIS = "case"            # 案例分析型
    COMPARATIVE = "comparative"       # 制度比较型
    EMPIRICAL = "empirical"           # 实证研究型
    LEGISLATIVE = "legislative"       # 立法建议型
    LITERATURE_REVIEW = "review"      # 文献综述型


class ChapterType(str, Enum):
    """章节类型 → 决定 CoT 侧重点和输入素材"""
    INTRODUCTION = "introduction"
    CONCEPT_DEFINITION = "concept_definition"      # 概念界定（理论型）
    THEORETICAL_ANALYSIS = "theoretical_analysis"
    CASE_OVERVIEW = "case_overview"                # 案情概述（案例型）
    CASE_ANALYSIS = "case_analysis"
    DOMESTIC_STATUS = "domestic_status"            # 中国制度现状（比较型）
    FOREIGN_EXAMINATION = "foreign_examination"    # 域外制度考察（比较型）
    COMPARATIVE_ANALYSIS = "comparative_analysis"  # 比较分析（比较型）
    RESEARCH_DESIGN = "research_design"            # 研究设计（实证型）
    DATA_ANALYSIS = "data_analysis"                # 数据分析（实证型）
    FINDINGS = "findings"                          # 研究发现（实证型）
    CURRENT_LAW_REVIEW = "current_law_review"      # 现行法评析（立法型）
    AMENDMENT_NECESSITY = "amendment_necessity"    # 修法必要性（立法型）
    DRAFT_ARTICLES = "draft_articles"              # 条文建议（立法型）
    DOMESTIC_REVIEW = "domestic_review"            # 国内研究现状（综述型）
    FOREIGN_REVIEW = "foreign_review"              # 国外研究现状（综述型）
    REVIEW_COMMENTARY = "review_commentary"        # 研究述评（综述型）
    PROBLEM_SORTING = "problem_sorting"
    SUGGESTIONS = "suggestions"
    CONCLUSION = "conclusion"


class StepStatus(str, Enum):
    """单个 CoT 步骤的执行状态"""
    SUCCESS = "success"
    PARSE_FAILED = "parse_failed"
    VALIDATION_FAILED = "validation_failed"
    API_ERROR = "api_error"
    RETRY = "retry"


class Step4cVariant(str, Enum):
    """Step 4c 的输出变体 —— 不同论文类型的"本文立场"形式不同"""
    DOCTRINE_POSITION = "doctrine_position"        # 支持某种学说（理论型/案例型/实证型）
    COMPARATIVE_INSIGHT = "comparative_insight"    # 借鉴域外经验（比较型）
    LEGISLATIVE_PROPOSAL = "legislative_proposal"  # 条文修改建议（立法建议型）
    RESEARCH_GAP = "research_gap"                  # 研究空白指出（综述型）


# 论文类型 → 4c 变体的映射
PAPER_TYPE_TO_4C = {
    PaperType.THEORY: Step4cVariant.DOCTRINE_POSITION,
    PaperType.CASE_ANALYSIS: Step4cVariant.DOCTRINE_POSITION,
    PaperType.COMPARATIVE: Step4cVariant.COMPARATIVE_INSIGHT,
    PaperType.EMPIRICAL: Step4cVariant.DOCTRINE_POSITION,
    PaperType.LEGISLATIVE: Step4cVariant.LEGISLATIVE_PROPOSAL,
    PaperType.LITERATURE_REVIEW: Step4cVariant.RESEARCH_GAP,
}
