# 作战手册 —— 这份教程究竟是怎么做出来的

> **读者**：下一个 gstack 教程（No. 3）的作者。
> **这是什么**：`gstack-tutorial-2` 的完整作业流程，趁记忆还热，按**真实发生顺序**写下来。
> **这不是什么**：不是待填模板。内容会变，**顺序与不变式**不变。

| | |
|---|---|
| 仓库 | <https://github.com/mikelix/gstack-tutorial-2> |
| 提交 | 3 次（`db12056` 骨架 → `5aa3de8` 发布 → `61f5230` 图示 + 模拟章节） |
| 受版本控制文件 | 45 |
| 教程正文 | 英文 1195 行 / 中文 1135 行 · 各 61 个 `##` 小节 · 双语一致性由 CI 强制 |
| 交付物 | `TUTORIAL.md`+`.zh.md`（唯一事实来源）→ `.docx` ×2 → `.pptx` ×2（各 39 页） |
| Release | `v1.0`、`v1.0.1` |
| CI | `repo self-check` —— 29 个必需文件、3 个版本锁、循环性守卫、导出器确定性 |

---

## 0. 唯一不变式

```
                ┌─────────────────────────────┐
   你只改这里 ─► │  TUTORIAL.md / .zh.md       │  ◄── 唯一事实来源
                └──────────┬──────────────────┘
                           │  _build/
          ┌────────────────┼──────────────────┐
          ▼                ▼                  ▼
   md2docx.py        build_en.py         GitHub 直接渲染
   (.docx)           build_zh.py           Markdown
                     (.pptx)
```

**永远不要手工改 `dist/` 里的任何东西。** 那里的每个二进制都是再生的：

```bash
PY=<装了 docx 与 pptx 的 python>
$PY _build/md2docx.py TUTORIAL.md    dist/gstack-tutorial-2_EN.docx
$PY _build/md2docx.py TUTORIAL.zh.md dist/gstack-tutorial-2_ZH.docx
$PY _build/build_en.py      # -> dist/gstack-tutorial-2_EN.pptx
$PY _build/build_zh.py      # -> dist/gstack-tutorial-2_ZH.pptx
```

谁一旦"顺手在 docx 里改个错字"，下次重建就静默覆盖，一周后没人记得。要改就改 Markdown。

---

## 1. 十步流程（按序）

### S0 —— 先让 AI CEO 定框（`/plan-ceo-review`），一个字都别先写

第一份产物不是章节，是 `reviews/01-ceo-review.md`。它必须用**数字**而非形容词回答三问：

1. **什么在范围内、什么刻意不在** —— 缺口要**写出来**，不能沉默
   （"PEX/RCX 属 v1.1+ 路线图，未实现" 远胜于不提）。
2. **诚实覆盖率是多少** —— 例如 教学/科研 ~70–85 %，商业签核 ~15–25 %。
3. **什么情况下该砍掉** —— 掉队分析。

之所以放第一步：这是唯一能替你省掉后面九步的环节。

### S1 —— 让 AI PM 拆解（`/spec`）

W1–W9，带明写的关键路径。两条真正起作用的性质：

- 只能跑通整条链才能验收的任务，必须**嵌在**构建它的任务**内部**（W5 嵌在 W4 里），
  不能排在它后面。
- 凡**结论**依赖领域物理的条目，一律点名上抛（E1/E2/E3）给领域智能体，PM 不得自行裁定。

### S2 —— 在写正文之前锁死工具链版本

三个版本锁，CI 跨六份文档交叉核对：

| 工具 | 版本 | 提交 |
|---|---|---|
| Magic | 8.3.681 | `4432d7e` |
| Netgen | 1.5.323 | `bb8a610` |
| open_pdks | 1.0.572 | `54435919` |

必须在 S2 做，不能拖：自检第一次跑就抓到**两个 README 根本没写版本锁**。这一项一次就回本了。

### S3 —— 设计门链与退出码契约

```
门 5      Magic DRC
门 6      Magic 提取
门 7A     Microlane 结构级 LVS
门 7B-1R2 Netgen 层次化 LVS
```

`starter/scripts/run_all.sh` 的退出码：

