# JurisCoT — 工程任务单

> ⏱ **每天 1 小时，一天一项**
> 📅 **总工期：40 天（约 8 周）**
> 🎯 **验收标准：4 项全部通过（格式/推理/引用/一致性）**
> 📚 **法条库**：本地法条库（263 份文件，路径不入库）

---

## 使用方式

```
1. 打开 TASKS.md
2. 看今天是第几天
3. 做完把 [ ] 改成 [x]
4. 关电脑，明天再来
```

---

## 第 1–5 天：基础环境

| 天数 | 任务 | 完成 |
|------|------|------|
| 第 1 天 | 创建虚拟环境，`pip install openai pydantic pyyaml python-dotenv pytest` | [ ] |
| 第 2 天 | 复制 LawAutoPaper 的 prompt 文件到 JurisCoT | [ ] |
| 第 3 天 | 写 `pyproject.toml`（包名 juriscot，入口 cli） | [ ] |
| 第 4 天 | 写 `src/__init__.py` + `src/types.py`（PaperType / ChapterType 枚举） | [ ] |
| 第 5 天 | 写 `src/schemas.py`：从 LawAutoPaper 的 schemas.py 提取 CoT 相关的全部 Schema | [ ] |

---

## 第 6–28 天：Prompt 完善 + 逐步测试

| 天数 | 任务 | 完成 |
|------|------|------|
| 第 6 天 | 完善 `prompts/base/system_prompt.md`：补充法学学术写作角色设定 | [ ] |
| 第 7 天 | 完善 `prompts/base/legal_rules.md`：补充完整的三段论规则和禁止事项 | [ ] |
| 第 8 天 | 完善 `prompts/cot/step1_problem.md`：加完整示例 | [ ] |
| 第 9 天 | 测试 step1：3 个不同部门法问题各跑一次，看输出格式 | [ ] |
| 第 10 天 | 修正 step1，直到 3 个测试全部稳定 | [ ] |
| 第 11 天 | 完善 `prompts/cot/step2_premise.md`：验证法条约束逻辑（只引用注入列表，禁止编造） | [ ] |
| 第 12 天 | 测试 step2：基于 step1 输出跑，检查构成要件拆分合理性 | [ ] |
| 第 13 天 | 修正 step2 | [ ] |
| 第 14 天 | 完善 `prompts/cot/step3_case.md`：加完整案件代入示例 | [ ] |
| 第 15 天 | 测试 step3：基于 step2 输出跑，检查要件比对完整性 | [ ] |
| 第 16 天 | 完善 `prompts/cot/step4a_doctrines.md`：加多学说示例 + 来源标注要求 | [ ] |
| 第 17 天 | 测试 step4a：给已知文献内容，看学说梳理是否完整不遗漏 | [ ] |
| 第 18 天 | 完善 `prompts/cot/step4b_analysis.md`：加"理据+解释力+局限"的示例 | [ ] |
| 第 19 天 | 测试 step4b + 修正 | [ ] |
| 第 20 天 | 完善 `prompts/cot/step4c_position.md`（学说立场型）| [ ] |
| 第 21 天 | 测试 step4c position | [ ] |
| 第 22 天 | 写 `prompts/cot/step4c_comparative.md`（比较型）+ 测试 | [ ] |
| 第 23 天 | 写 `prompts/cot/step4c_legislative.md`（立法建议型）+ 测试 | [ ] |
| 第 24 天 | 写 `prompts/cot/step4c_review.md`（综述型）+ 测试 | [ ] |
| 第 25 天 | 完善 `prompts/cot/step4d_application.md` + `step5_polish.md` | [ ] |
| 第 26 天 | 联调 step4d+step5，修正 | [ ] |
| 第 27 天 | Review 6 个 YAML 模板，确保步骤列表与最新 prompt 一致 | [ ] |
| 第 28 天 | 准备 3 套测试数据（理论型/案例型/比较型各一，JSON，含 mock 文献块） | [ ] |

---

## 第 29–37 天：引擎编码

| 天数 | 任务 | 完成 |
|------|------|------|
| 第 29 天 | 写 `src/prompt_loader.py`：加载 prompt 文件 + 变量替换 | [ ] |
| 第 30 天 | **写 `src/literature_formatter.py`**：文献-提示词映射层（按 6 种 Step 分配文献） | [ ] |
| 第 31 天 | 写 `src/pipeline.py`：单步执行 + JSON 解析容错 | [ ] |
| 第 32 天 | 写 `src/pipeline.py`：链式调用 + 集成 LiteratureFormatter + 4c 变体路由 | [ ] |
| 第 33 天 | 写 `src/engine.py`：ReasoningEngine（PaperType→模板+4c 变体+跑链路） | [ ] |
| 第 34 天 | 写 `src/cli.py`：`python -m src.cli --input test.json` | [ ] |
| 第 35 天 | 端到端（理论型）：刑法 mock 数据 | [ ] |
| 第 36 天 | 端到端（案例型+比较型）：民法 + 域外法 mock 数据 | [ ] |
| 第 37 天 | 端到端（立法型+实证型+综述型）| [ ] |

---

## 第 38–40 天：验收测试

| 天数 | 任务 | 完成 |
|------|------|------|
| 第 38 天 | **验收 1（格式）**：6 种模板各跑 1 次，JSON 解析成功率 ≥ 95% | [ ] |
| 第 39 天 | **验收 2+3（推理+引用）**：理论/案例/比较各 1 次，检查推理和引用 | [ ] |
| 第 40 天 | **验收 4（一致性）**：同输入连跑 3 次，检查结果稳定性 | [ ] |

---

## 验收通过后的标记

```
[ ] 验收 1: 格式符合性 — 6 种模板 JSON 解析成功率 ≥ 95%
[ ] 验收 2: 推理完整性 — 学说 ≥ 2 个，评析三维度齐全，4c 变体输出正确
[ ] 验收 3: 引用可溯源 — 每个学说标注了来源 chunk_id
[ ] 验收 4: 跨工具一致性 — 3 次跑同输入，4c 立场一致
```

---

## 当前进度

```
第 1-5 天   [..........]   基础环境
第 6-28 天  [..........]   Prompt 完善 + 测试（含 6 种类型）
第 29-37 天 [..........]   引擎编码 + 文献映射层
第 38-40 天 [..........]   验收测试
```