| 码 | 含义 |
|---|---|
| `0` | PASS |
| `1` | FAIL |
| `2` | **VOID** —— 这次运行没有证明它声称的东西 |
| `3` | 环境坏了 |

**`VOID` 拥有独立退出码，是本仓库最重要的设计决定。** 没有它，"门过了"和"这次跑毫无意义"
都打印成功，教程就什么也没教到。

### S4 —— 做可运行骨架，并让它响亮地失败

`starter/` 不是附录，是证据。里面有**机械化的循环性守卫**：若 LVS 参考网表是由被测 GDS
派生出来的，直接 `exit 2`，根本不进 Netgen。`db_export.py` 改为从 live 版图数据库导出参考，
并写一个标记文件供守卫检查。

确定性也要机械证明（这就是 CI 里的那个 job）：

```bash
python3 scripts/db_export.py --db-in designs/layout.db.json --out /tmp/ref1.v --marker /tmp/m1
python3 scripts/db_export.py --db-in designs/layout.db.json --out /tmp/ref2.v --marker /tmp/m2
diff /tmp/ref1.v /tmp/ref2.v     # 必须为空
```

### S5 —— 写教程正文

验证有效的结构：**第 0 部分心智模型 → 第 1–2 部分安装 → 第 3–7 部分对应 gstack 五阶段
→ 第 8–12 部分纪律、排错、考核、下一步**。每部分以**检查点**（带复选框）收尾。
附录 A–D 放提示词库、评审模板、可打印的版本锁定卡、术语表。

两条规则：
- 每个 gstack 阶段精确对应一条评审命令，并且教程里展示**真实的评审文件**，不是玩具示例。
- 每个论断都要带来源、推导，或明写"这是假设，证伪方式如下"。

### S6 —— 给领域智能体留独立章节

第 9 部分之所以存在，是因为编排层发明不出物理。它承载约 20 阶段的模拟设计工作流
（`指标 → 物理 → 架构 → 优化 → 统计 → 版图 → 硅`），
并明确对照 **NOT** `画电路图 → SPICE → 版图`，以及 AI 的四个层级
（助手 → 优化器 → 版图助手 → 自主智能体）。

**给 No.3 的规则**：只要教程主题涉及某个专业领域，就必须有专属的一"部分"，
而且是与领域智能体**合写**的、逐字引用的，不是转述的。

### S7 —— 边做边写五份评审

`reviews/01-ceo-review` → `02-spec` → `03-eng-review` → `04-qa-report` → `05-ship`。
**当时就写**，只追加不改写，结论只有一个词（`PASS` / `REVISE` / `BLOCKED`）。
审计轨迹本身就是产品；事后补写等于伪造。

分量最重的一份是 `03-eng-review`：首次 LVS 打印 `Circuits match uniquely.`，
被判 **VOID 而非 PASS** —— 因为参考网表是由被测 GDS 派生的。这一页是全教程的智识核心。

### S8 —— 构建，然后机械校验

```bash
python .github/scripts/selfcheck.py     # 必需文件、版本锁、守卫、双语一致性
```

再查二进制是否越界（见 §4）。跑出画布外的页、撑出栏外的表格单元格，都是缺陷，
而且是机器可检的缺陷。

### S9 —— 发布

```
自检 → 重新打包 zip → git add/commit → push → 看 CI → 起草 release
```

Release 资产：两份 `.docx`、两份 `.pptx`、外加交付 zip。Release 说明必须重述
**已知缺口** —— v1.0.1 缺 VM 侧基准 SHA 与门 7B-2，这两条印在说明里，不藏。

---

## 2. 双钥匙权限契约（不可谈判）

```
   gstack 编排层                    两个领域智能体
   CEO · PM · 工程师 · QC · DevOps   GDS-Architect · 资深模拟 IC 架构师
   ── 流程权 ──                      ── 物理权 ──
                    └──────────► 门链 ◄──────────┘
                     （中立裁判：Magic / Netgen / PDK）
                        冲突时，物理优先
```

- 流程决定（排期、拆解、打包）→ gstack。
- 物理决定（DRC/LVS/提取、PDK 规则、确定性）→ 领域智能体。
- 冲突时：**物理优先**；两份陈述并列提交给人类签字。
- 让渡条款逐字写进每一条 gstack 提示词：

  > CONSULT REQUIRED. 在敲定任何涉及 DRC、LVS、提取、确定性或 PDK 规则的表述前，
  > 先将该论断交给领域智能体并逐字引用其答复。若它与你的结论冲突，以领域智能体为准 ——
  > 不要自行裁决，把两方陈述并列提交给人类。

完整版：[`docs/expertise_division.zh.md`](docs/expertise_division.zh.md)；
图示：[`docs/two-key-authority.svg`](docs/two-key-authority.svg)。

---

## 3. 可复用工具

### 3.1 `deck.py` —— 页面原语

| 函数 | 用途 |
|---|---|
| `slide_title` | 封面 / 带 kicker 与 meta 的分节页 |
| `slide_section` | 带编号的部分分隔页 |
| `slide_bullets` · `slide_checklist` | 列表、检查点 |
| `slide_steps` | 有序流程 |
| `slide_table` | 表头 + 行（单元格要短，见 §4 P9） |
| `slide_code` | 代码 / 命令块 |
| `slide_two_col` · `slide_layers` · `slide_flow` | 对照、层级、流水线 |
| `slide_quote` | 引语 + 出处 |
| `slide_image` | 嵌入位图 |

画布 13.333 × 7.5 英寸。配色：`NAVY NAVY2 ACCENT ACCENT2 WHITE LIGHT GREY DARK`。
页面在 `build_en.py` / `build_zh.py` 中以列表声明，两者必须逐页一致。

### 3.2 `md2docx.py` —— 支持的 Markdown 子集

H1–H6 标题、`-`/`*` 无序列表、有序列表、`- [ ]` 复选框、围栏代码块、GFM 表格、
`---` 分隔线、`> ` 引用、`![alt](path)` 图片、`Figure N — …` 图注。
超出这个子集会原样渲染出标记符号 —— **照着子集写**。

### 3.3 `svg2png.py` —— 图示流水线及其锋利边缘

`docs/two-key-authority.svg` 是事实来源：GitHub 和浏览器都能渲染，所以 Markdown 版直接链它。
但 `python-docx` 与 `python-pptx` **无法嵌 SVG**，需要位图孪生。`svglib` + `reportlab`
是 obvious 路线，且在这台机器上不通（`renderPM` 无光栅后端），所以改用 matplotlib
按**相同坐标、颜色、文字**重绘。

> **后果**：改了 SVG 就必须手改 `svg2png.py` 里的 `LAYOUT`，二者没有联动。
> 这是整条构建链最脆弱的关节 —— 别"顺手优化"图示而不重跑渲染并肉眼看一下 PNG。

### 3.4 `.github/scripts/selfcheck.py`

必需文件（29 个）、跨文档版本锁一致性、循环性守卫是否存在、中英 H1 数一致、
中英图示引用一致、导出器确定性 diff。每新增一份交付物就扩展它 ——
一次运行能抓到一个真实缺陷的检查，比一页散文值钱。

---

## 4. 踩坑台账

每一条都实打实花了时间，按代价大致排序。

| # | 现象 | 原因 | 修法 |
|---|---|---|---|
| P1 | 命令执行中 `.git` 目录凭空消失 | `git rebase --root --exec …` 报 `could not mark as interactive` | **本环境绝不用 `git rebase`。** 重建仓库或用 `--amend`。工作区文件未受损。 |
| P2 | `git push` → `CONNECT tunnel failed, response 502` | 沙箱导出 `http_proxy`/`https_proxy`；`curl` 与 `gh api` 能过，流式 POST 不行 | 只对 push 清代理：`http_proxy= https_proxy= HTTP_PROXY= HTTPS_PROXY= git push origin main` |
| P3 | `remote rejected … without 'workflow' scope` | 看起来像 token 权限问题 | **虚警。** 同一个 token，清掉代理后直接推成功，workflow 文件照推。先查传输层再查凭据。 |
| P4 | `.sh` 报 `xxx\r: command not found` | 脚本是 CRLF | `.gitattributes` 锁 `.sh/.py/.tcl` 为 LF、`.bat` 为 CRLF。第一个提交就要有。 |
| P5 | `gh release create --notes-file /tmp/x.md` 失败 | MSYS 的 `/tmp` 与 Python 看到的 `/tmp` 不是一处 | 用真实 Windows 路径，如 `C:/Users/Admin/relnotes.md` |
| P6 | `Add-Type` + `System.IO.Compression` 被策略拦下 | PowerShell 安全策略 | 改用 `C:/Windows/System32/tar.exe -a -cf …`，并用 `tar -tf … \| wc -l` 复核条目数 |
| P7 | Python 写不了 `/d/…` | MSYS 路径 ≠ Windows 路径 | 给 Python 一律传 `D:\\…` |
| P8 | docx/pptx 无法嵌 SVG；`reportlab` renderPM 失败 | 无光栅后端 | matplotlib 重绘（`svg2png.py`），见 §3.3 |
| P9 | deck 表格单元格撑爆 / 页脚压住面板 | 单元格文字过长；note 的 y 越过面板 | deck 里压成一行，完整表述留在 Markdown；面板与注 ≤ 5.90 英寸 |
| P10 | docx 首个 H1 渲染两次（24pt + 20pt） | `continue` 前没推进行号 | `continue` 前先 `i += 1` |
| P11 | `git status -sb` 显示 `origin/main [gone]` | 沙箱文件系统不持久化 `refs/remotes` | 无害。用 `gh api` 或网页确认远端状态，别看这一行 |
| P12 | SVG 箭头渲染成黑色 | 部分渲染器不支持 `context-stroke` | marker 路径用显式描边色 |

---

## 5. 完成定义

- [ ] `reviews/` 五份齐全，当时写成，结论各一个词
- [ ] 每个阶段都有产物；每个论断都有来源或明写的假设
- [ ] 版本锁齐备且跨文档一致（CI 强制）
- [ ] `run_all.sh` 退出码契约完好；循环性守卫在位
- [ ] 导出器确定性由 byte-diff 证明，且在 CI 里
- [ ] 中英章节数一致；图示两份都引用
- [ ] `selfcheck.py` 本地与 GitHub Actions 双绿
- [ ] `.docx` / `.pptx` 在最后一次 Markdown 改动后重新生成；零越界
- [ ] Release 说明写明已知缺口
- [ ] 首个提交就含 `.gitattributes`
- [ ] LICENSE 有真实版权方（无 `<COPYRIGHT HOLDER>` 占位符）

---

## 6. 迁移到教程 No. 3

**保持不变**：§0 的不变式、十步顺序、双钥匙契约、退出码契约、五评审审计链、自检、`.gitattributes`。

**需要替换**：主题、领域智能体、门链、版本锁。

| 决策 | S0 阶段必须回答的问题 |
|---|---|
| 主题 | 读者做完之后，能做出哪一件此前做不到的事？ |
| 门链 | 谁当中立裁判？在**这个主题**下，什么情况算 **VOID**？ |
| 领域智能体 | 谁握物理权？给它们的让渡条款怎么写？ |
| starter 载荷 | 能跑、且能响亮失败的最小集合是什么？ |
| 交付物 | 哪几种格式？Markdown 是否仍是唯一事实来源？ |

**前 90 分钟，具体动作：**

1. `git init -b main`；加 `.gitattributes` 与 `.gitignore`；提交空骨架。
2. 写 `PLAN.md` —— 范围、范围外、团队拓扑、完成定义。
3. 跑 `/plan-ceo-review`；**在写任何正文之前**落地 `reviews/01-ceo-review.md`。
4. 跑 `/spec`；落地 `reviews/02-spec.md`，含 W 任务与上抛条目。
5. 锁定工具链；写 `versions.lock.template`。
6. 复制 `.github/scripts/selfcheck.py`，改必需文件清单。

之后就是 S3–S9 循环。

---

*许可：文字 CC BY 4.0，代码 Apache-2.0 —— Copyright 2026 Prof. Yi-Kuen Lee。*
